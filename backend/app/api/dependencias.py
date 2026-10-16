from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.sesion import obtener_db
from app.services.servicio_usuarios import ServicioUsuarios

esquema_bearer = OAuth2PasswordBearer(tokenUrl='api/autenticacion/ingresar')


def obtener_usuario_actual(token: str = Depends(esquema_bearer), db: Session = Depends(obtener_db)):
    servicio = ServicioUsuarios(db)
    return servicio.obtener_usuario_desde_token(token)
