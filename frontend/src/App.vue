<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TaskDialog from './components/TaskDialog.vue'
import { openCreate, store } from './store'

const route = useRoute()
const title = computed(() => route.meta.title || '工作台')
const desc = computed(() => route.meta.desc || '')

const links = [
  {
    to: '/',
    label: '工作台',
    icon: 'M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z',
  },
  {
    to: '/tasks',
    label: '任务中心',
    icon: 'M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01',
  },
  {
    to: '/board',
    label: '进度看板',
    icon: 'M7 4v16M12 4v10M17 4v13',
  },
]
</script>

<template>
  <div class="shell">
    <aside class="sider">
      <router-link class="brand" to="/">
        <span class="mark">枢</span>
        <span>
          <strong>任务中枢</strong>
          <small>企业工作台</small>
        </span>
      </router-link>

      <nav class="nav">
        <router-link v-for="link in links" :key="link.to" :to="link.to">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path :d="link.icon" />
          </svg>
          {{ link.label }}
        </router-link>
      </nav>

      <div class="sider-note">
        <strong>协作空间</strong>
        <p>按优先级、负责人和交付日期管理跨部门任务。</p>
      </div>
    </aside>

    <section class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">工作空间 / {{ title }}</p>
          <h1>{{ title }}</h1>
          <p class="muted">{{ desc }}</p>
        </div>
        <div class="top-actions">
          <button class="btn primary" type="button" @click="openCreate">新建任务</button>
          <div class="user">
            <span class="avatar" style="background:#1d4ed8">管</span>
            <span>
              <strong>系统管理员</strong>
              <small>本地账户</small>
            </span>
          </div>
        </div>
      </header>
      <main class="content">
        <router-view />
      </main>
    </section>

    <TaskDialog />
    <transition name="toast">
      <div v-if="store.toast" class="toast" :class="store.toast.type">
        {{ store.toast.text }}
      </div>
    </transition>
  </div>
</template>
