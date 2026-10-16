import json

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.modelos import ProgresoTema, ResultadoEvaluacion, Usuario


class ServicioProgreso:
    def __init__(self, db: Session):
        self.db = db

    def construir_resumen(self, usuario: Usuario) -> dict:
        resultados = (
            self.db.query(ResultadoEvaluacion)
            .filter(ResultadoEvaluacion.usuario_id == usuario.id)
            .order_by(desc(ResultadoEvaluacion.fecha))
            .all()
        )
        progresos = (
            self.db.query(ProgresoTema)
            .filter(ProgresoTema.usuario_id == usuario.id)
            .order_by(desc(ProgresoTema.fecha_actualizacion))
            .all()
        )

        promedio = round(
            sum(item.porcentaje_aciertos for item in resultados) / len(resultados), 2
        ) if resultados else 0

        tarjetas = [
            {'etiqueta': 'Promedio general', 'valor': promedio},
            {'etiqueta': 'Evaluaciones realizadas', 'valor': len(resultados)},
            {'etiqueta': 'Tema más reciente', 'valor': resultados[0].tema_principal if resultados else 'Sin datos'},
            {'etiqueta': 'Mejor puntaje', 'valor': max((item.puntaje for item in resultados), default=0)},
        ]

        historial = [
            {
                'fecha': item.fecha.strftime('%Y-%m-%d'),
                'porcentaje': item.porcentaje_aciertos,
                'tipo_evaluacion': item.tipo_evaluacion,
            }
            for item in reversed(resultados)
        ]

        temas = [
            {
                'tema': item.tema,
                'porcentaje': item.porcentaje_aciertos,
                'intentos': item.intentos,
            }
            for item in progresos[:8]
        ]

        fortalezas = []
        debilidades = []
        if resultados:
            ultimo = resultados[0]
            fortalezas = [item for item in ultimo.fortalezas.split('|') if item]
            debilidades = [item for item in ultimo.debilidades.split('|') if item]
            if not fortalezas and ultimo.detalle_temas:
                detalle = json.loads(ultimo.detalle_temas)
                fortalezas = [tema for tema, valor in detalle.items() if valor >= 80]
                debilidades = [tema for tema, valor in detalle.items() if valor < 60]

        return {
            'tarjetas': tarjetas,
            'historial': historial,
            'temas': temas,
            'fortalezas': fortalezas,
            'debilidades': debilidades,
        }
