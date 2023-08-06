from .._geo import Geo

class Place():
    def __init__(self, full_name: str, id: str, contained_within: list[str] = None, country: str = None, country_code: str = None, geo: Geo = None, name: str = None, place_type: str = None) -> None:
        self.full_name = full_name
        self.id = id
        self.contained_within = contained_within
        self.country = country
        self.country_code = country_code
        self.geo = geo
        self.name = name
        self.place_type = place_type
