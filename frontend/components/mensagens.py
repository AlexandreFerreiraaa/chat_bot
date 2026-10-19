"""Renderização do histórico de mensagens."""
import streamlit as st


def renderizar_mensagens(mensagens: list[dict]) -> None:
    for m in mensagens:
        with st.chat_message("user" if m["papel"] == "user" else "assistant"):
            st.markdown(m["conteudo"])
