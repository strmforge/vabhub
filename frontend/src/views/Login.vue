<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-form">
        <h2>登录 VabHub</h2>
        <el-form :model="form" :rules="rules" ref="loginForm">
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              prefix-icon="User"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          <el-form-item>
            <el-button 
              type="primary" 
              style="width: 100%" 
              :loading="loading"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api'

const router = useRouter()
const loginForm = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginForm.value) return
  
  try {
    await loginForm.value.validate()
    loading.value = true
    
    // 调用后端登录API
    const response = await authAPI.login({
      username: form.username,
      password: form.password
    })
    
    if (response.success) {
      localStorage.setItem('token', response.data.token)
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error('登录失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('登录失败: ' + error.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container {
  background: #fff;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-width: 400px;
}

.login-form h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}
</style>