from typing import Literal, Union
from tweetipy.helpers.API import API_OAUTH_1_0_a
from tweetipy.helpers.QueryBuilder import QueryStr
from tweetipy.types import Media, Poll, Reply, Tweet


class HandlerTweets():

    ReplySettings = Literal["mentionedUsers", "following"]

    def __init__(self, API: API_OAUTH_1_0_a) -> None:
        self.API = API

    def write(
        self,
        text: str = None, # Required if media not present
        # media, poll and quote_tweet_id are mutually exclusive
        media: Media = None,
        poll: Poll = None,
        quote_tweet_id: str = None,
        reply: Reply = None,
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
        # ----------------------------------------------------------------------

        body = {
            "media": media.json() if media != None else None,
            "poll": poll.json() if poll != None else None,
            "quote_tweet_id": quote_tweet_id,
            "direct_message_deep_link": direct_message_deep_link,
            "for_super_followers_only": for_super_followers_only,
            "reply": reply.json() if reply != None else None,
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
            return Tweet(**r.json()["data"])
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
