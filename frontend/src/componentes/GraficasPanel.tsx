import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { ResumenProgreso } from '../tipos'

function GraficasPanel({ resumen }: { resumen: ResumenProgreso }) {
  const datosPie = [
    { nombre: 'Fortalezas', valor: resumen.fortalezas.length || 1 },
    { nombre: 'Debilidades', valor: resumen.debilidades.length || 1 },
  ]

  return (
    <div className="bloque-graficas">
      <div className="grafica tarjeta-panel">
        <h3>Evolución del desempeño</h3>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={resumen.historial}>
            <defs>
              <linearGradient id="gradienteProgreso" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#16C6DF" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#16C6DF" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E6EEF8" />
            <XAxis dataKey="fecha" stroke="#6B7A90" />
            <YAxis domain={[0, 100]} stroke="#6B7A90" />
            <Tooltip />
            <Area type="monotone" dataKey="porcentaje" stroke="#0D4BA0" fill="url(#gradienteProgreso)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="grafica tarjeta-panel">
        <h3>Rendimiento por tema</h3>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={resumen.temas}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E6EEF8" />
            <XAxis dataKey="tema" stroke="#6B7A90" />
            <YAxis domain={[0, 100]} stroke="#6B7A90" />
            <Tooltip />
            <Bar dataKey="porcentaje" fill="#14A87A" radius={[10, 10, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grafica tarjeta-panel">
        <h3>Balance reciente</h3>
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie data={datosPie} dataKey="valor" nameKey="nombre" outerRadius={88} fill="#F5C542" />
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default GraficasPanel
