from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoginResponse(BaseModel):
    id: int
    firebase_uid: str
    email: str
    nombre: Optional[str] = None
    ya_voto: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
