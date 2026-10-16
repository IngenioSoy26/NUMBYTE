import { useState } from 'react'
import { useJuego } from '../contexto/ContextoJuego'

function PlanesPagina() {
  const { plan, activarPlus, volverAGratis } = useJuego()
  const [mensaje, setMensaje] = useState('')
  const [procesando, setProcesando] = useState(false)

  const esPlus = plan?.es_plus ?? false

  const manejarPlus = async () => {
    setProcesando(true)
    setMensaje('')
    try {
      await activarPlus()
      setMensaje('¡Plan Plus activado! Ya tienes acceso a todos los beneficios (demostración sin cobro).')
    } finally {
      setProcesando(false)
    }
  }

  const manejarGratis = async () => {
    setProcesando(true)
    setMensaje('')
    try {
      await volverAGratis()
      setMensaje('Volviste al plan Gratis (demostración).')
    } finally {
      setProcesando(false)
    }
  }

  return (
    <div className="pagina-planes">
      <section className="tarjeta-panel cabecera-seccion">
        <div>
          <h1>Planes de NUMBYTE</h1>
          <p>
            Compara el plan Gratis y el plan Plus. El plan Plus es una{' '}
            <strong>demostración académica</strong>: no existe pasarela de pago ni cobro real.
          </p>
        </div>
        <span className={esPlus ? 'burbuja-estado burbuja-plus' : 'burbuja-estado'}>
          Tu plan: {esPlus ? 'Plus' : 'Gratis'}
        </span>
      </section>

      {mensaje && <div className="mensaje-exito">{mensaje}</div>}

      <section className="rejilla-planes">
        <article className={esPlus ? 'tarjeta-plan' : 'tarjeta-plan destacado'}>
          <h2>Gratis</h2>
          <p className="precio-plan">$0</p>
          <p className="descripcion-plan">Todo lo esencial para empezar a aprender.</p>
          <ul>
            <li>Diagnóstico y práctica ilimitados</li>
            <li>Ruta de aprendizaje de 6°</li>
            <li>1 simulacro de práctica al día</li>
            <li>Insignias y misiones básicas</li>
          </ul>
          {esPlus ? (
            <button className="boton-secundario ancho-completo" onClick={manejarGratis} disabled={procesando}>
              {procesando ? 'Procesando...' : 'Volver a Gratis'}
            </button>
          ) : (
            <span className="pildora ok">Plan actual</span>
          )}
        </article>

        <article className={esPlus ? 'tarjeta-plan destacado plus' : 'tarjeta-plan plus'}>
          <div className="cabecera-plan-plus">
            <h2>Plus</h2>
            <span className="etiqueta-plus">Recomendado</span>
          </div>
          <p className="precio-plan">Demo</p>
          <p className="descripcion-plan">Desbloquea toda la experiencia de aprendizaje.</p>
          <ul>
            <li>Analítica avanzada de tu progreso</li>
            <li>Insignias y misiones exclusivas</li>
            <li>Todos los videos y recursos</li>
            <li>Simulacros ilimitados</li>
          </ul>
          {esPlus ? (
            <span className="pildora ok">Plan actual</span>
          ) : (
            <button className="boton-principal ancho-completo" onClick={manejarPlus} disabled={procesando}>
              {procesando ? 'Activando...' : 'Mejorar a Plus'}
            </button>
          )}
        </article>
      </section>

      <section className="tarjeta-panel">
        <h2>Comparación detallada de beneficios</h2>
        <div className="tabla-beneficios">
          {plan?.beneficios.map((beneficio) => (
            <div key={beneficio.titulo} className="fila-beneficio">
              <div>
                <strong>{beneficio.titulo}</strong>
                <span>{beneficio.descripcion}</span>
              </div>
              <div className="marcas-beneficio">
                <span className="marca gratis">{beneficio.solo_plus ? '—' : 'Incluido'}</span>
                <span className={beneficio.solo_plus ? 'marca plus activa' : 'marca plus'}>
                  {esPlus || beneficio.solo_plus ? 'Incluido' : 'Bloqueado'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default PlanesPagina
