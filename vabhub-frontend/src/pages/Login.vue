<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>{{ $t('common.appName') }}</h1>
        <p>{{ $t('auth.loginTitle') }}</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">{{ $t('auth.username') }}</label>
          <input
            id="username"
            v-model="loginForm.username"
            type="text"
            required
            :placeholder="$t('auth.username')"
            :class="{ 'error': errors.username }"
          />
          <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
        </div>
        
        <div class="form-group">
          <label for="password">{{ $t('auth.password') }}</label>
          <input
            id="password"
            v-model="loginForm.password"
            type="password"
            required
            :placeholder="$t('auth.password')"
            :class="{ 'error': errors.password }"
          />
          <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
        </div>
        
        <div class="form-options">
          <label class="checkbox-label">
            <input type="checkbox" v-model="loginForm.rememberMe" />
            <span>{{ $t('auth.rememberMe') }}</span>
          </label>
          <a href="#" class="forgot-password">{{ $t('auth.forgotPassword') }}</a>
        </div>
        
        <button 
          type="submit" 
          class="login-btn"
          :disabled="loading"
          :class="{ 'loading': loading }"
        >
          <span v-if="loading">{{ $t('common.loading') }}</span>
          <span v-else>{{ $t('auth.loginButton') }}</span>
        </button>
      </form>
      
      <div class="login-footer">
        <p>{{ $t('auth.registerPrompt') }} <a href="#" @click.prevent="showRegister">{{ $t('auth.registerNow') }}</a></p>
      </div>
    </div>
    
    <!-- 注册模态框 -->
    <div v-if="showRegisterModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ $t('auth.registerTitle') }}</h2>
          <button @click="closeRegisterModal" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <p>{{ $t('auth.registerContactAdmin') }}</p>
        </div>
        <div class="modal-footer">
          <button @click="closeRegisterModal" class="btn btn-primary">{{ $t('common.ok') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        rememberMe: false
      },
      errors: {
        username: '',
        password: ''
      },
      loading: false,
      showRegisterModal: false
    }
  },
  mounted() {
    // 检查是否有记住的登录信息
    const savedUsername = localStorage.getItem('rememberedUsername')
    if (savedUsername) {
      this.loginForm.username = savedUsername
      this.loginForm.rememberMe = true
    }
  },
  methods: {
    async handleLogin() {
      // 验证表单
      if (!this.validateForm()) {
        return
      }
      
      this.loading = true
      
      try {
        const authStore = useAuthStore()
        
        // 调用认证API
        const success = await authStore.login({
          username: this.loginForm.username,
          password: this.loginForm.password
        })
        
        if (success) {
          // 记住用户名
          if (this.loginForm.rememberMe) {
            localStorage.setItem('rememberedUsername', this.loginForm.username)
          } else {
            localStorage.removeItem('rememberedUsername')
          }
          
          // 登录成功，跳转到仪表板
          this.$router.push('/dashboard')
        } else {
          this.errors.password = '用户名或密码错误'
        }
      } catch (error) {
        console.error('登录失败:', error)
        this.errors.password = '登录失败，请检查网络连接'
      } finally {
        this.loading = false
      }
    },
    
    validateForm() {
      this.errors = { username: '', password: '' }
      let isValid = true
      
      if (!this.loginForm.username.trim()) {
        this.errors.username = '请输入用户名'
        isValid = false
      }
      
      if (!this.loginForm.password) {
        this.errors.password = '请输入密码'
        isValid = false
      }
      
      return isValid
    },
    
    showRegister() {
      this.showRegisterModal = true
    },
    
    closeRegisterModal() {
      this.showRegisterModal = false
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.login-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.login-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.login-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-group input.error {
  border-color: #e74c3c;
}

.error-message {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #7f8c8d;
}

.checkbox-label input {
  margin-right: 0.5rem;
}

.forgot-password {
  color: #3498db;
  text-decoration: none;
  font-size: 0.875rem;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-btn {
  width: 100%;
  padding: 0.875rem 1rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.login-btn:hover:not(:disabled) {
  background: #2980b9;
}

.login-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.login-btn.loading {
  position: relative;
  color: transparent;
}

.login-btn.loading::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  top: 50%;
  left: 50%;
  margin-left: -10px;
  margin-top: -10px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.login-footer {
  text-align: center;
  color: #7f8c8d;
}

.login-footer a {
  color: #3498db;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 0;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #2c3e50;
}

.modal-body {
  padding: 2rem;
  color: #7f8c8d;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e9ecef;
  text-align: right;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 1rem;
  }
  
  .login-card {
    padding: 2rem;
  }
  
  .login-header h1 {
    font-size: 2rem;
  }
  
  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>