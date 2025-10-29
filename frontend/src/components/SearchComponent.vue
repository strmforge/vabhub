<template>
  <div class="search-container">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <div class="search-input-container">
        <input
          v-model="searchQuery"
          @input="handleInput"
          @focus="showSuggestions = true"
          @blur="onInputBlur"
          @keyup.enter="performSearch"
          placeholder="搜索电影、电视剧、音乐..."
          class="search-input"
          type="text"
        />
        <button @click="performSearch" class="search-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" 
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <!-- 搜索建议 -->
      <div v-if="showSuggestions && suggestions.length > 0" class="suggestions-panel">
        <div class="suggestions-header">
          <span>搜索建议</span>
          <button @click="clearSuggestions" class="clear-suggestions">清除</button>
        </div>
        <div class="suggestions-list">
          <div 
            v-for="suggestion in suggestions" 
            :key="suggestion"
            @click="selectSuggestion(suggestion)"
            class="suggestion-item"
          >
            {{ suggestion }}
          </div>
        </div>
      </div>

      <!-- 热门搜索 -->
      <div v-if="showSuggestions && trendingSearches.length > 0" class="trending-panel">
        <div class="trending-header">
          <span>热门搜索</span>
        </div>
        <div class="trending-list">
          <span 
            v-for="trend in trendingSearches" 
            :key="trend"
            @click="selectSuggestion(trend)"
            class="trending-tag"
          >
            {{ trend }}
          </span>
        </div>
      </div>
    </div>

    <!-- 搜索结果 -->
    <div v-if="searchResults.length > 0" class="search-results">
      <div class="results-header">
        <h3>搜索结果 ({{ totalResults }} 个)</h3>
        <div class="results-filters">
          <select v-model="selectedType" @change="filterResults" class="filter-select">
            <option value="all">全部类型</option>
            <option value="movie">电影</option>
            <option value="tv">电视剧</option>
            <option value="anime">动漫</option>
            <option value="music">音乐</option>
          </select>
          <select v-model="selectedSource" @change="filterResults" class="filter-select">
            <option value="all">全部来源</option>
            <option value="tmdb">TMDB</option>
            <option value="douban">豆瓣</option>
            <option value="netflix_top10">Netflix Top 10</option>
            <option value="imdb_datasets">IMDb Datasets</option>
            <option value="local">本地</option>
          </select>
        </div>
      </div>

      <div class="results-grid">
        <div 
          v-for="result in filteredResults" 
          :key="result.id || result.title"
          class="result-card"
          @click="selectResult(result)"
        >
          <div class="result-image">
            <img v-if="result.metadata?.poster" :src="result.metadata.poster" :alt="result.title" />
            <div v-else class="placeholder-image">
              {{ getTypeIcon(result.type) }}
            </div>
          </div>
          <div class="result-content">
            <h4 class="result-title">{{ result.title }}</h4>
            <div class="result-meta">
              <span class="result-type">{{ getTypeName(result.type) }}</span>
              <span class="result-source">{{ getSourceName(result.source) }}</span>
              <span v-if="result.metadata?.year" class="result-year">{{ result.metadata.year }}</span>
              <span v-if="result.metadata?.rating" class="result-rating">⭐ {{ result.metadata.rating }}</span>
            </div>
            <p v-if="result.metadata?.overview" class="result-description">
              {{ result.metadata.overview }}
            </p>
            <div v-if="result.download_info" class="download-info">
              <span class="download-size">{{ result.download_info.size }}</span>
              <span class="download-seeds">{{ result.download_info.seeds }} 种子</span>
            </div>
          </div>
          <div class="result-actions">
            <button @click.stop="downloadResult(result)" class="action-btn download-btn">
              下载
            </button>
            <button @click.stop="addToLibrary(result)" class="action-btn library-btn">
              收藏
            </button>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalResults > pageSize" class="pagination">
        <button 
          @click="previousPage" 
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          上一页
        </button>
        <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
        <button 
          @click="nextPage" 
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          下一页
        </button>
      </div>
    </div>

    <!-- 搜索历史 -->
    <div v-if="searchHistory.length > 0 && !searchResults.length" class="search-history">
      <div class="history-header">
        <h3>搜索历史</h3>
        <button @click="clearHistory" class="clear-history">清除历史</button>
      </div>
      <div class="history-list">
        <div 
          v-for="history in searchHistory" 
          :key="history.timestamp"
          @click="selectHistory(history)"
          class="history-item"
        >
          <span class="history-query">{{ history.query }}</span>
          <span class="history-time">{{ formatTime(history.timestamp) }}</span>
          <button @click.stop="deleteHistory(history)" class="delete-history">×</button>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>搜索中...</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="retrySearch" class="retry-btn">重试</button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { searchAPI } from '../api/search'

