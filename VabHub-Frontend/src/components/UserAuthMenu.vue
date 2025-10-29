<template>
  <div class="user-auth-menu">
    <!-- 用户头像菜单 -->
    <div class="user-menu-trigger" @click="toggleMenu">
      <div class="user-avatar">
        <span class="avatar-icon">👤</span>
        <span class="user-name">{{ currentUser.username || '用户' }}</span>
        <span class="menu-arrow">{{ isMenuOpen ? '▲' : '▼' }}</span>
      </div>
    </div>

    <!-- 用户菜单 -->
    <div v-if="isMenuOpen" class="user-menu-dropdown">
      <!-- 用户信息 -->
      <div class="user-info-section">
        <div class="user-details">
          <div class="user-avatar-large">
            <span class="avatar-icon">👤</span>
          </div>
          <div class="user-text">
            <div class="user-name">{{ currentUser.username }}</div>
            <div class="user-role">{{ currentUser.role || '普通用户' }}</div>
          </div>
        </div>
      </div>

      <!-- 认证状态显示 -->
      <div class="auth-status-section" v-if="authStatus.is_authenticated">
        <div class="auth-status auth-success">
          <span class="status-icon">✅</span>
          <span class="status-text">已认证</span>
        </div>
        <div class="auth-sites" v-if="authStatus.auth_sites.length > 0">
          <div class="auth-site-item" v-for="site in authStatus.auth_sites" :key="site">
            <span class="site-icon">🌐</span>
            <span class="site-name">{{ getSiteDisplayName(site) }}</span>
          </div>
        </div>
      </div>

      <!-- 认证入口（未认证时显示） -->
      <div class="auth-section" v-if="authStatus.show_auth_menu">
        <div class="auth-prompt">
          <div class="prompt-icon">🔑</div>
          <div class="prompt-text">
            <div class="prompt-title">需要认证</div>
            <div class="prompt-description">完成PT站点认证以解锁全部功能</div>
          </div>
        </div>
        <button class="auth-button" @click="openAuthModal">
          用户认证
        </button>
      </div>

      <!-- 菜单选项 -->
      <div class="menu-options">
        <div class="menu-item" @click="navigateTo('profile')">
          <span class="menu-icon">👤</span>
          <span class="menu-text">个人资料</span>
        </div>
        
        <div class="menu-item" @click="navigateTo('settings')">
          <span class="menu-icon">⚙️</span>
          <span class="menu-text">系统设置</span>
        </div>
        
        <div class="menu-item" v-if="authStatus.is_authenticated" @click="navigateTo('pt-management')">
          <span class="menu-icon">📊</span>
          <span class="menu-text">PT管理</span>
        </div>
        
        <div class="menu-divider"></div>
        
        <div class="menu-item logout-item" @click="logout">
          <span class="menu-icon">🚪</span>
          <span class="menu-text">退出登录</span>
        </div>
      </div>
    </div>

    <!-- 认证弹窗 -->
    <div v-if="showAuthModal" class="auth-modal-overlay" @click="closeAuthModal">
      <div class="auth-modal" @click.stop>
        <div class="auth-modal-header">
          <h3>用户认证</h3>
          <button class="close-button" @click="closeAuthModal">×</button>
        </div>
        
        <div class="auth-modal-content">
          <!-- 选择认证站点 -->
          <div class="auth-step" v-if="currentAuthStep === 'select_site'">
            <h4>选择PT站点</h4>
            <div class="site-selection">
              <div 
                v-for="site in availableAuthSites" 
                :key="site.site_code"
                :class="['site-option', { 'selected': selectedAuthSite === site.site_code }]"
                @click="selectAuthSite(site)"
              >
                <div class="site-info">
                  <span class="site-icon">{{ site.icon }}</span>
                  <div class="site-details">
                    <div class="site-name">{{ site.site_name }}</div>
                    <div class="site-description">{{ site.description }}</div>
                  </div>
                </div>
                <div class="site-meta">
                  <span class="difficulty">难度：{{ site.difficulty }}</span>
                  <span class="recommended" v-if="site.recommended_method">推荐</span>
                </div>
              </div>
            </div>
            
            <div class="auth-actions">
              <button class="cancel-button" @click="closeAuthModal">取消</button>
              <button 
                class="next-button" 
                @click="proceedToAuthMethod"
                :disabled="!selectedAuthSite"
              >
                下一步
              </button>
            </div>
          </div>

          <!-- 选择认证方式 -->
          <div class="auth-step" v-if="currentAuthStep === 'select_method'">
            <h4>选择认证方式</h4>
            <div class="method-selection">
              <div 
                v-for="method in authMethods" 
                :key="method.id"
                :class="['method-option', { 'selected': selectedAuthMethod === method.id }]"
                @click="selectAuthMethod(method)"
              >
                <div class="method-info">
                  <span class="method-icon">{{ method.icon }}</span>
                  <div class="method-details">
                    <div class="method-name">{{ method.name }}</div>
                    <div class="method-description">{{ method.description }}</div>
                  </div>
                </div>
                <div class="method-meta">
                  <span class="difficulty">{{ method.difficulty }}</span>
                </div>
              </div>
            </div>
            
            <div class="auth-actions">
              <button class="back-button" @click="currentAuthStep = 'select_site'">上一步</button>
              <button 
                class="next-button" 
                @click="proceedToAuthForm"
                :disabled="!selectedAuthMethod"
              >
                下一步
              </button>
            </div>
          </div>

          <!-- 认证表单 -->
          <div class="auth-step" v-if="currentAuthStep === 'auth_form'">
            <h4>{{ selectedAuthSiteDisplayName }} 认证</h4>
            
            <div class="auth-form">
              <div v-if="selectedAuthMethod === 'smart_cookiecloud'">
                <div class="auth-guide">
                  <p>系统将自动检测您的认证状态并提供最优认证方案</p>
                </div>
                <button 
                  class="auth-submit-button" 
                  @click="submitSmartAuth"
                  :disabled="isAuthLoading"
                >
                  {{ isAuthLoading ? '认证中...' : '开始智能认证' }}
                </button>
              </div>
              
              <div v-if="selectedAuthMethod === 'username_password'">
                <div class="form-group">
                  <label>用户名：</label>
                  <input 
                    v-model="authData.username" 
                    type="text" 
                    placeholder="请输入PT站点用户名"
                  >
                </div>
                <div class="form-group">
                  <label>密码：</label>
                  <input 
                    v-model="authData.password" 
                    type="password" 
                    placeholder="请输入PT站点密码"
                  >
                </div>
                <button 
                  class="auth-submit-button" 
                  @click="submitUsernamePasswordAuth"
                  :disabled="!authData.username || !authData.password || isAuthLoading"
                >
                  {{ isAuthLoading ? '认证中...' : '开始认证' }}
                </button>
              </div>
              
              <div v-if="selectedAuthMethod === 'manual_cookie'">
                <div class="form-group">
                  <label>Cookie信息：</label>
                  <textarea 
                    v-model="authData.cookie" 
                    placeholder="请从浏览器复制Cookie信息"
                    rows="4"
                  ></textarea>
                </div>
                <button 
                  class="auth-submit-button" 
                  @click="submitManualCookieAuth"
                  :disabled="!authData.cookie || isAuthLoading"
                >
                  {{ isAuthLoading ? '认证中...' : '开始认证' }}
                </button>
              </div>
            </div>
            
            <div class="auth-actions">
              <button class="back-button" @click="currentAuthStep = 'select_method'">上一步</button>
              <button class="cancel-button" @click="closeAuthModal">取消</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 认证结果提示 -->
    <div v-if="authResult" class="auth-result-toast" :class="{ 'success': authResult.success, 'error': !authResult.success }">
      <div class="toast-content">
        <span class="toast-icon">{{ authResult.success ? '✅' : '❌' }}</span>
        <span class="toast-message">{{ authResult.message }}</span>
      </div>
      <button class="toast-close" @click="clearAuthResult">×</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 用户状态
