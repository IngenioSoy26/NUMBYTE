import json

from sqlalchemy.orm import Session

from app.core.seguridad import obtener_hash_contrasena
from app.models.modelos import (
    ActividadInteractiva,
    Insignia,
    Leccion,
    Mision,
    OpcionRespuesta,
    Pregunta,
    RecursoMultimedia,
    RespuestaUsuario,
    Usuario,
)
from app.seed.contenido_sexto import (
    ACTIVIDADES_SEXTO,
    INSIGNIAS,
    LECCIONES_SEXTO,
    MISIONES,
    PREGUNTAS_SEXTO,
    RECURSOS_SEXTO,
)


PREGUNTAS_DEMO = [
    {
        'enunciado': 'Si una camiseta cuesta $48.000 y tiene un descuento del 25%, ¿cuál es el precio final?',
        'grado': '6',
        'tema': 'Porcentajes',
        'competencia': 'Resolución de problemas',
        'dba': 'Uso de porcentajes en contextos cotidianos (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'El 25% de 48.000 es 12.000, por tanto el precio final es 36.000.',
        'justificacion_pedagogica': 'Evalúa el uso de porcentajes en compras cotidianas.',
        'opciones': [
            ('A', '$36.000', True, '', ''),
            ('B', '$24.000', False, 'Se aplicó un descuento incorrecto.', 'Calcular mal el porcentaje'),
            ('C', '$42.000', False, 'Se restó un valor arbitrario.', 'Resta sin procedimiento'),
            ('D', '$60.000', False, 'Se sumó en lugar de restar.', 'Confundir descuento con recargo'),
        ],
    },
    {
        'enunciado': 'En la expresión 3x + 5 = 20, el valor de x es:',
        'grado': '7',
        'tema': 'Ecuaciones',
        'competencia': 'Razonamiento algebraico',
        'dba': 'Resolución de ecuaciones lineales simples (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Primero se resta 5 y queda 3x = 15. Luego se divide entre 3 y x = 5.',
        'justificacion_pedagogica': 'Permite identificar si el estudiante domina operaciones inversas.',
        'opciones': [
            ('A', 'x = 5', True, '', ''),
            ('B', 'x = 15', False, 'No se dividió entre 3.', 'No aplicar la operación inversa final'),
            ('C', 'x = 25', False, 'Se sumó en lugar de despejar.', 'Confundir procedimiento algebraico'),
            ('D', 'x = 3', False, 'Se confundió el coeficiente con el resultado.', 'Confundir coeficiente con solución'),
        ],
    },
    {
        'enunciado': 'Un triángulo tiene base 8 cm y altura 5 cm. Su área es:',
        'grado': '8',
        'tema': 'Geometría',
        'competencia': 'Representación y medición',
        'dba': 'Cálculo de áreas de figuras planas (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Área = base × altura ÷ 2 = 8 × 5 ÷ 2 = 20 cm².',
        'justificacion_pedagogica': 'Verifica la aplicación correcta de una fórmula geométrica básica.',
        'opciones': [
            ('A', '20 cm²', True, '', ''),
            ('B', '40 cm²', False, 'Se omitió la división entre 2.', 'Olvidar parte de la fórmula'),
            ('C', '13 cm²', False, 'Se sumó en vez de multiplicar.', 'Aplicación incorrecta de operaciones'),
            ('D', '10 cm²', False, 'Se dividió mal el resultado.', 'Procedimiento incompleto'),
        ],
    },
    {
        'enunciado': 'La media de los datos 2, 4, 6, 8 es:',
        'grado': '6',
        'tema': 'Estadística',
        'competencia': 'Interpretación de información',
        'dba': 'Uso de medidas de tendencia central (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'La suma es 20 y se divide entre 4, dando 5.',
        'justificacion_pedagogica': 'Ayuda a reforzar el concepto de promedio aritmético.',
        'opciones': [
            ('A', '4', False, 'Se eligió uno de los datos, no el promedio.', 'Confundir dato con promedio'),
            ('B', '5', True, '', ''),
            ('C', '10', False, 'Se dividió incorrectamente.', 'Error al dividir'),
            ('D', '20', False, 'Se sumó pero no se promedió.', 'Olvidar dividir entre la cantidad de datos'),
        ],
    },
    {
        'enunciado': 'Si y = 2x + 1, ¿cuál es el valor de y cuando x = 4?',
        'grado': '7',
        'tema': 'Funciones',
        'competencia': 'Razonamiento algebraico',
        'dba': 'Evaluación de expresiones algebraicas (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Se reemplaza x por 4: y = 2(4) + 1 = 9.',
        'justificacion_pedagogica': 'Mide la capacidad de sustitución y cálculo en expresiones.',
        'opciones': [
            ('A', '8', False, 'Se olvidó sumar 1.', 'Omitir el término independiente'),
            ('B', '9', True, '', ''),
            ('C', '6', False, 'Se calculó 2+4.', 'Confundir multiplicación con suma'),
            ('D', '3', False, 'Se operó sin seguir la expresión.', 'Sustitución incorrecta'),
        ],
    },
    {
        'enunciado': '¿Cuál es la pendiente de la recta que pasa por (1,2) y (3,6)?',
        'grado': '9',
        'tema': 'Geometría analítica',
        'competencia': 'Razonamiento algebraico',
        'dba': 'Análisis de variación y cambio (demostrativo)',
        'nivel_dificultad': 'alta',
        'explicacion': 'm = (6-2)/(3-1) = 4/2 = 2.',
        'justificacion_pedagogica': 'Introduce análisis de cambio usando coordenadas.',
        'opciones': [
            ('A', '2', True, '', ''),
            ('B', '4', False, 'Se tomó solo la diferencia en y.', 'Olvidar dividir por el cambio en x'),
            ('C', '1/2', False, 'Se invirtió la razón.', 'Invertir numerador y denominador'),
            ('D', '8', False, 'Se sumaron diferencias.', 'Procedimiento incorrecto'),
        ],
    },
    {
        'enunciado': 'Una razón equivalente a 3/4 es:',
        'grado': '6',
        'tema': 'Fracciones',
        'competencia': 'Razonamiento numérico',
        'dba': 'Reconocimiento de fracciones equivalentes (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Si multiplicamos numerador y denominador por 2 obtenemos 6/8.',
        'justificacion_pedagogica': 'Evalúa el concepto de equivalencia.',
        'opciones': [
            ('A', '6/8', True, '', ''),
            ('B', '5/8', False, 'No mantiene la proporción.', 'Cambiar solo una parte de la fracción'),
            ('C', '3/8', False, 'Se alteró solo el denominador.', 'Modificar solo el denominador'),
            ('D', '7/8', False, 'No es equivalente.', 'Seleccionar una fracción cercana'),
        ],
    },
    {
        'enunciado': 'Si un carro recorre 180 km en 3 horas, su velocidad promedio es:',
        'grado': '8',
        'tema': 'Proporcionalidad',
        'competencia': 'Resolución de problemas',
        'dba': 'Relación entre distancia, tiempo y velocidad (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Velocidad = distancia/tiempo = 180/3 = 60 km/h.',
        'justificacion_pedagogica': 'Conecta proporcionalidad con una situación real.',
        'opciones': [
            ('A', '60 km/h', True, '', ''),
            ('B', '540 km/h', False, 'Se multiplicó en lugar de dividir.', 'Multiplicar en vez de dividir'),
            ('C', '30 km/h', False, 'Se dividió mal.', 'Error aritmético'),
            ('D', '183 km/h', False, 'Se sumaron magnitudes.', 'Confundir operación'),
        ],
    },
    {
        'enunciado': 'La probabilidad de obtener cara al lanzar una moneda equilibrada es:',
        'grado': '7',
        'tema': 'Probabilidad',
        'competencia': 'Interpretación de información',
        'dba': 'Cálculo de probabilidades simples (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Hay dos resultados equiprobables y uno favorable, por eso es 1/2.',
        'justificacion_pedagogica': 'Refuerza el concepto de espacio muestral simple.',
        'opciones': [
            ('A', '1/2', True, '', ''),
            ('B', '1/3', False, 'Se asumió un espacio muestral incorrecto.', 'Interpretación incorrecta del espacio muestral'),
            ('C', '2/1', False, 'Se invirtió la razón.', 'Invertir favorable y total'),
            ('D', '0', False, 'Se ignoró la posibilidad real del evento.', 'Negar el evento posible'),
        ],
    },
    {
        'enunciado': '¿Cuál es la solución del sistema x + y = 7 y x - y = 1?',
        'grado': '10',
        'tema': 'Sistemas de ecuaciones',
        'competencia': 'Razonamiento algebraico',
        'dba': 'Solución de sistemas lineales 2x2 (demostrativo)',
        'nivel_dificultad': 'alta',
        'explicacion': 'Al sumar las ecuaciones se obtiene 2x = 8, por tanto x = 4 y y = 3.',
        'justificacion_pedagogica': 'Mide el manejo de procedimientos de solución de sistemas.',
        'opciones': [
            ('A', '(4,3)', True, '', ''),
            ('B', '(3,4)', False, 'Se invirtieron los valores de x y y.', 'Intercambiar variables'),
            ('C', '(8,2)', False, 'No se completó correctamente el procedimiento.', 'No despejar tras sumar'),
            ('D', '(1,7)', False, 'Se tomaron los términos independientes como solución.', 'Leer mal el sistema'),
        ],
    },
    {
        'enunciado': 'Si f(x) = x², entonces f(-3) es:',
        'grado': '9',
        'tema': 'Funciones',
        'competencia': 'Razonamiento algebraico',
        'dba': 'Evaluación de funciones (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': '(-3)² = 9.',
        'justificacion_pedagogica': 'Permite revisar errores comunes con signos y potencias.',
        'opciones': [
            ('A', '-9', False, 'Se conservó el signo negativo por error.', 'Error con potencias de números negativos'),
            ('B', '9', True, '', ''),
            ('C', '6', False, 'Se multiplicó incorrectamente.', 'Error aritmético'),
            ('D', '3', False, 'Se confundió cuadrado con valor absoluto.', 'Confundir operación'),
        ],
    },
    {
        'enunciado': 'Un dado justo se lanza una vez. La probabilidad de sacar un número par es:',
        'grado': '8',
        'tema': 'Probabilidad',
        'competencia': 'Interpretación de información',
        'dba': 'Probabilidades simples con espacios muestrales finitos (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Los resultados pares son 2, 4 y 6: 3 de 6, es decir 1/2.',
        'justificacion_pedagogica': 'Fortalece el conteo de casos favorables.',
        'opciones': [
            ('A', '1/3', False, 'Se contaron mal los casos favorables.', 'Contar mal casos favorables'),
            ('B', '1/2', True, '', ''),
            ('C', '2/3', False, 'Se alteró el total de casos.', 'Error en el denominador'),
            ('D', '3', False, 'No se expresó como probabilidad.', 'No convertir a razón'),
        ],
    },
    {
        'enunciado': 'Al expandir (x + 2)² se obtiene:',
        'grado': '11',
        'tema': 'Álgebra',
        'competencia': 'Razonamiento algebraico',
        'dba': 'Productos notables (demostrativo)',
        'nivel_dificultad': 'alta',
        'explicacion': '(x + 2)² = x² + 4x + 4.',
        'justificacion_pedagogica': 'Permite verificar manejo de productos notables.',
        'opciones': [
            ('A', 'x² + 2x + 4', False, 'Faltó duplicar el producto.', 'Olvidar el término medio'),
            ('B', 'x² + 4x + 4', True, '', ''),
            ('C', 'x² + 4', False, 'Se omitió el término medio.', 'Eliminar término lineal'),
            ('D', 'x² + 8x + 4', False, 'Se duplicó mal el término medio.', 'Coeficiente mal calculado'),
        ],
    },
    {
        'enunciado': 'La mediana del conjunto 3, 7, 8, 12, 15 es:',
        'grado': '6',
        'tema': 'Estadística',
        'competencia': 'Interpretación de información',
        'dba': 'Cálculo de mediana en listas ordenadas (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'El dato central es 8.',
        'justificacion_pedagogica': 'Distingue medidas de tendencia central.',
        'opciones': [
            ('A', '7', False, 'Se eligió un dato cercano pero no el central.', 'Confundir posición central'),
            ('B', '8', True, '', ''),
            ('C', '9', False, 'Se promedió sin necesidad.', 'Confundir media con mediana'),
            ('D', '15', False, 'Se escogió el extremo.', 'Confundir mediana con máximo'),
        ],
    },
    {
        'enunciado': 'Si 5 cuadernos cuestan $20.000, entonces 1 cuaderno cuesta:',
        'grado': '6',
        'tema': 'Proporcionalidad',
        'competencia': 'Resolución de problemas',
        'dba': 'Razón unitaria en contextos cotidianos (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': '20.000 ÷ 5 = 4.000.',
        'justificacion_pedagogica': 'Trabaja el paso de razón global a razón unitaria.',
        'opciones': [
            ('A', '$4.000', True, '', ''),
            ('B', '$5.000', False, 'Se estimó sin dividir correctamente.', 'Estimación sin cálculo exacto'),
            ('C', '$25.000', False, 'Se sumó en lugar de dividir.', 'Operación incorrecta'),
            ('D', '$100.000', False, 'Se multiplicó en vez de dividir.', 'Multiplicar en vez de dividir'),
        ],
    },
]

