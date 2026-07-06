from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./solca_parte_diario.db"
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # Variables de base de datos HIS (Removidas para entorno demo)

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
