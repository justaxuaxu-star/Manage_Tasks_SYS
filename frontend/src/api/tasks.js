import axios from 'axios'
import { normalizeTask } from '../taskMeta'

const http = axios.create({
  baseURL: 'http://localhost:8000',
})

export async function listTasks() {
  const { data } = await http.get('/tasks')
  return data.map(normalizeTask)
}

export async function createTask(payload) {
  const { data } = await http.post('/tasks', payload)
  return normalizeTask(data)
}

export async function updateTask(id, payload) {
  const { data } = await http.put(`/tasks/${id}`, payload)
  return normalizeTask(data)
}

export async function removeTask(id) {
  await http.delete(`/tasks/${id}`)
}
