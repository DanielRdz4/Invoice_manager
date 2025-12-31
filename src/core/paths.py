from pathlib import Path

UTILS_DIR = Path(__file__).resolve().parent
SRC_DIR = UTILS_DIR.parent
ROOT_DIR = SRC_DIR.parent
DATA_DIR = SRC_DIR / "data"

# Directorio home del usuario (Windows / Linux / macOS)
HOME_DIR = Path.home()

# Secrets fuera del proyecto (no versionado)
SECRETS_DIR = HOME_DIR / ".secrets"

# Archivos sensibles
GMAIL_CLIENT_SECRET = SECRETS_DIR / "credentials.json"
GMAIL_TOKEN = SECRETS_DIR / "gmail_token.json"