const currentUser = reactive({
  username: 'admin',
  role: '超级管理员'
})

// 认证状态
const authStatus = reactive({
  is_authenticated: false,
  auth_sites: [],
  last_auth_time: null,
  auth_required: true,
  show_auth_menu: true
})

// 菜单状态
const isMenuOpen = ref(false)
const showAuthModal = ref(false)

// 认证流程状态
const currentAuthStep = ref('select_site')
const selectedAuthSite = ref('')
const selectedAuthMethod = ref('')
const authData = reactive({
  username: '',
  password: '',
  cookie: ''
})

// 认证结果
const authResult = ref(null)
const isAuthLoading = ref(false)

// 可用认证站点
const availableAuthSites = ref([])

// 认证方式
const authMethods = [
  {
    id: 'smart_cookiecloud',
    name: '智能CookieCloud认证',
    description: '自动检测插件状态，提供最优认证方案',
    icon: '🤖',
    difficulty: '非常简单'
  },
  {
    id: 'username_password', 
    name: '账号密码登录',
    description: '直接使用账号密码进行认证',
    icon: '🔑',
    difficulty: '简单'
  },
  {
    id: 'manual_cookie',
    name: '手动输入Cookie',
    description: '从浏览器手动复制Cookie信息',
    icon: '📋',
    difficulty: '中等'
  }
]

