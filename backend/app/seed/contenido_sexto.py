"""Contenido demostrativo del módulo de GRADO 6°.

IMPORTANTE (honestidad académica):
- Los textos, ejemplos y preguntas son material DEMOSTRATIVO elaborado para el
  prototipo. NO son contenido oficial del ICFES ni del Ministerio de Educación.
- Las descripciones de competencias y DBA son genéricas y están marcadas como
  "(demostrativo)": deben reemplazarse por la referencia oficial verificada.
- Los videos apuntan a búsquedas sugeridas de YouTube (enlaces externos, no se
  descarga ni redistribuye contenido). El docente debe reemplazarlos por el
  enlace específico validado.
"""

# --- Temas del módulo de 6° ---
TEMAS_SEXTO = [
    'Números naturales',
    'Fracciones',
    'Porcentajes',
    'Proporcionalidad',
    'Estadística',
    'Geometría',
    'Probabilidad',
]


LECCIONES_SEXTO = [
    {
        'tema': 'Números naturales',
        'titulo': 'Operaciones con números naturales',
        'subtitulo': 'Suma, resta, multiplicación y división en el orden correcto',
        'explicacion': (
            'Los números naturales son los que usamos para contar: 0, 1, 2, 3...\n'
            'Cuando en una expresión aparecen varias operaciones, se resuelven en este orden:\n'
            '1) Potencias y raíces.\n'
            '2) Multiplicaciones y divisiones (de izquierda a derecha).\n'
            '3) Sumas y restas (de izquierda a derecha).\n'
            'Si hay paréntesis, primero se resuelve lo que está dentro de ellos.'
        ),
        'ejemplo': (
            'Resolvamos 12 + 3 × 4:\n'
            'Primero la multiplicación: 3 × 4 = 12.\n'
            'Luego la suma: 12 + 12 = 24.\n'
            'Resultado: 24. Si se hubiera sumado primero habría dado 60, que es un error común.'
        ),
        'orden': 1,
    },
    {
        'tema': 'Fracciones',
        'titulo': 'Fracciones equivalentes',
        'subtitulo': 'La misma parte del entero escrita de otra forma',
        'explicacion': (
            'Una fracción representa una parte de un entero. En 3/4, el 3 es el numerador '
            '(partes que tomo) y el 4 el denominador (partes en que divido el entero).\n'
            'Dos fracciones son equivalentes si representan la misma cantidad. Para obtenerlas, '
            'se multiplica o se divide el numerador y el denominador por el mismo número.'
        ),
        'ejemplo': (
            '¿3/4 y 6/8 son equivalentes?\n'
            'Multiplicamos el numerador y el denominador de 3/4 por 2: 3 × 2 = 6 y 4 × 2 = 8.\n'
            'Se obtiene 6/8. Por lo tanto, 3/4 = 6/8: son equivalentes.'
        ),
        'orden': 2,
    },
    {
        'tema': 'Porcentajes',
        'titulo': 'El porcentaje como parte de 100',
        'subtitulo': 'Descuentos y aumentos en la vida diaria',
        'explicacion': (
            'Un porcentaje es una forma de comparar una parte con 100. El 25% significa 25 de cada 100, '
            'es decir, 25/100 = 0,25.\n'
            'Para calcular un porcentaje de una cantidad, se multiplica la cantidad por el porcentaje '
            'y se divide entre 100.'
        ),
        'ejemplo': (
            'Una camiseta cuesta $48.000 y tiene 25% de descuento.\n'
            'Descuento = 48.000 × 25 ÷ 100 = 12.000.\n'
            'Precio final = 48.000 − 12.000 = $36.000.'
        ),
        'orden': 3,
    },
    {
        'tema': 'Proporcionalidad',
        'titulo': 'Razón unitaria',
        'subtitulo': 'Cuánto vale una sola unidad',
        'explicacion': (
            'Una razón compara dos cantidades. La razón unitaria indica cuánto corresponde a una sola unidad.\n'
            'Se calcula dividiendo el total entre la cantidad de unidades.'
        ),
        'ejemplo': (
            'Si 5 cuadernos cuestan $20.000, ¿cuánto cuesta 1?\n'
            '20.000 ÷ 5 = 4.000. Entonces un cuaderno cuesta $4.000.'
        ),
        'orden': 4,
    },
    {
        'tema': 'Estadística',
        'titulo': 'Media, mediana y moda',
        'subtitulo': 'Formas de resumir un conjunto de datos',
        'explicacion': (
            'Media: se suman todos los datos y se dividen entre cuántos hay.\n'
            'Mediana: el dato que queda en el centro cuando los ordenamos de menor a mayor.\n'
            'Moda: el dato que más se repite.'
        ),
        'ejemplo': (
            'Para los datos 2, 4, 4, 6:\n'
            'Media = (2 + 4 + 4 + 6) ÷ 4 = 16 ÷ 4 = 4.\n'
            'Mediana = 4 (promedio de los dos centrales: 4 y 4).\n'
            'Moda = 4 (es el que más se repite).'
        ),
        'orden': 5,
    },
    {
        'tema': 'Geometría',
        'titulo': 'Perímetro y área',
        'subtitulo': 'Contorno y superficie de las figuras',
        'explicacion': (
            'El perímetro es la suma de todos los lados (el contorno de la figura).\n'
            'El área es la superficie que ocupa la figura.\n'
            'Rectángulo: Área = base × altura.\n'
            'Triángulo: Área = base × altura ÷ 2.'
        ),
        'ejemplo': (
            'Un triángulo tiene base 8 cm y altura 5 cm.\n'
            'Área = 8 × 5 ÷ 2 = 40 ÷ 2 = 20 cm².'
        ),
        'orden': 6,
    },
    {
        'tema': 'Probabilidad',
        'titulo': 'Probabilidad de un evento',
        'subtitulo': 'Qué tan posible es que ocurra algo',
        'explicacion': (
            'La probabilidad mide qué tan posible es un resultado. Se calcula así:\n'
            'Probabilidad = casos favorables ÷ casos posibles.\n'
            'Su valor va de 0 (imposible) a 1 (seguro).'
        ),
        'ejemplo': (
            'Al lanzar una moneda, ¿cuál es la probabilidad de obtener cara?\n'
            'Casos favorables = 1 (cara). Casos posibles = 2 (cara o sello).\n'
            'Probabilidad = 1/2.'
        ),
        'orden': 7,
    },
]


