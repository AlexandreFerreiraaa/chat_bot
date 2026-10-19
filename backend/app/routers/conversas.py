import sqlite3

from fastapi import APIRouter, Depends, status

from app.core.database import get_db
from app.core.deps import usuario_logado
from app.schemas.conversas import ConversaDetalheOut, ConversaOut, EnvioOut, MensagemIn
from app.services import conversas_service as svc

router = APIRouter(prefix="/conversas", tags=["Conversas"])


@router.get("", response_model=list[ConversaOut], summary="Lista as conversas do usuário logado")
def listar(usuario: dict = Depends(usuario_logado), db: sqlite3.Connection = Depends(get_db)):
    """Conversas da mais recente para a mais antiga. Nunca retorna conversas de outros usuários."""
    return svc.listar_conversas(db, usuario["id"])


@router.post("", response_model=ConversaOut, status_code=status.HTTP_201_CREATED,
             summary="Cria uma nova conversa")
def criar(usuario: dict = Depends(usuario_logado), db: sqlite3.Connection = Depends(get_db)):
    """Cria uma conversa vazia. O título é definido a partir da primeira mensagem."""
    return svc.criar_conversa(db, usuario["id"])


@router.get("/{conversa_id}", response_model=ConversaDetalheOut,
            summary="Abre uma conversa e seu histórico")
def abrir(conversa_id: int, usuario: dict = Depends(usuario_logado),
          db: sqlite3.Connection = Depends(get_db)):
    """Retorna a conversa com todas as mensagens. 404 se não existir ou pertencer a outro usuário."""
    return svc.abrir_conversa(db, usuario["id"], conversa_id)


@router.post("/{conversa_id}/mensagens", response_model=EnvioOut, status_code=status.HTTP_201_CREATED,
             summary="Envia uma mensagem e recebe a resposta do bot")
def enviar(conversa_id: int, dados: MensagemIn, usuario: dict = Depends(usuario_logado),
           db: sqlite3.Connection = Depends(get_db)):
    """Grava a mensagem do usuário, chama o modelo e grava a resposta. 503 se o modelo estiver indisponível."""
    return svc.enviar_mensagem(db, usuario["id"], conversa_id, dados.conteudo)
