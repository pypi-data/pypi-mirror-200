from __future__ import annotations
from typing import TYPE_CHECKING

from .. import Poll, User, Place, Media

if TYPE_CHECKING:
    from .. import Tweet

class Includes():
    def __init__(self, tweets: list[Tweet] = None, users: list[User] = None, places: list[Place] = None, media: list[Media] = None, polls: list[Poll] = None) -> None:
        self.tweets = [Tweet(**x) for x in tweets] if tweets != None else None
        self.users = [User(**x) for x in users] if users != None else None
        self.places = [Place(**x) for x in places] if places != None else None
        self.media = [Media(**x) for x in media] if media != None else None
        self.polls = [Poll(**x) for x in polls] if polls != None else None
