<template>
    <div class="task-list">
      <h1>任务列表</h1>
      <div class="task-form">
        <input v-model="newTask.title" placeholder="任务标题" />
        <textarea v-model="newTask.description" placeholder="任务描述"></textarea>
        <button @click="addTask">添加任务</button>
      </div>
  
      <div v-if="loading">加载中...</div>
      <div v-else>
        <div v-for="task in tasks" :key="task.id" class="task-item">
          <h3>{{ task.title }} 
            <span :class="['status', {completed: task.completed}]">
              {{ task.completed ? '已完成' : '未完成' }}
            </span>
          </h3>
          <p>{{ task.description }}</p>
          <div class="actions">
            <button @click="toggleTask(task)" :class="{complete: !task.completed, undo: task.completed}">
              {{ task.completed ? '撤销' : '完成' }}
            </button>
            <button @click="deleteTask(task.id)" class="delete">删除</button>
          </div>
        </div>
      </div>
  
      <div class="back-link">
        <router-link to="/">返回首页</router-link>
      </div>
    </div>
  </template>
  <script>
  import axios from 'axios'
  
  const API_BASE_URL = 'http://localhost:8000'
  
  export default {
    name: 'TaskList',
    data() {
      return {
        tasks: [],
        newTask: {
          title: '',
          description: ''
        },
        loading: true
      }
    },
    async mounted() {
      await this.fetchTasks()
    },
    methods: {
      async fetchTasks() {
        try {
          const response = await axios.get(`${API_BASE_URL}/tasks`)
          this.tasks = response.data
          this.loading = false
        } catch (error) {
          console.error('获取任务失败:', error)
          this.loading = false
        }
      },
  
      async addTask() {
        if (!this.newTask.title.trim()) return
  
        try {
          const response = await axios.post(`${API_BASE_URL}/tasks`, this.newTask)
          this.tasks.push(response.data)
          this.newTask = { title: '', description: '' }
        } catch (error) {
          console.error('添加任务失败:', error)
        }
      },
  
      async toggleTask(task) {
        try {
          const updatedTask = {
            ...task,
            completed: !task.completed
          }
          await axios.put(`${API_BASE_URL}/tasks/${task.id}`, updatedTask)
          task.completed = !task.completed
        } catch (error) {
          console.error('更新任务失败:', error)
        }
      },
  
      async deleteTask(id) {
        try {
          await axios.delete(`${API_BASE_URL}/tasks/${id}`)
          this.tasks = this.tasks.filter(task => task.id !== id)
        } catch (error) {
          console.error('删除任务失败:', error)
        }
      }
    }
  }
  </script>
  <style scoped>
  .task-list {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .task-form {
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 4px;
  }
  
  .task-form input,
  .task-form textarea {
    width: 100%;
    margin-bottom: 10px;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .task-form button {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .task-item {
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 4px;
  }
  
  .status {
    font-size: 0.8em;
    padding: 2px 6px;
    border-radius: 4px;
    background-color: #f0ad4e;
    color: white;
  }
  
  .status.completed {
    background-color: #5cb85c;
  }
  
  .actions {
    margin-top: 10px;
  }
  
  .actions button {
    margin-right: 10px;
    padding: 5px 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .complete {
    background-color: #5cb85c;
    color: white;
  }
  
  .undo {
    background-color: #f0ad4e;
    color: white;
  }
  
  .delete {
    background-color: #d9534f;
    color: white;
  }
  
  .back-link {
    margin-top: 20px;
  }
  
  .back-link a {
    color: #42b983;
    text-decoration: none;
  }
  </style>
  