"""ÚNICO módulo do front que fala com a API (via requests).

Páginas e componentes chamam as funções daqui e só lidam com `ApiError`,
cuja mensagem já é amigável para exibir ao usuário (sem traceback).
"""
import requests

from config import API_TIMEOUT, API_URL


class ApiError(Exception):
    def __init__(self, mensagem: str, status: int | None = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status


def _detalhe(resp: requests.Response, padrao: str) -> str:
    try:
        detail = resp.json().get("detail", padrao)
    except ValueError:
        return padrao
    if isinstance(detail, list):  # erro 422 do Pydantic
        return "Dados inválidos. Confira o que foi digitado."
    return str(detail)


def _request(metodo: str, caminho: str, token: str | None = None, json: dict | None = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        resp = requests.request(metodo, f"{API_URL}{caminho}", headers=headers, json=json,
                                timeout=API_TIMEOUT)
    except requests.ConnectionError:
        raise ApiError("Não foi possível conectar à API. Verifique se o back-end está rodando.")
    except requests.Timeout:
        raise ApiError("A API demorou demais para responder. Tente novamente.")
    except requests.RequestException:
        raise ApiError("Erro inesperado ao se comunicar com a API.")

    if resp.ok:
        return resp.json()

    mensagens = {
        401: _detalhe(resp, "Sessão expirada. Faça login novamente."),
        404: _detalhe(resp, "Item não encontrado."),
        409: _detalhe(resp, "Conflito: este registro já existe."),
        422: _detalhe(resp, "Dados inválidos."),
        503: _detalhe(resp, "O modelo de linguagem está indisponível no momento."),
    }
    raise ApiError(mensagens.get(resp.status_code, "Erro no servidor. Tente novamente mais tarde."),
                   status=resp.status_code)


# ---- Endpoints ----
def health() -> dict:
    return _request("GET", "/health")


def login(username: str, senha: str) -> dict:
    return _request("POST", "/auth/login", json={"username": username, "senha": senha})


def registrar(username: str, senha: str) -> dict:
    return _request("POST", "/auth/registro", json={"username": username, "senha": senha})


def listar_conversas(token: str) -> list[dict]:
    return _request("GET", "/conversas", token)


def criar_conversa(token: str) -> dict:
    return _request("POST", "/conversas", token)


def abrir_conversa(token: str, conversa_id: int) -> dict:
    return _request("GET", f"/conversas/{conversa_id}", token)


def enviar_mensagem(token: str, conversa_id: int, conteudo: str) -> dict:
    return _request("POST", f"/conversas/{conversa_id}/mensagens", token, {"conteudo": conteudo})
