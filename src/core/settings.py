from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All environment variables are loaded here.
    """

    model_config = SettingsConfigDict(env_file=".env")
    ENVIRONMENT: str = "LOCAL"
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int


settings: Settings = Settings()
