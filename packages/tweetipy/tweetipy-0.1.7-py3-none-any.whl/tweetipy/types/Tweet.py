class Tweet():
    def __init__(self, id: str, text: str, edit_history_tweet_ids: list[str] = None) -> None:
        self._id = id
        self._text = text
        self._edit_history_tweet_ids = edit_history_tweet_ids
    
    @property
    def id(self):
        return self._id
    
    @property
    def text(self):
        return self._text

    @property
    def url(self):
        return f'https://twitter.com/account/status/{self.id}'
    
    @property
    def edit_history_tweet_ids(self):
        return self._edit_history_tweet_ids
    
    def json(self):
        return {
            "id": self.id,
            "text": self.text,
            "url": self.url,
            "edit_history_tweet_ids": self.edit_history_tweet_ids
        }

    def __str__(self) -> str:
        return str(self.json())
    
    def __repr__(self) -> str:
        return str(self.json())
