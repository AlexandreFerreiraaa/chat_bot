"""Acesso ao banco: conversas e mensagens. Consultas de conversa sempre filtram por usuario_id."""
import sqlite3

from app.repositories.usuarios_repo import agora


def criar(db: sqlite3.Connection, usuario_id: int, titulo: str) -> dict:
    t = agora()
    cur = db.execute(
        "INSERT INTO conversas (usuario_id, titulo, criada_em, atualizada_em) VALUES (?, ?, ?, ?)",
        (usuario_id, titulo, t, t),
    )
    db.commit()
    return buscar(db, usuario_id, cur.lastrowid)


def listar(db: sqlite3.Connection, usuario_id: int) -> list[dict]:
    rows = db.execute(
        "SELECT id, titulo, criada_em, atualizada_em FROM conversas "
        "WHERE usuario_id = ? ORDER BY atualizada_em DESC, id DESC",
        (usuario_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def buscar(db: sqlite3.Connection, usuario_id: int, conversa_id: int) -> dict | None:
    row = db.execute(
        "SELECT id, titulo, criada_em, atualizada_em FROM conversas WHERE id = ? AND usuario_id = ?",
        (conversa_id, usuario_id),
    ).fetchone()
    return dict(row) if row else None


def mensagens(db: sqlite3.Connection, conversa_id: int) -> list[dict]:
    rows = db.execute(
        "SELECT id, papel, conteudo, criado_em FROM mensagens WHERE conversa_id = ? ORDER BY id",
        (conversa_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def adicionar_mensagem(db: sqlite3.Connection, conversa_id: int, papel: str, conteudo: str) -> dict:
    t = agora()
    cur = db.execute(
        "INSERT INTO mensagens (conversa_id, papel, conteudo, criado_em) VALUES (?, ?, ?, ?)",
        (conversa_id, papel, conteudo, t),
    )
    db.execute("UPDATE conversas SET atualizada_em = ? WHERE id = ?", (t, conversa_id))
    db.commit()
    return {"id": cur.lastrowid, "papel": papel, "conteudo": conteudo, "criado_em": t}


def renomear(db: sqlite3.Connection, conversa_id: int, titulo: str) -> None:
    db.execute("UPDATE conversas SET titulo = ? WHERE id = ?", (titulo, conversa_id))
    db.commit()
