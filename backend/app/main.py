"""Cria a aplicação FastAPI e registra routers e tratadores de erro."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.database import criar_tabelas
from app.core.exceptions import (CredenciaisInvalidas, ModeloIndisponivel, NaoEncontrado,
                                 UsuarioJaExiste)
from app.routers import auth, conversas, health


@asynccontextmanager
async def lifespan(_: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(
    title="Chat IA — API",
    description="API de chat com múltiplas conversas por usuário, autenticação JWT e persistência em SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(conversas.router)


def _erro(status_code: int, detail: str, headers: dict | None = None) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": detail}, headers=headers)


@app.exception_handler(CredenciaisInvalidas)
async def _h_cred(_: Request, __: CredenciaisInvalidas):
    return _erro(401, "Usuário ou senha incorretos.", {"WWW-Authenticate": "Bearer"})


@app.exception_handler(UsuarioJaExiste)
async def _h_existe(_: Request, __: UsuarioJaExiste):
    return _erro(409, "Este nome de usuário já está em uso.")


@app.exception_handler(NaoEncontrado)
async def _h_nf(_: Request, __: NaoEncontrado):
    return _erro(404, "Conversa não encontrada.")


@app.exception_handler(ModeloIndisponivel)
async def _h_llm(_: Request, exc: ModeloIndisponivel):
    return _erro(503, str(exc) or "O modelo de linguagem está indisponível no momento.")
