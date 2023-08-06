class QueryStr():
    def __init__(self, string: str) -> None:
        self._str = string

    def __or__(self, other):
        return QueryStr(f'{self} OR {other}')

    def __and__(self, other):
        return QueryStr(f'{self} {other}')

    def __invert__(self):
        if self._str.startswith('-'):
            return QueryStr(self._str[1:])
        else:
            return QueryStr(f'-({self._str})')

    def __str__(self) -> str:
        return self._str


class Has():
    def __init__(self, is_negation: bool = False) -> None:
        self._is_negation = is_negation

    @property
    def _prefix(self):
        return '-' if self._is_negation else ''

    def _return(self, value: str):
        return QueryStr(f'{self._prefix}{value}')

    @property
    def hashtags(self) -> QueryStr:
        return self._return(f'has:hashtags')

    @property
    def cashtags(self) -> QueryStr:
        """
        Requires API with elevated access.
        """
        return self._return(f'filter:cashtags')

    @property
    def links(self) -> QueryStr:
        return self._return(f'filter:links')

    @property
    def mentions(self) -> QueryStr:
        return self._return(f'filter:mentions')

    @property
    def media(self) -> QueryStr:
        return self._return(f'filter:media')

    @property
    def images(self) -> QueryStr:
        return self._return(f'filter:images')

    @property
    def video(self) -> QueryStr:
        return self._return(f'filter:native_video')

    # @property
    # def geolocation_data(self) -> QueryStr:
    #     """
    #     Requires elevated access to API.
    #     """
    #     return self._return(f'has:geo')


