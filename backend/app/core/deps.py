"""Dependências de autenticação: extrai o usuário logado do header Authorization."""
import sqlite3

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import get_db
from app.core.security import decodificar_token
from app.repositories import usuarios_repo

bearer = HTTPBearer(auto_error=False, description="Token JWT obtido em /auth/login")


def usuario_logado(
    cred: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: sqlite3.Connection = Depends(get_db),
) -> dict:
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token ausente ou inválido. Faça login novamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if cred is None:
        raise erro
    usuario_id = decodificar_token(cred.credentials)
    if usuario_id is None:
        raise erro
    usuario = usuarios_repo.buscar_por_id(db, usuario_id)
    if usuario is None:
        raise erro
    return usuario
