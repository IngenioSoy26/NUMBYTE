import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { ProveedorAutenticacion } from './contexto/ContextoAutenticacion'
import { ProveedorJuego } from './contexto/ContextoJuego'
import './estilos/global.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <ProveedorAutenticacion>
        <ProveedorJuego>
          <App />
        </ProveedorJuego>
      </ProveedorAutenticacion>
    </BrowserRouter>
  </React.StrictMode>,
)
