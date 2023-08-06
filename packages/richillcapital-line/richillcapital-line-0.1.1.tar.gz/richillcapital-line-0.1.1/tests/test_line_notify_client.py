import os

import dotenv
import pytest

from richillcapital_line import LineNotifyClient

dotenv.load_dotenv()

test_token = os.getenv("ACCESS_TOKEN", "")
invalid_token = "Invalid token"


@pytest.fixture
def client():
    return LineNotifyClient(test_token)


@pytest.mark.asyncio
async def test_send_notification_success(client: LineNotifyClient):
    message = "Test message from pytest"
    response = await client.send_notification_async(message)
    assert response is not None
    assert response.status == 200


@pytest.mark.asyncio
async def test_send_notification_invalid_token():
    invalid_client = LineNotifyClient(invalid_token)
    message = "Test message from pytest"
    with pytest.raises(Exception):
        await invalid_client.send_notification_async(message)


@pytest.mark.asyncio
async def test_send_notification_bad_request(client: LineNotifyClient):
    message = ""
    with pytest.raises(Exception):
        await client.send_notification_async(message)


@pytest.mark.asyncio
async def test_get_status_success(client: LineNotifyClient):
    response = await client.get_status_async()
    assert response is not None
