from pydantic import BaseModel


class InsigniaPublica(BaseModel):
    codigo: str
    nombre: str
    descripcion: str
    icono: str
    puntos_otorgados: int
    solo_plus: bool
    obtenida: bool


class MisionPublica(BaseModel):
    codigo: str
    titulo: str
    descripcion: str
    tipo: str
    meta: int
    puntos: int
    monedas: int
    solo_plus: bool
    progreso: int
    completada: bool
    bloqueada: bool


class PerfilJuegoPublico(BaseModel):
    puntos: int
    monedas: int
    nivel: int
    puntos_nivel_actual: int
    puntos_siguiente_nivel: int
    racha_actual: int
    racha_maxima: int


class ResumenGamificacion(BaseModel):
    perfil: PerfilJuegoPublico
    insignias: list[InsigniaPublica]
    misiones: list[MisionPublica]
    total_insignias: int
    insignias_obtenidas: int


class RecompensaPublica(BaseModel):
    """Respuesta que devuelve el premio obtenido tras una acción de aprendizaje."""

    puntos_ganados: int
    monedas_ganadas: int
    subio_nivel: bool
    perfil: PerfilJuegoPublico
    insignias_nuevas: list[InsigniaPublica]
    misiones_completadas: list[MisionPublica]
