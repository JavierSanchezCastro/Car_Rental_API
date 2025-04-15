from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MySQLDsn

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    DB_USER: str
    DB_HOST: str
    DB_NAME: str
    DB_PREFIX: str
    DB_PORT: int

    DB_PASSWORD: str
    
    @property
    def DB_URL(cls) -> MySQLDsn:
        return MySQLDsn.build(
            scheme=cls.DB_PREFIX,
            username=cls.DB_USER,
            password=str(cls.DB_PASSWORD),
            host=cls.DB_HOST,
            port=cls.DB_PORT,
            path=cls.DB_NAME,
        )
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()