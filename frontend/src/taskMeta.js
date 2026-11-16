export const STATUSES = [
  { value: 'pending', label: '待处理' },
  { value: 'in_progress', label: '进行中' },
  { value: 'review', label: '待验收' },
  { value: 'completed', label: '已完成' },
]

export const PRIORITIES = [
  { value: 'urgent', label: '紧急' },
  { value: 'high', label: '高' },
  { value: 'medium', label: '中' },
  { value: 'low', label: '低' },
]

export const ASSIGNEES = ['林晓晨', '周予安', '陈可', '赵启明', '苏晚']

export const DEPARTMENTS = ['产品部', '研发部', '设计部', '运营部', '综合部']

const PRIORITY_RANK = { urgent: 0, high: 1, medium: 2, low: 3 }
const STATUS_RANK = { pending: 0, in_progress: 1, review: 2, completed: 3 }

export function statusLabel(value) {
  return STATUSES.find((item) => item.value === value)?.label || '待处理'
}

export function priorityLabel(value) {
  return PRIORITIES.find((item) => item.value === value)?.label || '中'
}

export function priorityRank(value) {
  return PRIORITY_RANK[value] ?? 2
}

export function statusRank(value) {
  return STATUS_RANK[value] ?? 0
}

export function taskCode(id) {
  return `TMS-${String(id).padStart(3, '0')}`
}

export function dueInDays(task) {
  if (!task.due_date) return null
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const due = new Date(`${task.due_date}T00:00:00`)
  return Math.round((due - today) / 86400000)
}

export function isOverdue(task) {
  const days = dueInDays(task)
  return days !== null && days < 0 && task.status !== 'completed'
}

export function isDueSoon(task) {
  const days = dueInDays(task)
  return days !== null && days >= 0 && days <= 3 && task.status !== 'completed'
}

export function formatShort(value) {
  if (!value) return '未排期'
  const [, month, day] = value.split('-')
  return `${Number(month)}月${Number(day)}日`
}

export function formatDue(task) {
  const days = dueInDays(task)
  if (days === null) return '未排期'
  if (task.status === 'completed') return formatShort(task.due_date)
  if (days < 0) return `逾期 ${Math.abs(days)} 天`
  if (days === 0) return '今天到期'
  if (days === 1) return '明天到期'
  return formatShort(task.due_date)
}

export function normalizeTask(task) {
  const status = task.status || (task.completed ? 'completed' : 'pending')
  return {
    ...task,
    description: task.description || '',
    status,
    priority: task.priority || 'medium',
    assignee: task.assignee || '未分配',
    department: task.department || '综合部',
    due_date: task.due_date || '',
    completed: status === 'completed',
  }
}

export function toPayload(form) {
  return {
    title: form.title.trim(),
    description: form.description.trim(),
    status: form.status,
    priority: form.priority,
    assignee: form.assignee,
    department: form.department,
    due_date: form.due_date || null,
    completed: form.status === 'completed',
  }
}

const AVATAR_COLORS = ['#1d4ed8', '#0f766e', '#b45309', '#6d28d9', '#be123c']

export function avatarColor(name = '') {
  const total = [...name].reduce((sum, char) => sum + char.charCodeAt(0), 0)
  return AVATAR_COLORS[total % AVATAR_COLORS.length]
}

export function avatarText(name = '') {
  return name.trim().slice(0, 1) || '未'
}
