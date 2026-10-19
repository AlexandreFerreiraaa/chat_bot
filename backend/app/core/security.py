"""Hash de senha (PBKDF2) e tokens JWT."""
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings

ALGORITMO = "HS256"
ITERACOES = 200_000


def hash_senha(senha: str) -> str:
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, ITERACOES)
    return f"{salt.hex()}${h.hex()}"


def verificar_senha(senha: str, armazenado: str) -> bool:
    try:
        salt_hex, hash_hex = armazenado.split("$")
        h = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(salt_hex), ITERACOES)
    except ValueError:
        return False
    return hmac.compare_digest(h.hex(), hash_hex)


def criar_token(usuario_id: int) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRA_MINUTOS)
    return jwt.encode({"sub": str(usuario_id), "exp": exp}, settings.SECRET_KEY, algorithm=ALGORITMO)


def decodificar_token(token: str) -> int | None:
    """Retorna o id do usuário ou None se o token for inválido/expirado."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITMO])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None
