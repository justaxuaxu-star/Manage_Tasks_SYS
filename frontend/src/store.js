import { reactive } from 'vue'

export const store = reactive({
  drawerOpen: false,
  editing: null,
  version: 0,
  toast: null,
})

let toastTimer

export function openCreate() {
  store.editing = null
  store.drawerOpen = true
}

export function openEdit(task) {
  store.editing = { ...task }
  store.drawerOpen = true
}

export function closeDrawer() {
  store.drawerOpen = false
}

export function bumpTasks() {
  store.version += 1
}

export function notify(text, type = 'ok') {
  store.toast = { text, type }
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    store.toast = null
  }, 2600)
}
