from enum import StrEnum

class TweetExpansions(StrEnum):
    attachments_poll_ids = "attachments.poll_ids"
    attachments_media_keys = "attachments.media_keys"
    author_id = "author_id"
    edit_history_tweet_ids = "edit_history_tweet_ids"
    entities_mentions_username = "entities.mentions.username"
    geo_place_id = "geo.place_id"
    in_reply_to_user_id = "in_reply_to_user_id"
    referenced_tweets_id = "referenced_tweets.id"
    referenced_tweets_author_id = "referenced_tweets.id.author_id"
