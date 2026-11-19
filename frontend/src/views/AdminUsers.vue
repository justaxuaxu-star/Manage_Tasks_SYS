<script setup>
import { onMounted, ref } from 'vue'
import { createUser, listUsers, updateUser } from '../api/users'
import { listRoles } from '../api/roles'
import { hasPermission } from '../stores/auth'
import { notify } from '../store'

const users = ref([])
const roles = ref([])
const loading = ref(true)
const form = ref({
  username: '',
  password: '',
  display_name: '',
  department: '综合部',
  role_ids: [],
})

const canWrite = hasPermission('user:write')

async function load() {
  loading.value = true
  try {
    users.value = await listUsers()
    roles.value = await listRoles()
  } catch (err) {
    console.error(err)
    notify('用户数据加载失败', 'err')
  } finally {
    loading.value = false
  }
}

onMounted(load)

async function addUser() {
  if (!canWrite || !form.value.username || !form.value.password) return
  try {
    await createUser({
      ...form.value,
      role_ids: form.value.role_ids.map((id) => Number(id)),
    })
    form.value = { username: '', password: '', display_name: '', department: '综合部', role_ids: [] }
    notify('用户已创建')
    await load()
  } catch (err) {
    console.error(err)
    notify('创建失败', 'err')
  }
}

async function toggleActive(user) {
  if (!canWrite) return
  try {
    await updateUser(user.id, { is_active: !user.is_active })
    notify('用户状态已更新')
    await load()
  } catch (err) {
    console.error(err)
    notify('更新失败', 'err')
  }
}
</script>

<template>
  <section v-if="loading" class="panel skeleton"><i></i><i></i></section>
  <template v-else>
    <section v-if="canWrite" class="panel stack-block">
      <div class="panel-head"><h2>新建用户</h2></div>
      <div class="grid-2">
        <label class="field"><span>用户名</span><input v-model="form.username" /></label>
        <label class="field"><span>密码</span><input v-model="form.password" type="password" /></label>
        <label class="field"><span>姓名</span><input v-model="form.display_name" /></label>
        <label class="field"><span>部门</span><input v-model="form.department" /></label>
      </div>
      <label class="field">
        <span>角色</span>
        <select v-model="form.role_ids" multiple class="select multi">
          <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
        </select>
      </label>
      <button class="btn primary" type="button" @click="addUser">创建用户</button>
    </section>

    <section class="panel">
      <div class="panel-head"><h2>用户列表</h2></div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>用户名</th>
              <th>姓名</th>
              <th>部门</th>
              <th>角色</th>
              <th>状态</th>
              <th v-if="canWrite">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.username }}</td>
              <td>{{ user.display_name }}</td>
              <td>{{ user.department }}</td>
              <td>{{ user.roles.join('、') }}</td>
              <td>{{ user.is_active ? '启用' : '禁用' }}</td>
              <td v-if="canWrite">
                <button class="btn tiny" type="button" @click="toggleActive(user)">
                  {{ user.is_active ? '禁用' : '启用' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </template>
</template>

<style scoped>
.stack-block { margin-bottom: 14px; }
.select.multi { min-height: 90px; height: auto; }
</style>