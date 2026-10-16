"""Servicio de simulacros de práctica.

Los simulacros se presentan como "simulacro de práctica inspirado en las
características de las preguntas tipo Saber 11". NO son una reproducción
oficial del examen del ICFES.

El plan Gratis permite un simulacro por día; el plan Plus, sin límite.
"""

from datetime import datetime, time, timezone

from sqlalchemy.orm import Session

from app.models.modelos import ResultadoEvaluacion, Usuario
from app.services.servicio_gamificacion import ServicioGamificacion
from app.services.servicio_planes import LIMITE_SIMULACROS_GRATIS


class ServicioSimulacros:
    def __init__(self, db: Session):
        self.db = db
        self.gamificacion = ServicioGamificacion(db)

    def estado(self, usuario: Usuario) -> dict:
        realizados_hoy = self._contar_hoy(usuario)
        es_plus = usuario.es_plus
        limite = None if es_plus else LIMITE_SIMULACROS_GRATIS
        permitido = es_plus or realizados_hoy < LIMITE_SIMULACROS_GRATIS
        return {
            'es_plus': es_plus,
            'realizados_hoy': realizados_hoy,
            'limite_diario': limite,
            'permitido': permitido,
            'mensaje': (
                'Tienes simulacros ilimitados con el plan Plus.'
                if es_plus
                else (
                    'Puedes realizar tu simulacro de práctica de hoy.'
                    if permitido
                    else 'Alcanzaste tu simulacro diario del plan Gratis. Mejora a Plus para simulacros ilimitados.'
                )
            ),
        }

    def historial(self, usuario: Usuario, limite: int = 10) -> list[dict]:
        resultados = (
            self.db.query(ResultadoEvaluacion)
            .filter(
                ResultadoEvaluacion.usuario_id == usuario.id,
                ResultadoEvaluacion.tipo_evaluacion == 'simulacro',
            )
            .order_by(ResultadoEvaluacion.fecha.desc())
            .limit(limite)
            .all()
        )
        return [
            {
                'id': resultado.id,
                'fecha': resultado.fecha.isoformat() if resultado.fecha else None,
                'cantidad_preguntas': resultado.cantidad_preguntas,
                'respuestas_correctas': resultado.respuestas_correctas,
                'porcentaje_aciertos': resultado.porcentaje_aciertos,
                'puntaje': resultado.puntaje,
                'tiempo_utilizado_segundos': resultado.tiempo_utilizado_segundos,
            }
            for resultado in resultados
        ]

    def registrar_resultado(self, usuario: Usuario, resultado: ResultadoEvaluacion) -> dict:
        """Otorga puntos e insignias tras calificar un simulacro."""
        puntos = int(round(resultado.porcentaje_aciertos))
        monedas = max(int(round(resultado.porcentaje_aciertos / 4)), 5)
        misiones = self.gamificacion.actualizar_misiones(usuario, 'simulacros', 1)
        return self.gamificacion.construir_recompensa(usuario, puntos, monedas, misiones)

    def _contar_hoy(self, usuario: Usuario) -> int:
        inicio = datetime.combine(datetime.now(timezone.utc).date(), time.min)
        return (
            self.db.query(ResultadoEvaluacion)
            .filter(
                ResultadoEvaluacion.usuario_id == usuario.id,
                ResultadoEvaluacion.tipo_evaluacion == 'simulacro',
                ResultadoEvaluacion.fecha >= inicio,
            )
            .count()
        )
