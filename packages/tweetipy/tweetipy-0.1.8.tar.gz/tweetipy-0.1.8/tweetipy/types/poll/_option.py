class Option():
    def __init__(self, position: int, label: str, votes: int) -> None:
        self.position = position
        self.label = label
        self.votes = votes

    def __str__(self) -> str:
        return f"{self.position}: {self.label}. 🗳️: {self.votes}"
