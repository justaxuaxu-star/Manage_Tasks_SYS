<script setup>
import { computed, ref } from 'vue'
import { removeTask, updateTask } from '../api/tasks'
import { useTasks } from '../composables/useTasks'
import { notify, openEdit } from '../store'
import {
  ASSIGNEES,
  PRIORITIES,
  STATUSES,
  avatarColor,
  avatarText,
  formatDue,
  isOverdue,
  priorityLabel,
  priorityRank,
  statusLabel,
  statusRank,
  taskCode,
  toPayload,
} from '../taskMeta'

const { tasks, loading, error } = useTasks()
const keyword = ref('')
const statusFilter = ref('all')
const priorityFilter = ref('all')
const ownerFilter = ref('all')
const sortBy = ref('priority')
const confirmingId = ref(null)

const owners = computed(() => {
  const values = new Set(ASSIGNEES)
  tasks.value.forEach((task) => values.add(task.assignee))
  return [...values]
})

const visible = computed(() => {
  const text = keyword.value.trim().toLowerCase()
  return tasks.value
    .filter((task) => {
      const haystack = `${task.title} ${task.description} ${task.assignee} ${task.department}`.toLowerCase()
      const matchesText = !text || haystack.includes(text)
      const matchesStatus = statusFilter.value === 'all' || task.status === statusFilter.value
      const matchesPriority = priorityFilter.value === 'all' || task.priority === priorityFilter.value
      const matchesOwner = ownerFilter.value === 'all' || task.assignee === ownerFilter.value
      return matchesText && matchesStatus && matchesPriority && matchesOwner
    })
    .sort((a, b) => {
      if (sortBy.value === 'due') return (a.due_date || '9999').localeCompare(b.due_date || '9999')
      if (sortBy.value === 'status') return statusRank(a.status) - statusRank(b.status)
      return priorityRank(a.priority) - priorityRank(b.priority)
    })
})

const filtering = computed(() => {
  return keyword.value || statusFilter.value !== 'all' || priorityFilter.value !== 'all' || ownerFilter.value !== 'all'
})

function clearFilters() {
  keyword.value = ''
  statusFilter.value = 'all'
  priorityFilter.value = 'all'
  ownerFilter.value = 'all'
}

async function changeStatus(task, status) {
  const previous = { ...task }
  task.status = status
  task.completed = status === 'completed'
  try {
    await updateTask(task.id, toPayload(task))
    notify(`已更新为${statusLabel(status)}`)
  } catch (err) {
    console.error(err)
    Object.assign(task, previous)
    notify('状态更新失败', 'err')
  }
}

async function remove(task) {
  if (confirmingId.value !== task.id) {
    confirmingId.value = task.id
    return
  }
  try {
    await removeTask(task.id)
    tasks.value = tasks.value.filter((item) => item.id !== task.id)
    notify('任务已删除')
  } catch (err) {
    console.error(err)
    notify('删除失败', 'err')
  } finally {
    confirmingId.value = null
  }
}
</script>

<template>
  <div class="toolbar">
    <input v-model="keyword" class="search" type="search" placeholder="搜索标题、说明、负责人或部门" />
    <select v-model="statusFilter" class="select" aria-label="按状态筛选">
      <option value="all">全部状态</option>
      <option v-for="item in STATUSES" :key="item.value" :value="item.value">{{ item.label }}</option>
    </select>
    <select v-model="priorityFilter" class="select" aria-label="按优先级筛选">
      <option value="all">全部优先级</option>
      <option v-for="item in PRIORITIES" :key="item.value" :value="item.value">{{ item.label }}</option>
    </select>
    <select v-model="ownerFilter" class="select" aria-label="按负责人筛选">
      <option value="all">全部负责人</option>
      <option v-for="name in owners" :key="name" :value="name">{{ name }}</option>
    </select>
    <select v-model="sortBy" class="select" aria-label="排序">
      <option value="priority">按优先级</option>
      <option value="due">按截止日期</option>
      <option value="status">按状态</option>
    </select>
    <button v-if="filtering" class="btn" type="button" @click="clearFilters">清空筛选</button>
  </div>

  <section v-if="loading" class="panel skeleton"><i></i><i></i><i></i></section>
  <section v-else-if="error" class="panel error-box">{{ error }}</section>
  <section v-else class="panel">
    <div class="panel-head">
      <h2>任务台账</h2>
      <span class="muted">显示 {{ visible.length }} / {{ tasks.length }}</span>
    </div>
    <p v-if="!visible.length" class="empty">没有符合条件的任务。</p>
    <div v-else class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>编号</th>
            <th>任务</th>
            <th>优先级</th>
            <th>状态</th>
            <th>负责人</th>
            <th>部门</th>
            <th>截止日期</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in visible" :key="task.id">
            <td class="muted">{{ taskCode(task.id) }}</td>
            <td class="task-title">
              <button class="title-btn" type="button" @click="openEdit(task)">{{ task.title }}</button>
              <p class="clamp">{{ task.description || '暂无说明' }}</p>
            </td>
            <td><span class="tag" :class="task.priority">{{ priorityLabel(task.priority) }}</span></td>
            <td>
              <select :value="task.status" class="select" aria-label="更改状态" @change="changeStatus(task, $event.target.value)">
                <option v-for="item in STATUSES" :key="item.value" :value="item.value">{{ item.label }}</option>
              </select>
            </td>
            <td>
              <span class="person">
                <span class="avatar" :style="{ background: avatarColor(task.assignee) }">{{ avatarText(task.assignee) }}</span>
                {{ task.assignee }}
              </span>
            </td>
            <td>{{ task.department }}</td>
            <td>
              <span class="tag" :class="{ overdue: isOverdue(task) }">{{ formatDue(task) }}</span>
            </td>
            <td>
              <div class="actions">
                <button class="btn tiny" type="button" @click="openEdit(task)">编辑</button>
                <button class="btn tiny danger" type="button" @click="remove(task)">
                  {{ confirmingId === task.id ? '确认删除' : '删除' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
