from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from src.core.paths import GMAIL_CLIENT_SECRET, GMAIL_TOKEN

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_credentials() -> Credentials:
    """Obtiene credenciales OAuth válidas para Gmail"""

    creds = None

    # Cargar token existente
    if GMAIL_TOKEN.exists():
        creds = Credentials.from_authorized_user_file(
            GMAIL_TOKEN, SCOPES
        )

    # Refrescar o pedir login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not GMAIL_CLIENT_SECRET.exists():
                raise FileNotFoundError(
                    f"No existe el archivo OAuth: {GMAIL_CLIENT_SECRET}"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                GMAIL_CLIENT_SECRET,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Guardar token
        GMAIL_TOKEN.parent.mkdir(parents=True, exist_ok=True)
        GMAIL_TOKEN.write_text(creds.to_json())

    return creds
