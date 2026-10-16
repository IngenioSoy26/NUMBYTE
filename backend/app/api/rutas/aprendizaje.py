from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencias import obtener_usuario_actual
from app.database.sesion import obtener_db
from app.schemas.aprendizaje import (
    ActividadPublica,
    EnvioActividad,
    ResultadoActividad,
    RutaAprendizaje,
)
from app.schemas.gamificacion import RecompensaPublica
from app.services.servicio_aprendizaje import ServicioAprendizaje

router = APIRouter(prefix='/aprendizaje', tags=['Aprendizaje'])


@router.get('/ruta', response_model=RutaAprendizaje)
def obtener_ruta(
    grado: str = '6',
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioAprendizaje(db)
    return servicio.construir_ruta(usuario_actual, grado)


@router.post('/leccion/{leccion_id}/completar', response_model=RecompensaPublica)
def completar_leccion(
    leccion_id: int,
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioAprendizaje(db)
    return servicio.completar_leccion(usuario_actual, leccion_id)


@router.get('/actividad/{actividad_id}', response_model=ActividadPublica)
def obtener_actividad(
    actividad_id: int,
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioAprendizaje(db)
    return servicio.obtener_actividad(usuario_actual, actividad_id)


@router.post('/actividad/{actividad_id}/responder', response_model=ResultadoActividad)
def responder_actividad(
    actividad_id: int,
    envio: EnvioActividad,
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioAprendizaje(db)
    return servicio.responder_actividad(usuario_actual, actividad_id, envio.respuestas)
