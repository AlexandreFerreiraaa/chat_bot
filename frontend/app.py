"""Entrada do front: configura a página e faz o roteamento (st.navigation)."""
import streamlit as st

import state
from pages import chat, login

st.set_page_config(page_title="Chat IA", page_icon="💬", layout="wide")
state.init_state()

if state.esta_logado():
    pagina = st.navigation([st.Page(chat.render, title="Chat", icon="💬", url_path="chat")],
                           position="hidden")
else:
    pagina = st.navigation([st.Page(login.render, title="Login", icon="🔐", url_path="login")],
                           position="hidden")
pagina.run()
