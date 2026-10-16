import { Link } from 'react-router-dom'
import { useJuego } from '../contexto/ContextoJuego'

function LogrosPagina() {
  const { resumen, plan, cargando } = useJuego()

  if (cargando || !resumen) {
    return <div className="pantalla-carga">Cargando tus logros...</div>
  }

  const { perfil, insignias, misiones } = resumen
  const rango = perfil.puntos_siguiente_nivel - perfil.puntos_nivel_actual
  const avanceNivel = rango > 0
    ? Math.round(((perfil.puntos - perfil.puntos_nivel_actual) / rango) * 100)
    : 100

  return (
    <div className="pagina-logros">
      <section className="tarjeta-panel cabecera-seccion">
        <div>
          <h1>Mis logros</h1>
          <p>Gana puntos, sube de nivel y desbloquea insignias mientras aprendes.</p>
        </div>
        <span className={plan?.es_plus ? 'burbuja-estado burbuja-plus' : 'burbuja-estado'}>
          Plan {plan?.es_plus ? 'Plus' : 'Gratis'}
        </span>
      </section>

      <section className="rejilla-tarjetas">
        <div className="tarjeta-dato"><span>Nivel</span><strong>{perfil.nivel}</strong></div>
        <div className="tarjeta-dato"><span>Puntos</span><strong>{perfil.puntos}</strong></div>
        <div className="tarjeta-dato"><span>Monedas</span><strong>{perfil.monedas}</strong></div>
        <div className="tarjeta-dato"><span>Racha</span><strong>{perfil.racha_actual} días</strong></div>
      </section>

      <section className="tarjeta-panel">
        <div className="cabecera-seccion">
          <h2>Avance de nivel</h2>
          <span>{avanceNivel}% hacia el nivel {perfil.nivel + 1}</span>
        </div>
        <div className="barra-progreso">
          <div className="barra-progreso-relleno" style={{ width: `${avanceNivel}%` }} />
        </div>
        <small>
          {perfil.puntos - perfil.puntos_nivel_actual} de {rango} puntos en este nivel.
        </small>
      </section>

      <section className="tarjeta-panel">
        <div className="cabecera-seccion">
          <h2>Insignias ({resumen.insignias_obtenidas}/{resumen.total_insignias})</h2>
          <p>Se obtienen al alcanzar metas de aprendizaje.</p>
        </div>
        <div className="rejilla-insignias">
          {insignias.map((insignia) => (
            <div
              key={insignia.codigo}
              className={insignia.obtenida ? 'tarjeta-insignia obtenida' : 'tarjeta-insignia'}
            >
              <span className="icono-insignia">{insignia.obtenida ? insignia.icono : '🔒'}</span>
              <strong>{insignia.nombre}</strong>
              <small>{insignia.descripcion}</small>
              {insignia.solo_plus && <span className="etiqueta-plus">Plus</span>}
            </div>
          ))}
        </div>
      </section>

      <section className="tarjeta-panel">
        <div className="cabecera-seccion">
          <h2>Misiones</h2>
          <p>Retos con recompensa al completarse.</p>
        </div>
        <div className="rejilla-misiones">
          {misiones.map((mision) => {
            const avance = Math.min(Math.round((mision.progreso / mision.meta) * 100), 100)
            return (
              <div key={mision.codigo} className={mision.bloqueada ? 'tarjeta-mision bloqueada' : 'tarjeta-mision'}>
                <div className="cabecera-mision">
                  <strong>{mision.titulo}</strong>
                  {mision.solo_plus && <span className="etiqueta-plus">Plus</span>}
                </div>
                <p>{mision.descripcion}</p>
                <div className="barra-progreso">
                  <div className="barra-progreso-relleno" style={{ width: `${avance}%` }} />
                </div>
                <div className="pie-mision">
                  <span>{mision.progreso} / {mision.meta}</span>
                  <span>+{mision.puntos} pts · +{mision.monedas} monedas</span>
                </div>
                {mision.completada && <span className="pildora ok">Completada</span>}
                {mision.bloqueada && (
                  <Link className="enlace-ayuda" to="/planes">
                    Disponible con el plan Plus
                  </Link>
                )}
              </div>
            )
          })}
        </div>
      </section>
    </div>
  )
}

export default LogrosPagina
