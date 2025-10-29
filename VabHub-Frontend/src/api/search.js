import axios from 'axios'

// API基础配置
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8090'

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 添加认证token等
    const token = localStorage.getItem('auth_token')
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
      return Promise.reject(new Error(message))
    } else if (error.request) {
      // 请求已发出但没有收到响应
      return Promise.reject(new Error('网络连接失败，请检查网络设置'))
    } else {
      // 其他错误
      return Promise.reject(new Error(error.message))
    }
  }
)

// 搜索API接口
export const searchAPI = {
  // 基础搜索
  async search(params) {
    try {
      const response = await apiClient.post('/api/search/', params)
      return response
    } catch (error) {
      console.error('Search API error:', error)
      throw error
    }
  },

  // 增强版搜索
  async enhancedSearch(params) {
    try {
      const response = await apiClient.post('/api/search/v2/', params)
      return response
    } catch (error) {
      console.error('Enhanced search API error:', error)
      throw error
    }
  },

  // 根据ID搜索
  async searchById(params) {
    try {
      const response = await apiClient.post('/api/search/by-id', params)
      return response
    } catch (error) {
      console.error('Search by ID API error:', error)
      throw error
    }
  },

  // 音乐搜索
  async searchMusic(params) {
    try {
      const response = await apiClient.get('/api/search/music', { params })
      return response
    } catch (error) {
      console.error('Music search API error:', error)
      throw error
    }
  },

  // 本地搜索
  async searchLocal(params) {
    try {
      const response = await apiClient.get('/api/search/local', { params })
      return response
    } catch (error) {
      console.error('Local search API error:', error)
      throw error
    }
  },

  // 获取搜索建议
  async getSuggestions(query, limit = 10) {
    try {
      const response = await apiClient.get('/api/search/suggestions', {
        params: { query, limit }
      })
      return response
    } catch (error) {
      console.error('Get suggestions API error:', error)
      throw error
    }
  },

  // 获取搜索历史
  async getHistory(limit = 20, offset = 0) {
    try {
      const response = await apiClient.get('/api/search/history', {
        params: { limit, offset }
      })
      return response
    } catch (error) {
      console.error('Get search history API error:', error)
      throw error
    }
  },

  // 删除搜索历史
  async deleteHistory(queryId) {
    try {
      const response = await apiClient.delete(`/api/search/history/${queryId}`)
      return response
    } catch (error) {
      console.error('Delete search history API error:', error)
      throw error
    }
  },

  // 清空搜索历史
  async clearHistory() {
    try {
      const response = await apiClient.delete('/api/search/history')
      return response
    } catch (error) {
      console.error('Clear search history API error:', error)
      throw error
    }
  },

  // 获取热门搜索
  async getTrending() {
    try {
      const response = await apiClient.get('/api/search/trending')
      return response
    } catch (error) {
      console.error('Get trending searches API error:', error)
      throw error
    }
  },

  // 获取搜索源
  async getSources() {
    try {
      const response = await apiClient.get('/api/search/sources')
      return response
    } catch (error) {
      console.error('Get search sources API error:', error)
      throw error
    }
  },

  // 获取搜索类型
  async getTypes() {
    try {
      const response = await apiClient.get('/api/search/types')
      return response
    } catch (error) {
      console.error('Get search types API error:', error)
      throw error
    }
  },

  // 健康检查
  async healthCheck() {
    try {
      const response = await apiClient.get('/api/search/health')
      return response
    } catch (error) {
      console.error('Search health check API error:', error)
      throw error
    }
  }
}

