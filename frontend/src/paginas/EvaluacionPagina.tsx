import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import RecompensaBanner from '../componentes/RecompensaBanner'
import { useAutenticacion } from '../contexto/ContextoAutenticacion'
import { useJuego } from '../contexto/ContextoJuego'
import { api } from '../servicios/api'
import type {
  EstadoSimulacro,
  EvaluacionGenerada,
  Pregunta,
  ResultadoEvaluacion,
  TemaDisponible,
} from '../tipos'

const TITULOS: Record<string, string> = {
  diagnostico: 'Diagnóstico',
  practica: 'Práctica',
  simulacro: 'Simulacro',
}

function EvaluacionPagina() {
  const { tipo } = useParams()
  const tipoSeguro = tipo || 'diagnostico'
  const { usuario } = useAutenticacion()
  const { plan, refrescar } = useJuego()
  const navegar = useNavigate()

  const [temas, setTemas] = useState<TemaDisponible[]>([])
  const [temaSeleccionado, setTemaSeleccionado] = useState('')
  const [dificultad, setDificultad] = useState('')
  const [cantidadPreguntas, setCantidadPreguntas] = useState(5)
  const [evaluacion, setEvaluacion] = useState<EvaluacionGenerada | null>(null)
  const [respuestas, setRespuestas] = useState<Record<number, number>>({})
  const [resultado, setResultado] = useState<ResultadoEvaluacion | null>(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')
  const [inicioEvaluacion, setInicioEvaluacion] = useState<number | null>(null)
  const [estadoSimulacro, setEstadoSimulacro] = useState<EstadoSimulacro | null>(null)

  useEffect(() => {
    const cargarTemas = async () => {
      const respuesta = await api.get<TemaDisponible[]>('/contenidos/temas')
      setTemas(respuesta.data)
    }
    cargarTemas().catch(console.error)
  }, [])

  useEffect(() => {
    if (tipoSeguro !== 'simulacro') {
      setEstadoSimulacro(null)
      return
    }
    const cargarEstado = async () => {
      const respuesta = await api.get<EstadoSimulacro>('/simulacros/estado')
      setEstadoSimulacro(respuesta.data)
    }
    cargarEstado().catch(console.error)
  }, [tipoSeguro])

  const temasFiltrados = useMemo(
    () => temas.filter((tema) => tema.grado === usuario?.grado),
    [temas, usuario?.grado],
  )

  const generar = async () => {
    setError('')
    setResultado(null)
    setCargando(true)
    try {
      const respuesta = await api.post<EvaluacionGenerada>('/evaluaciones/generar', {
        tipo_evaluacion: tipoSeguro,
        grado: usuario?.grado,
        tema: temaSeleccionado || null,
        dificultad: dificultad || null,
        cantidad_preguntas: cantidadPreguntas,
      })
      setEvaluacion(respuesta.data)
      setRespuestas({})
      setInicioEvaluacion(Date.now())
    } catch (error: any) {
      setError(error?.response?.data?.detail || 'No fue posible generar la evaluación.')
    } finally {
      setCargando(false)
    }
  }

  const seleccionarOpcion = (preguntaId: number, opcionId: number) => {
    setRespuestas((anterior) => ({ ...anterior, [preguntaId]: opcionId }))
  }

  const enviar = async () => {
    if (!evaluacion) return
    setError('')
    setCargando(true)
    try {
      const tiempo = inicioEvaluacion ? Math.round((Date.now() - inicioEvaluacion) / 1000) : 0
      const carga = {
        tipo_evaluacion: tipoSeguro,
        grado: usuario?.grado,
        tema: temaSeleccionado || null,
        tiempo_utilizado_segundos: tiempo,
        respuestas: evaluacion.preguntas.map((pregunta) => ({
          pregunta_id: pregunta.id,
          opcion_id: respuestas[pregunta.id] || null,
        })),
      }
      const respuesta = await api.post<ResultadoEvaluacion>('/evaluaciones/calificar', carga)
      setResultado(respuesta.data)
      await refrescar()
      if (tipoSeguro === 'simulacro') {
        const estadoActualizado = await api.get<EstadoSimulacro>('/simulacros/estado')
        setEstadoSimulacro(estadoActualizado.data)
      }
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (error: any) {
      setError(error?.response?.data?.detail || 'No fue posible calificar la evaluación.')
    } finally {
      setCargando(false)
    }
  }

  const limpiar = () => {
    setEvaluacion(null)
    setResultado(null)
    setRespuestas({})
  }

  return (
    <div className="pagina-evaluacion">
      <div className="tarjeta-panel cabecera-seccion">
        <div>
          <h1>{TITULOS[tipoSeguro] || 'Evaluación'}</h1>
          <p>
            Configura la actividad, responde las preguntas y obtén una retroalimentación clara.
          </p>
        </div>
        <button className="boton-secundario" onClick={() => navegar('/panel')}>
          Volver al panel
        </button>
      </div>

      {tipoSeguro === 'simulacro' && estadoSimulacro && (
        <div className={estadoSimulacro.permitido ? 'aviso-simulacro-panel' : 'aviso-simulacro-panel bloqueado'}>
          <span>{estadoSimulacro.mensaje}</span>
          {!estadoSimulacro.permitido && (
            <Link className="boton-principal" to="/planes">
              Mejorar a Plus
            </Link>
          )}
          {estadoSimulacro.es_plus && <span className="etiqueta-plus">Plus</span>}
        </div>
      )}

      {!evaluacion && (
        <section className="tarjeta-panel formulario-configuracion">
          <div className="rejilla-formulario">
            <label>
              Tema
              <select value={temaSeleccionado} onChange={(e) => setTemaSeleccionado(e.target.value)}>
                <option value="">General</option>
                {temasFiltrados.map((tema) => (
                  <option key={`${tema.grado}-${tema.tema}`} value={tema.tema}>
                    {tema.tema}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Dificultad
              <select value={dificultad} onChange={(e) => setDificultad(e.target.value)}>
                <option value="">Mixta</option>
                <option value="baja">Baja</option>
                <option value="media">Media</option>
                <option value="alta">Alta</option>
              </select>
            </label>

            <label>
              Cantidad de preguntas
              <select value={cantidadPreguntas} onChange={(e) => setCantidadPreguntas(Number(e.target.value))}>
                {[3, 5, 8, 10].map((cantidad) => (
                  <option key={cantidad} value={cantidad}>
                    {cantidad}
                  </option>
                ))}
              </select>
            </label>
          </div>

          {error && <div className="mensaje-error">{error}</div>}

          <button className="boton-principal" onClick={generar} disabled={cargando}>
            {cargando ? 'Generando...' : 'Generar evaluación'}
          </button>
        </section>
      )}

      {evaluacion && !resultado && (
        <section className="tarjeta-panel">
          <div className="cabecera-seccion">
            <h2>Preguntas</h2>
            <button className="boton-secundario" onClick={limpiar}>
              Cambiar configuración
            </button>
          </div>

          {evaluacion.preguntas.map((pregunta: Pregunta, indice) => (
            <div key={pregunta.id} className="bloque-pregunta">
              <div className="meta-pregunta">
                <span>Pregunta {indice + 1}</span>
                <span>{pregunta.tema}</span>
                <span>{pregunta.nivel_dificultad}</span>
              </div>
              <h3>{pregunta.enunciado}</h3>
              <div className="opciones-pregunta">
                {pregunta.opciones.map((opcion) => (
                  <label key={opcion.id} className={respuestas[pregunta.id] === opcion.id ? 'opcion activa' : 'opcion'}>
                    <input
                      type="radio"
                      name={`pregunta-${pregunta.id}`}
                      checked={respuestas[pregunta.id] === opcion.id}
                      onChange={() => seleccionarOpcion(pregunta.id, opcion.id)}
                    />
                    <span>{opcion.identificador}. {opcion.texto}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}

          {error && <div className="mensaje-error">{error}</div>}

          <button className="boton-principal" onClick={enviar} disabled={cargando}>
            {cargando ? 'Calificando...' : 'Enviar respuestas'}
          </button>
        </section>
      )}

      {resultado && (
        <section className="tarjeta-panel resultado-evaluacion">
          <div className="cabecera-seccion">
            <h2>Resultado obtenido</h2>
            <button className="boton-secundario" onClick={limpiar}>
              Hacer otra evaluación
            </button>
          </div>

          {resultado.recompensa && (
            <div className="bloque-recompensa">
              <RecompensaBanner recompensa={resultado.recompensa} />
            </div>
          )}

          <div className="rejilla-tarjetas">
            <div className="tarjeta-dato"><span>Porcentaje</span><strong>{resultado.porcentaje_aciertos}%</strong></div>
            <div className="tarjeta-dato"><span>Puntaje</span><strong>{resultado.puntaje} / 5.0</strong></div>
            <div className="tarjeta-dato"><span>Correctas</span><strong>{resultado.respuestas_correctas}</strong></div>
            <div className="tarjeta-dato"><span>Incorrectas</span><strong>{resultado.respuestas_incorrectas}</strong></div>
          </div>

          <div className="tarjeta-resaltada">
            <h3>Interpretación pedagógica</h3>
            <p>{resultado.interpretacion_pedagogica}</p>
          </div>

          <div className="rejilla-listas">
            <div className="tarjeta-panel tarjeta-anidada">
              <h3>Fortalezas</h3>
              <ul>
                {resultado.fortalezas.length ? resultado.fortalezas.map((item: string) => <li key={item}>{item}</li>) : <li>Sin fortalezas destacadas aún.</li>}
              </ul>
            </div>
            <div className="tarjeta-panel tarjeta-anidada">
              <h3>Debilidades</h3>
              <ul>
                {resultado.debilidades.length ? resultado.debilidades.map((item: string) => <li key={item}>{item}</li>) : <li>No se detectaron debilidades claras.</li>}
              </ul>
            </div>
          </div>

          <div className="tarjeta-panel tarjeta-anidada">
            <h3>Recomendaciones</h3>
            <ul>
              {resultado.recomendaciones.map((item: string) => <li key={item}>{item}</li>)}
            </ul>
          </div>
        </section>
      )}
    </div>
  )
}

export default EvaluacionPagina
