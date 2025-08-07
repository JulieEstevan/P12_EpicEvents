import os
from dotenv import load_dotenv
from pathlib import Path


# Define the path to the .env file and token file
env_path = Path(__file__).resolve().parent / '.env'
token_path = Path(__file__).resolve().parent / '.token'

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# Secret Key
SECRET_KEY: str = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "The SECRET_KEY environment variable is not defined."
        "Please check your settings and .env file."
    )

# Database
DATABASE_URL: str = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "The DATABASE_URL environment variable is not defined."
        "Please check your settings and .env file."
    )

# Sentry
SENTRY_DSN: str = os.getenv("SENTRY_DSN")
if not SENTRY_DSN:
    raise ValueError(
        "The SENTRY_DSN environment variable is not defined."
        "Please check your settings and .env file."
    )
SENTRY_ENVIRONMENT: str = os.getenv("SENTRY_ENVIRONMENT", "production")
if not SENTRY_ENVIRONMENT:
    raise ValueError(
        "The SENTRY_ENVIRONMENT environment variable is not defined."
        "Please check your settings and .env file."
    )

# Token
TOKEN_FILE = Path(token_path).expanduser()
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
if not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError(
        "The ACCESS_TOKEN_EXPIRE_MINUTES environment variable is not defined."
        "Please check your settings and .env file."
    )
ALGORITHM: str = "HS256"
