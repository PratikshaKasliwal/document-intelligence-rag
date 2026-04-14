from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Document Intelligence System")
    ENV: str = os.getenv("ENV", "development")

settings = Settings()