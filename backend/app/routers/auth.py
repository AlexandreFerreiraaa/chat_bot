import sqlite3

from fastapi import APIRouter, Depends, status

from app.core.database import get_db
from app.core.deps import usuario_logado
from app.schemas.auth import CredenciaisIn, TokenOut, UsuarioOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registro", response_model=TokenOut, status_code=status.HTTP_201_CREATED,
             summary="Cria uma conta e já retorna um token")
def registro(dados: CredenciaisIn, db: sqlite3.Connection = Depends(get_db)):
    """Cadastra um usuário. A senha é armazenada com hash PBKDF2 (nunca em texto puro). 409 se o usuário já existir."""
    return auth_service.registrar(db, dados.username, dados.senha)


@router.post("/login", response_model=TokenOut, summary="Autentica e retorna um token JWT")
def login(dados: CredenciaisIn, db: sqlite3.Connection = Depends(get_db)):
    """Valida usuário e senha. Use o token no header `Authorization: Bearer <token>`. 401 se inválido."""
    return auth_service.autenticar(db, dados.username, dados.senha)


@router.get("/me", response_model=UsuarioOut, summary="Dados do usuário logado")
def me(usuario: dict = Depends(usuario_logado)):
    """Rota protegida; permite ao front validar se o token ainda é válido."""
    return {"id": usuario["id"], "username": usuario["username"]}
