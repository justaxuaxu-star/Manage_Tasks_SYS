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
      const status = err.response?.status
      const baseURL = err.config?.baseURL || 'http://localhost:8001'
      if (status === 404) {
        error.value = `接口返回 404，${baseURL} 上可能不是本任务系统后端。请用 8001 端口启动：uvicorn backend.main:app --reload --port 8001`
      } else if (err.code === 'ERR_NETWORK' || !err.response) {
        error.value = `无法连接任务服务。请确认已在 ${baseURL} 启动后端（默认 8001 端口）。`
      } else {
        error.value = `任务服务异常（HTTP ${status}）。请检查后端日志。`
      }
      notify('任务数据加载失败', 'err')
    } finally {
      loading.value = false
    }
  }

  onMounted(load)
  watch(() => store.version, load)

  return { tasks, loading, error, load }
}
