"""Barra lateral: usuário, botão Nova conversa e lista de conversas."""
import streamlit as st

import state
from services import api_client
from services.api_client import ApiError


def renderizar_sidebar() -> None:
    token = st.session_state.token
    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.username}**")
        if st.button("➕ Nova conversa", use_container_width=True, type="primary"):
            try:
                nova = api_client.criar_conversa(token)
                st.session_state.conversa_id = nova["id"]
                st.rerun()
            except ApiError as e:
                state.tratar_erro(e)

        st.divider()
        st.caption("Suas conversas")
        try:
            conversas = api_client.listar_conversas(token)
        except ApiError as e:
            state.tratar_erro(e)
            conversas = []

        if not conversas:
            st.caption("Nenhuma conversa ainda.")
        for c in conversas:
            ativa = c["id"] == st.session_state.conversa_id
            if st.button(c["titulo"], key=f"conv_{c['id']}", use_container_width=True,
                         type="secondary", icon="💬" if not ativa else "▶️", disabled=ativa):
                st.session_state.conversa_id = c["id"]
                st.rerun()

        st.divider()
        if st.button("Sair", use_container_width=True):
            state.sair()
            st.rerun()
