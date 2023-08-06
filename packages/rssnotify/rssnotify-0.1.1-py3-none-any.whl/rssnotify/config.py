from pydantic import BaseSettings, Field


class Config(BaseSettings):
    urls: list[str] = []
    keywords: list[str] = []
    since_hours: int = Field(gt=0)
    command: list[str] | None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()
