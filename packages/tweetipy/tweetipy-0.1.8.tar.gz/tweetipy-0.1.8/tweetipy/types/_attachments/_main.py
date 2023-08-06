class Attachments():
    def __init__(self, media_keys: list[str] = None, poll_ids: list[str] = None) -> None:
        self.media_keys = media_keys
        self.poll_ids = poll_ids
