import http from './http'

export async function listUsers() {
  const { data } = await http.get('/users')
  return data
}

export async function createUser(payload) {
  const { data } = await http.post('/users', payload)
  return data
}

export async function updateUser(id, payload) {
  const { data } = await http.put(`/users/${id}`, payload)
  return data
}