import json
import random
from collections import defaultdict

from sqlalchemy.orm import Session, joinedload

from app.models.modelos import OpcionRespuesta, Pregunta, ProgresoTema, RespuestaUsuario, ResultadoEvaluacion, Usuario
from app.motor_educativo.diagnostico import (
    detectar_fortalezas_y_debilidades,
    interpretar_desempeno,
    resumir_por_grupo,
)
from app.schemas.evaluacion import EntregaEvaluacion, SolicitudEvaluacion


class ServicioEvaluaciones:
    def __init__(self, db: Session):
        self.db = db

    def generar_evaluacion(self, solicitud: SolicitudEvaluacion) -> list[Pregunta]:
        consulta = self.db.query(Pregunta).options(joinedload(Pregunta.opciones)).filter(
            Pregunta.grado == solicitud.grado
        )

        if solicitud.tema:
            consulta = consulta.filter(Pregunta.tema == solicitud.tema)
        if solicitud.dificultad:
            consulta = consulta.filter(Pregunta.nivel_dificultad == solicitud.dificultad)

        preguntas = consulta.all()
        random.shuffle(preguntas)
        return preguntas[: solicitud.cantidad_preguntas]

    def calificar_evaluacion(self, usuario: Usuario, entrega: EntregaEvaluacion) -> ResultadoEvaluacion:
        ids_preguntas = [respuesta.pregunta_id for respuesta in entrega.respuestas]
        preguntas = (
            self.db.query(Pregunta)
            .options(joinedload(Pregunta.opciones))
            .filter(Pregunta.id.in_(ids_preguntas))
            .all()
        )
        mapa_preguntas = {pregunta.id: pregunta for pregunta in preguntas}

        detalle_filas = []
        cantidad_correctas = 0
        respuestas_modelo = []
        errores_frecuentes = defaultdict(int)

        for respuesta in entrega.respuestas:
            pregunta = mapa_preguntas.get(respuesta.pregunta_id)
            if not pregunta:
                continue

            opcion_correcta = next((opcion for opcion in pregunta.opciones if opcion.es_correcta), None)
            opcion_seleccionada = next(
                (opcion for opcion in pregunta.opciones if opcion.id == respuesta.opcion_id), None
            )
            es_correcta = bool(opcion_correcta and opcion_seleccionada and opcion_correcta.id == opcion_seleccionada.id)
            if es_correcta:
                cantidad_correctas += 1
            else:
                if opcion_seleccionada and opcion_seleccionada.tipo_error:
                    errores_frecuentes[opcion_seleccionada.tipo_error] += 1

            detalle_filas.append(
                {
                    'pregunta_id': pregunta.id,
                    'tema': pregunta.tema,
                    'competencia': pregunta.competencia,
                    'es_correcta': es_correcta,
                }
            )
            respuestas_modelo.append(
                RespuestaUsuario(
                    pregunta_id=pregunta.id,
                    opcion_seleccionada_id=respuesta.opcion_id,
                    es_correcta=es_correcta,
                )
            )

        cantidad_preguntas = len(detalle_filas)
        cantidad_incorrectas = cantidad_preguntas - cantidad_correctas
        porcentaje_aciertos = round((cantidad_correctas / cantidad_preguntas) * 100, 2) if cantidad_preguntas else 0
        puntaje = round((porcentaje_aciertos / 100) * 5, 2)

        detalle_temas = resumir_por_grupo(detalle_filas, 'tema')
        detalle_competencias = resumir_por_grupo(detalle_filas, 'competencia')
        fortalezas, debilidades = detectar_fortalezas_y_debilidades(detalle_temas)
        interpretacion, recomendaciones = interpretar_desempeno(porcentaje_aciertos)

        if errores_frecuentes:
            error_principal = max(errores_frecuentes, key=errores_frecuentes.get)
            interpretacion += f' Error frecuente detectado: {error_principal}.'

        resultado = ResultadoEvaluacion(
            usuario_id=usuario.id,
            tipo_evaluacion=entrega.tipo_evaluacion,
            grado=entrega.grado,
            tema_principal=entrega.tema or 'General',
            cantidad_preguntas=cantidad_preguntas,
            respuestas_correctas=cantidad_correctas,
            respuestas_incorrectas=cantidad_incorrectas,
            porcentaje_aciertos=porcentaje_aciertos,
            puntaje=puntaje,
            tiempo_utilizado_segundos=entrega.tiempo_utilizado_segundos,
            fortalezas='|'.join(fortalezas),
            debilidades='|'.join(debilidades),
            interpretacion_pedagogica=interpretacion,
            recomendaciones='|'.join(recomendaciones),
            detalle_temas=json.dumps(detalle_temas, ensure_ascii=False),
            detalle_competencias=json.dumps(detalle_competencias, ensure_ascii=False),
        )

        self.db.add(resultado)
        self.db.flush()
        for respuesta_modelo in respuestas_modelo:
            respuesta_modelo.resultado_id = resultado.id
            self.db.add(respuesta_modelo)

        self._actualizar_progreso(usuario, detalle_filas, fortalezas, debilidades)
        self.db.commit()
        self.db.refresh(resultado)
        return resultado

    def _actualizar_progreso(self, usuario: Usuario, detalle_filas: list[dict], fortalezas: list[str], debilidades: list[str]):
        agrupado = defaultdict(list)
        for fila in detalle_filas:
            agrupado[(fila['tema'], fila['competencia'])].append(fila)

        for (tema, competencia), filas in agrupado.items():
            porcentaje = round((sum(1 for fila in filas if fila['es_correcta']) / len(filas)) * 100, 2)
            progreso = (
                self.db.query(ProgresoTema)
                .filter(
                    ProgresoTema.usuario_id == usuario.id,
                    ProgresoTema.tema == tema,
                    ProgresoTema.competencia == competencia,
                )
                .first()
            )

            if not progreso:
                progreso = ProgresoTema(
                    usuario_id=usuario.id,
                    tema=tema,
                    competencia=competencia,
                    intentos=0,
                )
                self.db.add(progreso)

            progreso.intentos += 1
            progreso.porcentaje_aciertos = porcentaje
            progreso.porcentaje_errores = round(100 - porcentaje, 2)
            progreso.fortalezas = ', '.join(fortalezas)
            progreso.debilidades = ', '.join(debilidades)

    @staticmethod
    def serializar_resultado(resultado: ResultadoEvaluacion) -> dict:
        return {
            'id': resultado.id,
            'tipo_evaluacion': resultado.tipo_evaluacion,
            'grado': resultado.grado,
            'tema_principal': resultado.tema_principal,
            'cantidad_preguntas': resultado.cantidad_preguntas,
            'respuestas_correctas': resultado.respuestas_correctas,
            'respuestas_incorrectas': resultado.respuestas_incorrectas,
            'porcentaje_aciertos': resultado.porcentaje_aciertos,
            'puntaje': resultado.puntaje,
            'tiempo_utilizado_segundos': resultado.tiempo_utilizado_segundos,
            'fortalezas': [item for item in resultado.fortalezas.split('|') if item],
            'debilidades': [item for item in resultado.debilidades.split('|') if item],
            'interpretacion_pedagogica': resultado.interpretacion_pedagogica,
            'recomendaciones': [item for item in resultado.recomendaciones.split('|') if item],
            'detalle_temas': json.loads(resultado.detalle_temas or '{}'),
            'detalle_competencias': json.loads(resultado.detalle_competencias or '{}'),
        }
