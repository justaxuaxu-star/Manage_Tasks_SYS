<script setup>
import { onMounted, ref } from 'vue'
import { createRole, listPermissions, listRoles, updateRole } from '../api/roles'
import { hasPermission } from '../stores/auth'
import { notify } from '../store'

const roles = ref([])
const permissions = ref([])
const loading = ref(true)
const editingId = ref(null)
const picked = ref([])
const form = ref({ code: '', name: '' })

const canWrite = hasPermission('role:write')

async function load() {
  loading.value = true
  try {
    roles.value = await listRoles()
    permissions.value = await listPermissions()
  } catch (err) {
    console.error(err)
    notify('角色数据加载失败', 'err')
  } finally {
    loading.value = false
  }
}

onMounted(load)

function editRole(role) {
  editingId.value = role.id
  const codes = new Set(role.permissions)
  picked.value = permissions.value.filter((p) => codes.has(p.code)).map((p) => p.id)
}

async function saveRole() {
  if (!canWrite || editingId.value == null) return
  try {
    await updateRole(editingId.value, { permission_ids: picked.value })
    editingId.value = null
    notify('角色权限已保存')
    await load()
  } catch (err) {
    console.error(err)
    notify('保存失败', 'err')
  }
}

async function addRole() {
  if (!canWrite || !form.value.code) return
  try {
    await createRole({ ...form.value, permission_ids: picked.value })
    form.value = { code: '', name: '' }
    picked.value = []
    notify('角色已创建')
    await load()
  } catch (err) {
    console.error(err)
    notify('创建失败', 'err')
  }
}
</script>

<template>
  <section v-if="loading" class="panel skeleton"><i></i><i></i></section>
  <template v-else>
    <section class="panel stack-block">
      <div class="panel-head"><h2>角色列表</h2></div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>编码</th>
              <th>名称</th>
              <th>权限数</th>
              <th v-if="canWrite">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="role in roles" :key="role.id">
              <td>{{ role.code }}</td>
              <td>{{ role.name }}</td>
              <td>{{ role.permissions.length }}</td>
              <td v-if="canWrite">
                <button class="btn tiny" type="button" @click="editRole(role)">配置权限</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-if="canWrite" class="panel">
      <div class="panel-head">
        <h2>{{ editingId ? '编辑角色权限' : '新建角色' }}</h2>
      </div>
      <div v-if="!editingId" class="grid-2">
        <label class="field"><span>编码</span><input v-model="form.code" /></label>
        <label class="field"><span>名称</span><input v-model="form.name" /></label>
      </div>
      <div class="perm-grid">
        <label v-for="perm in permissions" :key="perm.id" class="perm-item">
          <input v-model="picked" type="checkbox" :value="perm.id" />
          <span>{{ perm.name }}</span>
          <small class="muted">{{ perm.code }}</small>
        </label>
      </div>
      <button v-if="editingId" class="btn primary" type="button" @click="saveRole">保存权限</button>
      <button v-else class="btn primary" type="button" @click="addRole">创建角色</button>
    </section>
  </template>
</template>

<style scoped>
.stack-block { margin-bottom: 14px; }
.perm-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 8px;
  margin-bottom: 12px;
}
.perm-item {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 8px;
  border: 1px solid #eef2f7;
  border-radius: 8px;
}
.perm-item small { margin-left: auto; }
</style>