RECURSOS_DEMO = [
    {
        'titulo': 'Introducción a los porcentajes',
        'url': 'https://www.youtube.com/watch?v=3nK1tqB3vW8',
        'tipo': 'video',
        'tema': 'Porcentajes',
        'grado': '10',
        'autor': 'Canal educativo (recurso demostrativo)',
        'descripcion': 'Recurso externo para reforzar el cálculo de porcentajes.',
    },
    {
        'titulo': 'Área de triángulos',
        'url': 'https://www.youtube.com/watch?v=5ch3WkK-8Pg',
        'tipo': 'video',
        'tema': 'Geometría',
        'grado': '10',
        'autor': 'Canal educativo (recurso demostrativo)',
        'descripcion': 'Explicación sencilla sobre el cálculo del área.',
    },
    {
        'titulo': 'Sistemas de ecuaciones',
        'url': 'https://www.youtube.com/watch?v=qA0uMwdm0vY',
        'tipo': 'video',
        'tema': 'Sistemas de ecuaciones',
        'grado': '10',
        'autor': 'Canal educativo (recurso demostrativo)',
        'descripcion': 'Apoyo complementario de práctica.',
    },
]


def _cargar_preguntas(db: Session, preguntas: list[dict]):
    for pregunta_data in preguntas:
        datos = dict(pregunta_data)
        opciones = datos.pop('opciones')
        pregunta = Pregunta(**datos)
        db.add(pregunta)
        db.flush()

        for identificador, texto, es_correcta, explicacion_distractor, tipo_error in opciones:
            db.add(
                OpcionRespuesta(
                    pregunta_id=pregunta.id,
                    identificador=identificador,
                    texto=texto,
                    es_correcta=es_correcta,
                    explicacion_distractor=explicacion_distractor,
                    tipo_error=tipo_error,
                )
            )


