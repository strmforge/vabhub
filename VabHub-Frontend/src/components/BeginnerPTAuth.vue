<template>
  <div class="beginner-auth-container">
    <!-- 认证引导页面 -->
    <div v-if="currentStep === 'welcome'" class="welcome-step">
      <div class="welcome-header">
        <h1>🎯 PT站点认证助手</h1>
        <p class="subtitle">为初级用户提供简化的PT站点认证流程</p>
      </div>
      
      <div class="welcome-content">
        <div class="info-card">
          <h3>📋 认证前准备</h3>
          <ul>
            <li>✅ 确保您已成功注册PT站点</li>
            <li>✅ 准备好账号和密码</li>
            <li>✅ 确保网络连接正常</li>
            <li>✅ 建议使用密码管理器</li>
          </ul>
        </div>
        
        <div class="estimated-info">
          <div class="info-item">
            <span class="label">预计时间：</span>
            <span class="value">5-10分钟</span>
          </div>
          <div class="info-item">
            <span class="label">难度等级：</span>
            <span class="value">简单</span>
          </div>
        </div>
        
        <button @click="startAuth" class="start-button">
          开始认证
        </button>
      </div>
    </div>

    <!-- 选择PT站点 -->
    <div v-if="currentStep === 'select_site'" class="select-site-step">
      <h2>选择PT站点</h2>
      <div class="site-grid">
        <div 
          v-for="site in supportedSites" 
          :key="site.code"
          :class="['site-card', { 'selected': selectedSite === site.code }]"
          @click="selectSite(site.code)"
        >
          <div class="site-header">
            <h4>{{ site.name }}</h4>
            <span v-if="site.recommended" class="recommended-badge">推荐</span>
          </div>
          <p class="site-url">{{ site.base_url }}</p>
          <div class="site-info">
            <span class="difficulty">难度：{{ site.difficulty }}</span>
          </div>
        </div>
      </div>
      
      <div class="step-actions">
        <button @click="currentStep = 'welcome'" class="back-button">返回</button>
        <button 
          @click="currentStep = 'auth_method'" 
          :disabled="!selectedSite"
          class="next-button"
        >
          下一步
        </button>
      </div>
    </div>

    <!-- 选择认证方式 -->
    <div v-if="currentStep === 'auth_method'" class="auth-method-step">
      <h2>选择认证方式</h2>
      <div class="builtin-feature" v-if="builtinCookiecloudEnabled">
        <div class="feature-badge">✨ 内置功能</div>
        <p class="feature-description">系统已内置CookieCloud服务，无需额外配置</p>
      </div>
      <div class="method-cards">
        <div 
          v-for="method in authMethods" 
          :key="method.id"
          :class="['method-card', { 'selected': selectedMethod === method.id, 'builtin': method.builtin }]"
          @click="selectMethod(method.id)"
        >
          <div class="method-icon">{{ method.icon }}</div>
          <h4>{{ method.name }}</h4>
          <p>{{ method.description }}</p>
          <div class="method-meta">
            <span class="difficulty">难度：{{ method.difficulty }}</span>
            <span v-if="method.recommended" class="recommended">推荐</span>
            <span v-if="method.builtin" class="builtin-tag">内置</span>
          </div>
        </div>
      </div>
      
      <div class="step-actions">
        <button @click="currentStep = 'select_site'" class="back-button">返回</button>
        <button 
          @click="proceedToAuth" 
          :disabled="!selectedMethod"
          class="next-button"
        >
          下一步
        </button>
      </div>
    </div>

    <!-- 账号密码认证 -->
    <div v-if="currentStep === 'username_password'" class="auth-form-step">
      <h2>账号密码认证</h2>
      <form @submit.prevent="submitUsernamePassword" class="auth-form">
        <div class="form-group">
          <label for="username">用户名：</label>
          <input 
            id="username"
            v-model="authData.username"
            type="text" 
            placeholder="请输入您的PT站点用户名"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="password">密码：</label>
          <input 
            id="password"
            v-model="authData.password"
            type="password" 
            placeholder="请输入您的PT站点密码"
            required
          >
        </div>
        
        <div class="security-tips">
          <h4>🔒 安全提示</h4>
          <ul>
            <li>您的密码将进行加密存储</li>
            <li>建议定期更换密码</li>
            <li>不要在公共网络进行认证</li>
          </ul>
        </div>
        
        <div class="step-actions">
          <button @click="currentStep = 'auth_method'" class="back-button">返回</button>
          <button 
            type="submit" 
            :disabled="!authData.username || !authData.password || isLoading"
            class="submit-button"
          >
            {{ isLoading ? '认证中...' : '开始认证' }}
          </button>
        </div>
      </form>
    </div>

    <!-- 内置CookieCloud认证 -->
    <div v-if="currentStep === 'builtin_cookiecloud'" class="auth-form-step">
      <h2>内置CookieCloud认证</h2>
      
      <div v-if="!showCredentialsForm" class="builtin-guide">
        <div class="feature-highlight">
          <h3>✨ 智能认证体验</h3>
          <p>系统将自动检测您的登录状态，提供最合适的认证方式</p>
        </div>
        
        <div class="benefits-list">
          <h4>🎯 认证流程：</h4>
          <ul>
            <li>✅ 自动检测浏览器Cookie状态</li>
            <li>✅ 如有Cookie则一键认证</li>
            <li>✅ 如无Cookie则引导账号密码登录</li>
            <li>✅ 登录后自动保存Cookie到内置服务</li>
            <li>✅ 后续认证无需重复登录</li>
          </ul>
        </div>
        
        <div class="privacy-notice">
          <h4>🔒 隐私保护</h4>
          <p>您的Cookie数据仅存储在本地，不会上传到任何第三方服务器</p>
        </div>
      </div>
      
      <!-- 账号密码输入表单（仅在需要时显示） -->
      <div v-if="showCredentialsForm" class="credentials-form">
        <div class="form-notice">
          <h3>🔑 请输入账号密码</h3>
          <p>系统检测到您尚未在浏览器中登录该PT站点，请输入账号密码进行首次认证</p>
        </div>
        
        <form @submit.prevent="submitBuiltinCookiecloudWithCredentials" class="auth-form">
          <div class="form-group">
            <label for="builtin-username">用户名：</label>
            <input 
              id="builtin-username"
              v-model="builtinAuthData.username"
              type="text" 
              placeholder="请输入您的PT站点用户名"
              required
            >
          </div>
          
          <div class="form-group">
            <label for="builtin-password">密码：</label>
            <input 
              id="builtin-password"
              v-model="builtinAuthData.password"
              type="password" 
              placeholder="请输入您的PT站点密码"
              required
            >
          </div>
          
          <div class="security-tips">
            <h4>🔒 安全提示</h4>
            <ul>
              <li>您的密码将进行加密存储</li>
              <li>登录成功后，Cookie将自动保存到内置CookieCloud</li>
              <li>后续认证无需再次输入账号密码</li>
            </ul>
          </div>
        </form>
      </div>
      
      <div class="step-actions">
        <button @click="currentStep = 'auth_method'" class="back-button">返回</button>
        
        <button 
          v-if="!showCredentialsForm"
          @click="checkBuiltinCookiecloudStatus" 
          :disabled="isLoading"
          class="submit-button builtin-button"
        >
          {{ isLoading ? '检测中...' : '开始智能认证' }}
        </button>
        
        <button 
          v-if="showCredentialsForm"
          @click="submitBuiltinCookiecloudWithCredentials" 
          :disabled="!builtinAuthData.username || !builtinAuthData.password || isLoading"
          class="submit-button builtin-button"
        >
          {{ isLoading ? '认证中...' : '开始认证' }}
        </button>
      </div>
    </div>

    <!-- 手动Cookie认证 -->
    <div v-if="currentStep === 'manual_cookie'" class="auth-form-step">
      <h2>手动Cookie认证</h2>
      <div class="cookie-guide">
        <h4>📋 获取Cookie步骤：</h4>
        <ol>
          <li>打开您的PT站点并登录</li>
          <li>按F12打开开发者工具</li>
          <li>切换到Network（网络）标签</li>
          <li>刷新页面，找到任意请求</li>
          <li>复制Request Headers中的Cookie字段</li>
        </ol>
      </div>
      
      <form @submit.prevent="submitManualCookie" class="auth-form">
        <div class="form-group">
          <label for="cookie">Cookie信息：</label>
          <textarea 
            id="cookie"
            v-model="authData.cookie"
            placeholder="粘贴您的Cookie信息，格式如：session=abc123; user_token=xyz789"
            rows="4"
            required
          ></textarea>
        </div>
        
        <div class="step-actions">
          <button @click="currentStep = 'auth_method'" class="back-button">返回</button>
          <button 
            type="submit" 
            :disabled="!authData.cookie || isLoading"
            class="submit-button"
          >
            {{ isLoading ? '认证中...' : '开始认证' }}
          </button>
        </div>
      </form>
    </div>

    <!-- 认证结果 -->
    <div v-if="currentStep === 'result'" class="result-step">
      <div v-if="authResult.success" class="success-result">
        <div class="result-icon">✅</div>
        <h3>认证成功！</h3>
        <p>{{ authResult.message }}</p>
        
        <div class="user-info" v-if="authResult.user_info">
          <h4>用户信息：</h4>
          <p>站点：{{ authResult.user_info.site_name }}</p>
          <p>用户名：{{ authResult.user_info.username }}</p>
        </div>
        
        <button @click="finishAuth" class="finish-button">
          开始使用PT功能
        </button>
      </div>
      
      <div v-else class="error-result">
        <div class="result-icon">❌</div>
        <h3>认证失败</h3>
        <p>{{ authResult.message }}</p>
        
        <div class="troubleshooting">
          <h4>💡 故障排除建议：</h4>
          <p>{{ authResult.next_step }}</p>
        </div>
        
        <div class="result-actions">
          <button @click="retryAuth" class="retry-button">重试</button>
          <button @click="currentStep = 'auth_method'" class="back-button">返回</button>
        </div>
      </div>
    </div>

    <!-- 进度指示器 -->
    <div v-if="currentStep !== 'welcome' && currentStep !== 'result'" class="progress-indicator">
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ width: progressPercentage + '%' }"
        ></div>
      </div>
      <div class="progress-text">
        步骤 {{ currentStepIndex }} / {{ totalSteps }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { usePTAuthStore } from '../stores/ptAuthStore'

export default {
  name: 'BeginnerPTAuth',
  setup() {
    const ptAuthStore = usePTAuthStore()
    
    // 步骤管理
    const steps = ['welcome', 'select_site', 'auth_method', 'builtin_cookiecloud', 'username_password', 'manual_cookie', 'result']
    const currentStep = ref('welcome')
    
    // 内置CookieCloud功能状态
    const builtinCookiecloudEnabled = ref(true)
    
    // 认证数据
    const selectedSite = ref('')
    const selectedMethod = ref('')
    const authData = ref({
      username: '',
      password: '',
      cookie: ''
    })
    
    // 内置CookieCloud认证相关状态
    const showCredentialsForm = ref(false)
    const builtinAuthData = ref({
      username: '',
      password: ''
    })
    
    // 状态管理
    const isLoading = ref(false)
    const authResult = ref({})
    
    // 支持的PT站点
    const supportedSites = ref([
      {
        name: 'M-Team',
        code: 'mteam',
        base_url: 'https://tp.m-team.cc',
        difficulty: '中等',
        recommended: true
      },
      {
        name: 'HDChina',
        code: 'hdchina',
        base_url: 'https://hdchina.org',
        difficulty: '简单',
        recommended: true
      },
      {
        name: 'TTG',
        code: 'ttg',
        base_url: 'https://totheglory.im',
        difficulty: '中等',
        recommended: false
      }
    ])
    
    // 认证方式
    const authMethods = ref([
      {
        id: 'builtin_cookiecloud',
        name: '内置CookieCloud认证',
        description: '使用系统内置的CookieCloud服务自动同步Cookie',
        icon: '✨',
        difficulty: '非常简单',
        recommended: true,
        builtin: true
      },
      {
        id: 'username_password',
        name: '账号密码登录',
        description: '直接使用账号密码进行认证',
        icon: '🔑',
        difficulty: '简单',
        recommended: false,
        builtin: false
      },
      {
        id: 'manual_cookie',
        name: '手动输入Cookie',
        description: '从浏览器手动复制Cookie信息',
        icon: '🍪',
        difficulty: '中等',
        recommended: false,
        builtin: false
      }
    ])
    
    // 计算属性
    const currentStepIndex = computed(() => {
      return steps.indexOf(currentStep.value) + 1
    })
    
    const totalSteps = computed(() => {
      return steps.length - 2 // 减去欢迎和结果页面
    })
    
    const progressPercentage = computed(() => {
      return ((currentStepIndex.value - 1) / totalSteps.value) * 100
    })
    
    // 方法
    const startAuth = () => {
      currentStep.value = 'select_site'
    }
    
    const selectSite = (siteCode) => {
      selectedSite.value = siteCode
    }
    
    const selectMethod = (methodId) => {
      selectedMethod.value = methodId
    }
    
    const proceedToAuth = () => {
      if (selectedMethod.value === 'builtin_cookiecloud') {
        currentStep.value = 'builtin_cookiecloud'
      } else if (selectedMethod.value === 'username_password') {
        currentStep.value = 'username_password'
      } else if (selectedMethod.value === 'manual_cookie') {
        currentStep.value = 'manual_cookie'
      }
    }
    
    const submitUsernamePassword = async () => {
      isLoading.value = true
      
      try {
        const result = await ptAuthStore.usernamePasswordAuth(
          selectedSite.value,
          authData.value.username,
          authData.value.password
        )
        
        authResult.value = result
        currentStep.value = 'result'
      } catch (error) {
        authResult.value = {
          success: false,
          message: '认证过程中出现错误',
          next_step: '请稍后重试或联系管理员'
        }
        currentStep.value = 'result'
      } finally {
        isLoading.value = false
      }
    }
    
    const checkBuiltinCookiecloudStatus = async () => {
      isLoading.value = true
      
      try {
        // 先尝试不提供账号密码进行认证（检测现有Cookie）
        const result = await ptAuthStore.builtinCookiecloudAuth(
          selectedSite.value
        )
        
        if (result.success) {
          // 有现有Cookie，认证成功
          authResult.value = result
          currentStep.value = 'result'
        } else if (result.requires_credentials) {
          // 需要账号密码，显示输入表单
          showCredentialsForm.value = true
        } else {
          // 其他错误
          authResult.value = result
          currentStep.value = 'result'
        }
      } catch (error) {
        authResult.value = {
          success: false,
          message: '内置CookieCloud认证过程中出现错误',
          next_step: '请检查网络连接或选择其他认证方式'
        }
        currentStep.value = 'result'
      } finally {
        isLoading.value = false
      }
    }
    
    const submitBuiltinCookiecloudWithCredentials = async () => {
      isLoading.value = true
      
      try {
        const result = await ptAuthStore.builtinCookiecloudAuth(
          selectedSite.value,
          builtinAuthData.value.username,
          builtinAuthData.value.password
        )
        
        authResult.value = result
        currentStep.value = 'result'
      } catch (error) {
        authResult.value = {
          success: false,
          message: '内置CookieCloud认证过程中出现错误',
          next_step: '请检查网络连接或选择其他认证方式'
        }
        currentStep.value = 'result'
      } finally {
        isLoading.value = false
      }
    }
    
    const submitManualCookie = async () => {
      isLoading.value = true
      
      try {
        // 解析Cookie字符串
        const cookies = {}
        authData.value.cookie.split(';').forEach(cookie => {
          const [key, value] = cookie.trim().split('=')
          if (key && value) {
            cookies[key] = value
          }
        })
        
        const result = await ptAuthStore.manualCookieAuth(
          selectedSite.value,
          cookies
        )
        
        authResult.value = result
        currentStep.value = 'result'
      } catch (error) {
        authResult.value = {
          success: false,
          message: 'Cookie认证过程中出现错误',
          next_step: '请检查Cookie格式或联系管理员'
        }
        currentStep.value = 'result'
      } finally {
        isLoading.value = false
      }
    }
    
    const retryAuth = () => {
      authData.value = { username: '', password: '', cookie: '' }
      currentStep.value = 'auth_method'
    }
    
    const finishAuth = () => {
      // 跳转到PT功能页面
      window.location.href = '/pt'
    }
    
    onMounted(() => {
      // 初始化认证状态检查
      ptAuthStore.checkExistingSessions()
    })
    
    return {
      currentStep,
      selectedSite,
      selectedMethod,
      authData,
      isLoading,
      authResult,
      supportedSites,
      authMethods,
      currentStepIndex,
      totalSteps,
      progressPercentage,
      startAuth,
      selectSite,
      selectMethod,
      proceedToAuth,
      submitUsernamePassword,
      submitManualCookie,
      retryAuth,
      finishAuth
    }
  }
}
</script>

<style scoped>
.beginner-auth-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.welcome-step {
  text-align: center;
  padding: 40px 20px;
}

.welcome-header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1.1em;
  margin-bottom: 30px;
}

