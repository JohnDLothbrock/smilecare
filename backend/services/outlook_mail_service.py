import html
import os
from pathlib import Path
from urllib.parse import urlencode

import msal
import requests
from dotenv import load_dotenv


BACKEND_DIR = (
    Path(__file__).resolve().parents[1]
)

ENV_FILE = (
    BACKEND_DIR / ".env"
)

TOKEN_CACHE_FILE = (
    BACKEND_DIR
    / ".microsoft_token_cache.bin"
)

load_dotenv(ENV_FILE)


MICROSOFT_CLIENT_ID = os.getenv(
    "MICROSOFT_CLIENT_ID"
)

MICROSOFT_AUTHORITY = os.getenv(
    "MICROSOFT_AUTHORITY",
    "https://login.microsoftonline.com/consumers"
)

MICROSOFT_SENDER_EMAIL = os.getenv(
    "MICROSOFT_SENDER_EMAIL"
)

FRONTEND_RESET_PASSWORD_URL = os.getenv(
    "FRONTEND_RESET_PASSWORD_URL",
    "http://localhost:5173/reset-password"
)


MAIL_SCOPES = [
    "https://graph.microsoft.com/Mail.Send"
]

GRAPH_SEND_MAIL_URL = (
    "https://graph.microsoft.com/"
    "v1.0/me/sendMail"
)


class OutlookMailService:

    def __init__(self):
        if not MICROSOFT_CLIENT_ID:
            raise RuntimeError(
                "MICROSOFT_CLIENT_ID no está "
                "configurado en backend/.env."
            )

        if not MICROSOFT_SENDER_EMAIL:
            raise RuntimeError(
                "MICROSOFT_SENDER_EMAIL no está "
                "configurado en backend/.env."
            )

        self.cache = (
            msal.SerializableTokenCache()
        )

        self._load_cache()

        self.app = (
            msal.PublicClientApplication(
                client_id=(
                    MICROSOFT_CLIENT_ID
                ),
                authority=(
                    MICROSOFT_AUTHORITY
                ),
                token_cache=self.cache
            )
        )

    def _load_cache(self):
        if not TOKEN_CACHE_FILE.exists():
            return

        serialized_cache = (
            TOKEN_CACHE_FILE.read_text(
                encoding="utf-8"
            )
        )

        if serialized_cache.strip():
            self.cache.deserialize(
                serialized_cache
            )

    def _save_cache(self):
        if not self.cache.has_state_changed:
            return

        TOKEN_CACHE_FILE.write_text(
            self.cache.serialize(),
            encoding="utf-8"
        )

    def _get_cached_account(self):
        matching_accounts = (
            self.app.get_accounts(
                username=(
                    MICROSOFT_SENDER_EMAIL
                )
            )
        )

        if matching_accounts:
            return matching_accounts[0]

        all_accounts = (
            self.app.get_accounts()
        )

        if len(all_accounts) == 1:
            return all_accounts[0]

        if len(all_accounts) > 1:
            raise RuntimeError(
                "Hay varias cuentas de Microsoft "
                "en la caché y no se pudo identificar "
                "la cuenta emisora configurada."
            )

        raise RuntimeError(
            "No existe una autorización de Microsoft "
            "en caché. Ejecute primero el script "
            "backend/scripts/authorize_outlook.py."
        )

    def _get_access_token(self) -> str:
        account = self._get_cached_account()

        result = self.app.acquire_token_silent(
            scopes=MAIL_SCOPES,
            account=account
        )

        self._save_cache()

        if not result:
            raise RuntimeError(
                "No se pudo obtener un token de "
                "Microsoft desde la caché. Ejecute "
                "nuevamente authorize_outlook.py."
            )

        access_token = result.get(
            "access_token"
        )

        if not access_token:
            error_description = (
                result.get(
                    "error_description"
                )
                or result.get("error")
                or "Error desconocido de Microsoft."
            )

            raise RuntimeError(
                "No se pudo obtener el token de "
                f"Microsoft: {error_description}"
            )

        return access_token

    @staticmethod
    def _build_reset_url(
        reset_token: str
    ) -> str:
        query = urlencode(
            {
                "token":
                    reset_token
            }
        )

        return (
            f"{FRONTEND_RESET_PASSWORD_URL}"
            f"?{query}"
        )

    def send_password_reset_email(
        self,
        to_email: str,
        username: str,
        reset_token: str,
        expire_minutes: int
    ):
        access_token = (
            self._get_access_token()
        )

        reset_url = self._build_reset_url(
            reset_token
        )

        safe_username = html.escape(
            username
        )

        safe_reset_url = html.escape(
            reset_url,
            quote=True
        )

        subject = (
            "SmileCare - Recuperación "
            "de contraseña"
        )

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #222;">
            <h2>Recuperación de contraseña de SmileCare</h2>

            <p>Hola <strong>{safe_username}</strong>,</p>

            <p>
              Se solicitó restablecer la contraseña de tu cuenta
              de SmileCare.
            </p>

            <p>
              Este enlace estará disponible durante
              <strong>{expire_minutes} minutos</strong> y solamente
              puede utilizarse una vez.
            </p>

            <p style="margin: 28px 0;">
              <a
                href="{safe_reset_url}"
                style="
                  display: inline-block;
                  padding: 12px 18px;
                  background: #1668c7;
                  color: white;
                  text-decoration: none;
                  border-radius: 6px;
                "
              >
                Restablecer contraseña
              </a>
            </p>

            <p>
              Si no solicitaste este cambio, puedes ignorar este
              mensaje. Tu contraseña actual seguirá funcionando.
            </p>

            <p>
              Equipo SmileCare
            </p>
          </body>
        </html>
        """

        payload = {
            "message": {
                "subject":
                    subject,

                "body": {
                    "contentType":
                        "HTML",

                    "content":
                        html_body
                },

                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":
                                to_email
                        }
                    }
                ]
            },

            "saveToSentItems":
                True
        }

        response = requests.post(
            GRAPH_SEND_MAIL_URL,
            headers={
                "Authorization": (
                    f"Bearer {access_token}"
                ),

                "Content-Type": (
                    "application/json"
                )
            },
            json=payload,
            timeout=30
        )

        if response.status_code != 202:
            response_text = (
                response.text[:1000]
            )

            raise RuntimeError(
                "Microsoft Graph no pudo enviar "
                "el correo. "
                f"HTTP {response.status_code}: "
                f"{response_text}"
            )