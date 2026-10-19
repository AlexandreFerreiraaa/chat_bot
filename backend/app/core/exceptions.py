"""Exceções de domínio; main.py as converte em códigos HTTP."""


class CredenciaisInvalidas(Exception):
    pass


class UsuarioJaExiste(Exception):
    pass


class NaoEncontrado(Exception):
    pass


class ModeloIndisponivel(Exception):
    pass
