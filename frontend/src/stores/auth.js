import { computed, reactive } from 'vue'
import { fetchMe, login as loginApi } from '../api/auth'

const TOKEN_KEY = 'task_access_token'

export const auth = reactive({
  token: localStorage.getItem(TOKEN_KEY) || '',
  user: null,
  ready: false,
})

export const permissions = computed(() => auth.user?.permissions || [])

export function hasPermission(code) {
  const roles = auth.user?.roles || []
  if (roles.includes('admin')) return true
  return permissions.value.includes(code)
}

export function setToken(token) {
  auth.token = token || ''
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

export async function ensureAuth() {
  if (!auth.token) {
    auth.ready = true
    return
  }
  try {
    auth.user = await fetchMe()
  } catch {
    setToken('')
    auth.user = null
  } finally {
    auth.ready = true
  }
}

export async function login(username, password) {
  const data = await loginApi(username, password)
  setToken(data.access_token)
  auth.user = data.user
  return data.user
}

export function logout() {
  setToken('')
  auth.user = null
  const path = window.location.pathname
  if (path !== '/login') window.location.assign('/login')
}