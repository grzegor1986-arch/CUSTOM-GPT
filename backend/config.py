"""Runtime configuration for backend services."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    stripe_secret_key: str = Field(default="", alias="STRIPE_SECRET_KEY")
    stripe_price_id: str = Field(default="", alias="STRIPE_PRICE_ID")
    stripe_webhook_secret: str = Field(default="", alias="STRIPE_WEBHOOK_SECRET")
    frontend_success_url: str = Field(
        default="https://yourdomain.com/success", alias="FRONTEND_SUCCESS_URL"
    )
    frontend_cancel_url: str = Field(
        default="https://yourdomain.com", alias="FRONTEND_CANCEL_URL"
    )
    app_name: str = Field(default="ai-product", alias="APP_NAME")
    vercel_token: str = Field(default="", alias="VERCEL_TOKEN")
    railway_token: str = Field(default="", alias="RAILWAY_TOKEN")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
