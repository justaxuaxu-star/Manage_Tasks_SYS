<script setup>
import { computed } from 'vue'
import { useTasks } from '../composables/useTasks'
import { openCreate, openEdit } from '../store'
import { hasPermission } from '../stores/auth'
import {
  formatDue,
  isDueSoon,
  isOverdue,
  priorityLabel,
  priorityRank,
  statusLabel,
} from '../taskMeta'

const { tasks, loading, error } = useTasks()

const now = new Date()
const todayText = `${now.toLocaleDateString('zh-CN', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
})} · ${now.toLocaleDateString('zh-CN', { weekday: 'long' })}`

const total = computed(() => tasks.value.length)
const done = computed(() => tasks.value.filter((task) => task.status === 'completed').length)
const active = computed(() => tasks.value.filter((task) => task.status === 'in_progress').length)
const review = computed(() => tasks.value.filter((task) => task.status === 'review').length)
const overdue = computed(() => tasks.value.filter(isOverdue).length)
const soon = computed(() => tasks.value.filter(isDueSoon).length)
const rate = computed(() => (total.value ? Math.round((done.value / total.value) * 100) : 0))

const focus = computed(() => {
  return [...tasks.value]
    .filter((task) => task.status !== 'completed')
    .sort((a, b) => {
      const overdueGap = Number(isOverdue(b)) - Number(isOverdue(a))
      if (overdueGap) return overdueGap
      const priorityGap = priorityRank(a.priority) - priorityRank(b.priority)
      if (priorityGap) return priorityGap
      return (a.due_date || '9999').localeCompare(b.due_date || '9999')
    })
    .slice(0, 6)
})

const priorityRows = computed(() => {
  return ['urgent', 'high', 'medium', 'low'].map((value) => {
    const count = tasks.value.filter((task) => task.priority === value).length
    return {
      value,
      label: priorityLabel(value),
      count,
      width: total.value ? Math.round((count / total.value) * 100) : 0,
    }
  })
})

const departments = computed(() => {
  const counts = new Map()
  tasks.value.forEach((task) => {
    if (task.status === 'completed') return
    counts.set(task.department, (counts.get(task.department) || 0) + 1)
  })
  const rows = [...counts.entries()].map(([name, count]) => ({ name, count }))
  const max = Math.max(1, ...rows.map((row) => row.count))
  return rows
    .sort((a, b) => b.count - a.count)
    .map((row) => ({ ...row, width: Math.round((row.count / max) * 100) }))
})
</script>

<template>
  <section v-if="loading" class="panel skeleton" aria-label="正在加载">
    <i></i><i></i><i></i>
  </section>
  <section v-else-if="error" class="panel error-box">{{ error }}</section>
  <template v-else>
    <section class="hero-panel">
      <div>
        <p class="eyebrow">{{ todayText }}</p>
        <h2>还有 {{ total - done }} 项工作未完成</h2>
        <p class="muted">其中 {{ overdue }} 项已逾期，{{ soon }} 项将在三天内到期。</p>
        <div class="meter" aria-hidden="true"><i :style="{ width: `${rate}%` }"></i></div>
        <p class="muted">完成率 {{ rate }}%，已交付 {{ done }} / {{ total }}</p>
      </div>
      <button v-if="hasPermission('task:create')" class="btn primary" type="button" @click="openCreate">安排新任务</button>
    </section>

    <section class="stats">
      <article class="stat">
        <p>全部任务</p>
        <strong>{{ total }}</strong>
        <span>当前工作空间</span>
      </article>
      <article class="stat">
        <p>进行中</p>
        <strong>{{ active }}</strong>
        <span>正在执行</span>
      </article>
      <article class="stat">
        <p>待验收</p>
        <strong>{{ review }}</strong>
        <span>等待确认结果</span>
      </article>
      <article class="stat" :class="{ alert: overdue }">
        <p>已逾期</p>
        <strong>{{ overdue }}</strong>
        <span>需要优先处理</span>
      </article>
    </section>

    <section class="split">
      <article class="panel">
        <div class="panel-head">
          <h2>优先处理</h2>
          <span class="muted">逾期、紧急和高优先级在前</span>
        </div>
        <p v-if="!focus.length" class="empty">当前没有待推进的任务。</p>
        <button v-for="task in focus" :key="task.id" class="row" type="button" @click="openEdit(task)">
          <span>
            <b>{{ task.title }}</b>
            <span class="meta">
              <span>{{ task.assignee }}</span>
              <span>{{ task.department }}</span>
              <span :class="{ overdue: isOverdue(task) }">{{ formatDue(task) }}</span>
            </span>
          </span>
          <span class="meta">
            <span class="tag" :class="task.priority">{{ priorityLabel(task.priority) }}</span>
            <span class="tag" :class="task.status">{{ statusLabel(task.status) }}</span>
          </span>
        </button>
      </article>

      <div class="stack">
        <article class="panel">
          <div class="panel-head">
            <h2>优先级分布</h2>
          </div>
          <div v-for="row in priorityRows" :key="row.value" class="bar-row">
            <span>{{ row.label }}</span>
            <span class="track"><i :style="{ width: `${row.width}%` }"></i></span>
            <b>{{ row.count }}</b>
          </div>
        </article>
        <article class="panel">
          <div class="panel-head">
            <h2>部门在办</h2>
            <span class="muted">不含已完成</span>
          </div>
          <p v-if="!departments.length" class="empty">暂无在办任务。</p>
          <div v-for="row in departments" :key="row.name" class="bar-row">
            <span>{{ row.name }}</span>
            <span class="track"><i :style="{ width: `${row.width}%` }"></i></span>
            <b>{{ row.count }}</b>
          </div>
        </article>
      </div>
    </section>
  </template>
</template>