.info-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  margin: 20px 0;
  text-align: left;
}

.info-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.info-card ul {
  list-style: none;
  padding: 0;
}

.info-card li {
  padding: 5px 0;
  color: #34495e;
}

.estimated-info {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 20px 0;
}

.info-item {
  text-align: center;
}

.label {
  display: block;
  color: #7f8c8d;
  font-size: 0.9em;
}

.value {
  display: block;
  color: #2c3e50;
  font-weight: bold;
  font-size: 1.1em;
}

.start-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  font-size: 1.1em;
  cursor: pointer;
  transition: background 0.3s;
}

.start-button:hover {
  background: #2980b9;
}

.site-grid, .method-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.site-card, .method-card {
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.site-card:hover, .method-card:hover {
  border-color: #3498db;
  transform: translateY(-2px);
}

.site-card.selected, .method-card.selected {
  border-color: #3498db;
  background: #f0f8ff;
}

.method-card.builtin.selected {
  border-color: #9b59b6;
  background: #f9f0ff;
}

.builtin-feature {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  text-align: center;
}

.feature-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
  display: inline-block;
  margin-bottom: 10px;
}

.feature-description {
  margin: 0;
  font-size: 1.1em;
}

.builtin-tag {
  background: #9b59b6;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: bold;
}

.builtin-guide {
  max-width: 600px;
  margin: 0 auto;
}

