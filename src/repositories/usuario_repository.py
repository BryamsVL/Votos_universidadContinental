from sqlalchemy.orm import Session
from src.models.usuario_model import Usuario
from src.schemas.usuario_schema import UsuarioCreate


def get_all(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()


def get_by_id(db: Session, usuario_id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def get_by_firebase_uid(db: Session, firebase_uid: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.firebase_uid == firebase_uid).first()


def get_by_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def create(db: Session, data: UsuarioCreate) -> Usuario:
    usuario = Usuario(
        firebase_uid=data.firebase_uid,
        email=data.email,
        nombre=data.nombre,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def mark_voted(db: Session, usuario: Usuario) -> Usuario:
    usuario.ya_voto = True
    db.commit()
    db.refresh(usuario)
    return usuario
