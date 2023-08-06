from enum import StrEnum

class PollFields(StrEnum):
    """
    The Tweet will only return poll fields if the Tweet contains a poll and if
    you've also included the expansions=attachments.poll_ids query parameter in
    your request.
    """
    duration_minutes = "duration_minutes"
    end_datetime = "end_datetime"
    id = "id"
    options = "options"
    voting_status = "voting_status"
