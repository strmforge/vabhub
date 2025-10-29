import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    // 应用状态
    isInitialized: false,
    isLoading: false,
    
    // 用户信息
    user: null,
    
    // 系统设置
    settings: {
      theme: 'light', // light | dark
      language: 'zh-CN',
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8090'
    },
    
    // 媒体库状态
    mediaStats: {
      total: 0,
      movies: 0,
      tvShows: 0,
      music: 0
    }
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.user,
    isDarkMode: (state) => state.settings.theme === 'dark'
  },
  
  actions: {
    // 初始化应用
    async initialize() {
      this.isLoading = true
      
      try {
        // 检查认证状态
        const token = localStorage.getItem('token')
        if (token) {
          await this.fetchUserInfo()
        }
        
        // 加载系统设置
        await this.loadSettings()
        
        this.isInitialized = true
      } catch (error) {
        console.error('初始化失败:', error)
      } finally {
        this.isLoading = false
      }
    },
    
    // 获取用户信息
    async fetchUserInfo() {
      // 调用后端API获取用户信息
      // this.user = await api.getUserInfo()
    },
    
    // 加载设置
    async loadSettings() {
      const savedSettings = localStorage.getItem('vabhub-settings')
      if (savedSettings) {
        this.settings = { ...this.settings, ...JSON.parse(savedSettings) }
      }
      
      // 应用主题
      this.applyTheme()
    },
    
    // 保存设置
    async saveSettings() {
      localStorage.setItem('vabhub-settings', JSON.stringify(this.settings))
      this.applyTheme()
    },
    
    // 应用主题
    applyTheme() {
      if (this.settings.theme === 'dark') {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    },
    
    // 切换主题
    toggleTheme() {
      this.settings.theme = this.settings.theme === 'light' ? 'dark' : 'light'
      this.saveSettings()
    },
    
    // 登录
    async login(credentials) {
      this.isLoading = true
      
      try {
        // 调用后端登录API
        // const response = await api.login(credentials)
        // localStorage.setItem('token', response.token)
        // await this.fetchUserInfo()
        
        return { success: true }
      } catch (error) {
        return { success: false, error: error.message }
      } finally {
        this.isLoading = false
      }
    },
    
    // 登出
    logout() {
      localStorage.removeItem('token')
      this.user = null
      
      // 跳转到登录页
      if (this.$router) {
        this.$router.push('/login')
      }
    }
  }
})