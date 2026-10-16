from pydantic import BaseModel


class TarjetaResumen(BaseModel):
    etiqueta: str
    valor: float | int | str


class PuntoHistorial(BaseModel):
    fecha: str
    porcentaje: float
    tipo_evaluacion: str


class ResumenTema(BaseModel):
    tema: str
    porcentaje: float
    intentos: int


class ResumenProgreso(BaseModel):
    tarjetas: list[TarjetaResumen]
    historial: list[PuntoHistorial]
    temas: list[ResumenTema]
    fortalezas: list[str]
    debilidades: list[str]
