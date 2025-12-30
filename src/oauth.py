from pathlib import Path
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

TOKEN_PATH = Path.home() / ".secrets" / "gmail_token.json"


def get_gmail_credentials() -> Credentials:
    """Obtiene credenciales OAuth válidas para Gmail"""

    creds = None

    # Cargar token existente
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH, SCOPES
        )

    # Si no es válido, refrescar o pedir login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

            if not credentials_path:
                raise RuntimeError(
                    "GOOGLE_APPLICATION_CREDENTIALS no está definida"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Guardar token
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())

    return creds
