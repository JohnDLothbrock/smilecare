import os
from pathlib import Path
from typing import Generator

import oracledb
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


def get_required_env_value(name: str) -> str:
    value = os.getenv(name)

    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


ORACLE_USER = get_required_env_value("ORACLE_USER")
ORACLE_PASSWORD = get_required_env_value("ORACLE_PASSWORD")
ORACLE_DSN = get_required_env_value("ORACLE_DSN")
ORACLE_WALLET_DIR = get_required_env_value("ORACLE_WALLET_DIR")
ORACLE_WALLET_PASSWORD = get_required_env_value("ORACLE_WALLET_PASSWORD")


def get_connection():
    connection = oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN,
        config_dir=ORACLE_WALLET_DIR,
        wallet_location=ORACLE_WALLET_DIR,
        wallet_password=ORACLE_WALLET_PASSWORD
    )

    return connection


def get_db() -> Generator:
    connection = get_connection()

    try:
        yield connection
    finally:
        connection.close()