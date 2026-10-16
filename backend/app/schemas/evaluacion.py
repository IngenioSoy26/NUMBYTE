from pydantic import BaseModel, Field

from app.schemas.gamificacion import RecompensaPublica
from app.schemas.pregunta import PreguntaPublica


class SolicitudEvaluacion(BaseModel):
    tipo_evaluacion: str = Field(pattern='^(diagnostico|practica|simulacro)$')
    grado: str
    tema: str | None = None
    dificultad: str | None = None
    cantidad_preguntas: int = Field(default=5, ge=3, le=15)


class RespuestaEnviada(BaseModel):
    pregunta_id: int
    opcion_id: int | None = None


class EntregaEvaluacion(BaseModel):
    tipo_evaluacion: str = Field(pattern='^(diagnostico|practica|simulacro)$')
    grado: str
    tema: str | None = None
    tiempo_utilizado_segundos: int = 0
    respuestas: list[RespuestaEnviada]


class EvaluacionGenerada(BaseModel):
    tipo_evaluacion: str
    grado: str
    tema: str | None = None
    preguntas: list[PreguntaPublica]


class ResultadoEvaluacionPublico(BaseModel):
    id: int
    tipo_evaluacion: str
    grado: str
    tema_principal: str
    cantidad_preguntas: int
    respuestas_correctas: int
    respuestas_incorrectas: int
    porcentaje_aciertos: float
    puntaje: float
    tiempo_utilizado_segundos: int
    fortalezas: list[str]
    debilidades: list[str]
    interpretacion_pedagogica: str
    recomendaciones: list[str]
    detalle_temas: dict
    detalle_competencias: dict
    recompensa: RecompensaPublica | None = None
