from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    api_token: SecretStr = Field(alias="API_TOKEN")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="UTF-8"
    )


config = Settings()
