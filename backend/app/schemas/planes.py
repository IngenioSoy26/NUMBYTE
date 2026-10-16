from pydantic import BaseModel


class BeneficioPlan(BaseModel):
    titulo: str
    descripcion: str
    solo_plus: bool


class PlanPublico(BaseModel):
    plan: str
    es_plus: bool
    fecha_activacion_plan: str | None = None
    beneficios: list[BeneficioPlan]


class RespuestaActivacionPlus(BaseModel):
    mensaje: str
    plan: PlanPublico
