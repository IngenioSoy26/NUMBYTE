"""Configuración de las pruebas del backend.

Elimina la base de datos de pruebas antes de cada sesión de pytest para que
las pruebas sean idempotentes: `numbyte_test.db` se recrea y se vuelve a
sembrar en el arranque de la aplicación. Debe ejecutarse antes de que se
importe `app` (fijar `APP_URL_BD`), por eso aquí no se importa la aplicación.
"""

from pathlib import Path

RUTA_BD_PRUEBAS = Path(__file__).resolve().parents[1] / 'numbyte_test.db'

if RUTA_BD_PRUEBAS.exists():
    RUTA_BD_PRUEBAS.unlink()
