from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.configuracion import configuracion

# Ajustes de conexión según el motor.
# - SQLite necesita `check_same_thread=False` porque la app abre sesiones
#   desde distintos hilos.
# - PostgreSQL gestionado (Railway, Neon, Supabase...) puede cerrar conexiones
#   inactivas, por eso usamos `pool_pre_ping` y reciclamos el pool.
if configuracion.es_sqlite:
    argumentos_conexion = {'check_same_thread': False}
    opciones_motor = {}
else:
    argumentos_conexion = {}
    opciones_motor = {'pool_pre_ping': True, 'pool_recycle': 300}

motor = create_engine(
    configuracion.url_bd,
    connect_args=argumentos_conexion,
    **opciones_motor,
)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)


def obtener_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
