import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    VERSION: str = os.getenv("VERSION", "")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "")
    EMBEDDING_URL: str = os.getenv("EMBEDDING_URL", "")

    PGADMIN_DEFAULT_EMAIL: str = os.getenv("PGADMIN_DEFAULT_EMAIL", "")
    PGADMIN_DEFAULT_PASSWORD: str = os.getenv("PGADMIN_DEFAULT_PASSWORD", "")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")

    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
