import { Navigate, Route, Routes } from 'react-router-dom'
import LayoutPrincipal from './componentes/LayoutPrincipal'
import RutaProtegida from './componentes/RutaProtegida'
import AccesoPagina from './paginas/AccesoPagina'
import EvaluacionPagina from './paginas/EvaluacionPagina'
import InicioPagina from './paginas/InicioPagina'
import LogrosPagina from './paginas/LogrosPagina'
import PanelPagina from './paginas/PanelPagina'
import PlanesPagina from './paginas/PlanesPagina'
import RecuperarPagina from './paginas/RecuperarPagina'
import RestablecerPagina from './paginas/RestablecerPagina'
import RutaPagina from './paginas/RutaPagina'

const paginasProtegidas = [
  { ruta: 'panel', elemento: <PanelPagina /> },
  { ruta: 'ruta', elemento: <RutaPagina /> },
  { ruta: 'logros', elemento: <LogrosPagina /> },
  { ruta: 'planes', elemento: <PlanesPagina /> },
]

function App() {
  return (
    <Routes>
      <Route path="/" element={<InicioPagina />} />
      <Route path="/acceso" element={<AccesoPagina />} />
      <Route path="/recuperar" element={<RecuperarPagina />} />
      <Route path="/restablecer" element={<RestablecerPagina />} />
      {paginasProtegidas.map((pagina) => (
        <Route
          key={pagina.ruta}
          path={`/${pagina.ruta}`}
          element={
            <RutaProtegida>
              <LayoutPrincipal>{pagina.elemento}</LayoutPrincipal>
            </RutaProtegida>
          }
        />
      ))}
      <Route
        path="/evaluacion/:tipo"
        element={
          <RutaProtegida>
            <LayoutPrincipal>
              <EvaluacionPagina />
            </LayoutPrincipal>
          </RutaProtegida>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
