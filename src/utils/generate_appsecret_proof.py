import os
import hmac
import hashlib
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

def generate_appsecret_proof(token: str) -> str:
    """
    Genera el appsecret_proof requerido por la API de WhatsApp.

    Args:
        token (str): Access token de usuario o página.

    Returns:
        str: Cadena HMAC-SHA256 en formato hexadecimal.
    """
    app_secret = os.getenv("FACEBOOK_APP_SECRET")
    if not app_secret:
        raise ValueError("FACEBOOK_APP_SECRET no está definido en el entorno (.env)")

    proof = hmac.new(
        key=app_secret.encode('utf-8'),
        msg=token.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    return proof
