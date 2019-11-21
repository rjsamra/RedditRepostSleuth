from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Text, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



#op.create_index('ingest_source', 'reddit_post', ['created_at', 'ingested_from'], unique=False)
#op.create_index('ingest_graph', 'reddit_post', ['ingested_at', 'post_type'], unique=False)
#op.create_index('image_repost_check', 'reddit_post', ['post_type', 'checked_repost', 'crosspost_parent', 'dhash_h'], unique=False)
#op.create_index('image_hash', 'reddit_post', ['post_type', 'dhash_h'], unique=False)
#op.create_index('create_at_index', 'reddit_image_post', ['created_at'], unique=False)

class Post(Base):

    def __lt__(self, other):
        return self.image_hash < other.image_hash

    def __repr__(self) -> str:
        return 'Post ID: {} - Type: {} - URL: {} - Source: {} - Created: {}'.format(self.post_id, self.post_type, self.url, self.ingested_from, self.created_at)

    # TODO - Move to_dict methods into JSON encoders

    __tablename__ = 'reddit_post'

    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False, unique=True)
    url = Column(String(2000, collation='utf8mb4_general_ci'), nullable=False)
    shortlink = Column(String(300))
    perma_link = Column(String(1000, collation='utf8mb4_general_ci'))
    post_type = Column(String(20))
    author = Column(String(100), nullable=False)
    selftext = Column(Text(75000, collation='utf8mb4_general_ci'))
    created_at = Column(DateTime)
    ingested_at = Column(DateTime, default=func.utc_timestamp())
    subreddit = Column(String(100), nullable=False)
    title = Column(String(1000, collation='utf8mb4_general_ci'), nullable=False)
    crosspost_parent = Column(String(200))
    dhash_v = Column(String(64))
    dhash_h = Column(String(64))
    ahash = Column(String(64))
    checked_repost = Column(Boolean, default=False)
    crosspost_checked = Column(Boolean, default=False)
    last_deleted_check = Column(DateTime, default=func.utc_timestamp())
    url_hash = Column(String(32)) # Needed to index URLs for faster lookups
    ingested_from = Column(String(40))
    left_comment = Column(Boolean, default=False)

    bad_url = Column(Boolean, default=False)
    repost_count = Column(Integer, default=0)
    #fullname = Column(String(30))

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'url': self.url,
            'shortlink': self.shortlink,
            'perma_link': self.perma_link,
            'title': self.title,
            'dhash_v': self.dhash_v,
            'dhash_h': self.dhash_h,
            'created_at': self.created_at.timestamp()
        }

class RedditImagePost(Base):
    __tablename__ = 'reddit_image_post'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    post_id = Column(String(100), nullable=False, unique=True)
    dhash_v = Column(String(64))
    dhash_h = Column(String(64))

class RedditImagePostCurrent(Base):
    __tablename__ = 'reddit_image_post_current'
    # Dirty but we need to maintain a seperate table to build indexes from
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    post_id = Column(String(100), nullable=False, unique=True)
    dhash_v = Column(String(64))
    dhash_h = Column(String(64))


class Summons(Base):
    __tablename__ = 'reddit_bot_summons'

    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False)
    requestor = Column(String(100))
    comment_id = Column(String(100), unique=True)
    comment_body = Column(String(1000, collation='utf8mb4_general_ci'))
    comment_reply = Column(String(5000))
    comment_reply_id = Column(String(100))
    summons_received_at = Column(DateTime)
    summons_replied_at = Column(DateTime)
    subreddit = Column(String(100), nullable=False)

class BotComment(Base):
    __tablename__ = 'reddit_bot_comment'

    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False)
    comment_body = Column(String(2000, collation='utf8mb4_general_ci'))
    perma_link = Column(String(1000, collation='utf8mb4_general_ci'))
    comment_left_at = Column(DateTime, default=func.utc_timestamp())
    source = Column(String(20), nullable=False)
    comment_id = Column(String(20), nullable=False)
    subreddit = Column(String(100), nullable=False)
    karma = Column(Integer)
    active = Column(Boolean, default=True)
    needs_review = Column(Boolean, default=False)


class Comment(Base):
    __tablename__ = 'reddit_comments'

    id = Column(Integer, primary_key=True)
    comment_id = Column(String(100), nullable=False, unique=True)
    body = Column(Text(collation='utf8mb4_general_ci'))
    ingested_at = Column(DateTime, default=func.utc_timestamp())

class RepostWatch(Base):
    __tablename__ = 'reddit_repost_watch'

    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False)
    user = Column(String(100), nullable=False)
    response_type = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=func.utc_timestamp())
    last_detection = Column(DateTime)

class ImageRepost(Base):

    __tablename__ = 'image_reposts'
    id = Column(Integer, primary_key=True)
    hamming_distance = Column(Integer)
    annoy_distance = Column(Float)
    post_id = Column(String(100), nullable=False, unique=True)
    repost_of = Column(String(100), nullable=False)
    detected_at = Column(DateTime, default=func.utc_timestamp())

