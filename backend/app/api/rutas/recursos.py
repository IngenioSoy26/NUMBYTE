from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencias import obtener_usuario_actual
from app.database.sesion import obtener_db
from app.services.servicio_recursos import ServicioRecursos

router = APIRouter(prefix='/recursos', tags=['Recursos'])


@router.get('')
def listar_recursos(
    grado: str | None = None,
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioRecursos(db)
    return servicio.listar(usuario_actual, grado)
