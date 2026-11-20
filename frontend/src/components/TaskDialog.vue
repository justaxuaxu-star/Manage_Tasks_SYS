<script setup>
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import {
  createTask,
  getStatusHistory,
  getStatusTransitions,
  removeTask,
  taskApiError,
  updateTask,
} from '../api/tasks'
import { bumpTasks, closeDrawer, notify, store } from '../store'
import { ASSIGNEES, DEPARTMENTS, PRIORITIES, STATUSES, statusLabel, toPayload } from '../taskMeta'
import { hasPermission } from '../stores/auth'

const canDelete = hasPermission('task:delete')

const saving = ref(false)
const confirming = ref(false)
const formError = ref('')
const form = reactive(blankForm())
const allowedStatuses = ref([])
const statusHistory = ref([])

const statusOptions = computed(() => {
  if (!store.editing) return STATUSES
  const allowed = new Set(allowedStatuses.value.map((item) => item.value))
  allowed.add(form.status)
  return STATUSES.filter((item) => allowed.has(item.value))
})

function historyFromLabel(code) {
  if (!code) return '（新建）'
  return statusLabel(code)
}

function formatHistoryTime(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('zh-CN', { hour12: false })
}

function blankForm() {
  return {
    title: '',
    description: '',
    status: 'pending',
    priority: 'medium',
    assignee: '未分配',
    department: '产品部',
    due_date: '',
  }
}

function onKeydown(event) {
  if (event.key === 'Escape' && store.drawerOpen) closeDrawer()
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))

watch(
  () => store.drawerOpen,
  async (open) => {
    if (!open) {
      allowedStatuses.value = []
      statusHistory.value = []
      return
    }
    const task = store.editing
    Object.assign(form, task ? {
      title: task.title || '',
      description: task.description || '',
      status: task.status || 'pending',
      priority: task.priority || 'medium',
      assignee: task.assignee || '未分配',
      department: task.department || '综合部',
      due_date: task.due_date || '',
    } : blankForm())
    formError.value = ''
    confirming.value = false
    if (task?.id) {
      try {
        const [transitions, history] = await Promise.all([
          getStatusTransitions(task.id),
          getStatusHistory(task.id),
        ])
        allowedStatuses.value = transitions.allowed || []
        statusHistory.value = history || []
      } catch (err) {
        console.error(err)
        allowedStatuses.value = []
        statusHistory.value = []
      }
    }
  },
)

async function submit() {
  if (!form.title.trim()) {
    formError.value = '请填写任务标题'
    return
  }
  saving.value = true
  formError.value = ''
  try {
    if (store.editing?.id) {
      await updateTask(store.editing.id, toPayload(form))
      notify('任务已更新')
    } else {
      await createTask(toPayload(form))
      notify('任务已创建')
    }
    bumpTasks()
    closeDrawer()
  } catch (err) {
    console.error(err)
    formError.value = taskApiError(err, '保存失败，请检查后端服务')
    notify(formError.value, 'err')
  } finally {
    saving.value = false
  }
}

async function remove() {
  if (!confirming.value) {
    confirming.value = true
    return
  }
  saving.value = true
  try {
    await removeTask(store.editing.id)
    notify('任务已删除')
    bumpTasks()
    closeDrawer()
  } catch (err) {
    console.error(err)
    notify('删除失败', 'err')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <transition name="fade">
    <div v-if="store.drawerOpen" class="mask" @click="closeDrawer"></div>
  </transition>
  <transition name="slide">
    <aside v-if="store.drawerOpen" class="drawer" role="dialog" aria-modal="true" aria-labelledby="task-dialog-title">
      <header>
        <div>
          <p class="eyebrow">{{ store.editing ? '编辑工作项' : '新建工作项' }}</p>
          <h2 id="task-dialog-title">{{ store.editing ? '更新任务' : '创建任务' }}</h2>
        </div>
        <button class="btn tiny" type="button" @click="closeDrawer">关闭</button>
      </header>
      <form @submit.prevent="submit">
        <label class="field">
          <span>标题</span>
          <input v-model="form.title" maxlength="80" placeholder="需要交付的具体事项" />
        </label>
        <label class="field">
          <span>说明</span>
          <textarea v-model="form.description" maxlength="400" placeholder="背景、完成标准和需要协同的人"></textarea>
        </label>
        <div class="grid-2">
          <label class="field">
            <span>状态</span>
            <select v-model="form.status">
              <option v-for="item in statusOptions" :key="item.value" :value="item.value">{{ item.label }}</option>
            </select>
          </label>
          <label class="field">
            <span>优先级</span>
            <select v-model="form.priority">
              <option v-for="item in PRIORITIES" :key="item.value" :value="item.value">{{ item.label }}</option>
            </select>
          </label>
        </div>
        <div class="grid-2">
          <label class="field">
            <span>负责人</span>
            <select v-model="form.assignee">
              <option value="未分配">未分配</option>
              <option v-for="name in ASSIGNEES" :key="name" :value="name">{{ name }}</option>
            </select>
          </label>
          <label class="field">
            <span>部门</span>
            <select v-model="form.department">
              <option v-for="name in DEPARTMENTS" :key="name" :value="name">{{ name }}</option>
            </select>
          </label>
        </div>
        <label class="field">
          <span>截止日期</span>
          <input v-model="form.due_date" type="date" />
        </label>
        <section v-if="store.editing && statusHistory.length" class="status-history">
          <h3>状态流转记录</h3>
          <ul>
            <li v-for="item in statusHistory" :key="item.id">
              <span class="history-main">
                {{ historyFromLabel(item.from_status) }} → {{ historyFromLabel(item.to_status) }}
              </span>
              <span class="history-meta muted">
                {{ item.changed_by_name || '系统' }} · {{ formatHistoryTime(item.created_at) }}
              </span>
            </li>
          </ul>
        </section>
        <p v-if="formError" class="form-error">{{ formError }}</p>
        <button class="btn primary" type="submit" :disabled="saving">
          {{ saving ? '保存中...' : '保存任务' }}
        </button>
      </form>
      <footer>
        <button v-if="store.editing && canDelete" class="btn danger" type="button" :disabled="saving" @click="remove">
          {{ confirming ? '确认删除' : '删除任务' }}
        </button>
        <span v-else class="muted">保存后会出现在工作台、台账和看板中。</span>
        <div class="footer-actions">
          <button class="btn" type="button" @click="closeDrawer">取消</button>
        </div>
      </footer>
    </aside>
  </transition>
</template>
