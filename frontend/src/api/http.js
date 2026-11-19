import axios from 'axios'
import { auth, logout, setToken } from '../stores/auth'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001',
})

http.interceptors.request.use((config) => {
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      setToken('')
      auth.user = null
      if (!window.location.pathname.startsWith('/login')) {
        logout()
      }
    }
    return Promise.reject(error)
  },
)

export default http