.feature-highlight {
  background: #e8f4fd;
  border: 1px solid #b3e0ff;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  text-align: center;
}

.feature-highlight h3 {
  color: #0066cc;
  margin-bottom: 10px;
}

.benefits-list {
  background: #f0f8f0;
  border: 1px solid #c8e6c9;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
}

.benefits-list h4 {
  color: #2e7d32;
  margin-bottom: 15px;
}

.benefits-list ul {
  list-style: none;
  padding: 0;
}

.benefits-list li {
  padding: 5px 0;
  color: #388e3c;
}

.privacy-notice {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 20px;
}

.privacy-notice h4 {
  color: #856404;
  margin-bottom: 10px;
}

.builtin-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.builtin-button:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

.site-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.recommended-badge {
  background: #27ae60;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
}

.site-url {
  color: #7f8c8d;
  font-size: 0.9em;
  margin-bottom: 10px;
}

.site-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.difficulty {
  color: #e67e22;
  font-weight: bold;
}

.method-icon {
  font-size: 2em;
  margin-bottom: 10px;
}

.method-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.recommended {
  color: #27ae60;
  font-weight: bold;
}

.auth-form {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #2c3e50;
  font-weight: bold;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
}

.security-tips {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 5px;
  padding: 15px;
  margin: 20px 0;
}

