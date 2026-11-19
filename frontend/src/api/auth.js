import http from './http'

export async function login(username, password) {
  const { data } = await http.post('/auth/login', { username, password })
  return data
}

export async function fetchMe() {
  const { data } = await http.get('/auth/me')
  return data
}