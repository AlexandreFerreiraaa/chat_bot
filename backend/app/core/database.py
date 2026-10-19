"""Conexão SQLite e criação das tabelas."""
import sqlite3
from app.core.config import settings


def conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas() -> None:
    conn = conectar()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            criado_em TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS conversas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            titulo TEXT NOT NULL,
            criada_em TEXT NOT NULL,
            atualizada_em TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversa_id INTEGER NOT NULL REFERENCES conversas(id) ON DELETE CASCADE,
            papel TEXT NOT NULL CHECK (papel IN ('user', 'assistant')),
            conteudo TEXT NOT NULL,
            criado_em TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def get_db():
    """Dependência FastAPI: uma conexão por requisição."""
    conn = conectar()
    try:
        yield conn
    finally:
        conn.close()
