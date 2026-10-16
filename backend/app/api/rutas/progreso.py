from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencias import obtener_usuario_actual
from app.database.sesion import obtener_db
from app.schemas.progreso import ResumenProgreso
from app.services.servicio_progreso import ServicioProgreso

router = APIRouter(prefix='/progreso', tags=['Progreso'])


@router.get('/resumen', response_model=ResumenProgreso)
def obtener_resumen_progreso(
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioProgreso(db)
    return servicio.construir_resumen(usuario_actual)
