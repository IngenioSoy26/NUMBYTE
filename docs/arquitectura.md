# Arquitectura general de NUMBYTE

## Capas del sistema

1. **Frontend**
   - Presenta la interfaz al estudiante.
   - Consume la API REST.
   - Renderiza paneles, gráficas y evaluaciones.

2. **API / Backend**
   - Gestiona autenticación.
   - Filtra preguntas.
   - Califica evaluaciones.
   - Resume progreso.

3. **Motor educativo**
   - Interpreta resultados.
   - Detecta fortalezas y debilidades.
   - Sugiere actividades.

4. **Persistencia**
   - SQLite en desarrollo.
   - PostgreSQL en producción (Railway), con detección automática por `DATABASE_URL`.

## Decisiones de diseño

- Se usó una estructura modular sencilla para que el proyecto sea entendible.
- Las rutas solo orquestan.
- La lógica real vive en `services` y `motor_educativo`.
- La base de datos contiene únicamente lo necesario para un MVP demostrativo.