.security-tips h4 {
  color: #856404;
  margin-bottom: 10px;
}

.security-tips ul {
  color: #856404;
  padding-left: 20px;
}

.cookie-guide {
  background: #e8f4fd;
  border: 1px solid #b3e0ff;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 20px;
}

.cookie-guide h4 {
  color: #0066cc;
  margin-bottom: 10px;
}

.cookie-guide ol {
  padding-left: 20px;
}

.step-actions, .result-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.back-button, .next-button, .submit-button, .finish-button, .retry-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.back-button {
  background: #95a5a6;
  color: white;
}

.next-button, .submit-button, .finish-button {
  background: #3498db;
  color: white;
}

.next-button:disabled, .submit-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.retry-button {
  background: #e74c3c;
  color: white;
}

.result-step {
  text-align: center;
  padding: 40px 20px;
}

.result-icon {
  font-size: 4em;
  margin-bottom: 20px;
}

.success-result h3 {
  color: #27ae60;
}

.error-result h3 {
  color: #e74c3c;
}

.user-info {
  background: #d5f4e6;
  border: 1px solid #27ae60;
  border-radius: 5px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.troubleshooting {
  background: #fdedec;
  border: 1px solid #e74c3c;
  border-radius: 5px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.progress-indicator {
  margin-top: 30px;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #ecf0f1;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #3498db;
  transition: width 0.3s;
}

.progress-text {
  text-align: center;
  color: #7f8c8d;
  margin-top: 10px;
  font-size: 0.9em;
}
</style>