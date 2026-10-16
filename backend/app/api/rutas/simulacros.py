from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencias import obtener_usuario_actual
from app.database.sesion import obtener_db
from app.services.servicio_simulacros import ServicioSimulacros

router = APIRouter(prefix='/simulacros', tags=['Simulacros'])


@router.get('/estado')
def obtener_estado(
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioSimulacros(db)
    return servicio.estado(usuario_actual)


@router.get('/historial')
def obtener_historial(
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioSimulacros(db)
    return servicio.historial(usuario_actual)
