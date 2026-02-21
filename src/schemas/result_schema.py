from pydantic import BaseModel
from typing import Optional


class ResultResponse(BaseModel):
    candidate_id: int
    nombre: str
    role: Optional[str] = None
    votes: int
