#Manages user's configuration

import json
from src.core.paths import DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, DB_DIR, XLSX_DIR
USER_CONFIG_PATH = DATA_DIR / "user_config.json"

def get_user_config():
    """Obtains user preferences for configurations"""

    while True:

        sender_email = input("Sender's e-mail: ").strip()
        print(f"Sender's email: {sender_email}")
        confirmation = input("Is the sender's email correct (Y/N): ").strip().upper()

        if confirmation == "Y":
            return {
                "sender_email": sender_email
            }
        
def load_user_config():
    """Reads existing user's configuration"""
    try:
        with USER_CONFIG_PATH.open("r", encoding= "utf-8") as f:
            return json.load(f)
        
    except (json.JSONDecodeError, FileNotFoundError):
        print("user_config.json can't be read.")
        return None


def fetch_user_config():
    """Looks for user configuration, creates it if it doesn´t exist"""

    DATA_DIR.mkdir(parents=True, exist_ok= True)
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    XLSX_DIR.mkdir(parents=True, exist_ok=True)

    config = load_user_config()

    if config is None:
       user_config = get_user_config()
       with USER_CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(user_config, f, indent= 4)
            return user_config
    return config

    

