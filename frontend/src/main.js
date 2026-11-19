import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { initUi } from './stores/ui'
import './style.css'

initUi()
createApp(App).use(router).mount('#app')