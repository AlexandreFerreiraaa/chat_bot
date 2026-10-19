"""ÚNICO ponto de acesso ao modelo de linguagem.

Trocar de provedor = mudar LLM_PROVIDER no .env. Rotas e front não mudam.
"""
import random

import requests

from app.core.config import settings
from app.core.exceptions import ModeloIndisponivel

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"


def nome_modelo() -> str:
    if settings.LLM_PROVIDER == "gemini":
        return settings.GEMINI_MODEL
    return "simulado"


def gerar_resposta(historico: list[dict]) -> str:
    """Recebe o histórico [{papel, conteudo}, ...] já com a nova pergunta no fim."""
    if settings.LLM_PROVIDER == "gemini":
        return _gemini(historico)
    return _simulado(historico)


def _simulado(historico: list[dict]) -> str:
    ultima = historico[-1]["conteudo"]
    n_perguntas = sum(1 for m in historico if m["papel"] == "user")
    opcoes = [
        f"Você disse: “{ultima}”. Esta é uma resposta simulada.",
        f"Sobre “{ultima[:60]}”: sou apenas um bot de teste, mas a API está funcionando!",
        f"Recebi sua mensagem de número {n_perguntas} nesta conversa. Como posso ajudar mais?",
    ]
    return random.choice(opcoes)


def _gemini(historico: list[dict]) -> str:
    if not settings.GEMINI_API_KEY:
        raise ModeloIndisponivel("Modelo não configurado: defina GEMINI_API_KEY no .env do back-end.")
    corpo = {
        "contents": [
            {"role": "user" if m["papel"] == "user" else "model", "parts": [{"text": m["conteudo"]}]}
            for m in historico
        ]
    }
    try:
        r = requests.post(
            GEMINI_URL.format(modelo=settings.GEMINI_MODEL),
            headers={"x-goog-api-key": settings.GEMINI_API_KEY},
            json=corpo,
            timeout=settings.LLM_TIMEOUT_SEGUNDOS,
        )
    except requests.RequestException:
        raise ModeloIndisponivel("Não foi possível contatar o modelo de linguagem. Tente novamente.")
    if r.status_code == 429:
        raise ModeloIndisponivel("Limite de uso do modelo atingido. Aguarde um pouco e tente de novo.")
    if r.status_code != 200:
        raise ModeloIndisponivel("O modelo de linguagem está indisponível no momento.")
    try:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, ValueError):
        raise ModeloIndisponivel("O modelo retornou uma resposta vazia ou inesperada.")
