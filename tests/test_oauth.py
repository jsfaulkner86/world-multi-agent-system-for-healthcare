"""test_oauth.py — Unit tests for Epic OAuth2 SMART on FHIR flows."""

import pytest
import time
from unittest.mock import patch, MagicMock
from config import oauth


@patch("config.oauth.httpx.post")
@patch("config.oauth._build_jwt_assertion", return_value="mocked.jwt.token")
def test_get_backend_access_token_success(mock_jwt, mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "test_token_abc", "expires_in": 3600}
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    # Clear cache
    oauth._token_cache["access_token"] = None
    oauth._token_cache["expires_at"] = 0

    token = oauth.get_backend_access_token()
    assert token == "test_token_abc"
    mock_post.assert_called_once()


@patch("config.oauth.httpx.post")
@patch("config.oauth._build_jwt_assertion", return_value="mocked.jwt.token")
def test_get_backend_access_token_uses_cache(mock_jwt, mock_post):
    # Pre-warm cache with a future expiry
    oauth._token_cache["access_token"] = "cached_token"
    oauth._token_cache["expires_at"] = int(time.time()) + 3600

    token = oauth.get_backend_access_token()
    assert token == "cached_token"
    mock_post.assert_not_called()  # Should NOT call Epic — using cache


def test_get_authorization_url_contains_client_id():
    with patch("config.oauth.settings") as mock_settings:
        mock_settings.epic_client_id = "test-client-123"
        mock_settings.epic_redirect_uri = "https://localhost/callback"
        mock_settings.epic_authorize_url = "https://fhir.epic.com/oauth2/authorize"
        mock_settings.epic_fhir_base_url = "https://fhir.epic.com/api/FHIR/R4"

        url = oauth.get_authorization_url(state="test-state")
        assert "test-client-123" in url
        assert "test-state" in url
        assert "response_type=code" in url


@patch("config.oauth.httpx.post")
def test_exchange_code_for_token(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "access_token": "exchange_token",
        "refresh_token": "refresh_abc",
        "expires_in": 3600,
    }
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    result = oauth.exchange_code_for_token(code="auth_code_xyz")
    assert result["access_token"] == "exchange_token"
    assert result["refresh_token"] == "refresh_abc"


@patch("config.oauth.httpx.post")
def test_refresh_access_token(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "refreshed_token", "expires_in": 3600}
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    result = oauth.refresh_access_token(refresh_token="refresh_abc")
    assert result["access_token"] == "refreshed_token"
