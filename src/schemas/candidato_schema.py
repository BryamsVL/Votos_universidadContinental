from pydantic import BaseModel
from typing import Optional


class CandidatoCreate(BaseModel):
    nombre: str
    propuesta: Optional[str] = None
    foto_url: Optional[str] = None
    role: Optional[str] = None  # 'delegado' o 'subdelegado'


class CandidatoResponse(BaseModel):
    id: int
    nombre: str
    propuesta: Optional[str] = None
    foto_url: Optional[str] = None
    role: Optional[str] = None

    model_config = {"from_attributes": True}
