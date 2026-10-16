from fastapi import HTTPException, status
import jwt
from sqlalchemy.orm import Session

from app.core.configuracion import configuracion
from app.models.modelos import Usuario


class ServicioUsuarios:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, usuario_id: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_desde_token(self, token: str) -> Usuario:
        try:
            carga = jwt.decode(
                token,
                configuracion.app_llave_secreta,
                algorithms=[configuracion.app_algoritmo_jwt],
            )
            usuario_id = int(carga.get('sub'))
        except (jwt.InvalidTokenError, TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token inválido o expirado.',
            )

        usuario = self.obtener_por_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='No se encontró el usuario del token.',
            )
        return usuario
