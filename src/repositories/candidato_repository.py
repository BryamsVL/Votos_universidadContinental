from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.candidato_model import Candidato
from src.models.voto_model import Voto
from src.schemas.candidato_schema import CandidatoCreate


def get_all(db: Session) -> list[Candidato]:
    return db.query(Candidato).all()


def get_by_id(db: Session, candidato_id: int) -> Candidato | None:
    return db.query(Candidato).filter(Candidato.id == candidato_id).first()


def create(db: Session, data: CandidatoCreate) -> Candidato:
    candidato = Candidato(
        nombre=data.nombre,
        propuesta=data.propuesta,
        foto_url=data.foto_url,
        role=data.role,
    )
    db.add(candidato)
    db.commit()
    db.refresh(candidato)
    return candidato


def get_results(db: Session) -> list[dict]:
    """
    Devuelve la cantidad de votos por candidato usando agregación SQL.
    Hace LEFT JOIN para incluir candidatos con 0 votos.
    """
    rows = (
        db.query(
            Candidato.id,
            Candidato.nombre,
            Candidato.role,
            func.count(Voto.id).label("votes"),
        )
        .outerjoin(Voto, Voto.candidato_id == Candidato.id)
        .group_by(Candidato.id, Candidato.nombre, Candidato.role)
        .order_by(Candidato.id)
        .all()
    )
    return [
        {"candidate_id": r.id, "nombre": r.nombre, "role": r.role, "votes": r.votes}
        for r in rows
    ]
