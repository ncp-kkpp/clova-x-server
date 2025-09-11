import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
        hyperclova_api_key: str
        hyperclova_primary_key: str
        hyperclova_request_id: str
        app_title: str = "HyperCLOVA X Chat API"
        app_version: str = "1.0.0"
                            
class Config:
        env_file = ".env"

settings = Settings()
