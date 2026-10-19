from pydantic import BaseModel, Field


class CredenciaisIn(BaseModel):
    username: str = Field(min_length=3, max_length=30, examples=["maria"])
    senha: str = Field(min_length=6, max_length=100, examples=["segredo123"])


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


class UsuarioOut(BaseModel):
    id: int
    username: str
