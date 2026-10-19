from typing import Literal

from pydantic import BaseModel, Field


class MensagemIn(BaseModel):
    conteudo: str = Field(min_length=1, max_length=4000, examples=["Me explique o que é uma API REST"])


class MensagemOut(BaseModel):
    id: int
    papel: Literal["user", "assistant"]
    conteudo: str
    criado_em: str


class ConversaOut(BaseModel):
    id: int
    titulo: str
    criada_em: str
    atualizada_em: str


class ConversaDetalheOut(ConversaOut):
    mensagens: list[MensagemOut]


class EnvioOut(BaseModel):
    conversa_id: int
    mensagem_usuario: MensagemOut
    resposta: MensagemOut
    modelo: str
    criado_em: str


class HealthOut(BaseModel):
    status: str
    provedor: str
    modelo: str
