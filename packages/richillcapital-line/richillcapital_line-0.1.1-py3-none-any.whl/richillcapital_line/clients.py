import json

from richillcapital_http import HttpClient, HttpMethod, HttpRequest

from richillcapital_line.exceptions import LineNotifyException

from .models import LineNotifyStatus


class LineNotifyClient:
    """
    A client for the LINE Notify API.

    Args:
        access_token: The LINE Notify API access token.
    """

    BASE_ADDRESS = "https://notify-api.line.me"

    def __init__(self, access_token: str) -> None:
        self.__access_token = access_token or ""
        self.__http_client = HttpClient(self.BASE_ADDRESS)

    async def send_notification_async(
        self, message: str, notification_disabled: bool = False
    ) -> LineNotifyStatus:
        """ """
        request = HttpRequest(
            HttpMethod.POST,
            "/api/notify",
            headers={
                "Authorization": f"Bearer {self.__access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body={"message": message, "notificationDisabled": notification_disabled},
        )
        response = await self.__http_client.send_async(request)
        content = await response.content.read_as_string_async()
        response_json: dict = json.loads(content)

        if response.status_code != 200:
            raise LineNotifyException(
                response.status_code, response_json.get("message", "")
            )

        return LineNotifyStatus.parse_response(response)

    async def get_status_async(self) -> LineNotifyStatus:
        """
        Get the status of the LINE Notify API.

        Returns:
            A dictionary containing the response from the API.
        """
        request = HttpRequest(
            HttpMethod.GET,
            "/api/status",
            headers={
                "Authorization": f"Bearer {self.__access_token}",
            },
        )
        response = await self.__http_client.send_async(request)
        content = await response.content.read_as_string_async()
        response_json: dict[str, str] = json.loads(content)
        if response.status_code != 200:
            raise LineNotifyException(
                response.status_code, response_json.get("message", "")
            )
        return LineNotifyStatus.parse_response(response)
