<template>
  <div class="discover-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1>发现推荐</h1>
      <p class="page-description">探索热门影视和音乐内容，发现你的下一部最爱</p>
    </div>

    <!-- 发现导航 -->
    <div class="discover-nav">
      <div class="nav-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
        >
          {{ tab.name }}
        </button>
      </div>
      
      <!-- 分类筛选 -->
      <div class="category-filters">
        <select v-model="selectedCategory" @change="handleCategoryChange" class="filter-select">
          <option value="all">全部分类</option>
          <option value="movie">电影</option>
          <option value="tv">电视剧</option>
          <option value="anime">动漫</option>
          <option value="music">音乐</option>
        </select>
        
        <select v-model="selectedSource" @change="handleSourceChange" class="filter-select">
          <option value="">全部来源</option>
          <option v-for="source in availableSources" :key="source" :value="source">
            {{ getSourceDisplayName(source) }}
          </option>
        </select>
      </div>
    </div>

    <!-- 发现内容区域 -->
    <div class="discover-content">
      <!-- 热门推荐 -->
      <div v-if="activeTab === 'trending'" class="tab-content">
        <div class="section-header">
          <h2>热门推荐</h2>
          <p>当前最受欢迎的内容</p>
        </div>
        <DiscoverGrid :items="trendingItems" />
      </div>

      <!-- 个性化推荐 -->
      <div v-if="activeTab === 'personalized'" class="tab-content">
        <div class="section-header">
          <h2>为你推荐</h2>
          <p>基于你的兴趣和观看历史</p>
        </div>
        <DiscoverGrid :items="personalizedItems" />
      </div>

      <!-- 影视榜单 -->
      <div v-if="activeTab === 'charts'" class="tab-content">
        <div class="section-header">
          <h2>影视榜单</h2>
          <p>权威榜单和热门排行</p>
        </div>
        
        <!-- 榜单分类 -->
        <div class="chart-categories">
          <button 
            v-for="chart in chartCategories" 
            :key="chart.id"
            @click="activeChart = chart.id"
            :class="['chart-btn', { active: activeChart === chart.id }]"
          >
            {{ chart.name }}
          </button>
        </div>
        
        <DiscoverGrid :items="chartItems" />
      </div>

      <!-- 音乐榜单 -->
      <div v-if="activeTab === 'music'" class="tab-content">
        <div class="section-header">
          <h2>音乐榜单</h2>
          <p>热门歌曲和最新专辑</p>
        </div>
        
        <!-- 音乐平台选择 -->
        <div class="music-platforms">
          <button 
            v-for="platform in musicPlatforms" 
            :key="platform.id"
            @click="activePlatform = platform.id"
            :class="['platform-btn', { active: activePlatform === platform.id }]"
          >
            {{ platform.name }}
          </button>
        </div>
        
        <DiscoverGrid :items="musicItems" />
      </div>

      <!-- 新发现 -->
      <div v-if="activeTab === 'new'" class="tab-content">
        <div class="section-header">
          <h2>新发现</h2>
          <p>最新发布和即将上线的内容</p>
        </div>
        <DiscoverGrid :items="newItems" />
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="retryLoad" class="retry-btn">重试</button>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="pagination">
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
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import DiscoverGrid from '../components/DiscoverGrid.vue'
import { discoverAPI } from '../api/discover.js'

