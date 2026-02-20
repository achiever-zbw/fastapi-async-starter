from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings) : 
    API_V1_STR : str = "/api/v1"
    PROJECT_NAME : str = "任务协作系统"
    DATABASE_URL : str
    REDIS_URL : str = "redis://127.0.0.1:6379"
    SECRET_KEY : str = "secret_key"
    JWT_ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 30
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()  