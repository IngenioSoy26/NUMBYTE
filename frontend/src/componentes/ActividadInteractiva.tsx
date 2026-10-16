import { useState } from 'react'
import { api } from '../servicios/api'
import type { ActividadPublica, ResultadoActividad } from '../tipos'

interface Props {
  actividad: ActividadPublica
  onResultado: (resultado: ResultadoActividad) => void
}

function ActividadInteractiva({ actividad, onResultado }: Props) {
  const [seleccion, setSeleccion] = useState<string | null>(null)
  const [asignaciones, setAsignaciones] = useState<Record<string, string>>({})
  const [enviando, setEnviando] = useState(false)
  const [resultado, setResultado] = useState<ResultadoActividad | null>(null)
  const [error, setError] = useState('')

  const categorias = actividad.datos.categorias || []
  const elementos = actividad.datos.elementos || []
  const opciones = actividad.datos.opciones || []

  const asignarCategoria = (categoriaId: string) => {
    if (!seleccion) return
    setAsignaciones((previas) => ({ ...previas, [seleccion]: categoriaId }))
    setSeleccion(null)
  }

  const nombreCategoria = (categoriaId: string) =>
    categorias.find((categoria) => categoria.id === categoriaId)?.nombre || ''

  const enviar = async () => {
    setError('')
    setEnviando(true)
    try {
      const respuestas =
        actividad.tipo === 'seleccionar' ? { seleccion } : { ...asignaciones }
      const respuesta = await api.post<ResultadoActividad>(
        `/aprendizaje/actividad/${actividad.id}/responder`,
        { respuestas },
      )
      setResultado(respuesta.data)
      onResultado(respuesta.data)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'No fue posible enviar la actividad.')
    } finally {
      setEnviando(false)
    }
  }

  const reiniciar = () => {
    setSeleccion(null)
    setAsignaciones({})
    setResultado(null)
    setError('')
  }

  if (resultado) {
    return (
      <div className={resultado.correcta ? 'resultado-actividad correcta' : 'resultado-actividad'}>
        <h4>{resultado.correcta ? '¡Actividad completada!' : 'Casi lo logras'}</h4>
        <p>
          Acertaste {resultado.puntaje} de {resultado.total} punto(s) posibles.
        </p>
        {resultado.recompensa.puntos_ganados > 0 && (
          <p className="mensaje-exito">Ganaste +{resultado.recompensa.puntos_ganados} puntos.</p>
        )}
        <button className="boton-secundario" onClick={reiniciar}>
          Intentar de nuevo
        </button>
      </div>
    )
  }

  return (
    <div className="juego-actividad">
      <p className="instrucciones-actividad">{actividad.instrucciones}</p>

      {actividad.tipo === 'seleccionar' && (
        <div>
          {actividad.datos.pregunta && <h4>{actividad.datos.pregunta}</h4>}
          <div className="opciones-juego">
            {opciones.map((opcion) => (
              <button
                key={opcion.id}
                className={seleccion === opcion.id ? 'opcion-juego activa' : 'opcion-juego'}
                onClick={() => setSeleccion(opcion.id)}
              >
                {opcion.texto}
              </button>
            ))}
          </div>
        </div>
      )}

      {actividad.tipo === 'clasificar' && (
        <div className="panel-clasificar">
          <div className="elementos-clasificar">
            {elementos.map((elemento) => {
              const asignada = asignaciones[elemento.id]
              return (
                <button
                  key={elemento.id}
                  className={seleccion === elemento.id ? 'elemento-juego activo' : 'elemento-juego'}
                  onClick={() => setSeleccion(elemento.id)}
                >
                  <span>{elemento.texto}</span>
                  {asignada && <em className="etiqueta-asignada">{nombreCategoria(asignada)}</em>}
                </button>
              )
            })}
          </div>

          <div className="columnas-clasificar">
            {categorias.map((categoria) => (
              <button
                key={categoria.id}
                className="columna-juego"
                disabled={!seleccion}
                onClick={() => asignarCategoria(categoria.id)}
              >
                <strong>{categoria.nombre}</strong>
                <span className="pista-columna">Clic para asignar</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {error && <div className="mensaje-error">{error}</div>}

      <button className="boton-principal" onClick={enviar} disabled={enviando}>
        {enviando ? 'Enviando...' : 'Comprobar respuesta'}
      </button>
    </div>
  )
}

export default ActividadInteractiva
