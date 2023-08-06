class ReplyConfig():
    def __init__(self, exclude_reply_user_ids: list[str], in_reply_to_tweet_id: str) -> None:
        """
        - exclude_reply_user_ids: A list of User IDs to be excluded from the
        reply Tweet thus removing a user from a thread.
        - in_reply_to_tweet_id: Tweet ID of the Tweet being replied to. Please
        note thatTweet ID of the Tweet being replied to. Please note that
        `in_reply_to_tweet_id` needs to be in the request if
        `exclude_reply_user_ids` is present.
        """
        self.exclude_reply_user_ids = exclude_reply_user_ids
        self.in_reply_to_tweet_id = in_reply_to_tweet_id

    def json(self):
        json_ctr = {}
        if self.exclude_reply_user_ids != None:
            json_ctr["exclude_reply_user_ids"] = self.exclude_reply_user_ids
        if self.in_reply_to_tweet_id != None:
            json_ctr["in_reply_to_tweet_id"] = self.in_reply_to_tweet_id
        return json_ctr
