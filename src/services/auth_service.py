import os  # ← falta esto
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.repositories import usuario_repository
from src.models.usuario_model import Usuario


# 🔥 INICIALIZAR FIREBASE CON SERVICE ACCOUNT
def _initialize_firebase() -> None:
    """Inicializa Firebase Admin SDK si no está ya inicializado."""
    if firebase_admin._apps:
        return

    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "token_uri": "https://oauth2.googleapis.com/token",
    })

    firebase_admin.initialize_app(cred)
    print("[OK] Firebase Admin inicializado con proyecto CORRECTO")


# 🔐 VERIFICAR TOKEN FIREBASE
def verify_firebase_token(authorization: str) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header requerido (Bearer <token>).",
        )

    token = authorization.split(" ", 1)[1]

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token de Firebase inválido o expirado.",
        )


# 👤 OBTENER USUARIO ACTUAL (CREA SI NO EXISTE)
def get_current_user(
    authorization: str,
    db: Session,
) -> Usuario:

    decoded = verify_firebase_token(authorization)

    email: str = decoded.get("email", "")

    # 🔒 SOLO CORREOS UNIVERSIDAD
    if not email.endswith("@continental.edu.pe"):
        raise HTTPException(
            status_code=403,
            detail="Acceso restringido a correos @continental.edu.pe.",
        )

    firebase_uid: str = decoded.get("uid", "")
    nombre: str = decoded.get("name", "")

    usuario = usuario_repository.get_by_firebase_uid(db, firebase_uid)

    if not usuario:
        from src.schemas.usuario_schema import UsuarioCreate

        data = UsuarioCreate(
            firebase_uid=firebase_uid,
            email=email,
            nombre=nombre or None,
        )

        usuario = usuario_repository.create(db, data)

    return usuario