from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # defaults allow running tests without .env; production should override via env vars
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "password"
    database_name: str = "fastAPI"
    database_username: str = "postgres"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

                        
settings = Settings()