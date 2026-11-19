<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TaskDialog from './components/TaskDialog.vue'
import { openCreate, store } from './store'
import { auth, hasPermission, logout } from './stores/auth'
import { toggleSider, toggleTheme, ui } from './stores/ui'

const route = useRoute()
const title = computed(() => route.meta.title || '工作台')
const desc = computed(() => route.meta.desc || '')
const isPublic = computed(() => Boolean(route.meta.public))
const displayName = computed(() => auth.user?.display_name || '未登录')
const userInitial = computed(() => (auth.user?.display_name || '未').slice(0, 1))
const canCreate = computed(() => hasPermission('task:create'))

const links = computed(() => {
  const items = [
    { to: '/', label: '工作台', icon: 'M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z' },
    { to: '/tasks', label: '任务中心', icon: 'M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01' },
    { to: '/board', label: '进度看板', icon: 'M7 4v16M12 4v10M17 4v13' },
  ]
  if (hasPermission('user:read')) {
    items.push({ to: '/admin/users', label: '用户管理', icon: 'M12 5c-4 0-7 2-7 5s3 5 7 5 7-2 7-5-3-5-7-5z' })
  }
  if (hasPermission('role:read')) {
    items.push({ to: '/admin/roles', label: '角色权限', icon: 'M5 5h6v6H5zM13 5h6v6h-6zM5 13h6v6H5z' })
  }
  return items
})
</script>

<template>
  <router-view v-if="isPublic" />
  <div v-else class="shell" :class="{ 'sider-collapsed': ui.siderCollapsed }">
    <aside class="sider">
      <router-link class="brand" to="/" :title="ui.siderCollapsed ? '齐天大圣科技数据中心后台' : undefined">
        <span class="mark">圣</span>
        <span class="brand-text">
          <strong>齐天大圣科技</strong>
          <small>数据中心后台</small>
        </span>
      </router-link>

      <nav class="nav">
        <router-link v-for="link in links" :key="link.to" :to="link.to" :title="link.label">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path :d="link.icon" />
          </svg>
          <span class="nav-label">{{ link.label }}</span>
        </router-link>
      </nav>

      <div class="sider-note">
        <strong>数据中心运营</strong>
        <p>任务协同 · 权限治理 · 实时态势感知</p>
      </div>

      <button
        class="btn sider-toggle"
        type="button"
        :aria-label="ui.siderCollapsed ? '展开侧边栏' : '收起侧边栏'"
        @click="toggleSider"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path
            v-if="ui.siderCollapsed"
            d="M14 6l-6 6 6 6M20 6v12"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          />
          <path
            v-else
            d="M10 6l6 6-6 6M4 6v12"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          />
        </svg>
        <span class="nav-label">{{ ui.siderCollapsed ? '展开' : '收起' }}</span>
      </button>
    </aside>

    <section class="workspace">
      <div class="workspace-bg" aria-hidden="true">
        <span class="orb orb-a" />
        <span class="orb orb-b" />
        <span class="grid-mesh" />
      </div>
      <header class="topbar">
        <div>
          <p class="eyebrow">齐天大圣科技数据中心 · {{ title }}</p>
          <h1>{{ title }}</h1>
          <p class="muted">{{ desc }}</p>
        </div>
        <div class="top-actions">
          <button
            class="theme-switch"
            type="button"
            role="switch"
            :aria-checked="ui.theme === 'dark'"
            :aria-label="ui.theme === 'dark' ? '当前深色，切换到浅色' : '当前浅色，切换到深色'"
            @click="toggleTheme"
          >
            <span class="theme-switch-track" :class="{ 'is-dark': ui.theme === 'dark' }">
              <span class="theme-switch-slot">
                <svg class="theme-switch-icon sun" viewBox="0 0 24 24" aria-hidden="true">
                  <circle cx="12" cy="12" r="4" fill="currentColor" />
                  <path
                    d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"
                    stroke="currentColor"
                    stroke-width="1.8"
                    stroke-linecap="round"
                    fill="none"
                  />
                </svg>
              </span>
              <span class="theme-switch-slot">
                <svg class="theme-switch-icon moon" viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    d="M20 14.5A8.5 8.5 0 0 1 9.5 4 7 7 0 1 0 20 14.5z"
                    fill="currentColor"
                  />
                </svg>
              </span>
              <span class="theme-switch-thumb" />
            </span>
          </button>
          <button v-if="canCreate" class="btn primary" type="button" @click="openCreate">新建任务</button>
          <div class="user">
            <span class="avatar">{{ userInitial }}</span>
            <span>
              <strong>{{ displayName }}</strong>
              <small>{{ auth.user?.roles?.join('、') || '成员' }}</small>
            </span>
          </div>
          <button class="btn" type="button" @click="logout">退出</button>
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