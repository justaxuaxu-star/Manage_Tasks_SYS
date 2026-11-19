import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'
import TaskList from './components/TaskList.vue'
import TaskBoard from './components/TaskBoard.vue'
import Login from './views/Login.vue'
import AdminUsers from './views/AdminUsers.vue'
import AdminRoles from './views/AdminRoles.vue'
import { auth, ensureAuth, hasPermission } from './stores/auth'

export const routes = [
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/', component: Home, meta: { title: '工作台', desc: '查看交付压力、逾期风险和团队负荷' } },
  { path: '/tasks', component: TaskList, meta: { title: '任务中心', desc: '检索、分派并更新全部工作项' } },
  { path: '/board', component: TaskBoard, meta: { title: '进度看板', desc: '按阶段拖拽任务，推进协作流转' } },
  { path: '/admin/users', component: AdminUsers, meta: { title: '用户管理', desc: '创建用户并分配角色', permission: 'user:read' } },
  { path: '/admin/roles', component: AdminRoles, meta: { title: '角色权限', desc: '维护角色与权限映射', permission: 'role:read' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  if (!auth.ready) await ensureAuth()
  if (to.meta.public) {
    if (auth.token && to.path === '/login') return '/'
    return true
  }
  if (!auth.token) return { path: '/login', query: { redirect: to.fullPath } }
  if (to.meta.permission && !hasPermission(to.meta.permission)) return '/'
  return true
})

export default router