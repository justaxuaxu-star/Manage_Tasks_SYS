import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/Home.vue'
import TaskList from './components/TaskList.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/tasks', component: TaskList }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')