"""Configuration management for the logger application."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the project directory
# First try to load from the package directory, then from current directory
_package_dir = Path(__file__).parent.parent.parent
_env_file = _package_dir / ".env"
if _env_file.exists():
    load_dotenv(_env_file)
else:
    load_dotenv()  # Try current directory as fallback


class Config:
    """Application configuration."""
    
    # Project root directory (where data should be stored)
    # For global installation, this points to the package installation directory
    ROOT_DIR = Path(__file__).parent.parent.parent
    
    # Default data directory in user's home directory for global installations
    DEFAULT_DATA_DIR = Path.home() / ".logger" / "data"
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Database Configuration
    # If DATABASE_PATH is set and is absolute, use it
    # If it's relative, resolve it relative to ROOT_DIR
    # If not set, use the default data directory in user's home
    _db_path = os.getenv("DATABASE_PATH")
    if _db_path:
        _db_path_obj = Path(_db_path)
        if _db_path_obj.is_absolute():
            DATABASE_PATH = str(_db_path_obj)
        else:
            # Relative path: resolve relative to ROOT_DIR
            DATABASE_PATH = str(ROOT_DIR / _db_path)
    else:
        # Default: use home directory
        DATABASE_PATH = str(DEFAULT_DATA_DIR / "logger.db")
    
    # Image Storage Configuration
    _img_path = os.getenv("IMAGE_STORAGE_PATH")
    if _img_path:
        _img_path_obj = Path(_img_path)
        if _img_path_obj.is_absolute():
            IMAGE_STORAGE_PATH = str(_img_path_obj)
        else:
            # Relative path: resolve relative to ROOT_DIR
            IMAGE_STORAGE_PATH = str(ROOT_DIR / _img_path)
    else:
        # Default: use home directory
        IMAGE_STORAGE_PATH = str(DEFAULT_DATA_DIR / "images")
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please set it in .env file or as environment variable."
            )
        
        # Ensure directories exist
        Path(cls.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
        Path(cls.IMAGE_STORAGE_PATH).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_database_url(cls):
        """Get SQLAlchemy database URL."""
        return f"sqlite:///{cls.DATABASE_PATH}"


# Create a singleton instance
config = Config()

