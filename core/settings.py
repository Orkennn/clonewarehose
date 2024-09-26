from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    api_prefix: str = "/api"
    db_user: str = "username1"
    db_password: str = "password123"
    db_name: str = "database"

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@clonewarehose-database-1:5433/{self.db_name}"

    @property
    def db_url_sync(self) -> str:
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@clonewarehose-database-1:5433/{self.db_name}"
    db_echo: bool = False


settings = Setting()