class Geo():
    def __init__(self, type: str, bbox: list[str] = None, properties: dict = None) -> None:
        self.type = type
        self.bbox = bbox
        self.properties = properties
