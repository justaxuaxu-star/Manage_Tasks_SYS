import http from './http'
import { normalizeTask } from '../taskMeta'

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

export async function getStatusTransitions(taskId) {
  const { data } = await http.get(`/tasks/${taskId}/status-transitions`)
  return data
}

export async function getStatusHistory(taskId) {
  const { data } = await http.get(`/tasks/${taskId}/status-history`)
  return data
}

export function taskApiError(err, fallback = '操作失败') {
  const detail = err.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => d.msg || String(d)).join('；')
  return fallback
}