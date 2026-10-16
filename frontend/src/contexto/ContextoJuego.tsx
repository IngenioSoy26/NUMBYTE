import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import { api } from '../servicios/api'
import type { PlanPublico, ResumenGamificacion } from '../tipos'
import { useAutenticacion } from './ContextoAutenticacion'

interface ContextoJuegoType {
  resumen: ResumenGamificacion | null
  plan: PlanPublico | null
  cargando: boolean
  refrescar: () => Promise<void>
  activarPlus: () => Promise<PlanPublico>
  volverAGratis: () => Promise<PlanPublico>
}

const ContextoJuego = createContext<ContextoJuegoType | undefined>(undefined)

export function ProveedorJuego({ children }: { children: ReactNode }) {
  const { usuario } = useAutenticacion()
  const [resumen, setResumen] = useState<ResumenGamificacion | null>(null)
  const [plan, setPlan] = useState<PlanPublico | null>(null)
  const [cargando, setCargando] = useState(true)

  const refrescar = useCallback(async () => {
    if (!localStorage.getItem('numbyte_token')) {
      setResumen(null)
      setPlan(null)
      setCargando(false)
      return
    }
    try {
      const [respuestaResumen, respuestaPlan] = await Promise.all([
        api.get<ResumenGamificacion>('/gamificacion/resumen'),
        api.get<PlanPublico>('/planes/mi-plan'),
      ])
      setResumen(respuestaResumen.data)
      setPlan(respuestaPlan.data)
    } catch (error) {
      console.error(error)
    } finally {
      setCargando(false)
    }
  }, [])

  useEffect(() => {
    refrescar()
  }, [refrescar, usuario?.id])

  const activarPlus = async () => {
    const respuesta = await api.post<{ mensaje: string; plan: PlanPublico }>('/planes/activar-plus')
    setPlan(respuesta.data.plan)
    await refrescar()
    return respuesta.data.plan
  }

  const volverAGratis = async () => {
    const respuesta = await api.post<{ mensaje: string; plan: PlanPublico }>('/planes/volver-a-gratis')
    setPlan(respuesta.data.plan)
    await refrescar()
    return respuesta.data.plan
  }

  const valor = useMemo(
    () => ({ resumen, plan, cargando, refrescar, activarPlus, volverAGratis }),
    [resumen, plan, cargando, refrescar],
  )

  return <ContextoJuego.Provider value={valor}>{children}</ContextoJuego.Provider>
}

export function useJuego() {
  const contexto = useContext(ContextoJuego)
  if (!contexto) {
    throw new Error('useJuego debe usarse dentro del proveedor.')
  }
  return contexto
}
