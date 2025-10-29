<template>
  <div class="search-test">
    <h1>搜索功能测试</h1>
    
    <div class="test-section">
      <h2>搜索组件测试</h2>
      <SearchComponent />
    </div>

    <div class="test-section">
      <h2>搜索历史测试</h2>
      <div class="history-test">
        <button @click="testAddHistory" class="test-btn">添加测试历史</button>
        <button @click="testClearHistory" class="test-btn">清空历史</button>
        <button @click="testGetStats" class="test-btn">获取统计</button>
        
        <div v-if="testStats" class="stats-display">
          <h3>搜索统计</h3>
          <p>总搜索次数: {{ testStats.totalSearches }}</p>
          <p>唯一查询数: {{ testStats.uniqueQueries }}</p>
          <p>今日搜索: {{ testStats.todaySearches }}</p>
        </div>
      </div>
    </div>

    <div class="test-section">
      <h2>API 测试</h2>
      <div class="api-test">
        <input v-model="testQuery" placeholder="输入测试查询" class="test-input" />
        <button @click="testSearchAPI" class="test-btn">测试搜索</button>
        <button @click="testSuggestionsAPI" class="test-btn">测试建议</button>
        
        <div v-if="apiResult" class="api-result">
          <h3>API 响应</h3>
          <pre>{{ JSON.stringify(apiResult, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import SearchComponent from '../components/SearchComponent.vue'
import { searchAPI } from '../api/search.js'
import { searchHistoryManager } from '../utils/searchHistory.js'

export default {
  name: 'SearchTest',
  components: {
    SearchComponent
  },
  setup() {
    const testStats = ref(null)
    const testQuery = ref('')
    const apiResult = ref(null)

    const testAddHistory = () => {
      const testQueries = [
        '阿凡达：水之道',
        '流浪地球2', 
        '漫长的季节',
        '周杰伦',
        'Taylor Swift'
      ]
      
      testQueries.forEach(query => {
        searchHistoryManager.addSearch(query, 'combined', 'all', [])
      })
      
      alert('测试历史记录已添加')
    }

    const testClearHistory = () => {
      searchHistoryManager.clearHistory()
      testStats.value = null
      alert('历史记录已清空')
    }

    const testGetStats = () => {
      testStats.value = searchHistoryManager.getSearchStats()
    }

    const testSearchAPI = async () => {
      if (!testQuery.value.trim()) {
        alert('请输入查询内容')
        return
      }

      try {
        const response = await searchAPI.search({
          query: testQuery.value,
          type: 'all',
          limit: 10
        })
        apiResult.value = response
      } catch (error) {
        apiResult.value = { error: error.message }
      }
    }

    const testSuggestionsAPI = async () => {
      if (!testQuery.value.trim()) {
        alert('请输入查询内容')
        return
      }

      try {
        const response = await searchAPI.getSuggestions(testQuery.value)
        apiResult.value = response
      } catch (error) {
        apiResult.value = { error: error.message }
      }
    }

    return {
      testStats,
      testQuery,
      apiResult,
      testAddHistory,
      testClearHistory,
      testGetStats,
      testSearchAPI,
      testSuggestionsAPI
    }
  }
}
</script>

<style scoped>
.search-test {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.test-section {
  margin-bottom: 40px;
  padding: 20px;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
}

.history-test, .api-test {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.test-btn {
  padding: 10px 20px;
  border: 1px solid #007bff;
  border-radius: 4px;
  background: #007bff;
  color: white;
  cursor: pointer;
  max-width: 200px;
}

.test-btn:hover {
  background: #0056b3;
}

.test-input {
  padding: 10px;
  border: 1px solid #e1e5e9;
  border-radius: 4px;
  max-width: 300px;
}

.stats-display, .api-result {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
  margin-top: 15px;
}

.api-result pre {
  background: white;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}
</style>