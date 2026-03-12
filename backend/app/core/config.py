from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Avigentis Cyber Readiness Scanner API'
    database_url: str = 'postgresql+psycopg2://avigentis:avigentis@db:5432/avigentis'
    redis_url: str = 'redis://redis:6379/0'
    secret_key: str = 'change-me'
    admin_email: str = 'admin@avigentis.bg'
    admin_password: str = 'admin123'
    frontend_url: str = 'http://localhost:3000'
    scan_rate_limit_per_minute: int = 5


settings = Settings()
