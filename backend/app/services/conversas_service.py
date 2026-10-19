"""Regras de negócio: conversas e mensagens."""
import sqlite3

from app.core.exceptions import NaoEncontrado
from app.llm import provider
from app.repositories import conversas_repo

TITULO_PADRAO = "Nova conversa"


def criar_conversa(db: sqlite3.Connection, usuario_id: int) -> dict:
    return conversas_repo.criar(db, usuario_id, TITULO_PADRAO)


def listar_conversas(db: sqlite3.Connection, usuario_id: int) -> list[dict]:
    return conversas_repo.listar(db, usuario_id)


def abrir_conversa(db: sqlite3.Connection, usuario_id: int, conversa_id: int) -> dict:
    conversa = conversas_repo.buscar(db, usuario_id, conversa_id)
    if conversa is None:  # inexistente OU de outro usuário: mesma resposta (404)
        raise NaoEncontrado()
    conversa["mensagens"] = conversas_repo.mensagens(db, conversa_id)
    return conversa


def enviar_mensagem(db: sqlite3.Connection, usuario_id: int, conversa_id: int, texto: str) -> dict:
    conversa = abrir_conversa(db, usuario_id, conversa_id)
    historico = conversa["mensagens"] + [{"papel": "user", "conteudo": texto}]

    # Chama o modelo ANTES de gravar: se falhar (503), nada fica pela metade.
    resposta_texto = provider.gerar_resposta(historico)

    msg_user = conversas_repo.adicionar_mensagem(db, conversa_id, "user", texto)
    msg_bot = conversas_repo.adicionar_mensagem(db, conversa_id, "assistant", resposta_texto)

    if conversa["titulo"] == TITULO_PADRAO:
        titulo = texto.strip().replace("\n", " ")
        conversas_repo.renomear(db, conversa_id, titulo[:40] + ("…" if len(titulo) > 40 else ""))

    return {
        "conversa_id": conversa_id,
        "mensagem_usuario": msg_user,
        "resposta": msg_bot,
        "modelo": provider.nome_modelo(),
        "criado_em": msg_bot["criado_em"],
    }