// 计算属性
const selectedAuthSiteDisplayName = computed(() => {
  const site = availableAuthSites.value.find(s => s.site_code === selectedAuthSite.value)
  return site ? site.site_name : ''
})

// 方法
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const openAuthModal = () => {
  showAuthModal.value = true
  currentAuthStep.value = 'select_site'
  resetAuthData()
  loadAvailableAuthSites()
}

const closeAuthModal = () => {
  showAuthModal.value = false
  resetAuthData()
}

const selectAuthSite = (site) => {
  selectedAuthSite.value = site.site_code
}

const selectAuthMethod = (method) => {
  selectedAuthMethod.value = method.id
}

const proceedToAuthMethod = () => {
  currentAuthStep.value = 'select_method'
}

const proceedToAuthForm = () => {
  currentAuthStep.value = 'auth_form'
}

const resetAuthData = () => {
  selectedAuthSite.value = ''
  selectedAuthMethod.value = ''
  authData.username = ''
  authData.password = ''
  authData.cookie = ''
}

const submitSmartAuth = async () => {
  isAuthLoading.value = true
  
  try {
    // 模拟API调用
    const result = await mockCompleteUserAuth('smart_cookiecloud')
    handleAuthResult(result)
  } catch (error) {
    handleAuthResult({
      success: false,
      message: '认证过程中出现错误'
    })
  } finally {
    isAuthLoading.value = false
  }
}

const submitUsernamePasswordAuth = async () => {
  isAuthLoading.value = true
  
  try {
    const result = await mockCompleteUserAuth('username_password')
    handleAuthResult(result)
  } catch (error) {
    handleAuthResult({
      success: false,
      message: '认证过程中出现错误'
    })
  } finally {
    isAuthLoading.value = false
  }
}

const submitManualCookieAuth = async () => {
  isAuthLoading.value = true
  
  try {
    const result = await mockCompleteUserAuth('manual_cookie')
    handleAuthResult(result)
  } catch (error) {
    handleAuthResult({
      success: false,
      message: '认证过程中出现错误'
    })
  } finally {
    isAuthLoading.value = false
  }
}

const handleAuthResult = (result) => {
  authResult.value = result
  
  if (result.success) {
    // 认证成功
    if (result.requires_relogin) {
      // 需要重新登录
      setTimeout(() => {
        logout()
      }, 2000)
    } else {
      // 更新认证状态
      updateAuthStatus()
      closeAuthModal()
    }
  }
}

const clearAuthResult = () => {
  authResult.value = null
}

const loadAvailableAuthSites = async () => {
  try {
    // 模拟API调用
    availableAuthSites.value = [
      {
        site_code: 'mteam',
        site_name: 'M-Team',
        description: '知名PT站点，资源丰富',
        icon: '🎯',
        difficulty: '中等',
        recommended_method: 'smart_cookiecloud'
      },
      {
        site_code: 'hdchina',
        site_name: 'HDChina',
        description: '高清中国，国内知名PT',
        icon: '🇨🇳',
        difficulty: '简单',
        recommended_method: 'smart_cookiecloud'
      },
      {
        site_code: 'ttg',
        site_name: 'TTG',
        description: '游戏资源丰富的PT站点',
        icon: '🎮',
        difficulty: '中等',
        recommended_method: 'smart_cookiecloud'
      }
    ]
  } catch (error) {
    console.error('加载认证站点失败:', error)
  }
}

const updateAuthStatus = async () => {
  try {
    // 模拟API调用获取认证状态
    const status = await mockGetUserAuthStatus()
    Object.assign(authStatus, status)
  } catch (error) {
    console.error('更新认证状态失败:', error)
  }
}

const getSiteDisplayName = (siteCode) => {
  const siteMap = {
    'mteam': 'M-Team',
    'hdchina': 'HDChina', 
    'ttg': 'TTG'
  }
  return siteMap[siteCode] || siteCode
}

const navigateTo = (route) => {
  isMenuOpen.value = false
  router.push(`/${route}`)
}

const logout = () => {
  // 清除认证状态
  authStatus.is_authenticated = false
  authStatus.auth_sites = []
  authStatus.show_auth_menu = true
  
  // 模拟重新登录流程
  router.push('/login')
}

