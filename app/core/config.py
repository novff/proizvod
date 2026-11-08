from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Software Support Lab"
    secret_key: str = "development-only-change-me"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./local.db"
    admin_email: str = "admin@example.com"
    admin_password: str = "Admin12345!"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
