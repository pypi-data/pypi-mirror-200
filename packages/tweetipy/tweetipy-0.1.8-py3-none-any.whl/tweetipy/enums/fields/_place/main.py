from enum import StrEnum

class PlaceFields(StrEnum):
    """
    The Tweet will only return place fields if the Tweet contains a place and if
    you've also included the expansions=geo.place_id query parameter in your
    request.
    """
    contained_within = "contained_within"
    country = "country"
    country_code = "country_code"
    full_name = "full_name"
    geo = "geo"
    id = "id"
    name = "name"
    place_type = "place_type"