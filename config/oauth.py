"""config/oauth.py — Epic OAuth2 SMART on FHIR authentication.

Supports two flows:
  1. Backend Services (M2M) — JWT client assertion, no user interaction.
     Used for system-level agent access (recommended for multi-agent systems).
  2. Standalone Launch — Authorization code flow for user-facing apps.

Docs: https://fhir.epic.com/Documentation?docId=oauth2
"""

import time
import uuid
import httpx
import jwt  # PyJWT
from loguru import logger
from config.settings import settings


# ---------------------------------------------------------------------------
# Token cache (in-memory; swap for Redis in production)
# ---------------------------------------------------------------------------
_token_cache: dict = {
    "access_token": None,
    "expires_at": 0,
}


# ---------------------------------------------------------------------------
# Backend Services Flow (JWT Client Assertion — SMART on FHIR Backend Services)
# ---------------------------------------------------------------------------

def _build_jwt_assertion() -> str:
    """Build a signed JWT client assertion for Epic Backend Services auth."""
    now = int(time.time())
    payload = {
        "iss": settings.epic_client_id,
        "sub": settings.epic_client_id,
        "aud": settings.epic_token_url,
        "jti": str(uuid.uuid4()),
        "exp": now + 300,  # 5-minute expiry
        "iat": now,
    }
    token = jwt.encode(
        payload,
        settings.epic_private_key,
        algorithm="RS384",
    )
    logger.debug("JWT client assertion built")
    return token


def get_backend_access_token() -> str:
    """
    Obtain an Epic access token using the SMART Backend Services flow.
    Caches the token until 60 seconds before expiry.
    """
    now = int(time.time())

    # Return cached token if still valid
    if _token_cache["access_token"] and now < _token_cache["expires_at"] - 60:
        logger.debug("Using cached Epic access token")
        return _token_cache["access_token"]

    logger.info("Requesting new Epic access token (Backend Services flow)")
    assertion = _build_jwt_assertion()

    response = httpx.post(
        settings.epic_token_url,
        data={
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": assertion,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )

    response.raise_for_status()
    token_data = response.json()

    _token_cache["access_token"] = token_data["access_token"]
    _token_cache["expires_at"] = now + int(token_data.get("expires_in", 3600))

    logger.info(f"Epic access token obtained. Expires in {token_data.get('expires_in', 3600)}s")
    return _token_cache["access_token"]


# ---------------------------------------------------------------------------
# Standalone Launch Flow (Authorization Code — user-facing apps)
# ---------------------------------------------------------------------------

def get_authorization_url(state: str = None) -> str:
    """Build the Epic authorization URL for Standalone Launch flow."""
    state = state or str(uuid.uuid4())
    params = (
        f"response_type=code"
        f"&client_id={settings.epic_client_id}"
        f"&redirect_uri={settings.epic_redirect_uri}"
        f"&scope=openid+fhirUser+launch+patient/*.read+patient/*.write"
        f"&state={state}"
        f"&aud={settings.epic_fhir_base_url}"
    )
    url = f"{settings.epic_authorize_url}?{params}"
    logger.info(f"Authorization URL built for state={state}")
    return url


def exchange_code_for_token(code: str) -> dict:
    """Exchange an authorization code for an Epic access + refresh token."""
    logger.info("Exchanging authorization code for Epic token")
    response = httpx.post(
        settings.epic_token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.epic_redirect_uri,
            "client_id": settings.epic_client_id,
            "client_secret": settings.epic_client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    response.raise_for_status()
    token_data = response.json()
    logger.info("Authorization code exchanged successfully")
    return token_data


def refresh_access_token(refresh_token: str) -> dict:
    """Refresh an expired Epic access token using a refresh token."""
    logger.info("Refreshing Epic access token")
    response = httpx.post(
        settings.epic_token_url,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": settings.epic_client_id,
            "client_secret": settings.epic_client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    response.raise_for_status()
    token_data = response.json()
    logger.info("Epic access token refreshed successfully")
    return token_data
