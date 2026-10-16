import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import { api } from '../servicios/api'
import type { Usuario } from '../tipos'

interface ContextoAutenticacionType {
  usuario: Usuario | null
  token: string | null
  cargando: boolean
  ingresar: (correo: string, contrasena: string) => Promise<void>
  registrar: (nombre: string, correo: string, contrasena: string, grado: string) => Promise<void>
  solicitarRecuperacion: (correo: string) => Promise<string>
  restablecerContrasena: (token: string, nuevaContrasena: string) => Promise<string>
  cerrarSesion: () => void
  refrescarPerfil: () => Promise<void>
}

const ContextoAutenticacion = createContext<ContextoAutenticacionType | undefined>(undefined)

export function ProveedorAutenticacion({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('numbyte_token'))
  const [usuario, setUsuario] = useState<Usuario | null>(null)
  const [cargando, setCargando] = useState(true)

  const refrescarPerfil = async () => {
    if (!localStorage.getItem('numbyte_token')) {
      setUsuario(null)
      setCargando(false)
      return
    }
    try {
      const respuesta = await api.get<Usuario>('/usuarios/yo')
      setUsuario(respuesta.data)
    } catch (error) {
      localStorage.removeItem('numbyte_token')
      setToken(null)
      setUsuario(null)
    } finally {
      setCargando(false)
    }
  }

  useEffect(() => {
    refrescarPerfil()
  }, [])

  const ingresar = async (correo: string, contrasena: string) => {
    const respuesta = await api.post<{ access_token: string }>('/autenticacion/ingresar', {
      correo,
      contrasena,
    })
    localStorage.setItem('numbyte_token', respuesta.data.access_token)
    setToken(respuesta.data.access_token)
    await refrescarPerfil()
  }

  const registrar = async (nombre: string, correo: string, contrasena: string, grado: string) => {
    await api.post('/autenticacion/registro', { nombre, correo, contrasena, grado })
    await ingresar(correo, contrasena)
  }

  const solicitarRecuperacion = async (correo: string) => {
    const respuesta = await api.post<{ mensaje: string }>('/autenticacion/recuperar', { correo })
    return respuesta.data.mensaje
  }

  const restablecerContrasena = async (token: string, nuevaContrasena: string) => {
    const respuesta = await api.post<{ mensaje: string }>('/autenticacion/restablecer', {
      token,
      nueva_contrasena: nuevaContrasena,
    })
    return respuesta.data.mensaje
  }

  const cerrarSesion = () => {
    localStorage.removeItem('numbyte_token')
    setToken(null)
    setUsuario(null)
  }

  const valor = useMemo(
    () => ({
      usuario,
      token,
      cargando,
      ingresar,
      registrar,
      solicitarRecuperacion,
      restablecerContrasena,
      cerrarSesion,
      refrescarPerfil,
    }),
    [usuario, token, cargando],
  )

  return <ContextoAutenticacion.Provider value={valor}>{children}</ContextoAutenticacion.Provider>
}

export function useAutenticacion() {
  const contexto = useContext(ContextoAutenticacion)
  if (!contexto) {
    throw new Error('useAutenticacion debe usarse dentro del proveedor.')
  }
  return contexto
}
