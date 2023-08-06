from datetime import datetime as DateTime

from richillcapital_http import HttpResponse


class RateLimit:
    """ """

    def __init__(self, limit: int, remaining: int) -> None:
        self.__limit = limit
        self.__remaning = remaining

    @property
    def limit(self) -> int:
        return self.__limit

    @property
    def remaining(self) -> int:
        return self.__remaning


class LineNotifyStatus(object):
    """ """

    def __init__(
        self,
        reset_time: DateTime,
        message_rate_limit: RateLimit,
        image_rate_limit: RateLimit,
    ):
        """"""
        self.__message_rate_limit: RateLimit = message_rate_limit
        self.__image_rate_limit: RateLimit = image_rate_limit
        self.__reset_time = reset_time

    @property
    def message(self) -> RateLimit:
        return self.__message_rate_limit

    @property
    def image(self) -> RateLimit:
        return self.__image_rate_limit

    @property
    def reset_time(self) -> DateTime:
        return self.__reset_time

    @classmethod
    def parse_response(cls, response: HttpResponse) -> "LineNotifyStatus":
        headers: dict = response.headers
        return LineNotifyStatus(
            DateTime.fromtimestamp(int(headers.get("X-RateLimit-Reset", 0))),
            RateLimit(
                headers.get("X-RateLimit-Limit", 0),
                headers.get("X-RateLimit-Remaining", 0),
            ),
            RateLimit(
                headers.get("X-RateLimit-ImageLimit", 0),
                headers.get("X-RateLimit-ImageRemaining", 0),
            ),
        )
