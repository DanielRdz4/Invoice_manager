from src.oauth import get_gmail_credentials
from src.gmail_api import get_gmail_service
from src.core.config import fetch_user_config


def main():

    #login
    creds = get_gmail_credentials()
    service = get_gmail_service(creds)

    #Show active user's email
    profile = service.users().getProfile(userId="me").execute()
    print("Correo autenticado:", profile["emailAddress"])

    user_config = fetch_user_config()
    print(user_config)

if __name__ == "__main__":
    main()