export default {
  name: 'SearchComponent',
  setup() {
    // 响应式数据
    const searchQuery = ref('')
    const searchResults = ref([])
    const suggestions = ref([])
    const trendingSearches = ref([])
    const searchHistory = ref([])
    const showSuggestions = ref(false)
    const loading = ref(false)
    const error = ref('')
    const selectedType = ref('all')
    const selectedSource = ref('all')
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalResults = ref(0)

    // 计算属性
    const filteredResults = computed(() => {
      return searchResults.value.filter(result => {
        const typeMatch = selectedType.value === 'all' || result.type === selectedType.value
        const sourceMatch = selectedSource.value === 'all' || result.source === selectedSource.value
        return typeMatch && sourceMatch
      })
    })

    const totalPages = computed(() => {
      return Math.ceil(totalResults.value / pageSize.value)
    })

    // 方法
    const handleInput = async () => {
      if (searchQuery.value.length > 1) {
        await getSuggestions()
      } else {
        suggestions.value = []
      }
    }

    const onInputBlur = () => {
      setTimeout(() => {
        showSuggestions.value = false
      }, 200)
    }

    const performSearch = async () => {
      if (!searchQuery.value.trim()) return
      
      loading.value = true
      error.value = ''
      
      try {
        const response = await searchAPI.search({
          query: searchQuery.value,
          type: 'all',
          limit: pageSize.value,
          offset: (currentPage.value - 1) * pageSize.value
        })
        
        searchResults.value = response.results
        totalResults.value = response.total
        
        // 添加到搜索历史
        addToHistory(searchQuery.value)
        
      } catch (err) {
        error.value = '搜索失败，请重试'
        console.error('Search error:', err)
      } finally {
        loading.value = false
        showSuggestions.value = false
      }
    }

    const getSuggestions = async () => {
      try {
        const response = await searchAPI.getSuggestions(searchQuery.value)
        suggestions.value = response.suggestions.slice(0, 5)
      } catch (err) {
        console.error('Get suggestions error:', err)
      }
    }

    const selectSuggestion = (suggestion) => {
      searchQuery.value = suggestion
      performSearch()
    }

    const clearSuggestions = () => {
      suggestions.value = []
    }

    const filterResults = () => {
      currentPage.value = 1
    }

    const previousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        performSearch()
      }
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
        performSearch()
      }
    }

    const selectResult = (result) => {
      // 处理结果选择
      console.log('Selected result:', result)
      // 这里可以跳转到详情页面或执行其他操作
    }

    const downloadResult = (result) => {
      // 处理下载
      console.log('Download result:', result)
    }

    const addToLibrary = (result) => {
      // 添加到媒体库
      console.log('Add to library:', result)
    }

    const addToHistory = (query) => {
      const historyRecord = searchHistoryManager.addSearch(query, 'combined', 'all', [])
      searchHistory.value = searchHistoryManager.getHistory()
    }

    const selectHistory = (history) => {
      searchQuery.value = history.query
      performSearch()
    }

    const deleteHistory = (history) => {
      searchHistoryManager.deleteSearch(history.id)
      searchHistory.value = searchHistoryManager.getHistory()
    }

    const clearHistory = () => {
      searchHistoryManager.clearHistory()
      searchHistory.value = []
    }

    const retrySearch = () => {
      error.value = ''
      performSearch()
    }

    const getTypeIcon = (type) => {
      const icons = {
        movie: '🎬',
        tv: '📺',
        anime: '🎨',
        music: '🎵'
      }
      return icons[type] || '📄'
    }

    const getTypeName = (type) => {
      const names = {
        movie: '电影',
        tv: '电视剧',
        anime: '动漫',
        music: '音乐'
      }
      return names[type] || '未知'
    }

    const getSourceName = (source) => {
      const names = {
        tmdb: 'TMDB',
        douban: '豆瓣',
        netflix_top10: 'Netflix Top 10',
        imdb_datasets: 'IMDb Datasets',
        spotify: 'Spotify',
        apple_music: 'Apple Music',
        local: '本地'
      }
      return names[source] || source
    }

    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date
      
      if (diff < 60000) return '刚刚'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
      
      return date.toLocaleDateString()
    }

    // 生命周期
    onMounted(() => {
      // 加载搜索历史
      searchHistory.value = searchHistoryManager.getHistory()
      
      // 加载热门搜索
      loadTrendingSearches()
    })

    const loadTrendingSearches = async () => {
      try {
        const response = await searchAPI.getTrending()
        trendingSearches.value = response.trending_searches || []
      } catch (err) {
        console.error('Load trending searches error:', err)
      }
    }

    return {
      searchQuery,
      searchResults,
      suggestions,
      trendingSearches,
      searchHistory,
      showSuggestions,
      loading,
      error,
      selectedType,
      selectedSource,
      currentPage,
      pageSize,
      totalResults,
      filteredResults,
      totalPages,
      handleInput,
      onInputBlur,
      performSearch,
      selectSuggestion,
      clearSuggestions,
      filterResults,
      previousPage,
      nextPage,
      selectResult,
      downloadResult,
      addToLibrary,
      selectHistory,
      deleteHistory,
      clearHistory,
      retrySearch,
      getTypeIcon,
      getTypeName,
      getSourceName,
      formatTime
    }
  }
}
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-bar {
  position: relative;
  margin-bottom: 30px;
}

