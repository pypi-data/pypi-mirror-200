from typing import Literal, Union
from tweetipy.helpers.API import API_OAUTH_1_0_a
from tweetipy.helpers.QueryBuilder import QueryStr
from tweetipy.types import MediaToUpload, Poll, Tweet
from tweetipy.enums.fields import TweetFields, MediaFields, PlaceFields, PollFields, UserFields
from tweetipy.enums.expansions import TweetExpansions
from tweetipy.types.tweet import ReplyConfig


class HandlerTweets():

    ReplySettings = Literal["everyone", "mentionedUsers", "following"]

    def __init__(self, API: API_OAUTH_1_0_a) -> None:
        self.API = API

    def write(
        self,
        text: str = None, # Required if media not present
        # media, poll and quote_tweet_id are mutually exclusive
        media: MediaToUpload = None,
        # media: Union[PathLike, list[PathLike]] = [],
        # media_id: Union[str, list[str]] = None,
        poll: Poll = None,
        quote_tweet_id: str = None,
        in_reply_to_tweet_id: str = None,
        user_ids_to_exclude_from_thread: list[str] = None,
        reply_settings: ReplySettings = None,
        direct_message_deep_link: str = None,
        for_super_followers_only: bool = None,
    ) -> Tweet:
        endpoint = 'https://api.twitter.com/2/tweets'

        # body logic ---------------------------------------------------------
        if (media != None) + (poll != None) + (quote_tweet_id != None) > 1:
            raise Exception(
                "media, poll and quote_tweet_id are mutually exclusive. This means you can only use one of them at the same time.")
        if media == None and text == None:
            raise Exception(
                "text argument is required if no media is present.")
        if user_ids_to_exclude_from_thread != None and in_reply_to_tweet_id == None:
            raise Exception('If you provide `user_ids_to_exclude_from_thread`, you need to specify the tweet that you are replying to with `in_reply_to_tweet_id`.')
        # ----------------------------------------------------------------------

        reply_config = ReplyConfig(user_ids_to_exclude_from_thread, in_reply_to_tweet_id)

        body = {
            "media": media.json() if media != None else None,
            "poll": poll.json() if poll != None else None,
            "quote_tweet_id": quote_tweet_id,
            "direct_message_deep_link": direct_message_deep_link,
            "for_super_followers_only": for_super_followers_only,
            "reply": reply_config if in_reply_to_tweet_id != None else None,
            "reply_settings": reply_settings,
            "text": text,
        }

        # Remove unused params -------------------------------------------------
        clean_body = {}
        for key, val in body.items():
            if val != None:
                clean_body[key] = val
        body = clean_body.copy()
        # ----------------------------------------------------------------------

        r = self.API.post(url=endpoint, json=body)
        if r.status_code == 201:
            tweet_raw = r.json()["data"]
            return Tweet(**tweet_raw)
        else:
            print(r.text)
            r.raise_for_status()
    
    def search(
        self,
        query: Union[str, QueryStr],
        max_results: int = 10,
        sort_order: Literal["recency", "relevancy"] = "recency",
        start_time_iso: str = None,
        end_time_iso: str = None,
        since_id: str = None,
        until_id: str = None,
        next_token: str = None
    ) -> list[Tweet]:
        """
        - max_results: int between 10 and 100
        """
        endpoint = 'https://api.twitter.com/2/tweets/search/recent'

        body = {
            "query": str(query),
            "max_results": max_results,
            "sort_order": sort_order,
            "start_time": start_time_iso,
            "end_time": end_time_iso,
            "since_id": since_id,
            "until_id": until_id,
            "next_token": next_token,
        }

        # Remove unused params -------------------------------------------------
        clean_body = {}
        for key, val in body.items():
            if val != None:
                clean_body[key] = val
        body = clean_body.copy()
        # ----------------------------------------------------------------------

        r = self.API.get(url=endpoint, params=body)
        if r.status_code == 200:
            r_json: dict = r.json()
            if "data" in r_json.keys():
                raw_tweets = r_json["data"]
                tweets = [Tweet(**t) for t in raw_tweets]
                return tweets
            else:
                return []
        else:
            print(r.text)
            r.raise_for_status()

    def getOne(
        self,
        id: str,
        include_media_fields: list[MediaFields] = [],
        include_place_fields: list[PlaceFields] = [PlaceFields.country, PlaceFields.full_name, PlaceFields.place_type],
        include_poll_fields: list[PollFields] = [],
        include_tweet_fields: list[TweetFields] = [TweetFields.author_id, TweetFields.public_metrics, TweetFields.geo, TweetFields.created_at],
        include_user_fields: list[UserFields] = [UserFields.username, UserFields.verified, UserFields.verified_type],
    ) -> Union[Tweet, list[Tweet]]:

        endpoint = f'https://api.twitter.com/2/tweets/{id}'
        
        expansions = []
        if len(include_media_fields) > 0:
            expansions.append(TweetExpansions.attachments_media_keys)
        if len(include_place_fields) > 0:
            expansions.append(TweetExpansions.geo_place_id)
        if len(include_poll_fields) > 0:
            expansions.append(TweetExpansions.attachments_poll_ids)
        if len(include_user_fields) > 0:
            expansions.append(TweetExpansions.author_id)
        
        body = {
            "ids": None,
            "expansions": None if len(expansions) == 0 else ','.join(expansions),
            "media.fields": None if len(include_media_fields) == 0 else ','.join(include_media_fields),
            "place.fields": None if len(include_place_fields) == 0 else ','.join(include_place_fields),
            "poll.fields": None if len(include_poll_fields) == 0 else ','.join(include_poll_fields),
            "tweet.fields": None if len(include_tweet_fields) == 0 else ','.join(include_tweet_fields),
            "user.fields": None if len(include_user_fields) == 0 else ','.join(include_user_fields),
        }
        
        # Remove unused params -------------------------------------------------
        clean_body = {}
        for key, val in body.items():
            if val != None:
                clean_body[key] = val
        body = clean_body.copy()
        # ----------------------------------------------------------------------

        r = self.API.get(url=endpoint, params=body)
        if r.status_code == 200:
            res_json = r.json()
            tweet_raw = {}
            try:
                tweet_raw = res_json['data']
            except KeyError as e:
                raise Exception(f'There was an error downloading the data. See details: {e}')
            if len(expansions)>0:
                try:
                    tweet_raw['includes'] = res_json["includes"]
                except KeyError as e:
                    raise Exception(f'There was an error downloading the requested expansions. See details: {e}')
            return Tweet(**tweet_raw)
        else:
            print(r.text)
            r.raise_for_status()
