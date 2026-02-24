import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL missing in .env")

APP_ENV = os.getenv("APP_ENV", "development")
DEFAULT_CONSENT_VERSION = os.getenv("DEFAULT_CONSENT_VERSION", "v1.0")