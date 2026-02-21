from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from src.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.get_all(db)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return usuario_service.get_by_id(db, usuario_id)


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.create(db, data)
