#Manages user's configuration

import json
from src.core.paths import DATA_DIR
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
        print("user_config.json can't be read. Recreating it")
        USER_CONFIG_PATH.unlink()
        return fetch_user_config()


def fetch_user_config():
    """Looks for user configuration, creates it if it doesn´t exist"""

    DATA_DIR.mkdir(parents=True, exist_ok= True)

    if not USER_CONFIG_PATH.exists():
       
       user_config = get_user_config()
       with USER_CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(user_config, f, indent= 4)
    

    
    return load_user_config()
    

    

