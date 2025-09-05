from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    mango_api_key: str = Field(..., description="Mango Office API key")
    mango_salt: str = Field(..., description="Salt for request signature")
    mango_api_url: str = Field(
        default="https://app.mango-office.ru/vpbx/trunks/numbers",
        description="Mango Office API URL",
    )

    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")
    postgres_db: str = Field(..., description="PostgreSQL database name")
    postgres_user: str = Field(..., description="PostgreSQL user")
    postgres_password: str = Field(..., description="PostgreSQL password")

    log_level: str = Field(default="INFO", description="Logging level")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
