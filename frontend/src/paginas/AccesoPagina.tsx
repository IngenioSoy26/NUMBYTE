import { FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAutenticacion } from '../contexto/ContextoAutenticacion'

function AccesoPagina() {
  const [modo, setModo] = useState<'ingreso' | 'registro'>('ingreso')
  const [nombre, setNombre] = useState('')
  const [correo, setCorreo] = useState('estudiante@numbyte.com')
  const [contrasena, setContrasena] = useState('Numbyte2026*')
  const [grado, setGrado] = useState('10')
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)

  const { ingresar, registrar } = useAutenticacion()
  const navegar = useNavigate()

  const manejarEnvio = async (evento: FormEvent) => {
    evento.preventDefault()
    setError('')
    setEnviando(true)
    try {
      if (modo === 'ingreso') {
        await ingresar(correo, contrasena)
      } else {
        await registrar(nombre, correo, contrasena, grado)
      }
      navegar('/panel')
    } catch (error: any) {
      setError(error?.response?.data?.detail || 'Ocurrió un error al procesar la solicitud.')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pagina-acceso">
      <div className="tarjeta-acceso">
        <div className="encabezado-acceso">
          <img src="/logo-numbyte.png" alt="NUMBYTE" className="logo-acceso" />
          <h2>{modo === 'ingreso' ? 'Bienvenido de nuevo' : 'Crea tu cuenta'}</h2>
          <p>Ingresa y continúa fortaleciendo tus matemáticas.</p>
        </div>

        <div className="interruptor-modo">
          <button className={modo === 'ingreso' ? 'activo' : ''} onClick={() => setModo('ingreso')}>
            Ingresar
          </button>
          <button className={modo === 'registro' ? 'activo' : ''} onClick={() => setModo('registro')}>
            Registrarse
          </button>
        </div>

        <form onSubmit={manejarEnvio} className="formulario-acceso">
          {modo === 'registro' && (
            <label>
              Nombre completo
              <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
            </label>
          )}

          <label>
            Correo electrónico
            <input type="email" value={correo} onChange={(e) => setCorreo(e.target.value)} required />
          </label>

          <label>
            Contraseña
            <input type="password" value={contrasena} onChange={(e) => setContrasena(e.target.value)} required />
          </label>

          {modo === 'ingreso' && (
            <Link to="/recuperar" className="enlace-ayuda">
              ¿Olvidaste tu contraseña?
            </Link>
          )}

          {modo === 'registro' && (
            <label>
              Grado
              <select value={grado} onChange={(e) => setGrado(e.target.value)}>
                {['6', '7', '8', '9', '10', '11'].map((valor) => (
                  <option key={valor} value={valor}>
                    {valor}
                  </option>
                ))}
              </select>
            </label>
          )}

          {error && <div className="mensaje-error">{error}</div>}

          <button className="boton-principal ancho-completo" type="submit" disabled={enviando}>
            {enviando ? 'Procesando...' : modo === 'ingreso' ? 'Ingresar' : 'Crear cuenta'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default AccesoPagina