// 搜索工具函数
export const searchUtils = {
  // 格式化搜索结果
  formatSearchResults(results) {
    return results.map(result => ({
      id: result.id || this.generateId(),
      title: result.title,
      type: result.type,
      source: result.source,
      score: result.score || 0,
      metadata: result.metadata || {},
      download_info: result.download_info || null,
      timestamp: result.timestamp || new Date().toISOString()
    }))
  },

  // 生成唯一ID
  generateId() {
    return 'search_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
  },

  // 过滤搜索结果
  filterResults(results, filters) {
    return results.filter(result => {
      for (const filter of filters) {
        if (!this.matchesFilter(result, filter)) {
          return false
        }
      }
      return true
    })
  },

  // 检查结果是否匹配过滤器
  matchesFilter(result, filter) {
    const { field, operator, value } = filter
    
    switch (field) {
      case 'type':
        return this.compareValues(result.type, operator, value)
      case 'source':
        return this.compareValues(result.source, operator, value)
      case 'quality':
        return this.compareValues(result.metadata?.quality, operator, value)
      case 'year':
        return this.compareValues(result.metadata?.year, operator, value)
      case 'rating':
        return this.compareValues(result.metadata?.rating, operator, value)
      default:
        return true
    }
  },

  // 比较值
  compareValues(actual, operator, expected) {
    if (actual === undefined || actual === null) return false
    
    switch (operator) {
      case 'equals':
        return actual === expected
      case 'contains':
        return String(actual).toLowerCase().includes(String(expected).toLowerCase())
      case 'greater_than':
        return Number(actual) > Number(expected)
      case 'less_than':
        return Number(actual) < Number(expected)
      default:
        return true
    }
  },

  // 排序搜索结果
  sortResults(results, sortBy = 'score', sortOrder = 'desc') {
    return results.sort((a, b) => {
      let aValue = a[sortBy]
      let bValue = b[sortBy]
      
      // 处理嵌套属性
      if (sortBy.includes('.')) {
        const keys = sortBy.split('.')
        aValue = keys.reduce((obj, key) => obj?.[key], a)
        bValue = keys.reduce((obj, key) => obj?.[key], b)
      }
      
      if (sortOrder === 'asc') {
        return this.compare(aValue, bValue)
      } else {
        return this.compare(bValue, aValue)
      }
    })
  },

  // 通用比较函数
  compare(a, b) {
    if (a === b) return 0
    if (a === undefined || a === null) return 1
    if (b === undefined || b === null) return -1
    
    if (typeof a === 'number' && typeof b === 'number') {
      return a - b
    }
    
    return String(a).localeCompare(String(b))
  },

  // 分页结果
  paginateResults(results, page = 1, pageSize = 20) {
    const startIndex = (page - 1) * pageSize
    const endIndex = startIndex + pageSize
    
    return {
      data: results.slice(startIndex, endIndex),
      pagination: {
        page,
        pageSize,
        total: results.length,
        totalPages: Math.ceil(results.length / pageSize),
        hasNext: endIndex < results.length,
        hasPrev: page > 1
      }
    }
  },

  // 搜索关键词高亮
  highlightText(text, query) {
    if (!query || !text) return text
    
    const regex = new RegExp(`(${this.escapeRegex(query)})`, 'gi')
    return text.replace(regex, '<mark>$1</mark>')
  },

  // 转义正则表达式特殊字符
  escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  },

  // 计算搜索相关性分数
  calculateRelevanceScore(result, query) {
    let score = 0
    
    // 标题匹配度
    if (result.title && query) {
      const titleLower = result.title.toLowerCase()
      const queryLower = query.toLowerCase()
      
      if (titleLower === queryLower) {
        score += 10
      } else if (titleLower.includes(queryLower)) {
        score += 5
      } else if (this.calculateSimilarity(titleLower, queryLower) > 0.7) {
        score += 3
      }
    }
    
    // 源优先级
    const sourceScores = {
      'tmdb': 3,
      'douban': 2,
      'local': 4,
      'netflix_top10': 3,
      'imdb_datasets': 3
    }
    score += sourceScores[result.source] || 1
    
    // 质量分数
    if (result.metadata?.quality) {
      const qualityScores = {
        'REMUX': 3,
        'BluRay': 2,
        'WEB-DL': 2,
        'HDTV': 1
      }
      score += qualityScores[result.metadata.quality] || 0
    }
    
    // 评分分数
    if (result.metadata?.rating) {
      score += result.metadata.rating / 2
    }
    
    return score
  },

  // 计算字符串相似度
  calculateSimilarity(str1, str2) {
    const len1 = str1.length
    const len2 = str2.length
    const maxLen = Math.max(len1, len2)
    
    if (maxLen === 0) return 1
    
    const distance = this.levenshteinDistance(str1, str2)
    return 1 - distance / maxLen
  },

  // 莱文斯坦距离算法
  levenshteinDistance(str1, str2) {
    const matrix = []
    
    for (let i = 0; i <= str2.length; i++) {
      matrix[i] = [i]
    }
    
    for (let j = 0; j <= str1.length; j++) {
      matrix[0][j] = j
    }
    
    for (let i = 1; i <= str2.length; i++) {
      for (let j = 1; j <= str1.length; j++) {
        if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1]
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          )
        }
      }
    }
    
    return matrix[str2.length][str1.length]
  }
}

// 默认导出
export default searchAPI