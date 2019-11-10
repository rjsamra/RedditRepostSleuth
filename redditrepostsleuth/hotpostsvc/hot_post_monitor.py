import time
from time import perf_counter

from praw import Reddit
from praw.models import Comment
from redlock import RedLockError

from redditrepostsleuth.core.config import config
from redditrepostsleuth.core.services.reddit_manager import RedditManager
from redditrepostsleuth.core.services.response_handler import ResponseHandler
from redditrepostsleuth.core.util.constants import CUSTOM_FILTER_LEVELS, BANNED_SUBS, ONLY_COMMENT_REPOST_SUBS, \
    NO_LINK_SUBREDDITS
from redditrepostsleuth.core.util.replytemplates import DEFAULT_COMMENT_OC

from redditrepostsleuth.core.db.uow.unitofworkmanager import UnitOfWorkManager
from redditrepostsleuth.core.exception import NoIndexException
from redditrepostsleuth.core.logging import log
from redditrepostsleuth.core.db.databasemodels import Post, BotComment
from redditrepostsleuth.core.util.helpers import build_msg_values_from_search
from redditrepostsleuth.core.util.reposthelpers import check_link_repost
from redditrepostsleuth.core.duplicateimageservice import DuplicateImageService
from redditrepostsleuth.core.services.responsebuilder import ResponseBuilder


class TopPostMonitor:

    def __init__(self, reddit: RedditManager, uowm: UnitOfWorkManager, image_service: DuplicateImageService, response_builder: ResponseBuilder, response_handler: ResponseHandler):
        self.reddit = reddit
        self.uowm = uowm
        self.image_service = image_service
        self.response_builder = response_builder
        self.response_handler = response_handler


    def monitor(self):
        while True:
            with self.uowm.start() as uow:
                submissions = [sub for sub in self.reddit.subreddit('all').top('day')]
                submissions = submissions + [sub for sub in self.reddit.subreddit('all').rising()]
                #submissions = submissions + [sub for sub in self.reddit.subreddit('all').controversial('day')]
                submissions = submissions + [sub for sub in self.reddit.subreddit('all').hot()]
                for sub in submissions:
                    post = uow.posts.get_by_post_id(sub.id)
                    if not post:
                        continue

                    if post and post.left_comment:
                        continue

                    if post.subreddit.lower() in BANNED_SUBS:
                        log.info('Post %s is in a banned sub, %s.', post.post_id, post.subreddit)
                        continue

                    if post.crosspost_parent:
                        log.info('Skipping cross post')
                        continue

                    monitored_sub = uow.monitored_sub.get_by_sub(post.subreddit)
                    if monitored_sub:
                        log.info('Skipping monitored sub %s', post.subreddit)
                        continue

                    self.check_for_repost(post)
                    time.sleep(0.2)

                # TODO - Add checked posts to checked table

            log.info('Processed all top posts.  Sleeping')
            time.sleep(3600)

    def check_for_repost(self, post: Post):

        if post.post_type == 'image':
            if not post.dhash_h:
                log.info('Post %s has no dhash value, skipping', post.post_id)
                return
            try:
                target_annoy = None
                target_hamming = None
                if post.subreddit in CUSTOM_FILTER_LEVELS:
                    log.info('Using custom filter values for sub %s', post.subreddit)
                    target_annoy = CUSTOM_FILTER_LEVELS.get(post.subreddit)['annoy']
                    target_hamming = CUSTOM_FILTER_LEVELS.get(post.subreddit)['hamming']
                search_results = self.image_service.check_duplicates_wrapped(post, target_hamming_distance=target_hamming,
                                                                      target_annoy_distance=target_annoy, same_sub=True)
            except NoIndexException:
                log.error('No available index for image repost check.  Trying again later')
                return
            except RedLockError:
                log.error('Could not get RedLock.  Trying again later')
                return
            self.add_comment(post, search_results)
        elif post.post_type == 'link':
            return
            # TODO - Deal with imgur posts marked as link
            # TODO - Change link reposts to use same wrapper as image reposts
            if 'imgur' in post.url:
                log.info('Skipping imgur post marked as link')
                return
            start = perf_counter()
            search_results = check_link_repost(post, self.uowm).matches
            search_time = perf_counter() - start
            with self.uowm.start() as uow:
                total_searched = uow.posts.count_by_type('link')
            self.add_comment(post, search_results, search_time, total_searched)
        else:
            log.info(f'Post {post.post_id} is a {post.post_type} post.  Skipping')
            return

    def add_comment(self, post: Post, search_results):
        msg_values = build_msg_values_from_search(search_results, self.uowm)
        if search_results.matches:
            msg = self.response_builder.build_default_repost_comment(msg_values)
        else:
            if not config.comment_on_oc:
                log.info('Sub %s is set to repost comment only.  Skipping OC comment', post.subreddit)
                return
            msg = self.response_builder.build_default_oc_comment(msg_values)

        self.response_handler.reply_to_submission(post.post_id, msg)


        with self.uowm.start() as uow:
            post.left_comment = True
            uow.posts.update(post)
            uow.commit()

    def _log_comment(self, comment: Comment, post: Post):
        """
        Log reply comment to database
        :param comment:
        """
        bot_comment = BotComment(
            post_id=post.post_id,
            comment_body=comment.body,
            perma_link=comment.permalink,
            source='toppost',
            comment_id=comment.id,
            subreddit=post.subreddit
        )
        with self.uowm.start() as uow:
            uow.bot_comment.add(bot_comment)
            try:
                uow.commit()
            except Exception as e:
                log.exception('Failed to save bot comment', exc_info=True)