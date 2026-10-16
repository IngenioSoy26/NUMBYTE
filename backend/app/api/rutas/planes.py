from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencias import obtener_usuario_actual
from app.database.sesion import obtener_db
from app.schemas.planes import PlanPublico, RespuestaActivacionPlus
from app.services.servicio_planes import ServicioPlanes

router = APIRouter(prefix='/planes', tags=['Planes'])


@router.get('/mi-plan', response_model=PlanPublico)
def obtener_mi_plan(
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioPlanes(db)
    return servicio.obtener_plan(usuario_actual)


@router.post('/activar-plus', response_model=RespuestaActivacionPlus)
def activar_plus(
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioPlanes(db)
    plan = servicio.activar_plus(usuario_actual)
    return {
        'mensaje': 'Plan Plus activado (demostración sin cobro real). ¡Disfruta todos los beneficios!',
        'plan': plan,
    }


@router.post('/volver-a-gratis', response_model=RespuestaActivacionPlus)
def volver_a_gratis(
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioPlanes(db)
    plan = servicio.volver_a_gratis(usuario_actual)
    return {'mensaje': 'Volviste al plan Gratis (demostración).', 'plan': plan}
