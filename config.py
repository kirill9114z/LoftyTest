import os
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()


@dataclass(frozen=True)
class Config:
    API_KEY: str
    LIMITS_PER_MIN: int
    BASE_URL: str
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2


def get_config() -> Config:
    return Config(
        API_KEY=str(os.getenv("API_KEY", '')),
        LIMITS_PER_MIN=int(os.getenv("LIMITS_PER_MIN", 0)),
        BASE_URL="https://api.openweathermap.org"
    )