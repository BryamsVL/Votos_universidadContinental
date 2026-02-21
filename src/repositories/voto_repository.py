from sqlalchemy.orm import Session
from src.models.voto_model import Voto
from src.schemas.voto_schema import VotoCreate


def get_by_usuario_id(db: Session, usuario_id: int) -> Voto | None:
    return db.query(Voto).filter(Voto.usuario_id == usuario_id).first()


def create(db: Session, data: VotoCreate, usuario_id: int) -> Voto:
    voto = Voto(
        usuario_id=usuario_id,
        candidato_id=data.candidato_id,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    db.add(voto)
    db.commit()
    db.refresh(voto)
    return voto
