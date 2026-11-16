import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/Home.vue'
import TaskList from './components/TaskList.vue'
import TaskBoard from './components/TaskBoard.vue'
import './style.css'

const routes = [
  { path: '/', component: Home, meta: { title: '工作台', desc: '查看交付压力、逾期风险和团队负荷' } },
  { path: '/tasks', component: TaskList, meta: { title: '任务中心', desc: '检索、分派并更新全部工作项' } },
  { path: '/board', component: TaskBoard, meta: { title: '进度看板', desc: '按阶段拖拽任务，推进协作流转' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).mount('#app')
