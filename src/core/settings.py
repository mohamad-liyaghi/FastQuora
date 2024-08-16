from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All environment variables are loaded here.
    """

    model_config = SettingsConfigDict(env_file=".env")
    ENVIRONMENT: str = "LOCAL"
    DEBUG: bool = True if ENVIRONMENT == "LOCAL" else False
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_URL: str


settings: Settings = Settings()
