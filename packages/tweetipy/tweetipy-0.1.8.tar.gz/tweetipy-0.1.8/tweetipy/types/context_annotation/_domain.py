class Domain():
    def __init__(self, id: str, name: str, description: str = None) -> None:
        self.id = id
        self.name = name
        self.description = description

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
