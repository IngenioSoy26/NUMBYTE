import { Link } from 'react-router-dom'

function InicioPagina() {
  return (
    <div className="pagina-inicio">
      <section className="hero-inicio">
        <div className="hero-texto">
          <span className="insignia">Proyecto educativo digital</span>
          <h1>NUMBYTE</h1>
          <p className="lema">Educando y mejorando por un mundo mejor</p>
          <p className="descripcion">
            Plataforma interactiva para fortalecer matemáticas en estudiantes de 6° a 11° mediante
            diagnóstico, práctica, seguimiento y simulacros.
          </p>
          <div className="grupo-botones">
            <Link className="boton-principal" to="/acceso">
              Ingresar a la plataforma
            </Link>
            <a className="boton-secundario" href="#caracteristicas">
              Ver características
            </a>
          </div>
        </div>

        <div className="hero-visual tarjeta-flotante">
          <img src="/logo-numbyte.png" alt="Logo NUMBYTE" className="logo-principal" />
          <div className="mini-puntos">
            <div>
              <strong>6° a 11°</strong>
              <span>Aprendizaje adaptado por grado</span>
            </div>
            <div>
              <strong>Diagnóstico</strong>
              <span>Fortalezas y debilidades</span>
            </div>
            <div>
              <strong>Simulacros</strong>
              <span>Práctica progresiva tipo Saber 11</span>
            </div>
          </div>
        </div>
      </section>

      <section id="caracteristicas" className="seccion-caracteristicas">
        <article className="tarjeta-info">
          <h3>Diagnóstico inteligente</h3>
          <p>Detecta temas por reforzar y genera una interpretación pedagógica útil.</p>
        </article>
        <article className="tarjeta-info">
          <h3>Práctica guiada</h3>
          <p>Permite practicar por tema, dificultad y grado con retroalimentación inmediata.</p>
        </article>
        <article className="tarjeta-info">
          <h3>Seguimiento visual</h3>
          <p>Muestra resultados con gráficas modernas, claras y orientadas al progreso.</p>
        </article>
      </section>
    </div>
  )
}

export default InicioPagina
