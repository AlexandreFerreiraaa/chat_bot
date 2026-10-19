from fastapi import APIRouter

from app.core.config import settings
from app.llm import provider
from app.schemas.conversas import HealthOut

router = APIRouter(tags=["Saúde"])


@router.get("/health", response_model=HealthOut, summary="Verifica se a API está no ar")
def health():
    """Retorna o status da API e qual provedor/modelo de linguagem está em uso."""
    return {"status": "ok", "provedor": settings.LLM_PROVIDER, "modelo": provider.nome_modelo()}
