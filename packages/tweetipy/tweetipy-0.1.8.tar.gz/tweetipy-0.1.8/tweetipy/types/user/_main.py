from .metrics import PublicMetrics

class User():
    def __init__(self, id: str, name: str, username: str, created_at: str = None, description: str = None, entities: str = None, location: str = None, pinned_tweet_id: str = None, profile_image_url: str = None, protected: str = None, public_metrics: PublicMetrics = None, url: str = None, verified: bool = None, verified_type: str = None, withheld = None) -> None:
        self.id = id
        self.name = name
        self.username = username
        self.created_at = created_at
        self.description = description
        self.entities = entities
        self.location = location
        self.pinned_tweet_id = pinned_tweet_id
        self.profile_image_url = profile_image_url
        self.protected = protected
        self.public_metrics = public_metrics
        self.url = url
        self.verified = verified
        self.verified_type = verified_type
        self.withheld = withheld
