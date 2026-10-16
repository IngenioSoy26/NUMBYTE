from pydantic import BaseModel


class OpcionPublica(BaseModel):
    id: int
    identificador: str
    texto: str


class PreguntaPublica(BaseModel):
    id: int
    enunciado: str
    grado: str
    tema: str
    competencia: str
    dba: str
    nivel_dificultad: str
    tipo_pregunta: str
    opciones: list[OpcionPublica]


class TemaDisponible(BaseModel):
    tema: str
    grado: str
    cantidad_preguntas: int
