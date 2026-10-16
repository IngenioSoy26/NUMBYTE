import { Link } from 'react-router-dom'

function TarjetaAccion({
  titulo,
  descripcion,
  ruta,
}: {
  titulo: string
  descripcion: string
  ruta: string
}) {
  return (
    <div className="tarjeta-accion">
      <h3>{titulo}</h3>
      <p>{descripcion}</p>
      <Link to={ruta}>Comenzar</Link>
    </div>
  )
}

export default TarjetaAccion
