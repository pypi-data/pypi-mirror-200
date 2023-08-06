from typing import Literal
from ._option import Option


class Poll():
    def __init__(self, id: str, options: list[Option], duration_minutes: int, end_datetime: str = None, voting_status: Literal['open', 'closed'] = None) -> None:
        """
        - options: Contains objects describing each choice in the referenced poll.
        """
        self.id = id
        self.options = [Option(**x) for x in options]
        self.duration_minutes = duration_minutes
        self.end_datetime = end_datetime
        self.voting_status = voting_status

    def json(self):
        return {
            "id": self.id,
            "options": str(self.options),
            "duration_minutes": self.duration_minutes,
            "end_datetime": self.end_datetime,
            "voting_status": self.voting_status,
        }

    def __str__(self) -> str:
        return '\n'.join([
            '{s:{c}<{n}}'.format(s=f'Poll: ({self.voting_status}) ', n=70, c='-'),
            '\n'.join([str(o) for o in self.options]),
            "--",
            f"Duration (minutes): {self.duration_minutes}",
            f"End date: {self.end_datetime}",
            "-"*70
        ])
