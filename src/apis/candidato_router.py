from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.candidato_schema import CandidatoCreate, CandidatoResponse
from src.services import candidato_service

router = APIRouter(tags=["Candidatos"])


@router.get("/candidatos", response_model=list[CandidatoResponse])
@router.get("/candidates", response_model=list[CandidatoResponse])
def listar_candidatos(db: Session = Depends(get_db)):
    """
    Devuelve la lista completa de candidatos (delegados y subdelegados).
    Disponible en /candidatos y /candidates.
    """
    return candidato_service.get_all(db)


@router.post("/candidatos", response_model=CandidatoResponse, status_code=201)
def crear_candidato(data: CandidatoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo candidato."""
    return candidato_service.create(db, data)
