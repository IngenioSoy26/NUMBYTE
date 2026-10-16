from fastapi import APIRouter, Depends

from app.api.dependencias import obtener_usuario_actual
from app.schemas.usuario import UsuarioPublico

router = APIRouter(prefix='/usuarios', tags=['Usuarios'])


@router.get('/yo', response_model=UsuarioPublico)
def leer_mi_perfil(usuario_actual=Depends(obtener_usuario_actual)):
    return usuario_actual
