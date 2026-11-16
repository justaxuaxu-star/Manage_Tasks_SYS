<template>
    <div class="home">
      <h1>欢迎使用任务管理系统</h1>
      <p>这是一个使用FastAPI和Vue3构建的前后端分离应用</p>
      <router-link to="/tasks">查看任务列表</router-link>
    </div>
  </template>
  <script>
  export default {
    name: 'Home'
  }
  </script>
  <style scoped>
  .home {
    text-align: center;
    margin-top: 50px;
  }
  a {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #42b983;
    color: white;
    text-decoration: none;
    border-radius: 4px;
  }
  </style>