import { FormEvent, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useAutenticacion } from '../contexto/ContextoAutenticacion'

function RestablecerPagina() {
  const [parametros] = useSearchParams()
  const token = parametros.get('token') || ''

  const [contrasena, setContrasena] = useState('')
  const [confirmacion, setConfirmacion] = useState('')
  const [mensaje, setMensaje] = useState('')
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)

  const { restablecerContrasena } = useAutenticacion()

  const manejarEnvio = async (evento: FormEvent) => {
    evento.preventDefault()
    setError('')
    if (contrasena !== confirmacion) {
      setError('Las contraseñas no coinciden.')
      return
    }
    setEnviando(true)
    try {
      const respuesta = await restablecerContrasena(token, contrasena)
      setMensaje(respuesta)
    } catch (error: any) {
      setError(error?.response?.data?.detail || 'No se pudo restablecer la contraseña.')
    } finally {
      setEnviando(false)
    }
  }

  const sinToken = !token

  return (
    <div className="pagina-acceso">
      <div className="tarjeta-acceso">
        <div className="encabezado-acceso">
          <img src="/logo-numbyte.png" alt="NUMBYTE" className="logo-acceso" />
          <h2>Nueva contraseña</h2>
          <p>Crea una nueva contraseña para tu cuenta NUMBYTE.</p>
        </div>

        {mensaje ? (
          <>
            <div className="mensaje-exito">{mensaje}</div>
            <Link to="/acceso" className="boton-principal ancho-completo enlace-boton">
              Iniciar sesión
            </Link>
          </>
        ) : sinToken ? (
          <>
            <div className="mensaje-error">
              El enlace no es válido. Solicita uno nuevo desde la pantalla de acceso.
            </div>
            <Link to="/recuperar" className="boton-secundario ancho-completo enlace-boton">
              Solicitar un nuevo enlace
            </Link>
          </>
        ) : (
          <form onSubmit={manejarEnvio} className="formulario-acceso">
            <label>
              Nueva contraseña
              <input
                type="password"
                value={contrasena}
                onChange={(e) => setContrasena(e.target.value)}
                minLength={8}
                required
              />
            </label>

            <label>
              Confirmar contraseña
              <input
                type="password"
                value={confirmacion}
                onChange={(e) => setConfirmacion(e.target.value)}
                minLength={8}
                required
              />
            </label>

            {error && <div className="mensaje-error">{error}</div>}

            <button className="boton-principal ancho-completo" type="submit" disabled={enviando}>
              {enviando ? 'Guardando...' : 'Guardar contraseña'}
            </button>
          </form>
        )}
      </div>
    </div>
  )
}

export default RestablecerPagina
