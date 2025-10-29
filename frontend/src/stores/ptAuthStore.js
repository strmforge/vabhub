import { defineStore } from 'pinia'
import { ref } from 'vue'

// 模拟API调用
const mockApiCall = (data, delay = 1000) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(data)
    }, delay)
  })
}

export const usePTAuthStore = defineStore('ptAuth', () => {
  // 状态
  const userSessions = ref({})
  const isLoading = ref(false)
  const error = ref(null)
  
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
  
  // 内置CookieCloud认证
  const builtinCookiecloudAuth = async (siteCode, username = null, password = null) => {
    isLoading.value = true
    error.value = null
    
    try {
      // 模拟API调用 - 内置CookieCloud认证
      let result
      
      if (username && password) {
        // 使用账号密码进行认证
        result = await mockApiCall({
          success: true,
          message: `${siteCode} 内置CookieCloud认证成功！`,
          next_step: '开始使用PT功能',
          cookie_count: 3,
          auth_type: 'builtin_cookiecloud',
          auth_source: 'new_login'
        })
      } else {
        // 尝试使用现有Cookie进行认证
        // 模拟检测：50%概率有现有Cookie，50%概率需要账号密码
        const hasExistingCookie = Math.random() > 0.5
        
        if (hasExistingCookie) {
          result = {
            success: true,
            message: `${siteCode} 内置CookieCloud认证成功！`,
            next_step: '开始使用PT功能',
            cookie_count: 5,
            auth_type: 'builtin_cookiecloud',
            auth_source: 'existing_cookie'
          }
        } else {
          result = {
            success: false,
            message: `未找到 ${siteCode} 的Cookie信息`,
            next_step: '请先在浏览器中登录PT站点，或使用账号密码登录',
            requires_credentials: true
          }
        }
      }
      
      if (result.success) {
        // 保存会话
        userSessions.value[siteCode] = {
          auth_type: 'builtin_cookiecloud',
          auth_time: new Date().toISOString(),
          last_used: new Date().toISOString(),
          status: 'authenticated',
          auth_source: result.auth_source
        }
      }
      
      return result
    } catch (err) {
      error.value = err.message
      return {
        success: false,
        message: '内置CookieCloud认证失败',
        next_step: '请检查网络连接或选择其他认证方式'
      }
    } finally {
      isLoading.value = false
    }
  }

  // 认证方法
  const usernamePasswordAuth = async (siteCode, username, password) => {
    isLoading.value = true
    error.value = null
    
    try {
      // 模拟API调用
      const result = await mockApiCall({
        success: true,
        message: `${siteCode} 登录成功！`,
        user_info: {
          username: username,
          site_name: siteCode
        },
        next_step: '开始使用PT功能'
      })
      
      // 保存会话
      userSessions.value[siteCode] = {
        auth_type: 'username_password',
        auth_time: new Date().toISOString(),
        last_used: new Date().toISOString(),
        status: 'authenticated',
        username: username
      }
      
      return result
    } catch (err) {
      error.value = err.message
      return {
        success: false,
        message: '认证失败，请检查网络连接',
        next_step: '稍后重试或联系管理员'
      }
    } finally {
      isLoading.value = false
    }
  }
  
  // 手动Cookie认证
  const manualCookieAuth = async (siteCode, cookies) => {
    isLoading.value = true
    error.value = null
    
    try {
      // 验证Cookie格式
      if (!cookies || Object.keys(cookies).length === 0) {
        return {
          success: false,
          message: 'Cookie信息为空，请检查输入',
          next_step: '重新输入Cookie'
        }
      }
      
      // 模拟API调用
      const result = await mockApiCall({
        success: true,
        message: `${siteCode} Cookie认证成功！`,
        next_step: '开始使用PT功能'
      })
      
      // 保存会话
      userSessions.value[siteCode] = {
        auth_type: 'manual_cookie',
        auth_time: new Date().toISOString(),
        last_used: new Date().toISOString(),
        status: 'authenticated'
      }
      
      return result
    } catch (err) {
      error.value = err.message
      return {
        success: false,
        message: 'Cookie认证失败',
        next_step: '检查Cookie格式或联系管理员'
      }
    } finally {
      isLoading.value = false
    }
  }
  
  // 检查现有会话
  const checkExistingSessions = () => {
    // 从本地存储加载会话
    const storedSessions = localStorage.getItem('pt_user_sessions')
    if (storedSessions) {
      userSessions.value = JSON.parse(storedSessions)
    }
  }
  
  // 验证会话有效性
  const validateSession = (siteCode) => {
    if (!userSessions.value[siteCode]) {
      return false
    }
    
    const session = userSessions.value[siteCode]
    const lastUsed = new Date(session.last_used)
    const now = new Date()
    const hoursDiff = (now - lastUsed) / (1000 * 60 * 60)
    
    // 会话24小时后过期
    if (hoursDiff > 24) {
      session.status = 'expired'
      return false
    }
    
    // 更新最后使用时间
    session.last_used = now.toISOString()
    saveSessionsToStorage()
    
    return true
  }
  
  // 获取会话状态
  const getSessionStatus = (siteCode) => {
    if (!userSessions.value[siteCode]) {
      return {
        is_authenticated: false,
        auth_type: null,
        auth_time: null,
        last_used: null,
        status: 'not_authenticated'
      }
    }
    
    const session = userSessions.value[siteCode]
    return {
      is_authenticated: session.status === 'authenticated',
      auth_type: session.auth_type,
      auth_time: session.auth_time,
      last_used: session.last_used,
      status: session.status
    }
  }
  
  // 登出
  const logout = (siteCode) => {
    if (userSessions.value[siteCode]) {
      delete userSessions.value[siteCode]
      saveSessionsToStorage()
    }
  }
  
  // 保存会话到本地存储
  const saveSessionsToStorage = () => {
    localStorage.setItem('pt_user_sessions', JSON.stringify(userSessions.value))
  }
  
  // 获取支持的站点列表
  const getSupportedSites = () => {
    return supportedSites.value
  }
  
  // 获取故障排除指南
  const getTroubleshootingGuide = () => {
    return {
      common_issues: [
        {
          issue: '认证失败',
          solution: '检查账号密码是否正确，确保网络连接正常',
          priority: '高'
        },
        {
          issue: '无法连接到PT站点',
          solution: '检查网络设置，尝试使用代理或VPN',
          priority: '高'
        },
        {
          issue: 'Cookie格式错误',
          solution: '确保Cookie格式正确，参考浏览器开发者工具',
          priority: '中'
        },
        {
          issue: '会话过期',
          solution: '重新登录或刷新会话',
          priority: '低'
        }
      ],
      contact_support: {
        email: 'support@vabhub.org',
        documentation: 'https://docs.vabhub.org/beginner-guide',
        community: 'https://community.vabhub.org'
      }
    }
  }
  
  return {
    // 状态
    userSessions,
    isLoading,
    error,
    supportedSites,
    
    // 方法
    builtinCookiecloudAuth,
    usernamePasswordAuth,
    manualCookieAuth,
    checkExistingSessions,
    validateSession,
    getSessionStatus,
    logout,
    getSupportedSites,
    getTroubleshootingGuide
  }
})