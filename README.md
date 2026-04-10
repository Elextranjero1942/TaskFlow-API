# TaskFlow API

API REST para gestion de tareas con autenticacion JWT, desarrollada con FastAPI y SQLAlchemy sobre PostgreSQL.

## Caracteristicas

- Registro e inicio de sesion de usuarios.
- Autenticacion con token Bearer (JWT).
- Hash seguro de contrasenas con Argon2.
- CRUD completo de tareas por usuario autenticado.
- Control de acceso: cada usuario solo puede ver y editar sus tareas.
- Paginacion en listado de tareas (`limit` y `offset`).
- Migraciones de base de datos con Alembic.
- Base de datos PostgreSQL en Docker Compose.

## Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Alembic
- Pydantic v2
- Passlib (Argon2)
- python-jose (JWT)

## Estructura del proyecto

```text
Taskflow/
├── app/
│   ├── auth/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── database.py
│   └── main.py
├── alembic/
├── alembic.ini
├── docker-compose.yml
└── requirements.txt
```

## Variables de entorno

Crea un archivo `.env` en la raiz del proyecto:

```env
DATABASE_URL=postgresql+psycopg://taskflow_user:taskflow_pass@localhost:5433/taskflow_db
SECRET_KEY=pon_aqui_una_clave_larga_y_segura
```

## Instalacion y ejecucion

1. Crear y activar entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Levantar PostgreSQL con Docker:

```powershell
docker compose up -d
```

4. Ejecutar migraciones:

```powershell
alembic upgrade head
```

5. Ejecutar la API:

```powershell
uvicorn app.main:app --reload
```

## Documentacion interactiva

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints principales

### Auth

- `POST /auth/register` registrar usuario.
- `POST /auth/login` obtener access token.

### Users

- `GET /users/me` ver perfil autenticado.
- `PATCH /users/me` actualizar perfil.

### Tasks

- `GET /tasks` listar tareas del usuario (con paginacion).
- `POST /tasks` crear tarea.
- `GET /tasks/{id}` obtener tarea por id.
- `PATCH /tasks/{id}` actualizar tarea.
- `DELETE /tasks/{id}` eliminar tarea.

## Notas

- Todos los endpoints de `users` y `tasks` requieren token Bearer.
- El orden del listado de tareas prioriza pendientes y luego fecha de creacion.
