# 🗳️ Sistema de Votación - Delegado Universitario

Backend RESTful API construido con **FastAPI** y **PostgreSQL** para gestionar la
elección de delegado universitario en la Universidad Continental.

---

## 📋 Requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) como gestor de dependencias
- PostgreSQL (local o en la nube, ej. Render / Supabase / Neon)

---

## ⚙️ Configuración

### 1. Clonar e instalar dependencias

```bash
# Instalar uv si no lo tienes
pip install uv

# Instalar dependencias del proyecto
uv sync
```

### 2. Configurar variables de entorno

Edita el archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_bd
```

> **Nota:** Nunca subas el `.env` a Git. Ya está incluido en `.gitignore`.

---

## 🚀 Ejecutar localmente

```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

---

## 📡 Endpoints

| Método | Ruta                | Descripción                           |
|--------|---------------------|---------------------------------------|
| GET    | `/`                 | Health check                          |
| GET    | `/usuarios`         | Listar todos los usuarios             |
| GET    | `/usuarios/{id}`    | Obtener un usuario por ID             |
| POST   | `/usuarios`         | Registrar un nuevo usuario            |
| GET    | `/candidatos`       | Listar todos los candidatos           |
| POST   | `/candidatos`       | Crear un nuevo candidato              |
| POST   | `/votar`            | Emitir un voto                        |

### Registro de usuario (`POST /usuarios`)
```json
{
  "firebase_uid": "abc123",
  "email": "juan.perez@continental.edu.pe",
  "nombre": "Juan Pérez"
}
```
> ⚠️ El email **debe** terminar en `@continental.edu.pe`.

### Emitir voto (`POST /votar`)
```json
{
  "usuario_id": 1,
  "candidato_id": 2
}
```
> ⚠️ Si el usuario ya votó, se devuelve un error `400`.

---

## 🏗️ Estructura del proyecto

```
backend/
├── main.py              # Entrada de la aplicación
├── database.py          # Engine, SessionLocal, Base
├── models/              # Modelos SQLAlchemy
├── schemas/             # Schemas Pydantic (validación)
├── repositories/        # Acceso a datos
├── services/            # Lógica de negocio
├── routers/             # Definición de endpoints
├── .env                 # Variables de entorno (no subir a Git)
├── render.yaml          # Configuración de despliegue en Render
└── pyproject.toml       # Dependencias del proyecto (uv)
```

---

## 🔐 Preparación para Firebase Auth

El endpoint `POST /votar` está preparado para agregar validación de
**Firebase ID Token** en el futuro. Ver comentarios en:

- `services/voto_service.py` — instrucciones paso a paso
- `routers/voto_router.py` — cómo agregar el header `Authorization`

---

## ☁️ Despliegue en Render

1. Sube tu código a GitHub.
2. Crea un nuevo **Web Service** en [Render](https://render.com).
3. Conecta tu repositorio.
4. Render detectará el `render.yaml` automáticamente.
5. En el dashboard de Render, configura la variable de entorno `DATABASE_URL`
   con tu cadena de conexión a PostgreSQL.
