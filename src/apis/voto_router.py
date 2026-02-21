from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.voto_schema import VotoCreate, VotoResponse
from src.schemas.result_schema import ResultResponse
from src.services import voto_service, auth_service
from src.repositories import candidato_repository

router = APIRouter(tags=["Votación"])


def _get_current_user(
    authorization: str = Header(..., alias="Authorization"),
    db: Session = Depends(get_db),
):
    """Dependencia reutilizable: valida token y retorna usuario autenticado."""
    return auth_service.get_current_user(authorization=authorization, db=db)


@router.post("/vote", response_model=VotoResponse, status_code=201)
def votar(
    data: VotoCreate,
    db: Session = Depends(get_db),
    authorization: str = Header(..., alias="Authorization"),
):
    """
    Registra el voto del usuario autenticado.

    **Header requerido:** `Authorization: Bearer <firebase_token>`

    **Body:**
    ```json
    {
      "candidate_id": 1,
      "latitude": -12.047280,
      "longitude": -75.199052
    }
    ```

    **Errores:**
    - 401: Token inválido o ausente.
    - 403: Email no es @continental.edu.pe o fuera del área de votación.
    - 400: Usuario ya votó.
    - 404: Candidato no encontrado.
    """
    usuario = auth_service.get_current_user(authorization=authorization, db=db)
    return voto_service.registrar_voto(db=db, data=data, usuario=usuario)


@router.get("/results", response_model=list[ResultResponse])
def resultados(db: Session = Depends(get_db)):
    """
    Devuelve los resultados en tiempo real con el conteo de votos por candidato.
    Incluye candidatos con 0 votos. No requiere autenticación.
    """
    return candidato_repository.get_results(db)
