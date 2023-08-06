



class LineNotifyException(Exception):
    """Exception raised when there is an error in LINE Notify API response."""

    def __init__(self, status: int, message: str):
        super().__init__(f"LineNotify API returned error {status}: {message}")
        self.status = status
        self.message = message
