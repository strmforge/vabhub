// API响应基础类型
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  code?: number
  timestamp?: string
}

// 分页响应类型
export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination?: {
    page: number
    size: number
    total: number
    totalPages: number
  }
}

// 认证相关类型
export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
  user: UserInfo
  expiresIn: number
}

export interface UserInfo {
  id: string
  username: string
  email: string
  avatar?: string
  role: string
  permissions: string[]
  createdAt: string
  updatedAt: string
}

// 媒体相关类型
export interface MediaItem {
  id: string
  title: string
  type: 'movie' | 'tv' | 'anime' | 'documentary'
  year?: number
  poster?: string
  backdrop?: string
  overview?: string
  rating?: number
  genres?: string[]
  duration?: number
  status: 'available' | 'downloading' | 'processing' | 'error'
  filePath?: string
  fileSize?: number
  createdAt: string
  updatedAt: string
}

export interface MediaSearchParams {
  q: string
  page?: number
  size?: number
  type?: string
  genre?: string
  year?: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

// 订阅相关类型
export interface Subscription {
  id: string
  name: string
  type: 'movie' | 'tv' | 'anime' | 'custom'
  enabled: boolean
  status: 'active' | 'paused' | 'error'
  searchQuery?: string
  filters?: Record<string, any>
  downloadPath?: string
  quality?: string
  language?: string
  lastRun?: string
  nextRun?: string
  createdAt: string
  updatedAt: string
}

export interface SubscriptionCreateRequest {
  name: string
  type: string
  searchQuery?: string
  filters?: Record<string, any>
  downloadPath?: string
  quality?: string
  language?: string
}

// AI推荐相关类型
export interface Recommendation {
  id: string
  title: string
  type: string
  poster: string
  overview: string
  rating: number
  similarity: number
  reasons: string[]
  source: 'collaborative' | 'content' | 'popular' | 'trending'
}

export interface RecommendationFeedback {
  itemId: string
  feedback: 'like' | 'dislike' | 'neutral'
}

export interface RecommendationStats {
  totalRecommendations: number
  likedCount: number
  dislikedCount: number
  accuracy: number
  lastUpdated: string
}

// 插件相关类型
export interface Plugin {
  id: string
  name: string
  version: string
  description: string
  author: string
  enabled: boolean
  installed: boolean
  hasUpdate: boolean
  configSchema?: Record<string, any>
  config?: Record<string, any>
  dependencies?: string[]
  createdAt: string
  updatedAt: string
}

// 系统相关类型
export interface SystemInfo {
  version: string
  build: string
  nodeVersion: string
  platform: string
  arch: string
  uptime: number
  memory: {
    total: number
    used: number
    free: number
  }
  disk: {
    total: number
    used: number
    free: number
  }
}

export interface SystemStatus {
  status: 'running' | 'stopped' | 'error'
  services: {
    database: boolean
    downloader: boolean
    scanner: boolean
    notifier: boolean
  }
  activeTasks: number
  queueSize: number
  lastError?: string
}

export interface LogEntry {
  id: string
  level: 'debug' | 'info' | 'warning' | 'error'
  source: string
  message: string
  timestamp: string
  metadata?: Record<string, any>
}

// 文件管理相关类型
export interface FileItem {
  name: string
  path: string
  type: 'file' | 'directory'
  size?: number
  modified: string
  extension?: string
}

export interface FileUploadResponse {
  success: boolean
  filePath: string
  message?: string
}

// WebSocket消息类型
export interface WSMessage {
  type: string
  payload?: any
  timestamp: string
}

export interface NotificationMessage {
  level: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  duration?: number
}

export interface DownloadProgressMessage {
  taskId: string
  fileName: string
  progress: number
  speed: number
  eta: number
  status: 'downloading' | 'completed' | 'error'
}

export interface SystemStatusMessage {
  status: SystemStatus
  timestamp: string
}