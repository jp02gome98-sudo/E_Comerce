
import os
from pathlib import Path
from dotenv import load_dotenv

# Buscar el archivo .env en la carpeta principal
BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "clave-temporal-de-desarrollo"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///ecommerce.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
