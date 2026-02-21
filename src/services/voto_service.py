from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.schemas.voto_schema import VotoCreate, VotoResponse
from src.repositories import usuario_repository, candidato_repository, voto_repository
from src.services import geo_service
from src.models.usuario_model import Usuario


def registrar_voto(db: Session, data: VotoCreate, usuario: Usuario) -> VotoResponse:
    """
    Lógica de negocio para registrar un voto:
    1. Verificar que el usuario no haya votado.
    2. Verificar geolocalización con fórmula Haversine.
    3. Verificar que el candidato exista.
    4. Registrar el voto y marcar al usuario.
    """
    # 1. Verificar que no haya votado antes
    if usuario.ya_voto:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya emitió su voto. No se permite votar dos veces.",
        )

    # 2. Validar geolocalización (lanza HTTP 403 si está fuera del área)
    geo_service.validar_ubicacion(data.latitude, data.longitude)

    # 3. Verificar que el candidato exista
    candidato = candidato_repository.get_by_id(db, data.candidato_id)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado.")

    # 4. Registrar el voto
    voto = voto_repository.create(db, data, usuario_id=usuario.id)

    # 5. Marcar al usuario como ya votó
    usuario_repository.mark_voted(db, usuario)

    return voto
