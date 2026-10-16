import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import GraficasPanel from '../componentes/GraficasPanel'
import TarjetaAccion from '../componentes/TarjetaAccion'
import TarjetaDato from '../componentes/TarjetaDato'
import { useAutenticacion } from '../contexto/ContextoAutenticacion'
import { useJuego } from '../contexto/ContextoJuego'
import { api } from '../servicios/api'
import type { ResumenProgreso, RutaAprendizaje, EstadoSimulacro } from '../tipos'

const resumenVacio: ResumenProgreso = {
  tarjetas: [],
  historial: [],
  temas: [],
  fortalezas: [],
  debilidades: [],
}

function PanelPagina() {
  const { usuario } = useAutenticacion()
  const { resumen: juego, plan } = useJuego()
  const [resumen, setResumen] = useState<ResumenProgreso>(resumenVacio)
  const [ruta, setRuta] = useState<RutaAprendizaje | null>(null)
  const [simulacro, setSimulacro] = useState<EstadoSimulacro | null>(null)
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    const cargar = async () => {
      try {
        const [respuestaProgreso, respuestaRuta, respuestaSimulacro] = await Promise.all([
          api.get<ResumenProgreso>('/progreso/resumen'),
          api.get<RutaAprendizaje>('/aprendizaje/ruta', { params: { grado: '6' } }),
          api.get<EstadoSimulacro>('/simulacros/estado'),
        ])
        setResumen(respuestaProgreso.data)
        setRuta(respuestaRuta.data)
        setSimulacro(respuestaSimulacro.data)
      } catch (error) {
        console.error(error)
      } finally {
        setCargando(false)
      }
    }
    cargar()
  }, [])

  return (
    <div className="pagina-panel">
      <section className="cabecera-panel tarjeta-panel">
        <div>
          <h1>Hola, {usuario?.nombre}</h1>
          <p>
            Estás en grado {usuario?.grado}. Sigue practicando para fortalecer tus competencias
            matemáticas.
          </p>
        </div>
        <div className="estado-cabecera">
          <span className={plan?.es_plus ? 'burbuja-estado burbuja-plus' : 'burbuja-estado'}>
            Plan {plan?.es_plus ? 'Plus' : 'Gratis'}
          </span>
          <span className="burbuja-estado">Nivel {juego?.perfil.nivel ?? 1}</span>
        </div>
      </section>

      <section className="rejilla-tarjetas">
        <TarjetaDato etiqueta="Puntos" valor={juego?.perfil.puntos ?? 0} />
        <TarjetaDato etiqueta="Monedas" valor={juego?.perfil.monedas ?? 0} />
        <TarjetaDato
          etiqueta="Insignias"
          valor={`${juego?.insignias_obtenidas ?? 0} / ${juego?.total_insignias ?? 0}`}
        />
        <TarjetaDato etiqueta="Racha" valor={`${juego?.perfil.racha_actual ?? 0} días`} />
      </section>

      <section className="tarjeta-panel progreso-ruta-panel">
        <div className="cabecera-seccion">
          <div>
            <h2>Tu ruta de aprendizaje de 6°</h2>
            <p>Microlecciones, videos y actividades de clic por tema.</p>
          </div>
          <Link className="boton-principal" to="/ruta">
            Continuar ruta
          </Link>
        </div>
        <div className="barra-progreso">
          <div className="barra-progreso-relleno" style={{ width: `${ruta?.porcentaje ?? 0}%` }} />
        </div>
        <small>
          {ruta?.items_completados ?? 0} de {ruta?.total_items ?? 0} temas completados (
          {ruta?.porcentaje ?? 0}%).
        </small>
        {simulacro && (
          <p className="aviso-simulacro">
            {simulacro.mensaje} {simulacro.limite_diario !== null && `(límite diario: ${simulacro.limite_diario})`}
          </p>
        )}
      </section>

      <section className="rejilla-tarjetas">
        {resumen.tarjetas.map((tarjeta) => (
          <TarjetaDato key={tarjeta.etiqueta} etiqueta={tarjeta.etiqueta} valor={tarjeta.valor} />
        ))}
      </section>

      <section className="rejilla-acciones">
        <TarjetaAccion
          titulo="Ruta 6°"
          descripcion="Aprende tema por tema con lecciones, videos y juegos de clic."
          ruta="/ruta"
        />
        <TarjetaAccion
          titulo="Diagnóstico"
          descripcion="Identifica fortalezas y debilidades para orientar tu ruta de estudio."
          ruta="/evaluacion/diagnostico"
        />
        <TarjetaAccion
          titulo="Práctica por tema"
          descripcion="Entrena un tema específico con dificultad ajustable."
          ruta="/evaluacion/practica"
        />
        <TarjetaAccion
          titulo="Simulacro"
          descripcion="Realiza una prueba completa inspirada en preguntas tipo Saber 11."
          ruta="/evaluacion/simulacro"
        />
        <TarjetaAccion
          titulo="Logros"
          descripcion="Revisa tus insignias, misiones y avance de nivel."
          ruta="/logros"
        />
        <TarjetaAccion
          titulo="Planes"
          descripcion="Compara el plan Gratis y el plan Plus (demostración)."
          ruta="/planes"
        />
      </section>

      <section className="tarjeta-panel">
        <div className="cabecera-seccion">
          <h2>Seguimiento académico</h2>
          <p>Gráficas modernas para entender mejor tu avance.</p>
        </div>
        {cargando ? <p>Cargando gráficas...</p> : <GraficasPanel resumen={resumen} />}
      </section>

      <section className="rejilla-listas">
        <div className="tarjeta-panel">
          <h3>Fortalezas</h3>
          <ul>
            {resumen.fortalezas.length ? resumen.fortalezas.map((item) => <li key={item}>{item}</li>) : <li>Aún no hay fortalezas detectadas.</li>}
          </ul>
        </div>
        <div className="tarjeta-panel">
          <h3>Temas por reforzar</h3>
          <ul>
            {resumen.debilidades.length ? resumen.debilidades.map((item) => <li key={item}>{item}</li>) : <li>Aún no hay debilidades detectadas.</li>}
          </ul>
        </div>
      </section>
    </div>
  )
}

export default PanelPagina
