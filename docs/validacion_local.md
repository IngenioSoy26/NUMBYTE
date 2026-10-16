# Validación realizada

## Ejecutado (con evidencia)

### 1. Pruebas automatizadas del backend

```bash
cd backend
python -m pytest -q
```

**Resultado:** `6 passed, 1 warning`

Las pruebas son idempotentes: `tests/conftest.py` elimina `numbyte_test.db` antes de cada
sesión, por lo que la suite se puede repetir sin limpieza manual.

### 2. Arranque de la API

```bash
uvicorn app.main:aplicacion --host 127.0.0.1 --port 8000
```

### 3. Verificación del endpoint de salud

```bash
curl http://127.0.0.1:8000/salud
```

**Respuesta obtenida:**

```json
{"estado":"ok","mensaje":"NUMBYTE API está funcionando correctamente."}
```

### 4. Build de producción del frontend

```bash
cd frontend
npm run build
```

**Resultado:** build exitoso (`tsc -b && vite build`). Se generó `dist/` con los assets
compilados y el valor de `VITE_API_URL` incrustado correctamente en el bundle.

### 5. Normalización de la cadena de conexión a PostgreSQL

Con `DATABASE_URL=postgres://usuario:clave@host:5432/bd` definida en el entorno:

```text
url_bd    = postgresql+psycopg://usuario:clave@host:5432/bd
es_sqlite = False
dialecto  = postgresql
```

El motor portable selecciona PostgreSQL automáticamente cuando `DATABASE_URL` está presente.

## Planificado (no ejecutado todavía)

- Despliegue real de los dos servicios en Railway y prueba end-to-end contra PostgreSQL
  gestionado. Requiere que el usuario cree el proyecto, el plugin de PostgreSQL y configure
  las variables descritas en `docs/despliegue.md`.

---

© IngenioSoy — Todos los derechos reservados.