.search-input-container {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 12px 50px 12px 20px;
  border: 2px solid #e1e5e9;
  border-radius: 25px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #007bff;
}

.search-button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 5px;
}

.search-button:hover {
  color: #007bff;
}

.suggestions-panel,
.trending-panel {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  z-index: 1000;
  margin-top: 5px;
}

.suggestions-header,
.trending-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #e1e5e9;
  font-weight: 600;
}

.clear-suggestions {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 12px;
}

.suggestions-list {
  max-height: 200px;
  overflow-y: auto;
}

.suggestion-item {
  padding: 10px 15px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.suggestion-item:hover {
  background: #f8f9fa;
}

.trending-list {
  padding: 10px 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.trending-tag {
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.3s;
}

.trending-tag:hover {
  background: #e9ecef;
}

.search-results {
  margin-top: 30px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.results-filters {
  display: flex;
  gap: 10px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #e1e5e9;
  border-radius: 4px;
  background: white;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.result-card {
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.result-image {
  width: 100%;
  height: 200px;
  background: #f8f9fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.placeholder-image {
  font-size: 48px;
}

.result-content {
  flex: 1;
}

.result-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.result-meta {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 12px;
  color: #666;
}

.result-description {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
  margin-bottom: 10px;
}

.download-info {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #888;
}

.result-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.action-btn {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #e1e5e9;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 12px;
}

.download-btn:hover {
  background: #007bff;
  color: white;
}

.library-btn:hover {
  background: #28a745;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.pagination-btn {
  padding: 8px 16px;
  border: 1px solid #e1e5e9;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.search-history {
  margin-top: 30px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.clear-history {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
}

.history-list {
  border: 1px solid #e1e5e9;
  border-radius: 8px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.history-item:hover {
  background: #f8f9fa;
}

.history-item:last-child {
  border-bottom: none;
}

.delete-history {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 16px;
}

.loading-container {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 40px;
  color: #dc3545;
}

.retry-btn {
  margin-top: 10px;
  padding: 8px 16px;
  border: 1px solid #dc3545;
  border-radius: 4px;
  background: white;
  color: #dc3545;
  cursor: pointer;
}

@media (max-width: 768px) {
  .search-container {
    padding: 10px;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
  
  .results-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .suggestions-panel,
  .trending-panel {
    position: fixed;
    top: 60px;
    left: 10px;
    right: 10px;
  }
}
</style>