class QueryBuilderAlt():
    def __init__(self, is_negation: bool = False) -> None:
        self._is_negation = is_negation

    @property
    def _prefix(self):
        return '-' if self._is_negation else ''

    def _return(self, value: str):
        return QueryStr(f'{self._prefix}{value}')
    
    def tweeted_since(self, date: str):
        return self._return(f'since:{date}')
    
    def tweeted_until(self, date: str):
        return self._return(f'until:{date}')

    def from_user(self, user_handle_or_id: str) -> QueryStr:
        return self._return(f'from:{user_handle_or_id}')

    def replying_to_user(self, user_handle_or_id: str) -> QueryStr:
        return self._return(f'to:{user_handle_or_id}')

    # def retweets_of_user(self, user_handle_or_id: str) -> QueryStr:
    #     """
    #     Needs more testing.
    #     """
    #     return self._return(f'retweets_of:{user_handle_or_id}')

    # def in_reply_to_tweet_id(self, tweet_id: str) -> QueryStr:
    #     return self._return(f'in_reply_to_tweet_id:{tweet_id}')

    # def retweets_of_tweet_id(self, tweet_id: str) -> QueryStr:
    #     return self._return(f'retweets_of_tweet_id:{tweet_id}')

    # def quotes_of_tweet_id(self, tweet_id: str) -> QueryStr:
    #     return self._return(f'quotes_of_tweet_id:{tweet_id}')

    # def with_annotated_context(self, context: str) -> QueryStr:
    #     """
    #     Matches Tweets with a specific domain id/enitity id pair. To learn more
    #     about this operator, please visit our page on annotations.
    #     You can only pass a single domain/entity per context: operator.
    #     context:domain_id.entity_id
    #     However, you can combine multiple domain/entities using the OR operator:
    #     (context:47.1139229372198469633 OR context:11.1088514520308342784)
    #     Examples:
    #     context:10.799022225751871488
    #     (domain_id.entity_id returns Tweets matching that specific domain-entity pair)
        
    #     See "annotations":
    #     https://developer.twitter.com/content/developer-twitter/en/docs/twitter-api/annotations

    #     See available context/entity pairs:
    #     https://github.com/twitterdev/twitter-context-annotations
    #     """
    #     return self._return(f'context:{context}')

    # def with_annotated_entity(self, entity: str) -> QueryStr:
    #     """
    #     Matches Tweets with a specific entity string value. To learn more about this operator, please visit our page on annotations.
    #     Please note that this is only available with recent search.
    #     You can only pass a single entity: operator.
    #     entity:"string declaration of entity/place"
    #     Examples: entity:"Michael Jordan" OR entity:"Barcelona"

    #     See "annotations":
    #     https://developer.twitter.com/content/developer-twitter/en/docs/twitter-api/annotations

    #     See available entities:
    #     https://github.com/twitterdev/twitter-context-annotations
    #     """
    #     return self._return(f'entity:"{entity}"')

    # def is_part_of_conversation_id(self, conversation_id: str) -> QueryStr:
    #     """
    #     Matches Tweets that share a common conversation ID. A conversation ID is set to the Tweet ID of a Tweet that started a conversation. As Replies to a Tweet are posted, even Replies to Replies, the conversation_id is added to its JSON payload.

    #     You can only pass a single conversation ID per conversation_id: operator.

    #     Example: conversation_id:1334987486343299072 (from:twitterdev OR from:twitterapi)
    #     """
    #     return self._return(f'conversation_id:{conversation_id}')

    def from_users_in_list(self, twitter_list: str) -> QueryStr:
        """
        Requires elevated API access.
        Matches Tweets posted by users who are members of a specified list. 
        For example, if @twitterdev and @twitterapi were members of List 123, and you included list:123 in your query, your response will only contain Tweets that have been published by those accounts. You can find List IDs by using the List lookup endpoint.
        Please note that you can only use a single list: operator per query, and you can only specify a single List per list: operator.
        Example: list:123
        """
        return self._return(f'list:{twitter_list}')

    def from_place(self, place: str, radius_km: int) -> QueryStr:
        """
        Requires elevated API access.
        Matches Tweets tagged with the specified location or Twitter place ID. Multi-word place names (“New York City”, “Palo Alto”) should be enclosed in quotes.
        You can only pass a single place per place: operator.
        Note: See the GET geo/search standard v1.1 endpoint for how to obtain Twitter place IDs.
        Note: This operator will not match on Retweets, since Retweet's places are attached to the original Tweet. It will also not match on places attached to the original Tweet of a Quote Tweet.
        Example: place:"new york city" OR place:seattle OR place:fd70c22040963ac7
        See:
        https://developer.twitter.com/en/docs/twitter-api/v1/geo/places-near-location/api-reference/get-geo-search
        """
        return self._return(f'near:{place} within:{radius_km}km')

    # def from_country(self, country_iso_2_letter: str) -> QueryStr:
    #     """
    #     Requires elevated API access.
    #     Matches Tweets where the country code associated with a tagged place/location matches the given ISO alpha-2 character code.
    #     You can find a list of valid ISO codes on Wikipedia.
    #     You can only pass a single ISO code per place_country: operator.
    #     Note: This operator will not match on Retweets, since Retweet's places are attached to the original Tweet. It will also not match on places attached to the original Tweet of a Quote Tweet.
    #     Example: place_country:US OR place_country:MX OR place_country:CA
    #     See:
    #     https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    #     """
    #     return self._return(f'place_country:{country_iso_2_letter}')

    # def near_coordinate(self, lng: float, lat: float, radius_km: int) -> QueryStr:
    #     """
    #     Requires elevated API access.
    #     Matches against the place.geo.coordinates object of the Tweet when present, and in Twitter, against a place geo polygon, where the Place polygon is fully contained within the defined region.
    #     point_radius:[longitude latitude radius]
    #     Radius must be less than 25mi
    #     Longitude is in the range of ±180
    #     Latitude is in the range of ±90
    #     All coordinates are in decimal degrees
    #     You can only pass a single geo polygon per point_radius: operator.
    #     Note: This operator will not match on Retweets, since Retweet's places are attached to the original Tweet. It will also not match on places attached to the original Tweet of a Quote Tweet.
    #     Example: point_radius:[2.355128 48.861118 16km] OR point_radius:[-41.287336 174.761070 20mi]
    #     """
    #     return self._return(f'point_radius:[{lng} {lat} {radius_km}km]')

    # def within_bounding_box(self, west_lng: float, south_lat: float, east_lng: float, north_lat: float) -> QueryStr:
    #     """
    #     Requires elevated API access.
    #     Matches against the place.geo.coordinates object of the Tweet when present, and in Twitter, against a place geo polygon, where the place polygon is fully contained within the defined region.
    #     bounding_box:[west_long south_lat east_long north_lat]
    #     west_long south_lat represent the southwest corner of the bounding box where west_long is the longitude of that point, and south_lat is the latitude.
    #     east_long north_lat represent the northeast corner of the bounding box, where east_long is the longitude of that point, and north_lat is the latitude.
    #     Width and height of the bounding box must be less than 25mi
    #     Longitude is in the range of ±180
    #     Latitude is in the range of ±90
    #     All coordinates are in decimal degrees.
    #     Rule arguments are contained within brackets, space delimited.
    #     You can only pass a single geo polygons per bounding_box: operator. 
    #     Note: This operator will not match on Retweets, since Retweet's places are attached to the original Tweet. It will also not match on places attached to the original Tweet of a Quote Tweet.
    #     Example: bounding_box:[-105.301758 39.964069 -105.178505 40.09455]
    #     """
    #     return self._return(f'bounding_box:[{west_lng} {south_lat} {east_lng} {north_lat}]')

    def in_language(self, lang: str) -> QueryStr:
        """
        Use lowercase 2 letter code for language (BCP 47 language identifier).
        For example, use "es" for spanish, "en" for english, "de" for german,
        etc.
        You may use "SupportedLanguages" enumeration to find a language code, or
        you can see the full list in the API docs:
        https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#list
        """
        return self._return(f'lang:{lang}')

    def with_url(self, url: str) -> QueryStr:
        return self._return(url)

    def with_all_keywords(self, keywords: list[str]) -> QueryStr:
        """
        Will filter for tweets containing ALL keywords
        """
        return self._return(' '.join(keywords))
    
    def with_any_keyword(self, keywords: list[str]) -> QueryStr:
        """
        Will filter for tweets containing at least one of the keywords provided.
        """
        return self._return(f'({" OR ".join(keywords)})')

    def with_exact_string(self, string: str) -> QueryStr:
        return self._return(f'"{string}"')

    @property
    def has(self):
        """
        Filter for tweets that have media, links, geolocation data, etc.
        """
        return Has(self._is_negation)

    @property
    def is_retweet(self) -> QueryStr:
        """
        If you use this, you need to begin your query with at least one keyword.
        In other words, this won't work as a standalone query.
        """
        if self._is_negation:
            return QueryStr('exclude:retweets')
        else:
            return QueryStr('filter:retweets')

    @property
    def is_reply(self) -> QueryStr:
        """
        If you use this, you need to begin your query with at least one keyword.
        In other words, this won't work as a standalone query.
        """
        if self._is_negation:
            return QueryStr('exclude:replies')
        else:
            return QueryStr('filter:replies')

    @property
    def is_quote(self) -> QueryStr:
        """
        If you use this, you need to begin your query with at least one keyword.
        In other words, this won't work as a standalone query.
        """
        if self._is_negation:
            return QueryStr('exclude:quote')
        else:
            return QueryStr('filter:quote')

    @property
    def is_from_verified_user(self) -> QueryStr:
        """
        If you use this, you need to begin your query with at least one keyword.
        In other words, this won't work as a standalone query.
        """
        if self._is_negation:
            return QueryStr('exclude:verified')
        else:
            return QueryStr('filter:verified')

    @property
    def NOT(self):
        return QueryBuilderAlt(not self._is_negation)
