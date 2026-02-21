from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.usuario_model import Usuario
from src.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from src.repositories import usuario_repository


def get_all(db: Session) -> list[UsuarioResponse]:
    return usuario_repository.get_all(db)


def get_by_id(db: Session, usuario_id: int) -> UsuarioResponse:
    usuario = usuario_repository.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


def create(db: Session, data: UsuarioCreate) -> UsuarioResponse:
    if usuario_repository.get_by_firebase_uid(db, data.firebase_uid):
        raise HTTPException(status_code=400, detail="El firebase_uid ya está registrado")
    if usuario_repository.get_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return usuario_repository.create(db, data)
