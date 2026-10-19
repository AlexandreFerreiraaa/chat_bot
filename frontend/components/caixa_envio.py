"""Caixa de envio de mensagem."""
import streamlit as st


def caixa_envio() -> str | None:
    return st.chat_input("Digite sua mensagem...")
