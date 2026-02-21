from sqlalchemy.orm import Session
from src.schemas.candidato_schema import CandidatoCreate, CandidatoResponse
from src.repositories import candidato_repository


def get_all(db: Session) -> list[CandidatoResponse]:
    return candidato_repository.get_all(db)


def create(db: Session, data: CandidatoCreate) -> CandidatoResponse:
    return candidato_repository.create(db, data)
