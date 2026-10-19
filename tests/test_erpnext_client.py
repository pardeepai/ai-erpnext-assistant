
import pytest
import requests
from unittest.mock import Mock, patch

from app.erpnext.client import ERPNextClient, ERPNextAPIError


@pytest.fixture
def client():
    # Avoid requiring real credentials for unit tests.
    with patch.dict(
        "os.environ",
        {
            "ERPNEXT_URL": "http://localhost:8000",
            "ERPNEXT_API_KEY": "test_key",
            "ERPNEXT_API_SECRET": "test_secret",
        },
    ):
        return ERPNextClient()


@patch("app.erpnext.client.requests.get")
def test_successful_request(mock_get, client):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"data": [{"name": "ITEM-001"}]}
    mock_get.return_value = response

    result = client.get("/api/resource/Item")

    assert result["data"][0]["name"] == "ITEM-001"


@patch("app.erpnext.client.requests.get")
def test_authentication_error(mock_get, client):
    response = Mock()
    response.status_code = 401

    mock_get.return_value = Mock(
        raise_for_status=Mock(
            side_effect=requests.HTTPError(response=response)
        )
    )

    with pytest.raises(
        ERPNextAPIError, match="authentication failed"
    ):
        client.get("/api/resource/Item")


@patch("app.erpnext.client.requests.get")
def test_timeout(mock_get, client):
    mock_get.side_effect = requests.Timeout()

    with pytest.raises(ERPNextAPIError, match="timed out"):
        client.get("/api/resource/Item")


@patch("app.erpnext.client.requests.get")
def test_connection_error(mock_get, client):
    mock_get.side_effect = requests.ConnectionError()

    with pytest.raises(ERPNextAPIError, match="connect to ERPNext"):
        client.get("/api/resource/Item")



@patch("app.erpnext.client.requests.get")
def test_internal_server_error(mock_get, client):
    response = Mock()
    response.status_code = 500

    mock_get.return_value = Mock(
        raise_for_status=Mock(
            side_effect=requests.HTTPError(response=response)
        )
    )

    with pytest.raises(
        ERPNextAPIError, match="status 500"
    ):
        client.get("/api/resource/Item")



@patch("app.erpnext.client.requests.get")
def test_permission_denied(mock_get, client):
    response = Mock()
    response.status_code = 403

    mock_get.return_value = Mock(
        raise_for_status=Mock(
            side_effect=requests.HTTPError(response=response)
        )
    )

    with pytest.raises(
        ERPNextAPIError, match="Permission denied"
    ):
        client.get("/api/resource/Item")