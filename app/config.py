# app/config.py
import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded from .env file")

class Settings:
    # Firebase settings
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "mdd2-2586d")  # Updated to new project ID
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", '')
    FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY", "")  # Add this line for the API key
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # API settings
    API_TITLE: str = "Data Dojo API"
    API_VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Logging
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

    def __init__(self):
        # Log key configuration values (but not sensitive ones like API keys)
        logger.debug(f"Firebase Project ID: {self.FIREBASE_PROJECT_ID}")
        logger.debug(f"Firebase Credentials Path: {self.FIREBASE_CREDENTIALS_PATH}")
        logger.debug(f"Debug mode: {self.DEBUG}")
        
        # Check if credential file exists
        if not os.path.exists(self.FIREBASE_CREDENTIALS_PATH):
            logger.warning(f"Firebase credentials file not found at: {self.FIREBASE_CREDENTIALS_PATH}")

settings = Settings()