def _cargar_contenido_sexto(db: Session):
    """Carga la ruta de microaprendizaje, actividades, insignias y misiones."""
    # Los recursos del seed anterior quedaron con grado por defecto; se retiran
    # para no mezclarlos con la biblioteca del módulo de 6°.
    db.query(RecursoMultimedia).filter(
        RecursoMultimedia.grado == '6', RecursoMultimedia.autor == ''
    ).delete()

    for recurso in RECURSOS_SEXTO:
        db.add(RecursoMultimedia(tipo='video', grado='6', **recurso))

    for leccion in LECCIONES_SEXTO:
        db.add(Leccion(grado='6', **leccion))

    for actividad in ACTIVIDADES_SEXTO:
        datos = dict(actividad)
        datos['datos'] = json.dumps(datos['datos'], ensure_ascii=False)
        db.add(ActividadInteractiva(grado='6', **datos))

    for insignia in INSIGNIAS:
        db.add(Insignia(**insignia))

    for mision in MISIONES:
        db.add(Mision(**mision))


def sincronizar_recursos_sexto(db: Session):
    """Actualiza la biblioteca de videos de 6° con los enlaces vigentes.

    Es idempotente y se ejecuta siempre al levantar la app: vuelve a crear las
    filas de recursos de grado 6° a partir de RECURSOS_SEXTO para que una
    instalación existente reciba los enlaces definitivos sin perder usuarios ni
    progreso. Los recursos no se referencian por clave foránea, por lo que
    recrearlos es seguro.
    """
    db.query(RecursoMultimedia).filter(
        RecursoMultimedia.grado == '6', RecursoMultimedia.tipo == 'video'
    ).delete(synchronize_session=False)

    for recurso in RECURSOS_SEXTO:
        db.add(RecursoMultimedia(tipo='video', grado='6', **recurso))

    db.commit()