export default {
  name: 'DiscoverPage',
  components: {
    DiscoverGrid
  },
  setup() {
    // 响应式数据
    const activeTab = ref('trending')
    const selectedCategory = ref('all')
    const selectedSource = ref('')
    const activeChart = ref('movie')
    const activePlatform = ref('qq_music')
    const currentPage = ref(1)
    const pageSize = ref(20)
    
    const trendingItems = ref([])
    const personalizedItems = ref([])
    const chartItems = ref([])
    const musicItems = ref([])
    const newItems = ref([])
    
    const loading = ref(false)
    const error = ref('')
    const totalItems = ref(0)

    // 计算属性
    const totalPages = computed(() => {
      return Math.ceil(totalItems.value / pageSize.value)
    })

    const availableSources = computed(() => {
      const sources = {
        'all': ['tmdb', 'douban', 'bangumi', 'netflix_top10', 'imdb_datasets', 'spotify', 'apple_music', 'tme_uni_chart', 'billboard_china_tme'],
        'movie': ['tmdb', 'douban', 'netflix_top10', 'imdb_datasets'],
        'tv': ['tmdb', 'douban', 'netflix_top10'],
        'anime': ['tmdb', 'douban', 'bangumi'],
        'music': ['spotify', 'apple_music', 'tme_uni_chart', 'billboard_china_tme']
      }
      return sources[selectedCategory.value] || sources['all']
    })

    // 标签页配置
    const tabs = [
      { id: 'trending', name: '热门推荐' },
      { id: 'personalized', name: '为你推荐' },
      { id: 'charts', name: '影视榜单' },
      { id: 'music', name: '音乐榜单' },
      { id: 'new', name: '新发现' }
    ]

    // 榜单分类
    const chartCategories = [
      { id: 'movie', name: '电影榜单' },
      { id: 'tv', name: '电视剧榜单' },
      { id: 'anime', name: '动漫榜单' }
    ]

    // 音乐平台
    const musicPlatforms = [
      { id: 'spotify', name: 'Spotify' },
      { id: 'apple_music', name: 'Apple Music' },
      { id: 'tme_uni_chart', name: 'TME由你榜' },
      { id: 'billboard_china_tme', name: 'Billboard China TME' }
    ]

    // 方法
    const getSourceDisplayName = (source) => {
      const names = {
        'tmdb': 'TMDB',
        'douban': '豆瓣',
        'bangumi': 'Bangumi',
        'netflix_top10': 'Netflix Top 10',
        'imdb_datasets': 'IMDb Datasets',
        'spotify': 'Spotify',
        'apple_music': 'Apple Music',
        'tme_uni_chart': 'TME由你榜',
        'billboard_china_tme': 'Billboard China TME'
      }
      return names[source] || source
    }

    const handleCategoryChange = () => {
      selectedSource.value = ''
      currentPage.value = 1
      loadDiscoverData()
    }

    const handleSourceChange = () => {
      currentPage.value = 1
      loadDiscoverData()
    }

    const loadDiscoverData = async () => {
      loading.value = true
      error.value = ''
      
      try {
        let response
        
        switch (activeTab.value) {
          case 'trending':
            response = await discoverAPI.getTrending({
              category: selectedCategory.value,
              limit: pageSize.value
            })
            trendingItems.value = response.items
            totalItems.value = response.total
            break
            
          case 'personalized':
            response = await discoverAPI.getPersonalized({
              limit: pageSize.value
            })
            personalizedItems.value = response.items
            totalItems.value = response.total
            break
            
          case 'charts':
            response = await discoverAPI.getDiscover({
              category: activeChart.value,
              source: selectedSource.value,
              page: currentPage.value,
              limit: pageSize.value
            })
            chartItems.value = response.items
            totalItems.value = response.total
            break
            
          case 'music':
            response = await discoverAPI.getDiscover({
              category: 'music',
              source: activePlatform.value,
              page: currentPage.value,
              limit: pageSize.value
            })
            musicItems.value = response.items
            totalItems.value = response.total
            break
            
          case 'new':
            response = await discoverAPI.getDiscover({
              category: selectedCategory.value,
              source: selectedSource.value,
              page: currentPage.value,
              limit: pageSize.value
            })
            newItems.value = response.items
            totalItems.value = response.total
            break
        }
        
      } catch (err) {
        error.value = '加载发现数据失败，请重试'
        console.error('Discover data load error:', err)
      } finally {
        loading.value = false
      }
    }

    const previousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        loadDiscoverData()
      }
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
        loadDiscoverData()
      }
    }

    const retryLoad = () => {
      error.value = ''
      loadDiscoverData()
    }

    // 监听标签页变化
    watch(activeTab, (newTab) => {
      currentPage.value = 1
      loadDiscoverData()
    })

    // 监听榜单分类变化
    watch(activeChart, () => {
      currentPage.value = 1
      loadDiscoverData()
    })

    // 监听音乐平台变化
    watch(activePlatform, () => {
      currentPage.value = 1
      loadDiscoverData()
    })

    // 生命周期
    onMounted(() => {
      loadDiscoverData()
    })

    return {
      activeTab,
      selectedCategory,
      selectedSource,
      activeChart,
      activePlatform,
      currentPage,
      pageSize,
      trendingItems,
      personalizedItems,
      chartItems,
      musicItems,
      newItems,
      loading,
      error,
      totalItems,
      totalPages,
      tabs,
      chartCategories,
      musicPlatforms,
      availableSources,
      getSourceDisplayName,
      handleCategoryChange,
      handleSourceChange,
      previousPage,
      nextPage,
      retryLoad
    }
  }
}
</script>

<style scoped>
.discover-page {
  min-height: 100vh;
  background: var(--bg-secondary);
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.page-description {
  font-size: 1.1rem;
  color: var(--text-secondary);
}

.discover-nav {
  background: var(--bg-primary);
  border-radius: var(--radius);
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: var(--shadow);
}

.nav-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 20px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
}

.tab-btn:hover,
.tab-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.category-filters {
  display: flex;
  gap: 15px;
  align-items: center;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background: var(--bg-primary);
  color: var(--text-primary);
}

.discover-content {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 30px;
}

.section-header h2 {
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.section-header p {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.chart-categories,
.music-platforms {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.chart-btn,
.platform-btn {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
}

.chart-btn:hover,
.chart-btn.active,
.platform-btn:hover,
.platform-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.loading-container {
  text-align: center;
  padding: 60px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid var(--border-color);
  border-top: 5px solid var(--primary-color);
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
  color: var(--accent-color);
}

.retry-btn {
  margin-top: 10px;
  padding: 8px 16px;
  border: 1px solid var(--accent-color);
  border-radius: var(--radius);
  background: white;
  color: var(--accent-color);
  cursor: pointer;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.pagination-btn {
  padding: 10px 20px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .discover-page {
    padding: 10px;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .nav-tabs {
    justify-content: center;
  }
  
  .category-filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .chart-categories,
  .music-platforms {
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 10px;
  }
}
</style>