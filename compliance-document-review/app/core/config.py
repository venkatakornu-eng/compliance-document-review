from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Compliance Document Review App"
    ENVIRONMENT: str = "development"

    MAX_UPLOAD_MB: int = 15

    PII_LANGUAGE: str = "en"
    PII_SCORE_THRESHOLD: float = 0.45

    ENABLE_DEV_PAYLOAD_VIEWER: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()