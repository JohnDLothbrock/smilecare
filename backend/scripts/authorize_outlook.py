import os
import sys
from pathlib import Path

import msal
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


CLIENT_ID = os.getenv(
    "MICROSOFT_CLIENT_ID"
)

AUTHORITY = os.getenv(
    "MICROSOFT_AUTHORITY",
    "https://login.microsoftonline.com/consumers"
)

SENDER_EMAIL = os.getenv(
    "MICROSOFT_SENDER_EMAIL"
)

SCOPES = [
    "https://graph.microsoft.com/Mail.Send"
]


if not CLIENT_ID:
    raise RuntimeError(
        "MICROSOFT_CLIENT_ID no está configurado "
        "en backend/.env."
    )


if not SENDER_EMAIL:
    raise RuntimeError(
        "MICROSOFT_SENDER_EMAIL no está configurado "
        "en backend/.env."
    )


cache = (
    msal.SerializableTokenCache()
)


if TOKEN_CACHE_FILE.exists():
    serialized_cache = (
        TOKEN_CACHE_FILE.read_text(
            encoding="utf-8"
        )
    )

    if serialized_cache.strip():
        cache.deserialize(
            serialized_cache
        )


app = (
    msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache
    )
)


accounts = app.get_accounts(
    username=SENDER_EMAIL
)


if not accounts:
    accounts = app.get_accounts()


result = None


if accounts:
    result = app.acquire_token_silent(
        scopes=SCOPES,
        account=accounts[0]
    )


if not result:
    print(
        "Se abrirá el navegador para autorizar "
        "la cuenta de Outlook."
    )

    result = app.acquire_token_interactive(
        scopes=SCOPES,
        login_hint=SENDER_EMAIL,
        prompt="select_account"
    )


if cache.has_state_changed:
    TOKEN_CACHE_FILE.write_text(
        cache.serialize(),
        encoding="utf-8"
    )


if "access_token" not in result:
    print(
        "\nNo se pudo completar la autorización "
        "de Microsoft."
    )

    print(
        result.get(
            "error_description"
        )
        or result.get("error")
        or result
    )

    sys.exit(1)


authorized_account = (
    result.get(
        "id_token_claims",
        {}
    ).get(
        "preferred_username"
    )
)


print(
    "\nAutorización de Outlook "
    "completada correctamente."
)


if authorized_account:
    print(
        f"Cuenta autorizada: "
        f"{authorized_account}"
    )


print(
    "\nLa caché de Microsoft fue guardada en:"
)

print(
    TOKEN_CACHE_FILE
)

print(
    "\nNo agregue ese archivo a GitHub."
)