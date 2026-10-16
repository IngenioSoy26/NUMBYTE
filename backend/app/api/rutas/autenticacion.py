from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.sesion import obtener_db
from app.schemas.autenticacion import (
    CredencialesIngreso,
    MensajeRespuesta,
    RestablecerContrasena,
    SolicitudRecuperacion,
    TokenRespuesta,
    UsuarioCrear,
)
from app.schemas.usuario import UsuarioPublico
from app.services.servicio_autenticacion import ServicioAutenticacion

router = APIRouter(prefix='/autenticacion', tags=['Autenticación'])


@router.post('/registro', response_model=UsuarioPublico, status_code=status.HTTP_201_CREATED)
def registrar_usuario(datos: UsuarioCrear, db: Session = Depends(obtener_db)):
    try:
        servicio = ServicioAutenticacion(db)
        return servicio.crear_usuario(datos)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post('/ingresar', response_model=TokenRespuesta)
def ingresar(datos: CredencialesIngreso, db: Session = Depends(obtener_db)):
    try:
        servicio = ServicioAutenticacion(db)
        token = servicio.autenticar_usuario(datos)
        return {'access_token': token, 'token_type': 'bearer'}
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


@router.post('/recuperar', response_model=MensajeRespuesta)
def solicitar_recuperacion(datos: SolicitudRecuperacion, db: Session = Depends(obtener_db)):
    """Envía al correo un enlace para restablecer la contraseña.

    La respuesta es siempre la misma para no revelar qué correos están registrados.
    """
    servicio = ServicioAutenticacion(db)
    servicio.solicitar_restablecimiento(datos.correo)
    return {
        'mensaje': 'Si el correo está registrado, enviamos las instrucciones para restablecer la contraseña.'
    }


@router.post('/restablecer', response_model=MensajeRespuesta)
def restablecer_contrasena(datos: RestablecerContrasena, db: Session = Depends(obtener_db)):
    try:
        servicio = ServicioAutenticacion(db)
        servicio.restablecer_contrasena(datos.token, datos.nueva_contrasena)
        return {'mensaje': 'Contraseña actualizada correctamente. Ya puedes iniciar sesión.'}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
