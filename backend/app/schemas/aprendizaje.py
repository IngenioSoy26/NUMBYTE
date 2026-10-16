from pydantic import BaseModel

from app.schemas.gamificacion import RecompensaPublica


class LeccionPublica(BaseModel):
    id: int
    grado: str
    tema: str
    titulo: str
    subtitulo: str
    explicacion: str
    ejemplo: str
    puntos: int
    orden: int


class ActividadPublica(BaseModel):
    id: int
    grado: str
    tema: str
    titulo: str
    instrucciones: str
    tipo: str
    datos: dict
    puntos: int
    solo_plus: bool
    bloqueada: bool


class ItemRuta(BaseModel):
    tema: str
    orden: int
    leccion: LeccionPublica | None = None
    actividad: ActividadPublica | None = None
    recurso: dict | None = None
    leccion_completada: bool
    actividad_completada: bool
    progreso: int


class RutaAprendizaje(BaseModel):
    grado: str
    total_items: int
    items_completados: int
    porcentaje: float
    items: list[ItemRuta]


class EnvioActividad(BaseModel):
    respuestas: dict


class ResultadoActividad(BaseModel):
    correcta: bool
    puntaje: int
    total: int
    recompensa: RecompensaPublica
