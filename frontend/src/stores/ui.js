import { reactive } from 'vue'

const KEY_THEME = 'qtds_theme'
const KEY_SIDER = 'qtds_sider_collapsed'

export const ui = reactive({
  theme: 'dark',
  siderCollapsed: false,
})

function applyTheme() {
  document.documentElement.dataset.theme = ui.theme
  document.documentElement.style.colorScheme = ui.theme
}

export function initUi() {
  const saved = localStorage.getItem(KEY_THEME)
  if (saved === 'light' || saved === 'dark') ui.theme = saved
  ui.siderCollapsed = localStorage.getItem(KEY_SIDER) === '1'
  applyTheme()
}

export function toggleTheme() {
  ui.theme = ui.theme === 'dark' ? 'light' : 'dark'
  localStorage.setItem(KEY_THEME, ui.theme)
  applyTheme()
}

export function toggleSider() {
  ui.siderCollapsed = !ui.siderCollapsed
  localStorage.setItem(KEY_SIDER, ui.siderCollapsed ? '1' : '0')
}

export const isDark = () => ui.theme === 'dark'