from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # 1. Define fields with types.
    # If a variable is missing from .env and has no default here, the app will crash (Good!)
    APP_NAME: str = "EdgeCtrl Central Server"
    DEBUG_MODE: bool = False

    # Database (Required - no default)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    # Computed property (Optional helper)
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"

    # 2. Configuration to read from .env file automatically
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# 3. Caching: Read the file once, then cache it in memory.
# This prevents reading the disk on every single API request.
@lru_cache
def get_settings():
    return Settings()