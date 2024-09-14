import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from portals.click_pay import ClickPay
from rest_server import app
from utils import get_data_from_sqlite


@pytest.mark.asyncio
async def test_click_pay(snapshot):
    async with ClickPay("micael.lasry@gmail.com", "Micael123") as click_pay:
        response = await click_pay.get_data()
        snapshot.assert_match(json.dumps(response, indent=2), "get_click_pay_snapshot")


client = TestClient(app)


@pytest.mark.asyncio
async def test_save_data():
    # Mock the get_data method
    with patch(
        "portals.click_pay.ClickPay.get_data", new_callable=AsyncMock
    ) as mock_get_data:
        # Define the mock return value
        mock_get_data.return_value = {
            "email": "test@example.com",
            "phone": "+1234567890",
            "management_company": "Test Company",
            "address": "123 Test St, Test City, TX",
        }

        # Prepare the command request data
        command_data = {
            "tenant_portal": "click_pay",
            "username": "testuser",
            "password": "testpassword",
        }

        # Perform the request
        response = client.post("/save_data/", json=command_data)

        # Check the response status code
        assert response.status_code == 200
        assert response.json() == {
            "message": "Data saved or updated in SQLite database."
        }

        # Ensure that get_data was called
        mock_get_data.assert_called_once()

        saved_data = await get_data_from_sqlite("test@example.com")

        # Check that the saved data matches the expected data
        assert saved_data == (
            "test@example.com",
            "+1234567890",
            "Test Company",
            "123 Test St, Test City, TX",
        )
