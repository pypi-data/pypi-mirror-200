class Response:
    def __init__(
        self,
        status_code: int,
        text: str = None,
        json: str = None,
    ):
        self.text = text
        self.json = json
        self.status_code = status_code
