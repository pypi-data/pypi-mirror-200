class PublicMetrics():
    def __init__(self, followers_count: int, following_count: int, tweet_count: int, listed_count: int) -> None:
        self.followers_count = followers_count
        self.following_count = following_count
        self.tweet_count = tweet_count
        self.listed_count = listed_count

    def json(self):
        return {
            "followers_count": self.followers_count,
            "following_count": self.following_count,
            "tweet_count": self.tweet_count,
            "listed_count": self.listed_count
        }

    def __str__(self) -> str:
        return f"Followers: {self.followers_count} Following: {self.following_count} Tweets: {self.tweet_count} Listed: {self.listed_count}"
