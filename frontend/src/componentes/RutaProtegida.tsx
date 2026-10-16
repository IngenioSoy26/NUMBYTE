import type { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAutenticacion } from '../contexto/ContextoAutenticacion'

function RutaProtegida({ children }: { children: ReactNode }) {
  const { token, cargando } = useAutenticacion()

  if (cargando) {
    return <div className="pantalla-carga">Cargando NUMBYTE...</div>
  }

  if (!token) {
    return <Navigate to="/acceso" replace />
  }

  return <>{children}</>
}

export default RutaProtegida
