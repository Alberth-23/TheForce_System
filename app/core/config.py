from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "TheForce System Enterprise"
    DATABASE_URL: str = "postgresql://theforce:JiLchuSwX6xksmeJi8k0a13ITSH0Shov@dpg-d8190avavr4c73b6rmq0-a.virginia-postgres.render.com/theforcedb"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"

settings = Settings()
