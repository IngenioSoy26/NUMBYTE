from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.modelos import Pregunta


class ServicioContenidos:
    def __init__(self, db: Session):
        self.db = db

    def listar_temas_disponibles(self):
        consulta = (
            self.db.query(Pregunta.tema, Pregunta.grado, func.count(Pregunta.id))
            .group_by(Pregunta.tema, Pregunta.grado)
            .order_by(Pregunta.grado, Pregunta.tema)
            .all()
        )
        return [
            {'tema': tema, 'grado': grado, 'cantidad_preguntas': cantidad}
            for tema, grado, cantidad in consulta
        ]
