import { onMounted, ref, watch } from 'vue'
import { listTasks } from '../api/tasks'
import { notify, store } from '../store'

export function useTasks() {
  const tasks = ref([])
  const loading = ref(true)
  const error = ref('')

  async function load() {
    if (!tasks.value.length) loading.value = true
    error.value = ''
    try {
      tasks.value = await listTasks()
    } catch (err) {
      console.error(err)
      error.value = '无法连接任务服务。请确认后端已在 8000 端口启动。'
      notify('任务数据加载失败', 'err')
    } finally {
      loading.value = false
    }
  }

  onMounted(load)
  watch(() => store.version, load)

  return { tasks, loading, error, load }
}
