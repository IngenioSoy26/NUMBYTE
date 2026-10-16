from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencias import obtener_usuario_actual
from app.database.sesion import obtener_db
from app.schemas.gamificacion import ResumenGamificacion
from app.services.servicio_gamificacion import ServicioGamificacion

router = APIRouter(prefix='/gamificacion', tags=['Gamificación'])


@router.get('/resumen', response_model=ResumenGamificacion)
def obtener_resumen(
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioGamificacion(db)
    return servicio.resumen(usuario_actual)
