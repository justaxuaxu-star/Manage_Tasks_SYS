<script setup>
import { computed, ref } from 'vue'
import { taskApiError, updateTask } from '../api/tasks'
import { useTasks } from '../composables/useTasks'
import { notify, openEdit } from '../store'
import { hasPermission } from '../stores/auth'

const canDrag = hasPermission('task:change_status')
import {
  STATUSES,
  avatarColor,
  avatarText,
  formatDue,
  isOverdue,
  priorityLabel,
  taskCode,
  toPayload,
} from '../taskMeta'

const { tasks, loading, error } = useTasks()
const keyword = ref('')
const draggingId = ref(null)
const overStatus = ref('')

const columns = computed(() => {
  const text = keyword.value.trim().toLowerCase()
  return STATUSES.map((status) => ({
    ...status,
    tasks: tasks.value.filter((task) => {
      const haystack = `${task.title} ${task.assignee} ${task.department}`.toLowerCase()
      return task.status === status.value && (!text || haystack.includes(text))
    }),
  }))
})

function onDragStart(event, task) {
  if (!canDrag) {
    event.preventDefault()
    return
  }
  draggingId.value = task.id
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/plain', String(task.id))
}

function onDragEnd() {
  draggingId.value = null
  overStatus.value = ''
}

function onColumnLeave(event, status) {
  const next = event.relatedTarget
  if (next && event.currentTarget.contains(next)) return
  if (overStatus.value === status) overStatus.value = ''
}

async function onDrop(status) {
  const task = tasks.value.find((item) => item.id === draggingId.value)
  overStatus.value = ''
  draggingId.value = null
  if (!task || task.status === status) return
  const previous = { ...task }
  task.status = status
  task.completed = status === 'completed'
  try {
    await updateTask(task.id, toPayload(task))
    notify('任务阶段已更新')
  } catch (err) {
    console.error(err)
    Object.assign(task, previous)
    notify(taskApiError(err, '不允许移动到该阶段'), 'err')
  }
}
</script>

<template>
  <div class="toolbar">
    <input v-model="keyword" class="search" type="search" placeholder="在看板中搜索任务或负责人" />
  </div>

  <section v-if="loading" class="panel skeleton"><i></i><i></i><i></i></section>
  <section v-else-if="error" class="panel error-box">{{ error }}</section>
  <div v-else class="board-scroll">
    <div class="board">
      <section
        v-for="column in columns"
        :key="column.value"
        class="column"
        :class="{ over: overStatus === column.value }"
        @dragover.prevent="overStatus = column.value"
        @dragleave="onColumnLeave($event, column.value)"
        @drop="onDrop(column.value)"
      >
        <header class="column-head">
          <h2>{{ column.label }}</h2>
          <span class="count">{{ column.tasks.length }}</span>
        </header>
        <p v-if="!column.tasks.length" class="empty">暂无任务</p>
        <article
          v-for="task in column.tasks"
          :key="task.id"
          class="card"
          :class="{ dragging: draggingId === task.id }"
          :draggable="canDrag"
          @dragstart="onDragStart($event, task)"
          @dragend="onDragEnd"
        >
          <header>
            <span class="tag" :class="task.priority">{{ priorityLabel(task.priority) }}</span>
            <span class="muted">{{ taskCode(task.id) }}</span>
          </header>
          <h3>{{ task.title }}</h3>
          <p class="clamp">{{ task.description || '暂无说明' }}</p>
          <footer>
            <span class="person">
              <span class="avatar" :style="{ background: avatarColor(task.assignee) }">{{ avatarText(task.assignee) }}</span>
              {{ task.assignee }}
            </span>
            <span class="tag" :class="{ overdue: isOverdue(task) }">{{ formatDue(task) }}</span>
          </footer>
          <button class="btn tiny" type="button" @click="openEdit(task)">查看详情</button>
        </article>
      </section>
    </div>
  </div>
</template>
