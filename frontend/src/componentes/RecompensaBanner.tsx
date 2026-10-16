import type { Recompensa } from '../tipos'

function RecompensaBanner({ recompensa }: { recompensa: Recompensa }) {
  const nada = recompensa.puntos_ganados === 0 && recompensa.insignias_nuevas.length === 0
  if (nada) {
    return (
      <div className="aviso-recompensa aviso-neutro">
        ¡Ya habías completado esta parte! Sigue avanzando en tu ruta.
      </div>
    )
  }

  return (
    <div className="aviso-recompensa">
      <div className="aviso-recompensa-encabezado">
        <strong>¡Buen trabajo!</strong>
        {recompensa.subio_nivel && <span className="chip-subida">¡Subiste de nivel!</span>}
      </div>

      <div className="aviso-recompensa-logros">
        {recompensa.puntos_ganados > 0 && (
          <span className="chip-logro">+{recompensa.puntos_ganados} puntos</span>
        )}
        {recompensa.monedas_ganadas > 0 && (
          <span className="chip-logro">+{recompensa.monedas_ganadas} monedas</span>
        )}
        {recompensa.insignias_nuevas.map((insignia) => (
          <span key={insignia.codigo} className="chip-logro">
            {insignia.icono} Insignia: {insignia.nombre}
          </span>
        ))}
        {recompensa.misiones_completadas.map((mision) => (
          <span key={mision.codigo} className="chip-logro">
            Misión cumplida: {mision.titulo}
          </span>
        ))}
      </div>
    </div>
  )
}

export default RecompensaBanner
