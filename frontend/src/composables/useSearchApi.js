import { ref } from 'vue'
import { useApi } from './useApi'

/**
 * 搜索API组合函数
 * 提供统一的搜索功能，支持电影、电视剧、动漫、音乐等多种媒体类型
 */

export function useSearchApi() {
  const { get, post, del } = useApi()
  
  // 响应式数据
  const searchResults = ref([])
  const searchHistory = ref([])
  const suggestions = ref([])
  const searching = ref(false)
  const totalResults = ref(0)
  const lastQuery = ref('')

  /**
   * 执行搜索
   * @param {Object} params - 搜索参数
   * @param {string} params.query - 搜索关键词
   * @param {string} params.type - 搜索类型
   * @param {string[]} params.sources - 搜索源
   */
  const performSearch = async (params) => {
    searching.value = true
    
    try {
      const response = await post('/api/search/', params)
      
      if (response.success) {
        searchResults.value = response.data.results || []
        suggestions.value = response.data.suggestions || []
        totalResults.value = response.data.total || 0
        lastQuery.value = response.data.query || ''
        
        // 更新搜索历史
        await getSearchHistory()
      } else {
        console.error('搜索失败:', response.message)
        searchResults.value = []
        suggestions.value = []
        totalResults.value = 0
      }
    } catch (error) {
      console.error('搜索请求失败:', error)
      searchResults.value = []
      suggestions.value = []
      totalResults.value = 0
    } finally {
      searching.value = false
    }
  }

  /**
   * 根据ID搜索
   * @param {string} mediaId - 媒体ID
   * @param {string} source - 搜索源
   * @param {string} type - 搜索类型
   */
  const searchById = async (mediaId, source = 'tmdb', type = 'all') => {
    try {
      const response = await post('/api/search/by-id', {
        media_id: mediaId,
        source: source,
        type: type
      })
      
      return response.data
    } catch (error) {
      console.error('根据ID搜索失败:', error)
      return null
    }
  }

  /**
   * 搜索音乐
   * @param {string} query - 搜索关键词
   * @param {string[]} sources - 搜索源
   * @param {number} limit - 结果数量限制
   */
  const searchMusic = async (query, sources = null, limit = 20) => {
    searching.value = true
    
    try {
      const params = { query }
      if (sources) {
        params.sources = sources.join(',')
      }
      if (limit) {
        params.limit = limit
      }
      
      const response = await get('/api/search/music', params)
      
      if (response.success) {
        searchResults.value = response.data.results || []
        suggestions.value = response.data.suggestions || []
        totalResults.value = response.data.total || 0
        lastQuery.value = response.data.query || ''
        return response.data
      } else {
        console.error('音乐搜索失败:', response.message)
        return null
      }
    } catch (error) {
      console.error('音乐搜索请求失败:', error)
      return null
    } finally {
      searching.value = false
    }
  }

  /**
   * 搜索本地媒体库
   * @param {string} query - 搜索关键词
   * @param {string} type - 搜索类型
   * @param {number} limit - 结果数量限制
   */
  const searchLocal = async (query, type = 'all', limit = 50) => {
    try {
      const response = await get('/api/search/local', {
        query: query,
        type: type,
        limit: limit
      })
      
      return response.data
    } catch (error) {
      console.error('本地搜索失败:', error)
      return null
    }
  }

  /**
   * 获取搜索建议
   * @param {string} query - 搜索关键词
   * @param {number} limit - 建议数量限制
   */
  const getSuggestions = async (query, limit = 10) => {
    try {
      const response = await get('/api/search/suggestions', {
        query: query,
        limit: limit
      })
      
      suggestions.value = response.data || []
      return suggestions.value
    } catch (error) {
      console.error('获取搜索建议失败:', error)
      suggestions.value = []
      return []
    }
  }

  /**
   * 获取搜索历史
   * @param {number} limit - 历史记录数量限制
   */
  const getSearchHistory = async (limit = 20) => {
    try {
      const response = await get('/api/search/history', { limit })
      
      if (response.success) {
        searchHistory.value = response.data.history || []
        return searchHistory.value
      } else {
        console.error('获取搜索历史失败:', response.message)
        searchHistory.value = []
        return []
      }
    } catch (error) {
      console.error('获取搜索历史请求失败:', error)
      searchHistory.value = []
      return []
    }
  }

  /**
   * 清空搜索历史
   */
  const clearSearchHistory = async () => {
    try {
      const response = await del('/api/search/history')
      
      if (response.success) {
        searchHistory.value = []
        return true
      } else {
        console.error('清空搜索历史失败:', response.message)
        return false
      }
    } catch (error) {
      console.error('清空搜索历史请求失败:', error)
      return false
    }
  }

  /**
   * 获取可用的搜索源
   */
  const getSearchSources = async () => {
    try {
      const response = await get('/api/search/sources')
      return response.data
    } catch (error) {
      console.error('获取搜索源失败:', error)
      return { sources: {} }
    }
  }

  /**
   * 获取可用的搜索类型
   */
  const getSearchTypes = async () => {
    try {
      const response = await get('/api/search/types')
      return response.data
    } catch (error) {
      console.error('获取搜索类型失败:', error)
      return { types: [] }
    }
  }

  /**
   * 清空搜索结果
   */
  const clearResults = () => {
    searchResults.value = []
    suggestions.value = []
    totalResults.value = 0
    lastQuery.value = ''
  }

  /**
   * 检查搜索服务状态
   */
  const checkSearchHealth = async () => {
    try {
      const response = await get('/api/search/health')
      return response.data.status === 'healthy'
    } catch (error) {
      console.error('搜索服务健康检查失败:', error)
      return false
    }
  }

  return {
    // 响应式数据
    searchResults,
    searchHistory,
    suggestions,
    searching,
    totalResults,
    lastQuery,
    
    // 方法
    performSearch,
    searchById,
    searchMusic,
    searchLocal,
    getSuggestions,
    getSearchHistory,
    clearSearchHistory,
    getSearchSources,
    getSearchTypes,
    clearResults,
    checkSearchHealth
  }
}