class LinkRepost(Base):

    __tablename__ = 'link_reposts'
    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False, unique=True)
    repost_of = Column(String(100), nullable=False)
    detected_at = Column(DateTime, default=func.utc_timestamp())

class VideoHash(Base):
    __tablename__ = 'reddit_video_hashes'
    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.utc_timestamp())
    hashes = Column(String(1300))
    length = Column(Integer)

class AudioFingerPrint(Base):
    __tablename__ = 'audio_fingerprints'
    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False)
    hash = Column(String(30), nullable=False)
    offset = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.utc_timestamp())

class IndexBuildTimes(Base):
    __tablename__ = 'index_build_times'
    id = Column(Integer, primary_key=True)
    index_type = Column(String(50), nullable=False)
    hostname = Column(String(200), nullable=False)
    items = Column(Integer, nullable=False)
    build_start = Column(DateTime, nullable=False)
    build_end = Column(DateTime, nullable=False)
    build_minutes = Column(Integer)

class MonitoredSub(Base):
    __tablename__ = 'reddit_monitored_sub'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    active = Column(Boolean, default=False)
    repost_only = Column(Boolean, default=True)
    report_submission = Column(Boolean, default=False)
    report_msg = Column(String(200), default='RepostSleuthBot-Repost')
    requestor = Column(String(150))
    added_at = Column(DateTime, default=func.utc_timestamp())
    target_hamming = Column(Integer)
    target_annoy = Column(Float)
    target_days_old = Column(Integer)
    same_sub_only = Column(Boolean, default=False)
    notes = Column(String(500))
    sticky_comment = Column(Boolean, default=False)
    repost_response_template = Column(String(2000))
    oc_response_template = Column(String(2000))
    search_depth = Column(Integer, default=100)
    meme_filter = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            'repost_only': self.repost_only,
            'report_submission': self.report_submission,
            'report_msg': self.report_msg,
            'requestor': self.requestor,
            'added_at': str(self.added_at),
            'target_hamming': self.target_hamming,
            'target_annoy': self.target_annoy,
            'target_days_old': self.target_days_old,
            'same_sub_only': self.same_sub_only,
            'notes': self.notes,
            'sticky_comment': self.sticky_comment,
            'repost_response_template': self.repost_response_template,
            'oc_response_template': self.oc_response_template,
            'search_depth': self.search_depth,
            'meme_filter': self.meme_filter
        }

class MonitoredSubChecks(Base):
    __tablename__ = 'reddit_monitored_sub_checked'

    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False)
    checked_at = Column(DateTime, default=func.utc_timestamp())
    subreddit = Column(String(100))

class MonitoredSubConfigRevision(Base):
    __tablename__ = 'reddit_monitored_sub_config_revision'
    id = Column(Integer, primary_key=True)
    revision_id = Column(String(36), nullable=False, unique=True)
    revised_by = Column(String(100), nullable=False)
    config = Column(String(1000), nullable=False)
    config_loaded_at = Column(DateTime)
    is_valid = Column(Boolean, default=False)
    notified = Column(Boolean, default=False)
    subreddit = Column(String(100), nullable=False)


class MemeTemplate(Base):
    __tablename__ = 'meme_template'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    dhash_v = Column(String(64))
    dhash_h = Column(String(64))
    ahash = Column(String(64))
    target_hamming = Column(Integer)
    target_annoy = Column(Float)
    example = Column(String(500))
    template_detection_hamming = Column(Integer)
    created_from_submission = Column(String(100))
    approved = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dhash_v': self.dhash_v,
            'dhash_h': self.dhash_h,
            'ahash': self.ahash,
            'target_hamming': self.target_hamming,
            'target_annoy': self.target_annoy,
            'example': self.example,
            'template_detection_hamming': self.template_detection_hamming,
            'created_from_submission': self.created_from_submission,
            'approved': self.approved
        }

class InvestigatePost(Base):
    __tablename__ = 'investigate_post'

    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False, unique=True)
    matches = Column(Integer)
    found_at = Column(DateTime, default=func.utc_timestamp())
    url = Column(String(2000, collation='utf8mb4_general_ci'), nullable=False)
    flag_reason = Column(String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'matches': self.matches,
            'found_at': str(self.found_at),
            'shortlink': f'https://redd.it/{self.post_id}',
            'url': self.url,
            'flag_reason': self.flag_reason
        }

class ImageSearch(Base):
    __tablename__ = 'reddit_image_search'
    id = Column(Integer, primary_key=True)
    post_id = Column(String(100), nullable=False, unique=True)
    used_historical_index = Column(Boolean, nullable=False)
    used_current_index = Column(Boolean, nullable=False)
    target_hamming_distance = Column(Integer, nullable=False)
    target_annoy_distance = Column(Float, nullable=False)
    same_sub = Column(Boolean, nullable=False)
    max_days_old = Column(Integer, nullable=False)
    filter_dead_matches = Column(Boolean, nullable=False)
    only_older_matches = Column(Boolean, nullable=False)
    meme_filter = Column(Boolean, nullable=False)
    meme_template_Used = Column(Integer)
    search_time = Column(Float, nullable=False)