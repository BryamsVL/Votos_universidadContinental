from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.auth_schema import LoginResponse
from src.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


def _get_db_and_user(
    authorization: str = Header(..., alias="Authorization"),
    db: Session = Depends(get_db),
):
    return auth_service.get_current_user(authorization=authorization, db=db)


# 🔐 LOGIN CON FIREBASE TOKEN
@router.post("/login", response_model=LoginResponse)
def login(
    authorization: str = Header(..., alias="Authorization"),
    db: Session = Depends(get_db),
):
    usuario = auth_service.get_current_user(authorization=authorization, db=db)
    return usuario


# 🧪 ENDPOINT DE PRUEBA SIN AUTENTICACIÓN
@router.get("/test")
def test_endpoint():
    return {
        "status": "ok",
        "message": "Auth router funcionando correctamente"
    }