#Manages user's configuration
import json
from src.utils.json_management import load_json, create_json
from src.core.paths import DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, DB_DIR, XLSX_DIR, USER_CONFIG_PATH


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
        return load_json(USER_CONFIG_PATH)
    
    except (json.JSONDecodeError, FileNotFoundError):
        print("user_config.json can't be read.")
        return None

def confirm_structure():
    """Makes sure that necessary directories exist"""

    DATA_DIR.mkdir(parents=True, exist_ok= True)
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    XLSX_DIR.mkdir(parents=True, exist_ok=True)


def fetch_user_config():
    """Looks for user configuration, creates it if it doesn´t exist"""
    
    confirm_structure()
    config = load_user_config()
    
    if config is None:
       user_config = get_user_config()
       create_json(user_config, USER_CONFIG_PATH)
       return user_config
    
    return config

    

