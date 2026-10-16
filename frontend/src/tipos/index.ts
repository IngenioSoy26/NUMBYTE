export interface Usuario {
  id: number
  nombre: string
  correo: string
  grado: string
  estado_cuenta: string
  plan: string
  es_plus: boolean
  fecha_registro: string
}

export interface TokenRespuesta {
  access_token: string
  token_type: string
}

export interface TemaDisponible {
  tema: string
  grado: string
  cantidad_preguntas: number
}

export interface Opcion {
  id: number
  identificador: string
  texto: string
}

export interface Pregunta {
  id: number
  enunciado: string
  grado: string
  tema: string
  competencia: string
  dba: string
  nivel_dificultad: string
  tipo_pregunta: string
  opciones: Opcion[]
}

export interface EvaluacionGenerada {
  tipo_evaluacion: string
  grado: string
  tema?: string
  preguntas: Pregunta[]
}

export interface ResultadoEvaluacion {
  id: number
  tipo_evaluacion: string
  grado: string
  tema_principal: string
  cantidad_preguntas: number
  respuestas_correctas: number
  respuestas_incorrectas: number
  porcentaje_aciertos: number
  puntaje: number
  tiempo_utilizado_segundos: number
  fortalezas: string[]
  debilidades: string[]
  interpretacion_pedagogica: string
  recomendaciones: string[]
  detalle_temas: Record<string, number>
  detalle_competencias: Record<string, number>
  recompensa?: Recompensa | null
}

export interface TarjetaResumen {
  etiqueta: string
  valor: number | string
}

export interface PuntoHistorial {
  fecha: string
  porcentaje: number
  tipo_evaluacion: string
}

export interface ResumenTema {
  tema: string
  porcentaje: number
  intentos: number
}

export interface ResumenProgreso {
  tarjetas: TarjetaResumen[]
  historial: PuntoHistorial[]
  temas: ResumenTema[]
  fortalezas: string[]
  debilidades: string[]
}

// --- Gamificación ---
export interface PerfilJuego {
  puntos: number
  monedas: number
  nivel: number
  puntos_nivel_actual: number
  puntos_siguiente_nivel: number
  racha_actual: number
  racha_maxima: number
}

export interface Insignia {
  codigo: string
  nombre: string
  descripcion: string
  icono: string
  puntos_otorgados: number
  solo_plus: boolean
  obtenida: boolean
}

export interface Mision {
  codigo: string
  titulo: string
  descripcion: string
  tipo: string
  meta: number
  puntos: number
  monedas: number
  solo_plus: boolean
  progreso: number
  completada: boolean
  bloqueada: boolean
}

export interface ResumenGamificacion {
  perfil: PerfilJuego
  insignias: Insignia[]
  misiones: Mision[]
  total_insignias: number
  insignias_obtenidas: number
}

export interface Recompensa {
  puntos_ganados: number
  monedas_ganadas: number
  subio_nivel: boolean
  perfil: PerfilJuego
  insignias_nuevas: Insignia[]
  misiones_completadas: Mision[]
}

// --- Aprendizaje (ruta de grado 6°) ---
export interface Leccion {
  id: number
  grado: string
  tema: string
  titulo: string
  subtitulo: string
  explicacion: string
  ejemplo: string
  puntos: number
  orden: number
}

export interface RecursoMultimedia {
  id: number
  titulo: string
  url: string
  tipo: string
  tema: string
  grado: string
  autor: string
  descripcion: string
  solo_plus: boolean
  bloqueado: boolean
  url_embed: string | null
}

export interface CategoriaActividad {
  id: string
  nombre: string
}

export interface ElementoActividad {
  id: string
  texto: string
  categoria?: string
}

export interface OpcionActividad {
  id: string
  texto: string
  correcta?: boolean
}

export interface DatosActividad {
  pregunta?: string
  opciones?: OpcionActividad[]
  categorias?: CategoriaActividad[]
  elementos?: ElementoActividad[]
}

export interface ActividadPublica {
  id: number
  grado: string
  tema: string
  titulo: string
  instrucciones: string
  tipo: string
  datos: DatosActividad
  puntos: number
  solo_plus: boolean
  bloqueada: boolean
}

export interface ItemRuta {
  tema: string
  orden: number
  leccion: Leccion | null
  actividad: ActividadPublica | null
  recurso: RecursoMultimedia | null
  leccion_completada: boolean
  actividad_completada: boolean
  progreso: number
}

export interface RutaAprendizaje {
  grado: string
  total_items: number
  items_completados: number
  porcentaje: number
  items: ItemRuta[]
}

export interface ResultadoActividad {
  correcta: boolean
  puntaje: number
  total: number
  recompensa: Recompensa
}

// --- Planes ---
export interface BeneficioPlan {
  titulo: string
  descripcion: string
  solo_plus: boolean
}

export interface PlanPublico {
  plan: string
  es_plus: boolean
  fecha_activacion_plan: string | null
  beneficios: BeneficioPlan[]
}

export interface RespuestaPlan {
  mensaje: string
  plan: PlanPublico
}

// --- Simulacros ---
export interface EstadoSimulacro {
  es_plus: boolean
  realizados_hoy: number
  limite_diario: number | null
  permitido: boolean
  mensaje: string
}

export interface ResultadoSimulacroHistorial {
  id: number
  fecha: string | null
  cantidad_preguntas: number
  respuestas_correctas: number
  porcentaje_aciertos: number
  puntaje: number
  tiempo_utilizado_segundos: number
}
