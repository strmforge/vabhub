import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo, LoginRequest, LoginResponse } from '@/types/api'
import ApiService from '@/services/api'

interface AuthState {
  token: string | null
  userInfo: UserInfo | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<UserInfo | null>(null)
  const isAuthenticated = computed(() => !!token.value)

  // 动作
  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
  }

  const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
    try {
      const response = await ApiService.auth.login(credentials)
      
      if (response.success && response.data) {
        setToken(response.data.token)
        setUserInfo(response.data.user)
        return response.data
      } else {
        throw new Error(response.message || '登录失败')
      }
    } catch (error) {
      console.error('登录错误:', error)
      throw error
    }
  }

  const logout = async () => {
    try {
      await ApiService.auth.logout()
    } catch (error) {
      console.error('登出错误:', error)
    } finally {
      token.value = null
      userInfo.value = null
      localStorage.removeItem('token')
    }
  }

  const checkAuth = async (): Promise<boolean> => {
    if (!token.value) return false

    try {
      const response = await ApiService.auth.verify()
      
      if (response.success && response.data) {
        setUserInfo(response.data)
        return true
      } else {
        logout()
        return false
      }
    } catch (error) {
      console.error('验证token失败:', error)
      logout()
      return false
    }
  }

  const refreshToken = async (): Promise<boolean> => {
    try {
      const response = await ApiService.auth.refresh()
      
      if (response.success && response.data) {
        setToken(response.data.token)
        return true
      }
      return false
    } catch (error) {
      console.error('刷新token失败:', error)
      return false
    }
  }

  return {
    // 状态
    token,
    userInfo,
    isAuthenticated,
    
    // 动作
    setToken,
    setUserInfo,
    login,
    logout,
    checkAuth,
    refreshToken
  }
})