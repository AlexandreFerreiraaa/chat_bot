"""Página de chat: sidebar com conversas + área de mensagens."""
import streamlit as st

import state
from components.caixa_envio import caixa_envio
from components.mensagens import renderizar_mensagens
from components.sidebar import renderizar_sidebar
from services import api_client
from services.api_client import ApiError


def render() -> None:
    renderizar_sidebar()
    token = st.session_state.token
    conversa_id = st.session_state.conversa_id

    st.title("💬 Chat IA")

    # O histórico vem sempre da API.
    if conversa_id is not None:
        try:
            conversa = api_client.abrir_conversa(token, conversa_id)
            st.caption(f"Conversa: {conversa['titulo']}")
            renderizar_mensagens(conversa["mensagens"])
            if not conversa["mensagens"]:
                st.info("Conversa vazia. Envie a primeira mensagem!")
        except ApiError as e:
            if e.status == 404:
                st.session_state.conversa_id = None
                conversa_id = None
                st.warning("Essa conversa não existe mais. Escolha outra ou crie uma nova.")
            else:
                state.tratar_erro(e)
    else:
        st.info("Selecione uma conversa na barra lateral, crie uma nova ou apenas escreva abaixo.")

    prompt = caixa_envio()
    if not prompt:
        return

    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                if conversa_id is None:  # nenhuma conversa ativa: cria uma automaticamente
                    conversa_id = api_client.criar_conversa(token)["id"]
                    st.session_state.conversa_id = conversa_id
                api_client.enviar_mensagem(token, conversa_id, prompt)
            except ApiError as e:
                state.tratar_erro(e)
                return
    st.rerun()  # recarrega histórico da API e atualiza títulos na sidebar
