<template>
  <div class="recommendation-list">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>
    
    <div v-else-if="error" class="error-container">
      <el-result
        icon="warning"
        title="加载失败"
        :sub-title="error"
      >
        <template #extra>
          <el-button type="primary" @click="loadData">重试</el-button>
        </template>
      </el-result>
    </div>
    
    <div v-else class="recommendation-content">
      <div class="list-header">
        <h3>{{ getListTitle }}</h3>
        <el-button 
          type="primary" 
          size="small" 
          :loading="refreshing" 
          @click="refreshData"
        >
          刷新推荐
        </el-button>
      </div>
      
      <div class="media-grid">
        <MediaCard
          v-for="item in recommendations"
          :key="item.id"
          :media="item"
          @click="handleMediaClick(item)"
        />
      </div>
      
      <div v-if="recommendations.length === 0" class="empty-state">
        <el-empty description="暂无推荐内容" />
      </div>
      
      <div v-if="hasMore" class="load-more">
        <el-button 
          :loading="loadingMore" 
          @click="loadMore"
          style="width: 100%"
        >
          加载更多
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import MediaCard from '@/components/media/MediaCard.vue'

interface Recommendation {
  id: number
  title: string
  year: string
  rating: number
  poster: string
  type: string
  reason: string
  similarity?: number
}

interface Props {
  type: 'hot' | 'personalized' | 'similar' | 'discovery'
}

const props = defineProps<Props>()

const loading = ref(true)
const loadingMore = ref(false)
const refreshing = ref(false)
const error = ref('')
const recommendations = ref<Recommendation[]>([])
const currentPage = ref(1)
const hasMore = ref(true)

const getListTitle = computed(() => {
  const titles = {
    hot: '热门推荐',
    personalized: '个性化推荐',
    similar: '相似内容',
    discovery: '新发现'
  }
  return titles[props.type]
})

const loadData = async (page = 1, isRefresh = false) => {
  try {
    if (isRefresh) {
      refreshing.value = true
    } else if (page === 1) {
      loading.value = true
    } else {
      loadingMore.value = true
    }
    
    error.value = ''
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))
    
    const mockData: Recommendation[] = [
      {
        id: page * 10 + 1,
        title: '推荐内容 ' + (page * 10 + 1),
        year: '2023',
        rating: 8.5,
        poster: '/images/posters/default.jpg',
        type: 'movie',
        reason: '基于您的观看历史推荐',
        similarity: 0.85
      },
      {
        id: page * 10 + 2,
        title: '推荐内容 ' + (page * 10 + 2),
        year: '2022',
        rating: 7.8,
        poster: '/images/posters/default.jpg',
        type: 'tv',
        reason: '热门内容',
        similarity: 0.72
      }
    ]
    
    if (page === 1) {
      recommendations.value = mockData
    } else {
      recommendations.value.push(...mockData)
    }
    
    // 模拟分页逻辑
    hasMore.value = page < 3
    currentPage.value = page
    
    if (isRefresh) {
      ElMessage.success('推荐已刷新')
    }
  } catch (err) {
    error.value = '加载推荐数据失败'
    ElMessage.error('加载失败')
    console.error('加载推荐数据失败:', err)
  } finally {
    loading.value = false
    loadingMore.value = false
    refreshing.value = false
  }
}

const refreshData = () => {
  loadData(1, true)
}

const loadMore = () => {
  if (!loadingMore.value && hasMore.value) {
    loadData(currentPage.value + 1)
  }
}

const handleMediaClick = (media: Recommendation) => {
  console.log('点击媒体:', media)
  ElMessage.info(`查看 ${media.title}`)
}

// 监听类型变化
watch(() => props.type, () => {
  loadData(1)
})

onMounted(() => {
  loadData(1)
})
</script>

<style scoped>
.recommendation-list {
  min-height: 400px;
}

.loading-container,
.error-container {
  padding: 40px 0;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.list-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.empty-state {
  padding: 60px 0;
}

.load-more {
  margin-top: 30px;
}

@media (max-width: 768px) {
  .media-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 15px;
  }
  
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .list-header h3 {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .media-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
  }
}
</style>