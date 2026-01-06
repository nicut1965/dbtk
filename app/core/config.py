from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str  = "postgresql+psycopg2://nictic2002:admin123@localhost:5432/dbtk"
    
    class Config:
        env_file = ".env"

settings = Settings()