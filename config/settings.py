"""config/settings.py — Pydantic-based system configuration."""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")

    # Epic FHIR Base
    epic_fhir_base_url: str = Field(
        default="https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4",
        env="EPIC_FHIR_BASE_URL",
    )

    # Epic OAuth2 SMART on FHIR
    epic_client_id: str = Field(default="", env="EPIC_CLIENT_ID")
    epic_client_secret: str = Field(default="", env="EPIC_CLIENT_SECRET")
    epic_redirect_uri: str = Field(default="https://localhost/callback", env="EPIC_REDIRECT_URI")
    epic_token_url: str = Field(
        default="https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
        env="EPIC_TOKEN_URL",
    )
    epic_authorize_url: str = Field(
        default="https://fhir.epic.com/interconnect-fhir-oauth/oauth2/authorize",
        env="EPIC_AUTHORIZE_URL",
    )

    # Epic Backend Services (JWT / RS384)
    # Path to your RSA private key PEM file registered in Epic App Orchard
    epic_private_key_path: str = Field(default="", env="EPIC_PRIVATE_KEY_PATH")

    @property
    def epic_private_key(self) -> str:
        """Load RSA private key from file path."""
        if not self.epic_private_key_path:
            raise ValueError("EPIC_PRIVATE_KEY_PATH is not set in .env")
        with open(self.epic_private_key_path, "r") as f:
            return f.read()

    # Redis
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_password: str = Field(default="", env="REDIS_PASSWORD")

    # System
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    environment: str = Field(default="development", env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
