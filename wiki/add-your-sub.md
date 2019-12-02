### Repost Sleuth Can Check All Your Posts!
We now allow you to register your sub to have all new submissions checked. 

The process to active Repost Sleuth is simple. 

All you have to do is add u/RepostSleuthBot as a mod with Post and Wiki permissions.  That's it. 

The bot will accept the request, set some sensible default values and start checking posts. 

## Configuration

Repost Sleuth will create a new wiki page called 'repost_sleuth_config'.  In this wiki page you will find the bot settings in JSON format. 

To change settings simply update the JSON and save.  The bot will load the new config within a few minutes.  Once the new config is loaded you will received a modmail.

**Example Config**
```
{
  "active": true,
  "only_comment_on_repost": true,
  "report_reposts": false,
  "report_msg": "RepostSleuthBot-Repost",
  "match_percent_dif": 5,
  "same_sub_only": true,
  "sticky_comment": false,
  "search_depth": 100,
  "target_days_old": null,
  "meme_filter": false,
  "check_post_types": ["image", "link"],
  "oc_response_template": null,
  "repost_response_template": null
}
```

### Config Value Explanation
active: Enable / Disable the bot

only_comment_on_repost: If true the bot only comments on reposts.  If false it will also comment on OC

report_reposts: Bot will report any reposts it finds

report_msg: The message it will use when reporting

match_percent_dif: How strict matching is when determining if an image is a repost. Use values between 0 and 10

same_sub_only: Only check for matches within our sub

sticky_comment: Comments left by the bot will be stickied

search_depth: How many historical posts the bot will check when activated. Max 500

target_days_old: Only report matches X days old or newer

oc_response_template: Comment template when commenting on OC

repost_response_template: Comment template when commenting on reposts

**Comment Templates:** Must be in markdown format.  You have a number of variables you can use in the template.  [Click here for a list](https://www.reddit.com/r/RepostSleuthBot/wiki/add-you-sub/repost-message-template)