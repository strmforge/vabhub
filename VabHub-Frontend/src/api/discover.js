// 发现推荐API客户端
import axios from 'axios'

// API基础配置
const API_BASE_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8000'
const DISCOVER_API_ENDPOINT = '/api/discover'

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token
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
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    
    if (error.response) {
      // 服务器返回错误状态码
      const message = error.response.data?.detail || error.response.data?.message || '请求失败'
      throw new Error(`API Error (${error.response.status}): ${message}`)
    } else if (error.request) {
      // 请求未收到响应
      throw new Error('网络连接错误，请检查网络连接')
    } else {
      // 其他错误
      throw new Error(error.message)
    }
  }
)

// API方法
export const discoverAPI = {
  // 获取发现项目
  async getDiscover(params = {}) {
    const { category = 'all', source = null, page = 1, limit = 20 } = params
    
    const requestData = {
      category,
      source,
      page,
      limit
    }
    
    return await apiClient.post(DISCOVER_API_ENDPOINT + '/', requestData)
  },
  
  // 获取个性化推荐
  async getPersonalized(params = {}) {
    const { user_id = null, limit = 10 } = params
    
    const requestData = {
      user_id,
      limit
    }
    
    return await apiClient.post(DISCOVER_API_ENDPOINT + '/personalized', requestData)
  },
  
  // 获取趋势推荐
  async getTrending(params = {}) {
    const { category = 'all', limit = 10 } = params
    
    const requestData = {
      category,
      limit
    }
    
    return await apiClient.post(DISCOVER_API_ENDPOINT + '/trending', requestData)
  },
  
  // 获取发现系统信息
  async getInfo() {
    return await apiClient.get(DISCOVER_API_ENDPOINT + '/info')
  },
  
  // 获取分类列表
  async getCategories() {
    return await apiClient.get(DISCOVER_API_ENDPOINT + '/categories')
  },
  
  // 获取数据源列表
  async getSources() {
    return await apiClient.get(DISCOVER_API_ENDPOINT + '/sources')
  },
  
  // 手动刷新发现数据
  async refreshData() {
    return await apiClient.post(DISCOVER_API_ENDPOINT + '/refresh')
  },
  
  // 获取电影发现
  async getMovies(params = {}) {
    const { source = null, page = 1, limit = 20 } = params
    
    return await apiClient.get(DISCOVER_API_ENDPOINT + '/movies', {
      params: {
        source,
        page,
        limit
      }
    })
  },
  
  // 获取电视剧发现
  async getTVs(params = {}) {
    const { source = null, page = 1, limit = 20 } = params
    
    return await apiClient.get(DISCOVER_API_ENDPOINT + '/tvs', {
      params: {
        source,
        page,
        limit
      }
    })
  },
  
  // 获取音乐发现
  async getMusic(params = {}) {
    const { source = null, page = 1, limit = 20 } = params
    
    return await apiClient.get(DISCOVER_API_ENDPOINT + '/music', {
      params: {
        source,
        page,
        limit
      }
    })
  },
  
  // 健康检查
  async healthCheck() {
    return await apiClient.get(DISCOVER_API_ENDPOINT + '/health')
  }
}

// 工具函数
export const discoverUtils = {
  // 获取分类显示名称
  getCategoryDisplayName(category) {
    const names = {
      'all': '全部',
      'movie': '电影',
      'tv': '电视剧',
      'anime': '动漫',
      'music': '音乐'
    }
    return names[category] || category
  },
  
  // 获取数据源显示名称
  getSourceDisplayName(source) {
    const names = {
      'tmdb': 'TMDB',
      'douban': '豆瓣',
      'bangumi': 'Bangumi',
      'netflix_top10': 'Netflix Top 10',
      'imdb_datasets': 'IMDb Datasets',
      'spotify': 'Spotify',
      'apple_music': 'Apple Music'
    }
    return names[source] || source
  },
  
  // 获取分类图标
  getCategoryIcon(category) {
    const icons = {
      'movie': '🎬',
      'tv': '📺',
      'anime': '🎨',
      'music': '🎵',
      'all': '📄'
    }
    return icons[category] || '📄'
  },
  
  // 格式化日期
  formatDate(dateString) {
    try {
      const date = new Date(dateString)
      return date.getFullYear() + '-' + 
             String(date.getMonth() + 1).padStart(2, '0') + '-' + 
             String(date.getDate()).padStart(2, '0')
    } catch {
      return dateString
    }
  },
  
  // 截断描述文本
  truncateText(text, maxLength = 100) {
    if (!text) return ''
    if (text.length <= maxLength) {
      return text
    }
    return text.substring(0, maxLength) + '...'
  },
  
  // 处理图片加载错误
  handleImageError(event, placeholderClass = 'placeholder-poster') {
    const target = event.target
    target.style.display = 'none'
    
    // 显示占位符
    const placeholder = target.parentElement.querySelector(`.${placeholderClass}`)
    if (placeholder) {
      placeholder.style.display = 'flex'
    }
  },
  
  // 获取默认海报URL
  getDefaultPosterUrl(category) {
    const defaultImages = {
      'movie': '/images/default-movie-poster.jpg',
      'tv': '/images/default-tv-poster.jpg',
      'anime': '/images/default-anime-poster.jpg',
      'music': '/images/default-music-cover.jpg',
      'all': '/images/default-poster.jpg'
    }
    return defaultImages[category] || defaultImages['all']
  }
}

// 导出默认配置
export default {
  api: discoverAPI,
  utils: discoverUtils
}