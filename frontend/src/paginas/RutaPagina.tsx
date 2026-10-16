import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import ActividadInteractiva from '../componentes/ActividadInteractiva'
import RecompensaBanner from '../componentes/RecompensaBanner'
import { useJuego } from '../contexto/ContextoJuego'
import { api } from '../servicios/api'
import type { ItemRuta, Recompensa, ResultadoActividad, RutaAprendizaje } from '../tipos'

const GRADO_MODULO = '6'

function Parrafos({ texto }: { texto: string }) {
  return (
    <>
      {texto.split('\n').map((linea, indice) => (
        <p key={indice}>{linea}</p>
      ))}
    </>
  )
}

function RutaPagina() {
  const { plan, refrescar } = useJuego()
  const [ruta, setRuta] = useState<RutaAprendizaje | null>(null)
  const [cargando, setCargando] = useState(true)
  const [abierto, setAbierto] = useState<number | null>(null)
  const [recompensa, setRecompensa] = useState<Recompensa | null>(null)
  const [mensajeActividad, setMensajeActividad] = useState('')

  const cargarRuta = useCallback(async () => {
    try {
      const respuesta = await api.get<RutaAprendizaje>('/aprendizaje/ruta', {
        params: { grado: GRADO_MODULO },
      })
      setRuta(respuesta.data)
    } catch (error) {
      console.error(error)
    } finally {
      setCargando(false)
    }
  }, [])

  useEffect(() => {
    cargarRuta()
  }, [cargarRuta])

  const completarLeccion = async (item: ItemRuta) => {
    if (!item.leccion) return
    try {
      const respuesta = await api.post<Recompensa>(
        `/aprendizaje/leccion/${item.leccion.id}/completar`,
      )
      setRecompensa(respuesta.data)
      await cargarRuta()
      await refrescar()
    } catch (error) {
      console.error(error)
    }
  }

  const manejarResultadoActividad = async (resultado: ResultadoActividad) => {
    setMensajeActividad(
      resultado.correcta
        ? '¡Excelente! Resolviste toda la actividad.'
        : `Acertaste ${resultado.puntaje} de ${resultado.total}. ¡Inténtalo otra vez!`,
    )
    if (resultado.recompensa.puntos_ganados > 0) {
      setRecompensa(resultado.recompensa)
      await cargarRuta()
      await refrescar()
    }
  }

  if (cargando) {
    return <div className="pantalla-carga">Cargando tu ruta de aprendizaje...</div>
  }

  return (
    <div className="pagina-ruta">
      <section className="tarjeta-panel cabecera-modulo">
        <div>
          <span className="insignia">Módulo demostrativo</span>
          <h1>Ruta de aprendizaje · Grado 6°</h1>
          <p>
            Microlecciones, videos y actividades de clic para reforzar tus matemáticas paso a paso.
            El contenido es material demostrativo, no oficial del ICFES.
          </p>
        </div>
        <div className="progreso-modulo">
          <strong>{ruta?.porcentaje ?? 0}%</strong>
          <span>
            {ruta?.items_completados ?? 0} de {ruta?.total_items ?? 0} temas
          </span>
          <div className="barra-progreso">
            <div className="barra-progreso-relleno" style={{ width: `${ruta?.porcentaje ?? 0}%` }} />
          </div>
        </div>
      </section>

      {recompensa && (
        <div className="bloque-recompensa">
          <RecompensaBanner recompensa={recompensa} />
          <button className="boton-secundario" onClick={() => setRecompensa(null)}>
            Cerrar aviso
          </button>
        </div>
      )}

      <section className="lista-ruta">
        {ruta?.items.map((item) => {
          const expandido = abierto === item.orden
          return (
            <article key={item.tema} className={expandido ? 'tarjeta-panel item-ruta abierto' : 'tarjeta-panel item-ruta'}>
              <button
                className="encabezado-item-ruta"
                onClick={() => setAbierto(expandido ? null : item.orden)}
              >
                <span className="numero-tema">{item.orden}</span>
                <div className="titulo-item-ruta">
                  <strong>{item.tema}</strong>
                  <span>{item.leccion?.subtitulo}</span>
                </div>
                <div className="estados-item-ruta">
                  <span className={item.leccion_completada ? 'pildora ok' : 'pildora'}>Lección</span>
                  <span className={item.actividad_completada ? 'pildora ok' : 'pildora'}>Actividad</span>
                  <span className="porcentaje-item">{item.progreso}%</span>
                </div>
              </button>

              {expandido && (
                <div className="detalle-item-ruta">
                  {item.leccion && (
                    <div className="bloque-leccion">
                      <h3>{item.leccion.titulo}</h3>
                      <div className="texto-leccion">
                        <Parrafos texto={item.leccion.explicacion} />
                      </div>
                      {item.leccion.ejemplo && (
                        <div className="caja-ejemplo">
                          <h4>Ejemplo resuelto</h4>
                          <Parrafos texto={item.leccion.ejemplo} />
                        </div>
                      )}
                      {item.leccion_completada ? (
                        <span className="pildora ok">Lección completada</span>
                      ) : (
                        <button className="boton-principal" onClick={() => completarLeccion(item)}>
                          Marcar lección como completada (+{item.leccion.puntos} pts)
                        </button>
                      )}
                    </div>
                  )}

                  <div className="bloque-recurso">
                    <h3>Recurso audiovisual</h3>
                    {!item.recurso && <p>No hay video asociado a este tema.</p>}
                    {item.recurso && item.recurso.bloqueado && (
                      <div className="recurso-bloqueado">
                        <p>Este recurso es exclusivo del plan Plus.</p>
                        <Link className="boton-principal" to="/planes">
                          Mejorar a Plus
                        </Link>
                      </div>
                    )}
                    {item.recurso && !item.recurso.bloqueado && (
                      <>
                        <h4>{item.recurso.titulo}</h4>
                        {item.recurso.url_embed ? (
                          <div className="marco-video">
                            <iframe
                              src={item.recurso.url_embed}
                              title={item.recurso.titulo}
                              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                              allowFullScreen
                            />
                          </div>
                        ) : (
                          <div className="recurso-externo">
                            <p>{item.recurso.descripcion}</p>
                            <a
                              className="boton-secundario"
                              href={item.recurso.url}
                              target="_blank"
                              rel="noreferrer"
                            >
                              Ver video sugerido en YouTube
                            </a>
                          </div>
                        )}
                        <small className="credito-recurso">Fuente: {item.recurso.autor}</small>
                      </>
                    )}
                  </div>

                  <div className="bloque-actividad">
                    <h3>Actividad de refuerzo</h3>
                    {!item.actividad && <p>No hay actividad para este tema.</p>}
                    {item.actividad && item.actividad.bloqueada && (
                      <div className="recurso-bloqueado">
                        <p>Esta actividad es exclusiva del plan Plus.</p>
                        {!plan?.es_plus && (
                          <Link className="boton-principal" to="/planes">
                            Mejorar a Plus
                          </Link>
                        )}
                      </div>
                    )}
                    {item.actividad && !item.actividad.bloqueada && (
                      <ActividadInteractiva
                        actividad={item.actividad}
                        onResultado={manejarResultadoActividad}
                      />
                    )}
                    {mensajeActividad && <p className="aviso-actividad">{mensajeActividad}</p>}
                  </div>
                </div>
              )}
            </article>
          )
        })}
      </section>
    </div>
  )
}

export default RutaPagina
