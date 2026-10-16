from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioPublico(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: EmailStr
    grado: str
    estado_cuenta: str
    plan: str
    es_plus: bool
    fecha_registro: datetime
