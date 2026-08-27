from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MCP_HOST: str = "0.0.0.0"
    MCP_PORT: int = 8000
    MCP_ENV: str = "local"

    DATAGOV_API_ENV: str = "prod"
    DATAGOV_API_BASE_URL: str = "https://www.data.gov.tn/api/3"
    DATAGOV_API_KEY: str = ""

    LOG_LEVEL: str = "INFO"

    SENTRY_DSN: str = ""
    SENTRY_SAMPLE_RATE: float = 1.0

    ALLOWED_HOSTS: str = "data.gov.tn,www.data.gov.tn,mcp.data.gov.tn"
    ALLOWED_ORIGINS: str = "*"
    CORS_ENABLED: bool = True

    MAX_PAGE_SIZE: int = 100
    MAX_DOWNLOAD_SIZE_MB: int = 100
    REQUEST_TIMEOUT: int = 30


settings = Settings()