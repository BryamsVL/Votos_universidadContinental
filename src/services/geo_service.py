import math
from fastapi import HTTPException


# ── Coordenadas oficiales del campus ─────────────────────────────────────────
CAMPUS_LATITUDE = -12.047280252392124
CAMPUS_LONGITUDE = -75.19905277573551
CAMPUS_RADIUS_METERS = 100.0
# ─────────────────────────────────────────────────────────────────────────────


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia en metros entre dos puntos geográficos
    usando la fórmula de Haversine.
    """
    R = 6_371_000  # Radio de la Tierra en metros

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # distancia en metros


def validar_ubicacion(latitude: float, longitude: float) -> None:
    """
    Verifica que las coordenadas estén dentro del radio permitido del campus.
    Lanza HTTP 403 si el usuario está fuera del área.
    """
    distancia = haversine(CAMPUS_LATITUDE, CAMPUS_LONGITUDE, latitude, longitude)

    if distancia > CAMPUS_RADIUS_METERS:
        raise HTTPException(
            status_code=403,
            detail=(
                f"Fuera del área de votación permitida. "
                f"Distancia al campus: {distancia:.1f}m "
                f"(máximo permitido: {CAMPUS_RADIUS_METERS}m)."
            ),
        )
