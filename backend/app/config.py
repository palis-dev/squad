from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Squad Platform"
    debug: bool = False
    
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    
    database_url: str = "postgresql+asyncpg://localhost/squad"
    
    devin_api_key: str = ""
    devin_api_url: str = "https://api.devin.ai"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
