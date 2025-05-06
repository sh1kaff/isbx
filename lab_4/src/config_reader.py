from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    """Class for settings (`.env` file with telegram bot `API_TOKEN`)"""
    api_token: SecretStr = Field(alias="API_TOKEN")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="UTF-8"
    )


config = Settings()
