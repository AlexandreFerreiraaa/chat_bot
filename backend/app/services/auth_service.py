"""Regras de negócio: cadastro e login."""
import sqlite3

from app.core import security
from app.core.exceptions import CredenciaisInvalidas, UsuarioJaExiste
from app.repositories import usuarios_repo


def registrar(db: sqlite3.Connection, username: str, senha: str) -> dict:
    username = username.strip().lower()
    if usuarios_repo.buscar_por_username(db, username):
        raise UsuarioJaExiste()
    uid = usuarios_repo.criar(db, username, security.hash_senha(senha))
    return {"access_token": security.criar_token(uid), "token_type": "bearer", "username": username}


def autenticar(db: sqlite3.Connection, username: str, senha: str) -> dict:
    username = username.strip().lower()
    usuario = usuarios_repo.buscar_por_username(db, username)
    if not usuario or not security.verificar_senha(senha, usuario["senha_hash"]):
        raise CredenciaisInvalidas()
    return {"access_token": security.criar_token(usuario["id"]), "token_type": "bearer", "username": username}
