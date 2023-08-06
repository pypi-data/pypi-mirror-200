from enum import StrEnum

class UserFields(StrEnum):
    created_at = "created_at"
    description = "description"
    entities = "entities"
    id = "id"
    location = "location"
    name = "name"
    pinned_tweet_id = "pinned_tweet_id"
    profile_image_url = "profile_image_url"
    protected = "protected"
    public_metrics = "public_metrics"
    url = "url"
    username = "username"
    verified = "verified"
    verified_type = "verified_type"
    withheld = "withheld"