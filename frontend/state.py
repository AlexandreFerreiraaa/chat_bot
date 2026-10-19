"""Estado mínimo na sessão: token, usuário e id da conversa ativa.
O histórico NUNCA fica aqui: é sempre lido da API."""
import streamlit as st


def init_state() -> None:
    st.session_state.setdefault("token", None)
    st.session_state.setdefault("username", None)
    st.session_state.setdefault("conversa_id", None)


def esta_logado() -> bool:
    return bool(st.session_state.get("token"))


def entrar(token: str, username: str) -> None:
    st.session_state.token = token
    st.session_state.username = username
    st.session_state.conversa_id = None


def sair() -> None:
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.conversa_id = None


def tratar_erro(erro) -> None:
    """Mostra o erro amigável; em caso de 401, derruba a sessão e volta ao login."""
    if erro.status == 401 and esta_logado():
        sair()
        st.session_state["aviso_login"] = "Sua sessão expirou. Faça login novamente."
        st.rerun()
    st.error(erro.mensagem)