PREGUNTAS_SEXTO = [
    # --- Tema: Números naturales ---
    {
        'enunciado': '¿Cuál es el resultado de 12 + 3 × 4?',
        'tema': 'Números naturales',
        'competencia': 'Razonamiento numérico',
        'dba': 'Uso de las operaciones básicas y su jerarquía (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Primero se resuelve la multiplicación (3 × 4 = 12) y luego la suma (12 + 12 = 24).',
        'justificacion_pedagogica': 'Verifica si el estudiante respeta la jerarquía de las operaciones.',
        'opciones': [
            ('A', '24', True, '', ''),
            ('B', '60', False, 'Se sumó primero 12 + 3 y luego se multiplicó por 4.', 'Ignorar la jerarquía de operaciones'),
            ('C', '48', False, 'Se multiplicó 12 × 4.', 'Aplicar una operación que no corresponde'),
            ('D', '19', False, 'Se sumó todo sin respetar el orden.', 'Resolver de izquierda a derecha sin analizar'),
        ],
    },
    {
        'enunciado': 'El resultado de 100 − 4 × 5 es:',
        'tema': 'Números naturales',
        'competencia': 'Razonamiento numérico',
        'dba': 'Jerarquía de operaciones con números naturales (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Primero 4 × 5 = 20; luego 100 − 20 = 80.',
        'justificacion_pedagogica': 'Refuerza el orden de las operaciones.',
        'opciones': [
            ('A', '80', True, '', ''),
            ('B', '480', False, 'Se multiplicó 100 − 4 por 5.', 'Error al agrupar operaciones'),
            ('C', '20', False, 'Se omitió la resta.', 'Omitir una operación de la expresión'),
            ('D', '96', False, 'Se restó 4 y luego se multiplicó por 5.', 'Orden de operaciones incorrecto'),
        ],
    },
    {
        'enunciado': 'Una tienda vende 8 cajas con 12 lápices cada una. ¿Cuántos lápices hay en total?',
        'tema': 'Números naturales',
        'competencia': 'Resolución de problemas',
        'dba': 'Multiplicación en contextos de agrupación (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Se multiplica 8 × 12 = 96.',
        'justificacion_pedagogica': 'Conecta la multiplicación con situaciones reales.',
        'opciones': [
            ('A', '96', True, '', ''),
            ('B', '20', False, 'Se sumó 8 + 12.', 'Confundir multiplicación con suma'),
            ('C', '108', False, 'Se calculó 9 × 12.', 'Error aritmético'),
            ('D', '84', False, 'Se calculó 7 × 12.', 'Error aritmético'),
        ],
    },
    # --- Tema: Fracciones ---
    {
        'enunciado': '¿Cuál fracción es equivalente a 3/4?',
        'tema': 'Fracciones',
        'competencia': 'Razonamiento numérico',
        'dba': 'Fracciones equivalentes (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Multiplicando numerador y denominador de 3/4 por 2 se obtiene 6/8.',
        'justificacion_pedagogica': 'Evalúa la comprensión de equivalencia.',
        'opciones': [
            ('A', '6/8', True, '', ''),
            ('B', '5/8', False, 'Solo se cambió el numerador.', 'Modificar solo una parte de la fracción'),
            ('C', '3/8', False, 'Solo se cambió el denominador.', 'Modificar solo el denominador'),
            ('D', '4/3', False, 'Se invirtieron numerador y denominador.', 'Confundir fracción con su inversa'),
        ],
    },
    {
        'enunciado': 'Al sumar 1/5 + 2/5 el resultado es:',
        'tema': 'Fracciones',
        'competencia': 'Razonamiento numérico',
        'dba': 'Adición de fracciones con igual denominador (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Con igual denominador se suman los numeradores: 1 + 2 = 3, quedando 3/5.',
        'justificacion_pedagogica': 'Verifica la suma de fracciones homogéneas.',
        'opciones': [
            ('A', '3/5', True, '', ''),
            ('B', '3/10', False, 'Se sumaron también los denominadores.', 'Sumar denominadores'),
            ('C', '2/5', False, 'Se restó en vez de sumar.', 'Operación incorrecta'),
            ('D', '1/5', False, 'Se omitió una de las fracciones.', 'Omitir un sumando'),
        ],
    },
    {
        'enunciado': 'Si una torta se divide en 8 partes iguales y se comen 3, ¿qué fracción se comió?',
        'tema': 'Fracciones',
        'competencia': 'Interpretación de información',
        'dba': 'Representación de fracciones en contextos cotidianos (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Se comieron 3 de 8 partes: 3/8.',
        'justificacion_pedagogica': 'Relaciona la fracción con una situación concreta.',
        'opciones': [
            ('A', '3/8', True, '', ''),
            ('B', '8/3', False, 'Se invirtió la fracción.', 'Invertir numerador y denominador'),
            ('C', '3/5', False, 'Se tomó el total como las partes restantes.', 'Confundir el total del entero'),
            ('D', '5/8', False, 'Se contaron las partes que quedaron.', 'Confundir lo comido con lo que resta'),
        ],
    },
    # --- Tema: Porcentajes ---
    {
        'enunciado': '¿Cuánto es el 25% de 48.000?',
        'tema': 'Porcentajes',
        'competencia': 'Resolución de problemas',
        'dba': 'Cálculo de porcentajes (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': '25% equivale a una cuarta parte: 48.000 ÷ 4 = 12.000.',
        'justificacion_pedagogica': 'Evalúa el cálculo de porcentajes sencillos.',
        'opciones': [
            ('A', '12.000', True, '', ''),
            ('B', '24.000', False, 'Se calculó el 50%.', 'Confundir el porcentaje'),
            ('C', '36.000', False, 'Se calculó el precio final, no el descuento.', 'Responder otra pregunta'),
            ('D', '4.800', False, 'Se calculó el 10%.', 'Error en el porcentaje aplicado'),
        ],
    },
    {
        'enunciado': 'Un pantalón cuesta $60.000 con 10% de descuento. El precio final es:',
        'tema': 'Porcentajes',
        'competencia': 'Resolución de problemas',
        'dba': 'Aplicación de descuentos porcentuales (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Descuento = 60.000 × 10 ÷ 100 = 6.000. Precio final = 60.000 − 6.000 = 54.000.',
        'justificacion_pedagogica': 'Integra porcentaje y resta en una situación real.',
        'opciones': [
            ('A', '$54.000', True, '', ''),
            ('B', '$6.000', False, 'Se dio el descuento, no el precio final.', 'Confundir descuento con precio final'),
            ('C', '$66.000', False, 'Se sumó en lugar de restar.', 'Confundir descuento con recargo'),
            ('D', '$50.000', False, 'Se restó un valor arbitrario.', 'Cálculo incorrecto del porcentaje'),
        ],
    },
    {
        'enunciado': 'El 50% de 90 es:',
        'tema': 'Porcentajes',
        'competencia': 'Razonamiento numérico',
        'dba': 'Porcentajes equivalentes a fracciones conocidas (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'El 50% es la mitad: 90 ÷ 2 = 45.',
        'justificacion_pedagogica': 'Refuerza el reconocimiento de porcentajes básicos.',
        'opciones': [
            ('A', '45', True, '', ''),
            ('B', '9', False, 'Se calculó el 10%.', 'Confundir el porcentaje'),
            ('C', '50', False, 'Se confundió el porcentaje con el resultado.', 'Confundir porcentaje con cantidad'),
            ('D', '180', False, 'Se duplicó la cantidad.', 'Operación inversa'),
        ],
    },
    # --- Tema: Proporcionalidad ---
    {
        'enunciado': 'Si 5 cuadernos cuestan $20.000, ¿cuánto cuesta 1 cuaderno?',
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
    {
        'enunciado': 'Un carro recorre 180 km en 3 horas. Su velocidad promedio es:',
        'tema': 'Proporcionalidad',
        'competencia': 'Resolución de problemas',
        'dba': 'Relación entre distancia, tiempo y velocidad (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Velocidad = distancia ÷ tiempo = 180 ÷ 3 = 60 km/h.',
        'justificacion_pedagogica': 'Conecta proporcionalidad con una situación real.',
        'opciones': [
            ('A', '60 km/h', True, '', ''),
            ('B', '540 km/h', False, 'Se multiplicó en lugar de dividir.', 'Multiplicar en vez de dividir'),
            ('C', '30 km/h', False, 'Se dividió mal.', 'Error aritmético'),
            ('D', '177 km/h', False, 'Se restaron las magnitudes.', 'Confundir la operación'),
        ],
    },
    {
        'enunciado': 'En una receta, 2 tazas de harina rinden 12 galletas. ¿Cuántas galletas rinden 3 tazas?',
        'tema': 'Proporcionalidad',
        'competencia': 'Resolución de problemas',
        'dba': 'Proporcionalidad directa (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Una taza rinde 6 galletas (12 ÷ 2). Entonces 3 tazas rinden 18.',
        'justificacion_pedagogica': 'Evalúa la proporcionalidad directa en un contexto cotidiano.',
        'opciones': [
            ('A', '18', True, '', ''),
            ('B', '15', False, 'Se sumó una taza extra sin proporción.', 'Sumar sin proporcionalidad'),
            ('C', '24', False, 'Se duplicó sin justificar.', 'Duplicar incorrectamente'),
            ('D', '13', False, 'Se sumó 12 + 1.', 'Operación incorrecta'),
        ],
    },
    # --- Tema: Estadística ---
    {
        'enunciado': 'La media de los datos 2, 4, 6, 8 es:',
        'tema': 'Estadística',
        'competencia': 'Interpretación de información',
        'dba': 'Medidas de tendencia central (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'La suma es 20 y se divide entre 4, dando 5.',
        'justificacion_pedagogica': 'Refuerza el concepto de promedio aritmético.',
        'opciones': [
            ('A', '5', True, '', ''),
            ('B', '4', False, 'Se eligió un dato, no el promedio.', 'Confundir dato con promedio'),
            ('C', '10', False, 'Se dividió incorrectamente.', 'Error al dividir'),
            ('D', '20', False, 'Se sumó pero no se promedió.', 'Olvidar dividir entre la cantidad de datos'),
        ],
    },
    {
        'enunciado': 'La mediana del conjunto 3, 7, 8, 12, 15 es:',
        'tema': 'Estadística',
        'competencia': 'Interpretación de información',
        'dba': 'Cálculo de la mediana (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Con los datos ordenados, el valor central es 8.',
        'justificacion_pedagogica': 'Distingue medidas de tendencia central.',
        'opciones': [
            ('A', '8', True, '', ''),
            ('B', '7', False, 'Se eligió un dato cercano pero no el central.', 'Confundir la posición central'),
            ('C', '9', False, 'Se promedió sin necesidad.', 'Confundir media con mediana'),
            ('D', '15', False, 'Se escogió el valor máximo.', 'Confundir mediana con máximo'),
        ],
    },
    {
        'enunciado': 'En los datos 3, 5, 5, 7, 5, 9, la moda es:',
        'tema': 'Estadística',
        'competencia': 'Interpretación de información',
        'dba': 'Cálculo de la moda (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'El dato que más se repite es 5 (aparece tres veces).',
        'justificacion_pedagogica': 'Identifica el dato más frecuente.',
        'opciones': [
            ('A', '5', True, '', ''),
            ('B', '3', False, 'Es el primer dato, no el más repetido.', 'Confundir orden con frecuencia'),
            ('C', '9', False, 'Es el mayor, no el más repetido.', 'Confundir frecuencia con valor'),
            ('D', '6', False, 'Se confundió la cantidad de datos con la moda.', 'Confundir conteo con moda'),
        ],
    },
    # --- Tema: Geometría ---
    {
        'enunciado': 'Un triángulo tiene base 8 cm y altura 5 cm. Su área es:',
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
        'enunciado': 'El perímetro de un cuadrado de lado 6 cm es:',
        'tema': 'Geometría',
        'competencia': 'Representación y medición',
        'dba': 'Cálculo de perímetros (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'El cuadrado tiene 4 lados iguales: 4 × 6 = 24 cm.',
        'justificacion_pedagogica': 'Refuerza el concepto de perímetro.',
        'opciones': [
            ('A', '24 cm', True, '', ''),
            ('B', '12 cm', False, 'Se sumaron solo dos lados.', 'Contar incompleto de lados'),
            ('C', '36 cm', False, 'Se calculó el área en vez del perímetro.', 'Confundir área con perímetro'),
            ('D', '6 cm', False, 'Se tomó un solo lado.', 'Confundir lado con perímetro'),
        ],
    },
    {
        'enunciado': 'El área de un rectángulo de base 9 cm y altura 4 cm es:',
        'tema': 'Geometría',
        'competencia': 'Representación y medición',
        'dba': 'Área de rectángulos (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Área = base × altura = 9 × 4 = 36 cm².',
        'justificacion_pedagogica': 'Aplica la fórmula del área del rectángulo.',
        'opciones': [
            ('A', '36 cm²', True, '', ''),
            ('B', '13 cm²', False, 'Se sumó base + altura.', 'Confundir área con perímetro'),
            ('C', '26 cm²', False, 'Se calculó el perímetro.', 'Confundir área con perímetro'),
            ('D', '18 cm²', False, 'Se dividió entre 2 sin razón.', 'Aplicar fórmula de triángulo'),
        ],
    },
    # --- Tema: Probabilidad ---
    {
        'enunciado': 'Al lanzar una moneda equilibrada, la probabilidad de obtener cara es:',
        'tema': 'Probabilidad',
        'competencia': 'Interpretación de información',
        'dba': 'Probabilidades simples (demostrativo)',
        'nivel_dificultad': 'baja',
        'explicacion': 'Hay 2 resultados posibles y 1 favorable: 1/2.',
        'justificacion_pedagogica': 'Refuerza el concepto de espacio muestral simple.',
        'opciones': [
            ('A', '1/2', True, '', ''),
            ('B', '1/3', False, 'Se supuso un espacio muestral incorrecto.', 'Interpretación incorrecta del espacio muestral'),
            ('C', '2/1', False, 'Se invirtió la razón.', 'Invertir favorable y total'),
            ('D', '0', False, 'Se negó un evento posible.', 'Negar el evento posible'),
        ],
    },
    {
        'enunciado': 'Un dado justo se lanza una vez. La probabilidad de sacar un número par es:',
        'tema': 'Probabilidad',
        'competencia': 'Interpretación de información',
        'dba': 'Probabilidades con espacios muestrales finitos (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Los pares son 2, 4 y 6: 3 de 6, es decir 1/2.',
        'justificacion_pedagogica': 'Fortalece el conteo de casos favorables.',
        'opciones': [
            ('A', '1/2', True, '', ''),
            ('B', '1/3', False, 'Se contaron mal los casos favorables.', 'Contar mal los casos favorables'),
            ('C', '2/3', False, 'Se alteró el total de casos.', 'Error en el denominador'),
            ('D', '3', False, 'No se expresó como probabilidad.', 'No convertir a razón'),
        ],
    },
    {
        'enunciado': 'En una bolsa hay 4 bolas rojas y 1 azul. La probabilidad de sacar una azul es:',
        'tema': 'Probabilidad',
        'competencia': 'Interpretación de información',
        'dba': 'Probabilidad de eventos simples (demostrativo)',
        'nivel_dificultad': 'media',
        'explicacion': 'Hay 5 bolas en total y 1 favorable: 1/5.',
        'justificacion_pedagogica': 'Evalúa el conteo del total de casos posibles.',
        'opciones': [
            ('A', '1/5', True, '', ''),
            ('B', '1/4', False, 'Se usó solo la cantidad de rojas.', 'Error en el total de casos'),
            ('C', '4/5', False, 'Se calculó la probabilidad de la roja.', 'Responder el evento contrario'),
            ('D', '5', False, 'No se expresó como probabilidad.', 'No convertir a razón'),
        ],
    },
]


RECURSOS_SEXTO = [
    {
        'tema': 'Números naturales',
        'titulo': 'Jerarquía de las operaciones',
        'url': 'https://www.youtube.com/watch?v=ozqKapcHyvw',
        'autor': 'Profe Jared (YouTube)',
        'descripcion': 'Video embebido que explica el orden correcto para resolver operaciones combinadas.',
        'solo_plus': False,
    },
    {
        'tema': 'Fracciones',
        'titulo': 'Fracciones equivalentes',
        'url': 'https://www.youtube.com/watch?v=osePKL39EBo',
        'autor': 'Daniel Carreón (YouTube)',
        'descripcion': 'Video embebido para reconocer y obtener fracciones equivalentes paso a paso.',
        'solo_plus': False,
    },
    {
        'tema': 'Porcentajes',
        'titulo': 'Cálculo de porcentajes',
        'url': 'https://www.youtube.com/watch?v=9CwbwpXNx0M',
        'autor': 'Khan Academy en Español (YouTube)',
        'descripcion': 'Video embebido que explica el significado de porcentaje con ejemplos visuales.',
        'solo_plus': False,
    },
    {
        'tema': 'Proporcionalidad',
        'titulo': 'Proporcionalidad y razón unitaria',
        'url': 'https://www.youtube.com/watch?v=6bNN0I4GwDQ',
        'autor': '@prende_mx (YouTube)',
        'descripcion': 'Recurso exclusivo del plan Plus (demostrativo). Clase de 6° sobre proporcionalidad.',
        'solo_plus': True,
    },
    {
        'tema': 'Estadística',
        'titulo': 'Media, mediana y moda',
        'url': 'https://www.youtube.com/watch?v=KFB5mWICDeQ',
        'autor': 'Daniel Carreón (YouTube)',
        'descripcion': 'Video embebido sobre las medidas de tendencia central para principiantes.',
        'solo_plus': False,
    },
    {
        'tema': 'Geometría',
        'titulo': 'Área y perímetro de figuras planas',
        'url': 'https://www.youtube.com/watch?v=wYNvY_bOGdc',
        'autor': 'Daniel Carreón (YouTube)',
        'descripcion': 'Recurso exclusivo del plan Plus (demostrativo). Áreas y perímetros explicados paso a paso.',
        'solo_plus': True,
    },
    {
        'tema': 'Probabilidad',
        'titulo': 'Probabilidad para principiantes',
        'url': 'https://www.youtube.com/watch?v=WeeEE8o1aqM',
        'autor': 'Daniel Carreón (YouTube)',
        'descripcion': 'Video embebido que introduce la probabilidad con ejemplos cotidianos.',
        'solo_plus': False,
    },
]


ACTIVIDADES_SEXTO = [
    {
        'tema': 'Números naturales',
        'titulo': 'Clasifica el resultado',
        'instrucciones': 'Haz clic en cada resultado y luego en la columna donde debe ir: PAR o IMPAR.',
        'tipo': 'clasificar',
        'datos': {
            'categorias': [{'id': 'par', 'nombre': 'PAR'}, {'id': 'impar', 'nombre': 'IMPAR'}],
            'elementos': [
                {'id': 'e1', 'texto': '6 × 4 = 24', 'categoria': 'par'},
                {'id': 'e2', 'texto': '7 + 8 = 15', 'categoria': 'impar'},
                {'id': 'e3', 'texto': '9 × 3 = 27', 'categoria': 'impar'},
                {'id': 'e4', 'texto': '12 + 6 = 18', 'categoria': 'par'},
            ],
        },
        'solo_plus': False,
    },
    {
        'tema': 'Fracciones',
        'titulo': 'Elige la fracción equivalente',
        'instrucciones': 'Haz clic en la fracción que es equivalente a la indicada.',
        'tipo': 'seleccionar',
        'datos': {
            'pregunta': '¿Cuál fracción es equivalente a 2/3?',
            'opciones': [
                {'id': 'o1', 'texto': '4/6', 'correcta': True},
                {'id': 'o2', 'texto': '3/4', 'correcta': False},
                {'id': 'o3', 'texto': '2/6', 'correcta': False},
                {'id': 'o4', 'texto': '6/2', 'correcta': False},
            ],
        },
        'solo_plus': False,
    },
    {
        'tema': 'Porcentajes',
        'titulo': 'Calcula y clasifica',
        'instrucciones': 'Haz clic en cada expresión y luego en el resultado correcto.',
        'tipo': 'clasificar',
        'datos': {
            'categorias': [{'id': 'c50', 'nombre': '50'}, {'id': 'c25', 'nombre': '25'}, {'id': 'c10', 'nombre': '10'}],
            'elementos': [
                {'id': 'p1', 'texto': '50% de 100', 'categoria': 'c50'},
                {'id': 'p2', 'texto': '10% de 250', 'categoria': 'c25'},
                {'id': 'p3', 'texto': '20% de 50', 'categoria': 'c10'},
            ],
        },
        'solo_plus': False,
    },
    {
        'tema': 'Proporcionalidad',
        'titulo': 'Empareja precio y cantidad',
        'instrucciones': 'Haz clic en cada situación y luego en su razón unitaria correcta.',
        'tipo': 'clasificar',
        'datos': {
            'categorias': [{'id': 'r4000', 'nombre': '$4.000'}, {'id': 'r2000', 'nombre': '$2.000'}],
            'elementos': [
                {'id': 'r1', 'texto': '5 cuadernos por $20.000', 'categoria': 'r4000'},
                {'id': 'r2', 'texto': '4 jugos por $8.000', 'categoria': 'r2000'},
            ],
        },
        'solo_plus': False,
    },
    {
        'tema': 'Estadística',
        'titulo': 'Clasifica la medida',
        'instrucciones': 'Haz clic en cada definición y luego en la medida que le corresponde.',
        'tipo': 'clasificar',
        'datos': {
            'categorias': [
                {'id': 'media', 'nombre': 'Media'},
                {'id': 'mediana', 'nombre': 'Mediana'},
                {'id': 'moda', 'nombre': 'Moda'},
            ],
            'elementos': [
                {'id': 's1', 'texto': 'Dato que más se repite', 'categoria': 'moda'},
                {'id': 's2', 'texto': 'Suma de los datos dividida entre su cantidad', 'categoria': 'media'},
                {'id': 's3', 'texto': 'Dato central al ordenar', 'categoria': 'mediana'},
            ],
        },
        'solo_plus': True,
    },
    {
        'tema': 'Geometría',
        'titulo': 'Área o perímetro',
        'instrucciones': 'Haz clic en cada situación y luego en si pide ÁREA o PERÍMETRO.',
        'tipo': 'clasificar',
        'datos': {
            'categorias': [{'id': 'area', 'nombre': 'Área'}, {'id': 'perimetro', 'nombre': 'Perímetro'}],
            'elementos': [
                {'id': 'g1', 'texto': 'Cantidad de césped para cubrir un parque', 'categoria': 'area'},
                {'id': 'g2', 'texto': 'Cerca para rodear un terreno', 'categoria': 'perimetro'},
                {'id': 'g3', 'texto': 'Pintura para cubrir una pared', 'categoria': 'area'},
            ],
        },
        'solo_plus': False,
    },
    {
        'tema': 'Probabilidad',
        'titulo': 'Seguro, posible o imposible',
        'instrucciones': 'Haz clic en cada evento y luego en la categoría que le corresponde.',
        'tipo': 'clasificar',
        'datos': {
            'categorias': [
                {'id': 'seguro', 'nombre': 'Seguro'},
                {'id': 'posible', 'nombre': 'Posible'},
                {'id': 'imposible', 'nombre': 'Imposible'},
            ],
            'elementos': [
                {'id': 'pr1', 'texto': 'Sacar un número menor que 7 en un dado', 'categoria': 'seguro'},
                {'id': 'pr2', 'texto': 'Sacar un 3 en un dado', 'categoria': 'posible'},
                {'id': 'pr3', 'texto': 'Sacar un 9 en un dado', 'categoria': 'imposible'},
            ],
        },
        'solo_plus': True,
    },
]


INSIGNIAS = [
    {'codigo': 'primer_paso', 'nombre': 'Primer paso', 'descripcion': 'Creaste tu cuenta en NUMBYTE.', 'icono': '🚀', 'puntos_otorgados': 10, 'solo_plus': False},
    {'codigo': 'explorador', 'nombre': 'Explorador', 'descripcion': 'Completaste tu primera lección.', 'icono': '🧭', 'puntos_otorgados': 20, 'solo_plus': False},
    {'codigo': 'fraccionista', 'nombre': 'Maestro de fracciones', 'descripcion': 'Lograste el 100% en un tema.', 'icono': '🥧', 'puntos_otorgados': 30, 'solo_plus': False},
    {'codigo': 'constante', 'nombre': 'Constante', 'descripcion': 'Mantuviste una racha de 3 días.', 'icono': '🔥', 'puntos_otorgados': 40, 'solo_plus': False},
    {'codigo': 'calculadora', 'nombre': 'Calculadora veloz', 'descripcion': 'Obtuviste 100% en un simulacro.', 'icono': '⚡', 'puntos_otorgados': 60, 'solo_plus': False},
    {'codigo': 'sabio', 'nombre': 'Sabio de sexto', 'descripcion': 'Alcanzaste el nivel 5.', 'icono': '🎓', 'puntos_otorgados': 80, 'solo_plus': False},
    {'codigo': 'coleccionista', 'nombre': 'Coleccionista', 'descripcion': 'Reuniste 5 insignias.', 'icono': '🏅', 'puntos_otorgados': 100, 'solo_plus': False},
    {'codigo': 'plus_oro', 'nombre': 'Membresía Plus', 'descripcion': 'Activaste el plan Plus.', 'icono': '💎', 'puntos_otorgados': 50, 'solo_plus': True},
]


MISIONES = [
    {'codigo': 'mision_correctas_10', 'titulo': 'Diez aciertos', 'descripcion': 'Responde 10 preguntas correctas.', 'tipo': 'correctas', 'meta': 10, 'puntos': 50, 'monedas': 20, 'solo_plus': False},
    {'codigo': 'mision_lecciones_3', 'titulo': 'Aprende 3 temas', 'descripcion': 'Completa 3 lecciones del módulo de 6°.', 'tipo': 'lecciones', 'meta': 3, 'puntos': 60, 'monedas': 25, 'solo_plus': False},
    {'codigo': 'mision_actividades_2', 'titulo': 'Juega 2 actividades', 'descripcion': 'Completa 2 actividades interactivas.', 'tipo': 'actividades', 'meta': 2, 'puntos': 40, 'monedas': 15, 'solo_plus': False},
    {'codigo': 'mision_simulacro_1', 'titulo': 'Primer simulacro', 'descripcion': 'Completa un simulacro de práctica.', 'tipo': 'simulacros', 'meta': 1, 'puntos': 70, 'monedas': 30, 'solo_plus': False},
    {'codigo': 'mision_racha_3', 'titulo': 'Tres días seguidos', 'descripcion': 'Mantén una racha de 3 días.', 'tipo': 'racha', 'meta': 3, 'puntos': 90, 'monedas': 40, 'solo_plus': True},
]
