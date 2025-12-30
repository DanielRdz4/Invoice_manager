from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def get_gmail_service(credentials: Credentials):
    """Crea el servicio Gmail API"""
    return build("gmail", "v1", credentials=credentials)

