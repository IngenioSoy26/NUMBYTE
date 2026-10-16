import axios from 'axios'

const urlBase = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

export const api = axios.create({
  baseURL: urlBase,
})

api.interceptors.request.use((configuracion: any) => {
  const token = localStorage.getItem('numbyte_token')
  if (token) {
    configuracion.headers.Authorization = `Bearer ${token}`
  }
  return configuracion
})
