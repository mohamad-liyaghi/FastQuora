from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All environment variables are loaded here.
    """

    model_config = SettingsConfigDict(env_file=".env")
    ENVIRONMENT: str
    DEBUG: bool
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_URL: str
    REDIS_URL: str
    JAEGER_HOST: str
    JAEGER_PORT: int
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUETS: int


settings: Settings = Settings()