// 模拟API调用
const mockCompleteUserAuth = async (method) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      // 模拟认证结果
      const success = Math.random() > 0.3 // 70%成功率
      
      if (success) {
        resolve({
          success: true,
          message: `${selectedAuthSiteDisplayName.value} 认证成功！`,
          requires_relogin: true,
          auth_completed: true
        })
      } else {
        resolve({
          success: false,
          message: '认证失败，请检查认证信息',
          requires_relogin: false,
          auth_completed: false
        })
      }
    }, 1500)
  })
}

const mockGetUserAuthStatus = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        is_authenticated: false,
        auth_sites: [],
        last_auth_time: null,
        auth_required: true,
        show_auth_menu: true
      })
    }, 500)
  })
}

onMounted(() => {
  updateAuthStatus()
})
</script>

<style scoped>
.user-auth-menu {
  position: relative;
  display: inline-block;
}

.user-menu-trigger {
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.user-menu-trigger:hover {
  background-color: #f5f5f5;
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar-icon {
  font-size: 20px;
}

.user-name {
  font-weight: 500;
}

.menu-arrow {
  font-size: 12px;
  color: #666;
}

.user-menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 280px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  margin-top: 8px;
}

.user-info-section {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.user-details {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar-large {
  font-size: 32px;
}

.user-text {
  flex: 1;
}

.user-name {
  font-weight: 600;
  font-size: 16px;
}

.user-role {
  color: #666;
  font-size: 14px;
}

.auth-status-section {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.auth-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.auth-success {
  color: #10b981;
}

.auth-sites {
  margin-top: 8px;
}

.auth-site-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
  font-size: 14px;
}

.auth-section {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.auth-prompt {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.prompt-icon {
  font-size: 20px;
  color: #f59e0b;
}

.prompt-title {
  font-weight: 600;
  font-size: 14px;
}

.prompt-description {
  color: #666;
  font-size: 12px;
}

.auth-button {
  width: 100%;
  padding: 8px 12px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.auth-button:hover {
  background: #2563eb;
}

.menu-options {
  padding: 8px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.menu-icon {
  font-size: 16px;
  width: 20px;
}

.menu-text {
  flex: 1;
  font-size: 14px;
}

.menu-divider {
  height: 1px;
  background: #f0f0f0;
  margin: 8px 0;
}

.logout-item {
  color: #ef4444;
}

.logout-item:hover {
  background-color: #fef2f2;
}

/* 认证弹窗样式 */
.auth-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.auth-modal {
  background: white;
  border-radius: 12px;
  width: 500px;
  max-width: 90vw;
  max-height: 80vh;
  overflow: hidden;
}

.auth-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e0e0e0;
}

.auth-modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.close-button:hover {
  color: #333;
}

.auth-modal-content {
  padding: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

.auth-step h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
}

.site-selection, .method-selection {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.site-option, .method-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.site-option:hover, .method-option:hover {
  border-color: #3b82f6;
  background-color: #f8fafc;
}

.site-option.selected, .method-option.selected {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.site-info, .method-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.site-icon, .method-icon {
  font-size: 20px;
}

.site-details, .method-details {
  flex: 1;
}

.site-name, .method-name {
  font-weight: 600;
  font-size: 14px;
}

.site-description, .method-description {
  color: #666;
  font-size: 12px;
  margin-top: 2px;
}

.site-meta, .method-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.difficulty {
  font-size: 12px;
  color: #666;
}

.recommended {
  background: #10b981;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
}

.auth-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 20px;
}

.back-button, .cancel-button, .next-button {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.back-button, .cancel-button {
  background: white;
  color: #666;
}

.back-button:hover, .cancel-button:hover {
  background: #f5f5f5;
}

.next-button {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.next-button:hover {
  background: #2563eb;
}

.next-button:disabled {
  background: #9ca3af;
  border-color: #9ca3af;
  cursor: not-allowed;
}

.auth-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
  font-size: 14px;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

.form-group input:focus, .form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.auth-submit-button {
  width: 100%;
  padding: 12px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.auth-submit-button:hover {
  background: #059669;
}

.auth-submit-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.auth-guide {
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #4b5563;
}

/* 认证结果提示 */
.auth-result-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 3000;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  max-width: 300px;
}

.auth-result-toast.success {
  border-left: 4px solid #10b981;
}

.auth-result-toast.error {
  border-left: 4px solid #ef4444;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.toast-icon {
  font-size: 16px;
}

.toast-message {
  font-size: 14px;
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #666;
}

.toast-close:hover {
  color: #333;
}
</style>