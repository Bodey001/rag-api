import os

from dotenv import load_dotenv

load_dotenv()



class Settings:
    VERSION: str = os.getenv("VERSION", "")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "")
    EMBEDDING_URL: str = os.getenv("EMBEDDING_URL", "")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    PGADMIN_DEFAULT_EMAIL: str = os.getenv("PGADMIN_DEFAULT_EMAIL", "")
    PGADMIN_DEFAULT_PASSWORD: str = os.getenv("PGADMIN_DEFAULT_PASSWORD", "")