def poblar_datos_iniciales(db: Session):
    """Carga información demostrativa únicamente si la base está vacía."""
    if db.query(Usuario).first():
        return

    usuario_demo = Usuario(
        nombre='Estudiante Demo',
        correo='estudiante@numbyte.com',
        contrasena_hash=obtener_hash_contrasena('Numbyte2026*'),
        grado='10',
    )
    db.add(usuario_demo)

    for recurso in RECURSOS_DEMO:
        db.add(RecursoMultimedia(**recurso))

    # Las preguntas de grado 6° provienen del módulo completo de contenido_sexto.
    preguntas_otros_grados = [item for item in PREGUNTAS_DEMO if item['grado'] != '6']
    _cargar_preguntas(db, preguntas_otros_grados)
    _cargar_preguntas(db, [{'grado': '6', **item} for item in PREGUNTAS_SEXTO])

    _cargar_contenido_sexto(db)

    db.commit()


def poblar_contenido_sexto(db: Session):
    """Siembra el módulo de 6° en bases que ya existían (idempotente).

    Permite actualizar una instalación anterior sin borrar los usuarios ya
    registrados: solo actúa cuando el módulo todavía no está cargado.
    """
    if db.query(Leccion).first():
        return

    # Retira las preguntas de 6° del seed anterior que no tengan respuestas
    # registradas, para evitar duplicados con el módulo nuevo.
    ids_con_respuestas = {
        fila[0] for fila in db.query(RespuestaUsuario.pregunta_id).distinct().all()
    }
    preguntas_antiguas = db.query(Pregunta).filter(Pregunta.grado == '6').all()
    for pregunta in preguntas_antiguas:
        if pregunta.id in ids_con_respuestas:
            continue
        db.query(OpcionRespuesta).filter(OpcionRespuesta.pregunta_id == pregunta.id).delete()
        db.delete(pregunta)

    _cargar_preguntas(db, [{'grado': '6', **item} for item in PREGUNTAS_SEXTO])
    _cargar_contenido_sexto(db)
    db.commit()
