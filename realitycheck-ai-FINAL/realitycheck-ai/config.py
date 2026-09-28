import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

# API Keys
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "").strip()

# Database Config
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "history.sqlite"

# App Metadata
APP_NAME = "REALITYCHECK AI"
APP_TAGLINE = "Search the live web. Compare the evidence. Understand the claim."
APP_VERSION = "1.0.0"

def get_serpapi_key(runtime_key: str = None) -> str:
    """Return runtime key if provided, else environment key."""
    if runtime_key and runtime_key.strip():
        return runtime_key.strip()
    return os.getenv("SERPAPI_KEY", "").strip()
