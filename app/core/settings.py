from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "socmed-analyst"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./database.db"
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    APIFY_API_KEY: str
    APIFY_TIKTOK_ACTOR: str = "GdWCkxBtKWOsKjdch"
    REDIS_URL: str = "redis://localhost:6379"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore[call-arg]
