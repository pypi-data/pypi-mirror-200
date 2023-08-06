class PublicMetrics():
    def __init__(self, retweet_count: int, reply_count: int, like_count: int, quote_count: int, impression_count: int) -> None:
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count
        self.quote_count = quote_count
        self.impression_count = impression_count

    def json(self):
        return {
            "retweet_count": self.retweet_count,
            "reply_count": self.reply_count,
            "like_count": self.like_count,
            "quote_count": self.quote_count,
            "impression_count": self.impression_count
        }

    def __str__(self) -> str:
        return f"❤️: {self.like_count} 🔃: {self.retweet_count} 💬: {self.reply_count} 📝: {self.quote_count} 👀: {self.impression_count}"
