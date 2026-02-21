from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VotoCreate(BaseModel):
    candidato_id: int
    latitude: float
    longitude: float


class VotoResponse(BaseModel):
    id: int
    usuario_id: int
    candidato_id: int
    fecha: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = {"from_attributes": True}
