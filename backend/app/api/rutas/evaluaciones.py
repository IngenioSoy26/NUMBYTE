from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencias import obtener_usuario_actual
from app.database.sesion import obtener_db
from app.schemas.evaluacion import EntregaEvaluacion, EvaluacionGenerada, ResultadoEvaluacionPublico, SolicitudEvaluacion
from app.schemas.pregunta import OpcionPublica, PreguntaPublica
from app.services.servicio_evaluaciones import ServicioEvaluaciones
from app.services.servicio_simulacros import ServicioSimulacros

router = APIRouter(prefix='/evaluaciones', tags=['Evaluaciones'])


@router.post('/generar', response_model=EvaluacionGenerada)
def generar_evaluacion(
    solicitud: SolicitudEvaluacion,
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    if solicitud.tipo_evaluacion == 'simulacro':
        estado = ServicioSimulacros(db).estado(usuario_actual)
        if not estado['permitido']:
            raise HTTPException(status_code=403, detail=estado['mensaje'])

    servicio = ServicioEvaluaciones(db)
    preguntas = servicio.generar_evaluacion(solicitud)
    if not preguntas:
        raise HTTPException(status_code=404, detail='No se encontraron preguntas para ese filtro.')

    preguntas_publicas = []
    for pregunta in preguntas:
        preguntas_publicas.append(
            PreguntaPublica(
                id=pregunta.id,
                enunciado=pregunta.enunciado,
                grado=pregunta.grado,
                tema=pregunta.tema,
                competencia=pregunta.competencia,
                dba=pregunta.dba,
                nivel_dificultad=pregunta.nivel_dificultad,
                tipo_pregunta=pregunta.tipo_pregunta,
                opciones=[
                    OpcionPublica(id=opcion.id, identificador=opcion.identificador, texto=opcion.texto)
                    for opcion in pregunta.opciones
                ],
            )
        )
    return {
        'tipo_evaluacion': solicitud.tipo_evaluacion,
        'grado': solicitud.grado,
        'tema': solicitud.tema,
        'preguntas': preguntas_publicas,
    }


@router.post('/calificar', response_model=ResultadoEvaluacionPublico)
def calificar_evaluacion(
    entrega: EntregaEvaluacion,
    db: Session = Depends(obtener_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    servicio = ServicioEvaluaciones(db)
    resultado = servicio.calificar_evaluacion(usuario_actual, entrega)
    salida = servicio.serializar_resultado(resultado)

    if entrega.tipo_evaluacion == 'simulacro':
        salida['recompensa'] = ServicioSimulacros(db).registrar_resultado(usuario_actual, resultado)

    return salida
