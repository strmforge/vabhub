import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8090',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加认证token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 处理错误响应
    if (error.response?.status === 401) {
      // 认证失败，清除token并跳转到登录页
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

// API方法定义
export const mediaAPI = {
  // 扫描媒体
  scan: (data) => api.post('/media/scan', data),
  
  // 获取媒体列表
  list: (params) => api.get('/media', { params }),
  
  // 获取媒体详情
  get: (id) => api.get(`/media/${id}`),
  
  // 更新媒体信息
  update: (id, data) => api.put(`/media/${id}`, data),
  
  // 删除媒体
  delete: (id) => api.delete(`/media/${id}`)
}

export const pluginAPI = {
  // 获取插件列表
  list: (status) => api.get('/plugins', { params: { status } }),
  
  // 安装插件
  install: (id) => api.post(`/plugins/${id}/install`),
  
  // 卸载插件
  uninstall: (id) => api.post(`/plugins/${id}/uninstall`),
  
  // 启用插件
  enable: (id) => api.post(`/plugins/${id}/enable`),
  
  // 禁用插件
  disable: (id) => api.post(`/plugins/${id}/disable`)
}

export const settingsAPI = {
  // 获取设置
  get: () => api.get('/settings'),
  
  // 更新设置
  update: (data) => api.post('/settings', data),
  
  // 重启系统
  restart: () => api.post('/system/restart')
}

export const authAPI = {
  // 登录
  login: (data) => api.post('/auth/login', data),
  
  // 登出
  logout: () => api.post('/auth/logout'),
  
  // 获取用户信息
  getUserInfo: () => api.get('/auth/user')
}

export const taskAPI = {
  // 获取任务状态
  getStatus: (id) => api.get(`/tasks/${id}`)
}

export const systemAPI = {
  // 健康检查
  health: () => api.get('/health'),
  
  // 获取配置
  config: () => api.get('/config'),
  
  // 更新配置
  updateConfig: (data) => api.post('/config/update', data)
}

// 事件系统API
export const eventAPI = {
  // 获取事件列表
  list: (params) => api.get('/events', { params }),
  
  // 触发事件
  trigger: (eventType, data) => api.post('/events/trigger', { event_type: eventType, data }),
  
  // 获取事件统计
  stats: () => api.get('/events/stats')
}

// 调度器API
export const schedulerAPI = {
  // 获取任务列表
  list: () => api.get('/scheduler/jobs'),
  
  // 添加任务
  add: (jobData) => api.post('/scheduler/jobs', jobData),
  
  // 暂停任务
  pause: (id) => api.post(`/scheduler/jobs/${id}/pause`),
  
  // 恢复任务
  resume: (id) => api.post(`/scheduler/jobs/${id}/resume`),
  
  // 删除任务
  remove: (id) => api.delete(`/scheduler/jobs/${id}`),
  
  // 立即执行任务
  run: (id) => api.post(`/scheduler/jobs/${id}/run`)
}

// 业务链API
export const chainAPI = {
  // 执行业务链
  execute: (chainId, data) => api.post(`/chains/${chainId}/execute`, data),
  
  // 获取执行历史
  history: (chainId) => api.get(`/chains/${chainId}/history`)
}

export default {
  media: mediaAPI,
  plugin: pluginAPI,
  settings: settingsAPI,
  auth: authAPI,
  task: taskAPI,
  system: systemAPI,
  event: eventAPI,
  scheduler: schedulerAPI,
  chain: chainAPI
}