from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 🔥 IMPORTANTE
from src.database import engine, Base
load_dotenv()
# Importar modelos para que SQLAlchemy los registre antes de create_all
import src.models.usuario_model  # noqa: F401
import src.models.candidato_model  # noqa: F401
import src.models.voto_model  # noqa: F401
import src.models.voting_location_model  # noqa: F401

from src.apis import usuario_router, candidato_router, voto_router, auth_router
from src.services.auth_service import _initialize_firebase


@asynccontextmanager

async def lifespan(app: FastAPI):
    # Inicializar Firebase Admin SDK
    _initialize_firebase()
    # Crear las tablas automáticamente al iniciar el servidor
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Sistema de Votación - Delegado Universitario",
    description=(
        "API REST para la elección de delegado y subdelegado de Ingeniería de Sistemas "
        "de la Universidad Continental. Requiere autenticación Firebase y validación "
        "geográfica (campus universitario, radio 100m)."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

# 🔥🔥🔥 AGREGADO — CORS PARA FLUTTER WEB 🔥🔥🔥
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para pruebas (luego restringir)
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router.router)
app.include_router(usuario_router.router)
app.include_router(candidato_router.router)
app.include_router(voto_router.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "API de votación funcionando correctamente"}