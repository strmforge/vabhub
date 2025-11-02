import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import { ErrorTypes, createFriendlyMessage } from '@/utils/errorHandler'

// API基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const API_TIMEOUT = 30000

// 请求拦截器
const requestInterceptor = (config: any) => {
  const authStore = useAuthStore()
  const appStore = useAppStore()
  
  // 添加认证token
  if (authStore.token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  
  // 设置超时
  config.timeout = API_TIMEOUT
  
  // 显示加载状态
  if (config.showLoading !== false) {
    appStore.setLoading(true)
  }
  
  return config
}

// 响应拦截器
const responseInterceptor = (response: any) => {
  const appStore = useAppStore()
  
  // 隐藏加载状态
  appStore.setLoading(false)
  
  return response
}

// 错误拦截器
const errorInterceptor = (error: any) => {
  const appStore = useAppStore()
  const authStore = useAuthStore()
  
  // 隐藏加载状态
  appStore.setLoading(false)
  
  // 处理错误
  let errorType = ErrorTypes.UNKNOWN_ERROR
  let errorMessage = '系统发生未知错误'
  
  if (!error.response) {
    errorType = ErrorTypes.NETWORK_ERROR
    errorMessage = '网络连接失败，请检查网络设置'
  } else if (error.response.status === 401) {
    errorType = ErrorTypes.AUTH_ERROR
    errorMessage = '身份验证失败，请重新登录'
    authStore.logout()
  } else if (error.response.status >= 500) {
    errorType = ErrorTypes.API_ERROR
    errorMessage = '服务器内部错误，请稍后重试'
  } else if (error.response.status >= 400) {
    errorType = ErrorTypes.VALIDATION_ERROR
    errorMessage = error.response.data?.message || '请求参数错误'
  }
  
  // 显示错误通知
  appStore.addNotification({
    type: 'error',
    title: '请求失败',
    message: createFriendlyMessage({ type: errorType }),
    duration: 5000
  })
  
  return Promise.reject(error)
}

// 基础请求方法
const request = async (endpoint: string, options: RequestInit = {}) => {
  const url = `${API_BASE_URL}${endpoint}`
  
  try {
    // 请求拦截
    const config = requestInterceptor({
      url,
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    })
    
    const response = await fetch(config.url, {
      method: config.method || 'GET',
      headers: config.headers,
      body: config.body,
      signal: AbortSignal.timeout(config.timeout)
    })
    
    // 响应拦截
    const processedResponse = responseInterceptor(response)
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    return errorInterceptor(error)
  }
}

// API服务类
export class ApiService {
  // 认证相关API
  static auth = {
    login: (credentials: { username: string; password: string }) =>
      request('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials)
      }),
    
    logout: () =>
      request('/auth/logout', { method: 'POST' }),
    
    verify: () =>
      request('/auth/verify'),
    
    refresh: () =>
      request('/auth/refresh', { method: 'POST' })
  }

  // 用户相关API
  static user = {
    getProfile: () =>
      request('/user/profile'),
    
    updateProfile: (profile: any) =>
      request('/user/profile', {
        method: 'PUT',
        body: JSON.stringify(profile)
      }),
    
    changePassword: (data: { currentPassword: string; newPassword: string }) =>
      request('/user/password', {
        method: 'PUT',
        body: JSON.stringify(data)
      })
  }

  // 媒体相关API
  static media = {
    // 获取媒体库
    getLibrary: (params?: { page?: number; size?: number; type?: string }) => {
      const query = new URLSearchParams(params as any)
      return request(`/media/library?${query}`)
    },
    
    // 搜索媒体
    search: (query: string, params?: { page?: number; size?: number }) => {
      const searchParams = new URLSearchParams({ q: query, ...params } as any)
      return request(`/media/search?${searchParams}`)
    },
    
    // 获取媒体详情
    getDetail: (id: string) =>
      request(`/media/${id}`),
    
    // 下载媒体
    download: (id: string) =>
      request(`/media/${id}/download`, { method: 'POST' }),
    
    // 删除媒体
    delete: (id: string) =>
      request(`/media/${id}`, { method: 'DELETE' })
  }

  // 订阅相关API
  static subscription = {
    // 获取订阅列表
    getList: (params?: { page?: number; size?: number; status?: string }) => {
      const query = new URLSearchParams(params as any)
      return request(`/subscriptions?${query}`)
    },
    
    // 创建订阅
    create: (data: any) =>
      request('/subscriptions', {
        method: 'POST',
        body: JSON.stringify(data)
      }),
    
    // 更新订阅
    update: (id: string, data: any) =>
      request(`/subscriptions/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
      }),
    
    // 删除订阅
    delete: (id: string) =>
      request(`/subscriptions/${id}`, { method: 'DELETE' }),
    
    // 启用/禁用订阅
    toggle: (id: string, enabled: boolean) =>
      request(`/subscriptions/${id}/toggle`, {
        method: 'POST',
        body: JSON.stringify({ enabled })
      })
  }

  // AI推荐相关API
  static ai = {
    // 获取推荐列表
    getRecommendations: (params?: { type?: string; limit?: number }) => {
      const query = new URLSearchParams(params as any)
      return request(`/ai/recommend?${query}`)
    },
    
    // 个性化推荐
    getPersonalized: () =>
      request('/ai/recommend/personalized'),
    
    // 搜索推荐
    searchRecommendations: (query: string) =>
      request(`/ai/recommend/search?q=${encodeURIComponent(query)}`),
    
    // 提交反馈
    submitFeedback: (data: { itemId: string; feedback: 'like' | 'dislike' | 'neutral' }) =>
      request('/ai/recommend/feedback', {
        method: 'POST',
        body: JSON.stringify(data)
      }),
    
    // 获取推荐统计
    getStats: () =>
      request('/ai/recommend/stats')
  }

  // 插件相关API
  static plugins = {
    // 获取插件列表
    getList: () =>
      request('/plugins'),
    
    // 安装插件
    install: (pluginId: string) =>
      request(`/plugins/${pluginId}/install`, { method: 'POST' }),
    
    // 卸载插件
    uninstall: (pluginId: string) =>
      request(`/plugins/${pluginId}/uninstall`, { method: 'POST' }),
    
    // 启用/禁用插件
    toggle: (pluginId: string, enabled: boolean) =>
      request(`/plugins/${pluginId}/toggle`, {
        method: 'POST',
        body: JSON.stringify({ enabled })
      }),
    
    // 获取插件配置
    getConfig: (pluginId: string) =>
      request(`/plugins/${pluginId}/config`),
    
    // 更新插件配置
    updateConfig: (pluginId: string, config: any) =>
      request(`/plugins/${pluginId}/config`, {
        method: 'PUT',
        body: JSON.stringify(config)
      })
  }

  // 系统相关API
  static system = {
    // 获取系统信息
    getInfo: () =>
      request('/system/info'),
    
    // 获取系统状态
    getStatus: () =>
      request('/system/status'),
    
    // 获取日志
    getLogs: (params?: { level?: string; source?: string; limit?: number }) => {
      const query = new URLSearchParams(params as any)
      return request(`/system/logs?${query}`)
    },
    
    // 清理缓存
    clearCache: () =>
      request('/system/cache/clear', { method: 'POST' }),
    
    // 重启服务
    restart: () =>
      request('/system/restart', { method: 'POST' })
  }

  // 仪表板相关API
  static dashboard = {
    // 获取仪表板统计数据
    getStats: () =>
      request('/dashboard/stats'),
    
    // 获取最近活动
    getRecentActivities: (limit?: number) => {
      const params = limit ? { limit: limit.toString() } : {}
      const query = new URLSearchParams(params)
      return request(`/dashboard/activities?${query}`)
    },
    
    // 获取系统概览
    getOverview: () =>
      request('/dashboard/overview')
  }

  // 设置相关API
  static settings = {
    // 获取设置
    getSettings: () =>
      request('/settings'),
    
    // 保存设置
    saveSettings: (settings: any) =>
      request('/settings', {
        method: 'POST',
        body: JSON.stringify(settings)
      }),
    
    // 检查更新
    checkForUpdates: () =>
      request('/settings/updates'),
    
    // 重置设置
    resetSettings: () =>
      request('/settings/reset', { method: 'POST' })
  }

  // 站点包管理API
  static siteBundle = {
    // 获取所有站点包
    listBundles: () =>
      request('/site-bundles'),
    
    // 获取指定站点包
    getBundle: (id: string) =>
      request(`/site-bundles/${id}`),
    
    // 创建站点包
    createBundle: (data: any) =>
      request('/site-bundles', {
        method: 'POST',
        body: JSON.stringify(data)
      }),
    
    // 更新站点包
    updateBundle: (id: string, data: any) =>
      request(`/site-bundles/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
      }),
    
    // 删除站点包
    deleteBundle: (id: string) =>
      request(`/site-bundles/${id}`, { method: 'DELETE' }),
    
    // 导入站点包
    importBundle: (content: string) =>
      request('/site-bundles/import', {
        method: 'POST',
        body: JSON.stringify({ file_content: content })
      }),
    
    // 导出站点包
    exportBundle: (id: string) =>
      request(`/site-bundles/${id}/export`)
  }

  // 文件管理相关API
  static file = {
    // 获取文件列表
    list: (path: string) =>
      request(`/file/list?path=${encodeURIComponent(path)}`),
    
    // 上传文件
    upload: (formData: FormData) =>
      request('/file/upload', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }),
    
    // 删除文件
    delete: (path: string) =>
      request(`/file/delete?path=${encodeURIComponent(path)}`, { method: 'DELETE' }),
    
    // 重命名文件
    rename: (oldPath: string, newPath: string) =>
      request('/file/rename', {
        method: 'POST',
        body: JSON.stringify({ oldPath, newPath })
      })
  }
}

export default ApiService