# NUMBYTE

NUMBYTE es un **MVP funcional** de una plataforma educativa enfocada en el fortalecimiento de las matemáticas para estudiantes de **6° a 11°**. El proyecto fue diseñado para servir como **prototipo demostrable, escalable y entendible** por aprendices de programación.

Esta versión incluye el **módulo completo de 6°** (7 temas, 7 lecciones, banco de preguntas, videos, actividades interactivas y simulacros) con **gamificación**, **planes Gratis y Plus** y **flujos de registro con correo**.

## Qué incluye esta versión

- Backend con **FastAPI + SQLAlchemy** y motor de base de datos portable: **SQLite** en desarrollo y **PostgreSQL** en producción.
- Frontend con **React + TypeScript + Vite**.
- Autenticación con **JWT** y flujo de **recuperación de contraseña** por correo (token de un solo uso).
- Registro con **correo de bienvenida**, **enlace de restablecimiento** y **confirmación de cambio de contraseña**.
- **Planes Gratis y Plus** con restricciones de acceso.
- **Gamificación:** puntos, monedas, niveles, rachas, insignias y misiones.
- **Videos de YouTube embebidos** y **actividades interactivas** (clic).
- Banco de preguntas demostrativas, diagnóstico, práctica y simulacro.
- Dashboard con gráficas modernas.
- Pruebas automatizadas del backend (idempotentes).
- Imágenes Docker de producción para **backend** y **frontend**.

> **Importante:** Los contenidos incluidos son **demostrativos**. No representan una base oficial del ICFES ni del Ministerio de Educación.

---

## Estructura del proyecto

```text
NUMBYTE/
├── backend/                 # API FastAPI
│   ├── app/
│   ├── tests/
│   ├── Dockerfile           # imagen de producción
│   ├── railway.json         # configuración de despliegue en Railway
│   ├── requirements.txt     # dependencias de producción
│   └── requirements-dev.txt # dependencias de desarrollo/pruebas
├── frontend/                # SPA React + Vite
│   ├── src/
│   ├── nginx/               # plantilla de nginx para la SPA
│   ├── Dockerfile           # build multi-stage (Vite + nginx)
│   └── railway.json
├── docker-compose.yml       # prueba local de las imágenes de producción
├── .gitignore
└── README.md
```

---

## Paleta de colores derivada del logo

| Variable | Color | Uso recomendado |
|---|---|---|
| `--azul-profundo` | `#062A63` | Fondo institucional, títulos fuertes |
| `--azul-academico` | `#0D4BA0` | Botones primarios, enlaces |
| `--cian-numbyte` | `#16C6DF` | Resaltes, estados interactivos |
| `--verde-aprendizaje` | `#14A87A` | Éxito, progreso, crecimiento |
| `--verde-brillo` | `#38C172` | Indicadores positivos |
| `--amarillo-sol` | `#F5C542` | Acentos, íconos, logros |
| `--arena-guajira` | `#F4E3BE` | Fondos suaves y detalles cálidos |
| `--blanco-nube` | `#F8FBFF` | Fondo principal |
| `--gris-tinta` | `#1F2A37` | Texto principal |
| `--gris-suave` | `#6B7A90` | Texto secundario |

---

## Requisitos

- Python 3.11+
- Node.js 20+
- npm 10+
- (Opcional) Docker y Docker Compose

---

## Ejecución local paso a paso

### 1) Backend

