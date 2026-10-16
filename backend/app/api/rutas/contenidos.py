from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.sesion import obtener_db
from app.schemas.pregunta import TemaDisponible
from app.services.servicio_contenidos import ServicioContenidos

router = APIRouter(prefix='/contenidos', tags=['Contenidos'])


@router.get('/temas', response_model=list[TemaDisponible])
def listar_temas(db: Session = Depends(obtener_db)):
    servicio = ServicioContenidos(db)
    return servicio.listar_temas_disponibles()
