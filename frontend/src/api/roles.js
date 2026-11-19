import http from './http'

export async function listRoles() {
  const { data } = await http.get('/roles')
  return data
}

export async function listPermissions() {
  const { data } = await http.get('/roles/permissions')
  return data
}

export async function createRole(payload) {
  const { data } = await http.post('/roles', payload)
  return data
}

export async function updateRole(id, payload) {
  const { data } = await http.put(`/roles/${id}`, payload)
  return data
}