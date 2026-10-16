import { FormEvent, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAutenticacion } from '../contexto/ContextoAutenticacion'

function RecuperarPagina() {
  const [correo, setCorreo] = useState('')
  const [mensaje, setMensaje] = useState('')
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)

  const { solicitarRecuperacion } = useAutenticacion()

  const manejarEnvio = async (evento: FormEvent) => {
    evento.preventDefault()
    setError('')
    setMensaje('')
    setEnviando(true)
    try {
      const respuesta = await solicitarRecuperacion(correo)
      setMensaje(respuesta)
    } catch (error: any) {
      setError(error?.response?.data?.detail || 'No se pudo procesar la solicitud.')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pagina-acceso">
      <div className="tarjeta-acceso">
        <div className="encabezado-acceso">
          <img src="/logo-numbyte.png" alt="NUMBYTE" className="logo-acceso" />
          <h2>Recuperar contraseña</h2>
          <p>Escribe tu correo y te enviaremos un enlace para crear una nueva contraseña.</p>
        </div>

        {mensaje ? (
          <>
            <div className="mensaje-exito">{mensaje}</div>
            <Link to="/acceso" className="boton-secundario ancho-completo enlace-boton">
              Volver a ingresar
            </Link>
          </>
        ) : (
          <form onSubmit={manejarEnvio} className="formulario-acceso">
            <label>
              Correo electrónico
              <input
                type="email"
                value={correo}
                onChange={(e) => setCorreo(e.target.value)}
                required
              />
            </label>

            {error && <div className="mensaje-error">{error}</div>}

            <button className="boton-principal ancho-completo" type="submit" disabled={enviando}>
              {enviando ? 'Enviando...' : 'Enviar enlace'}
            </button>

            <Link to="/acceso" className="enlace-ayuda centrado">
              Volver a ingresar
            </Link>
          </form>
        )}
      </div>
    </div>
  )
}

export default RecuperarPagina
