"""Página de login / cadastro."""
import streamlit as st

import state
from services import api_client
from services.api_client import ApiError


def render() -> None:
    st.title("💬 Chat IA")
    if aviso := st.session_state.pop("aviso_login", None):
        st.warning(aviso)

    aba_entrar, aba_criar = st.tabs(["Entrar", "Criar conta"])

    with aba_entrar:
        with st.form("form_login"):
            username = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            enviado = st.form_submit_button("Entrar", type="primary")
        if enviado:
            try:
                r = api_client.login(username, senha)
                state.entrar(r["access_token"], r["username"])
                st.rerun()
            except ApiError as e:
                st.error(e.mensagem)

    with aba_criar:
        with st.form("form_registro"):
            username = st.text_input("Novo usuário (mín. 3 caracteres)")
            senha = st.text_input("Senha (mín. 6 caracteres)", type="password")
            enviado = st.form_submit_button("Criar conta", type="primary")
        if enviado:
            try:
                r = api_client.registrar(username, senha)
                state.entrar(r["access_token"], r["username"])
                st.rerun()
            except ApiError as e:
                st.error(e.mensagem)
