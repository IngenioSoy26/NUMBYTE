import type { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAutenticacion } from '../contexto/ContextoAutenticacion'
import { useJuego } from '../contexto/ContextoJuego'

const MENU = [
  { ruta: '/panel', etiqueta: 'Panel' },
  { ruta: '/ruta', etiqueta: 'Ruta 6°' },
  { ruta: '/evaluacion/diagnostico', etiqueta: 'Diagnóstico' },
  { ruta: '/evaluacion/practica', etiqueta: 'Práctica' },
  { ruta: '/evaluacion/simulacro', etiqueta: 'Simulacro' },
  { ruta: '/logros', etiqueta: 'Logros' },
  { ruta: '/planes', etiqueta: 'Planes' },
]

function LayoutPrincipal({ children }: { children: ReactNode }) {
  const { usuario, cerrarSesion } = useAutenticacion()
  const { resumen, plan } = useJuego()
  const ubicacion = useLocation()

  return (
    <div className="layout-principal">
      <aside className="barra-lateral">
        <div className="marca-lateral">
          <img src="/logo-numbyte.png" alt="Logo NUMBYTE" className="logo-lateral" />
          <div>
            <h2>NUMBYTE</h2>
            <p>Educando y mejorando</p>
          </div>
        </div>

        <div className="panel-jugador">
          <div>
            <span className="etiqueta-jugador">Nivel</span>
            <strong>{resumen?.perfil.nivel ?? 1}</strong>
          </div>
          <div>
            <span className="etiqueta-jugador">Puntos</span>
            <strong>{resumen?.perfil.puntos ?? 0}</strong>
          </div>
          <div>
            <span className="etiqueta-jugador">Monedas</span>
            <strong>{resumen?.perfil.monedas ?? 0}</strong>
          </div>
        </div>

        <nav className="menu-lateral">
          {MENU.map((item) => (
            <Link
              key={item.ruta}
              className={ubicacion.pathname === item.ruta ? 'activo' : ''}
              to={item.ruta}
            >
              {item.etiqueta}
              {item.ruta === '/planes' && plan?.es_plus && <span className="marca-plus-menu">Plus</span>}
            </Link>
          ))}
        </nav>

        <div className="perfil-lateral">
          <strong>{usuario?.nombre}</strong>
          <span>Grado {usuario?.grado}</span>
          <span className={plan?.es_plus ? 'plan-actual plus' : 'plan-actual'}>
            Plan {plan?.es_plus ? 'Plus' : 'Gratis'}
          </span>
          <button onClick={cerrarSesion}>Cerrar sesión</button>
        </div>
      </aside>

      <main className="contenido-principal">
        {children}
        <footer className="pie-marca">© IngenioSoy - Todos los Derechos Reservados</footer>
      </main>
    </div>
  )
}

export default LayoutPrincipal
