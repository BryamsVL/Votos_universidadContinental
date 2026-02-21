from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class UsuarioCreate(BaseModel):
    firebase_uid: str
    email: EmailStr
    nombre: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validar_email_institucional(cls, v: str) -> str:
        if not v.endswith("@continental.edu.pe"):
            raise ValueError("El email debe terminar en @continental.edu.pe")
        return v


class UsuarioResponse(BaseModel):
    id: int
    firebase_uid: str
    email: str
    nombre: Optional[str] = None
    ya_voto: bool

    model_config = {"from_attributes": True}
