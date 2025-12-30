from utils.oauth import get_gmail_credentials
from utils.gmail_api import get_gmail_service


def main():
    creds = get_gmail_credentials()
    service = get_gmail_service(creds)

    profile = service.users().getProfile(userId="me").execute()
    print("Correo autenticado:", profile["emailAddress"])


if __name__ == "__main__":
    main()
