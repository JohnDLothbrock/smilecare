import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash


ENV_FILE = (
    Path(__file__).resolve().parents[1]
    / ".env"
)

load_dotenv(ENV_FILE)


JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY"
)

JWT_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        "480"
    )
)


if not JWT_SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY no está configurada "
        "en backend/.env."
    )


password_hash = PasswordHash.recommended()


def hash_password(
    plain_password: str
) -> str:
    return password_hash.hash(
        plain_password
    )


def is_modern_password_hash(
    stored_password: str
) -> bool:
    return str(
        stored_password or ""
    ).startswith("$argon2")


def verify_hashed_password(
    plain_password: str,
    stored_hash: str
) -> bool:
    try:
        return password_hash.verify(
            plain_password,
            stored_hash
        )

    except Exception:
        return False


def verify_legacy_password(
    plain_password: str,
    stored_password: str
) -> bool:
    return secrets.compare_digest(
        str(plain_password),
        str(stored_password)
    )


def generate_password_reset_token() -> str:
    return secrets.token_urlsafe(
        48
    )


def hash_password_reset_token(
    token: str
) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def create_access_token(
    subject: str,
    additional_claims: dict[str, Any]
    | None = None
) -> str:
    now = datetime.now(
        timezone.utc
    )

    expiration = now + timedelta(
        minutes=(
            JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": expiration
    }

    if additional_claims:
        payload.update(
            additional_claims
        )

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


def decode_access_token(
    token: str
) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[
            JWT_ALGORITHM
        ]
    )