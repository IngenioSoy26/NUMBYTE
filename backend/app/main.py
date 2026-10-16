from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.rutas import (
    aprendizaje,
    autenticacion,
    contenidos,
    evaluaciones,
    gamificacion,
    planes,
    progreso,
    recursos,
    salud,
    simulacros,
    usuarios,
)
from app.core.configuracion import configuracion
from app.database.base import Base
from app.database.migraciones import aplicar_migraciones_ligeras
from app.database.sesion import SesionLocal, motor
from app.seed.cargar_datos import (
    poblar_contenido_sexto,
    poblar_datos_iniciales,
    sincronizar_recursos_sexto,
)


@asynccontextmanager
async def ciclo_vida(aplicacion: FastAPI):
    """Inicializa la base y carga datos demostrativos al levantar la app."""
    Base.metadata.create_all(bind=motor)
    aplicar_migraciones_ligeras(motor)
    db = SesionLocal()
    try:
        poblar_datos_iniciales(db)
        poblar_contenido_sexto(db)
        sincronizar_recursos_sexto(db)
    finally:
        db.close()
    yield


aplicacion = FastAPI(
    title=configuracion.app_nombre,
    version='1.0.0',
    lifespan=ciclo_vida,
    description='API del prototipo educativo NUMBYTE.',
)

aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=configuracion.lista_origenes_cors,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

aplicacion.include_router(salud.router)
aplicacion.include_router(autenticacion.router, prefix='/api')
aplicacion.include_router(usuarios.router, prefix='/api')
aplicacion.include_router(contenidos.router, prefix='/api')
aplicacion.include_router(evaluaciones.router, prefix='/api')
aplicacion.include_router(progreso.router, prefix='/api')
aplicacion.include_router(aprendizaje.router, prefix='/api')
aplicacion.include_router(gamificacion.router, prefix='/api')
aplicacion.include_router(planes.router, prefix='/api')
aplicacion.include_router(recursos.router, prefix='/api')
aplicacion.include_router(simulacros.router, prefix='/api')
