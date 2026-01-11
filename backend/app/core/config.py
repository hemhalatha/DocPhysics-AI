import os

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    UPLOAD_DIR: str = "uploads"
    PROCESSED_DIR: str = "processed"

settings = Settings()
