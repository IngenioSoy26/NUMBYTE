from collections import defaultdict


def interpretar_desempeno(porcentaje_aciertos: float) -> tuple[str, list[str]]:
    """Interpreta el porcentaje global y devuelve un mensaje con recomendaciones base."""
    if porcentaje_aciertos < 50:
        return (
            'El estudiante necesita reforzamiento básico. Se recomienda repasar conceptos fundamentales y resolver ejercicios guiados.',
            [
                'Revisar la explicación del tema antes de volver a intentarlo.',
                'Resolver ejercicios básicos paso a paso.',
                'Hacer una práctica corta adicional hoy mismo.',
            ],
        )
    if porcentaje_aciertos < 70:
        return (
            'El estudiante muestra un avance inicial, pero todavía necesita consolidar varios procedimientos.',
            [
                'Practicar con dificultad intermedia.',
                'Comparar los errores cometidos con la explicación correcta.',
                'Repetir una evaluación corta sobre los temas débiles.',
            ],
        )
    if porcentaje_aciertos < 85:
        return (
            'El estudiante tiene un nivel aceptable y puede pasar a actividades de consolidación.',
            [
                'Alternar práctica con preguntas tipo reto.',
                'Enfocarse en precisión y lectura cuidadosa del enunciado.',
                'Prepararse para un simulacro general.',
            ],
        )
    return (
        'El estudiante presenta un desempeño sólido y puede avanzar a niveles más exigentes o simulacros.',
        [
            'Resolver simulacros completos con tiempo.',
            'Mantener práctica frecuente en temas variados.',
            'Profundizar en preguntas de mayor razonamiento.',
        ],
    )


def resumir_por_grupo(filas: list[dict], llave: str) -> dict:
    acumulado = defaultdict(lambda: {'correctas': 0, 'total': 0})
    for fila in filas:
        grupo = fila[llave]
        acumulado[grupo]['total'] += 1
        if fila['es_correcta']:
            acumulado[grupo]['correctas'] += 1

    respuesta = {}
    for grupo, valores in acumulado.items():
        respuesta[grupo] = round((valores['correctas'] / valores['total']) * 100, 2)
    return respuesta


def detectar_fortalezas_y_debilidades(detalle_temas: dict) -> tuple[list[str], list[str]]:
    fortalezas = [tema for tema, valor in detalle_temas.items() if valor >= 80]
    debilidades = [tema for tema, valor in detalle_temas.items() if valor < 60]
    return fortalezas, debilidades
