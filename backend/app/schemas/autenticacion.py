from pydantic import BaseModel, EmailStr, Field


class UsuarioCrear(BaseModel):
    nombre: str = Field(min_length=3, max_length=120)
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=60)
    grado: str


class CredencialesIngreso(BaseModel):
    correo: EmailStr
    contrasena: str


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class MensajeRespuesta(BaseModel):
    mensaje: str


class SolicitudRecuperacion(BaseModel):
    correo: EmailStr


class RestablecerContrasena(BaseModel):
    token: str = Field(min_length=10)
    nueva_contrasena: str = Field(min_length=8, max_length=60)