```bash
cd backend
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

Instala dependencias de producción:

```bash
pip install -r requirements.txt
```

Crea el archivo `.env` a partir del ejemplo (`copy .env.example .env` en Windows o `cp .env.example .env` en Linux/macOS).

Ejecuta la API:

```bash
uvicorn app.main:aplicacion --reload --host 127.0.0.1 --port 8000
```

La documentación interactiva quedará en:

- http://127.0.0.1:8000/docs
- Salud del servicio: http://127.0.0.1:8000/salud

### 2) Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

La aplicación quedará en:

- http://127.0.0.1:5173

---

## Usuario demo

Puedes entrar con:

- **Correo:** `estudiante@numbyte.com`
- **Contraseña:** `Numbyte2026*`

También puedes registrar un usuario nuevo desde la interfaz.

---

## Pruebas

### Backend

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

Las pruebas son idempotentes: `tests/conftest.py` elimina `numbyte_test.db` antes de cada sesión.

### Frontend

```bash
cd frontend
npm run build
```

---

## Docker (prueba local de las imágenes de producción)

```bash
docker compose up --build
```

- Frontend: http://localhost:8080
- Backend: http://localhost:8000

---

## Despliegue en producción (Railway + PostgreSQL)

La arquitectura son **dos servicios** en el mismo proyecto de Railway, más una base de datos PostgreSQL gestionada. Cada carpeta (`backend/` y `frontend/`) es independiente y tiene su propio `Dockerfile` y `railway.json`.

### Paso 1 — Crear el proyecto y la base de datos

1. En [Railway](https://railway.com) crea un **New Project**.
2. Agrega **New → Database → PostgreSQL**.

### Paso 2 — Servicio del backend

1. **New → GitHub Repo** y elige este repositorio.
2. En **Settings → Source**, define **Root Directory** = `backend`. Railway detectará el `Dockerfile`.
3. En la pestaña **Variables** define:

   ```env
   APP_AMBIENTE=produccion
   APP_LLAVE_SECRETA=<una cadena larga y aleatoria>
   APP_URL_FRONTEND=https://<dominio-del-frontend>
   CORS_ORIGENES=https://<dominio-del-frontend>
   CORREO_MODO=simulado
   ```

   La conexión a PostgreSQL **no se escribe a mano**: agrega una **Reference** a la
   variable del plugin de PostgreSQL y asígnala como `DATABASE_URL`. La aplicación la
   detecta automáticamente y normaliza el prefijo `postgres://` al driver `psycopg`.

4. En **Settings → Networking** genera un dominio público (por ejemplo,
   `https://numbyte-backend.up.railway.app`).
5. Verifica el despliegue en `https://<dominio-backend>/salud`.

> Si quieres correo real, cambia `CORREO_MODO=smtp` y define `SMTP_HOST`,
> `SMTP_PUERTO`, `SMTP_USUARIO`, `SMTP_CONTRASENA` y `SMTP_REMITENTE`.

### Paso 3 — Servicio del frontend

1. **New → GitHub Repo** y elige el mismo repositorio otra vez.
2. En **Settings → Source**, define **Root Directory** = `frontend`.
3. En **Variables** define:

   ```env
   VITE_API_URL=https://<dominio-backend>/api
   ```

   Esta variable se usa **en tiempo de build** (Vite la incrusta en el bundle), por lo
   que el `Dockerfile` la declara con `ARG` para que Railway la reciba durante la
   construcción. Si el dominio del backend cambia, hay que **volver a desplegar** el
   frontend.

4. En **Settings → Networking** genera un dominio público.
5. Vuelve al backend y actualiza `APP_URL_FRONTEND` y `CORS_ORIGENES` con el dominio
   final del frontend, luego redespliega.

### Notas de producción

- El backend escucha el puerto que Railway inyecta en `$PORT` (por defecto 8000 en local).
- El frontend se sirve con **nginx** y resuelve las rutas de React Router con `index.html`.
- Al arrancar, el backend crea las tablas, aplica migraciones ligeras y carga los datos
  demostrativos de 6° (operación idempotente: no borra usuarios ni progreso).
- **No** se sube ningún archivo `.env` al repositorio: las credenciales viven en Railway.

---

## Extensiones recomendadas a futuro

1. Panel docente.
2. Carga masiva de preguntas desde Excel/CSV.
3. Gestión curricular real por DBA validados.
4. Integración móvil con Capacitor.
5. Panel administrativo.
6. Analítica académica por curso, sede o institución.

---

## Nota importante para el aprendiz que continúe el proyecto

- Las variables y nombres están en español a propósito.
- Los comentarios fueron escritos para que el código sea más fácil de seguir.
- Si vas a crecer el sistema, procura mantener la separación entre:
  - modelos
  - esquemas
  - servicios
  - rutas
  - motor educativo

---

© IngenioSoy — Todos los derechos reservados.
