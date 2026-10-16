# Guía de despliegue de NUMBYTE (producción)

## Arquitectura

Dos servicios Docker en un mismo proyecto de **Railway**, más una base de datos **PostgreSQL** gestionada:

| Componente | Tecnología | Carpeta | Imagen |
|---|---|---|---|
| API | FastAPI + Uvicorn | `backend/` | `python:3.12-slim` |
| Interfaz | React + Vite servido por nginx | `frontend/` | `nginx:1.27-alpine` |
| Base de datos | PostgreSQL gestionado | — | plugin de Railway |

El backend usa **SQLite** en desarrollo y **PostgreSQL** en producción. La detección es automática:
si existe la variable `DATABASE_URL`, se usa esa conexión; si no, se usa `APP_URL_BD`.

## Escenario recomendado

### Backend (servicio 1 de Railway)

- **Root Directory:** `backend`
- El `Dockerfile` se detecta automáticamente y arranca con:

```bash
uvicorn app.main:aplicacion --host 0.0.0.0 --port ${PORT:-8000}
```

- **Healthcheck:** `GET /salud`

Variables de entorno:

```env
APP_AMBIENTE=produccion
APP_LLAVE_SECRETA=COLOCA_AQUI_UNA_LLAVE_LARGA_Y_SEGURA
APP_URL_FRONTEND=https://<dominio-del-frontend>
CORS_ORIGENES=https://<dominio-del-frontend>
CORREO_MODO=simulado
```

La conexión a PostgreSQL se agrega como **Reference** a la variable del plugin y se
asigna a `DATABASE_URL`; no se escribe a mano. Prefijos `postgres://` y `postgresql://`
se normalizan automáticamente al driver `psycopg`.

### Frontend (servicio 2 de Railway)

- **Root Directory:** `frontend`
- **Build:** multi-stage (Vite compila → nginx sirve la SPA).
- El puerto lo inyecta Railway vía `$PORT` en la plantilla de nginx.

Variables de entorno (**en tiempo de build**, Vite las incrusta en el bundle):

```env
VITE_API_URL=https://<dominio-del-backend>/api
```

> Si cambia el dominio del backend, hay que **redesplegar** el frontend para regenerar el bundle.

## Prueba local de las imágenes de producción

```bash
docker compose up --build
```

- Frontend: http://localhost:8080
- Backend: http://localhost:8000 (salud en `/salud`, documentación en `/docs`)

## Variables de entorno frontend (desarrollo local)

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

## Notas

- El `.env` nunca se sube al repositorio: las credenciales viven en Railway.
- Al arrancar, el backend crea las tablas, aplica migraciones ligeras y carga los datos
  demostrativos de 6° de forma idempotente (no borra usuarios ni progreso).

---

© IngenioSoy — Todos los derechos reservados.
