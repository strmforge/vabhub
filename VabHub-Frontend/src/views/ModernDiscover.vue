<template>
  <ModernLayout
    page-title="发现 - VabHub"
    page-description="探索丰富的媒体内容"
    :user-logged-in="userLoggedIn"
    :user-avatar="userAvatar"
    :user-name="userName"
    :user-email="userEmail"
    @search="handleSearch"
    @profile="handleProfile"
    @settings="handleSettings"
    @logout="handleLogout"
    @login="handleLogin"
  >
    <div class="modern-discover">
      <!-- 搜索和筛选区域 -->
      <section class="modern-discover__filters">
        <div class="modern-discover__filters-container">
          <!-- 搜索框 -->
          <div class="modern-discover__search">
            <ModernInput
              v-model="searchQuery"
              placeholder="搜索媒体内容..."
              icon="Search"
              size="large"
              @input="handleSearchInput"
            />
          </div>
          
          <!-- 筛选器 -->
          <div class="modern-discover__filter-options">
            <div class="modern-discover__filter-group">
              <label class="modern-discover__filter-label">类型</label>
              <div class="modern-discover__filter-buttons">
                <ModernButton
                  v-for="type in mediaTypes"
                  :key="type.value"
                  :variant="selectedType === type.value ? 'primary' : 'outline'"
                  size="small"
                  @click="selectType(type.value)"
                >
                  {{ type.label }}
                </ModernButton>
              </div>
            </div>
            
            <div class="modern-discover__filter-group">
              <label class="modern-discover__filter-label">排序</label>
              <div class="modern-discover__filter-buttons">
                <ModernButton
                  v-for="sort in sortOptions"
                  :key="sort.value"
                  :variant="selectedSort === sort.value ? 'primary' : 'outline'"
                  size="small"
                  @click="selectSort(sort.value)"
                >
                  {{ sort.label }}
                </ModernButton>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 内容网格 -->
      <section class="modern-discover__content">
        <div class="modern-discover__content-container">
          <!-- 加载状态 -->
          <div v-if="loading" class="modern-discover__loading">
            <LoadingSpinner
              type="spinner"
              size="large"
              message="正在加载内容..."
            />
          </div>
          
          <!-- 内容网格 -->
          <div v-else class="modern-discover__grid">
            <ModernCard
              v-for="item in filteredItems"
              :key="item.id"
              class="modern-discover__card"
              :hover-effect="true"
              :border-effect="true"
              @click="openItem(item)"
            >
              <template #image>
                <div class="modern-discover__card-image">
                  <img :src="item.thumbnail" :alt="item.title" />
                  <div class="modern-discover__card-overlay">
                    <div class="modern-discover__card-actions">
                      <ModernButton
                        variant="primary"
                        size="small"
                        icon="Play"
                        @click.stop="playItem(item)"
                      >
                        播放
                      </ModernButton>
                      <ModernButton
                        variant="outline"
                        size="small"
                        icon="Star"
                        @click.stop="favoriteItem(item)"
                      >
                        收藏
                      </ModernButton>
                    </div>
                  </div>
                </div>
              </template>
              
              <template #title>
                {{ item.title }}
              </template>
              
              <template #subtitle>
                <div class="modern-discover__card-meta">
                  <span class="modern-discover__card-type">{{ item.type }}</span>
                  <span class="modern-discover__card-duration">{{ item.duration }}</span>
                </div>
              </template>
              
              <template #content>
                <p class="modern-discover__card-description">{{ item.description }}</p>
              </template>
              
              <template #footer>
                <div class="modern-discover__card-footer">
                  <div class="modern-discover__card-stats">
                    <span class="modern-discover__card-stat">
                      <el-icon><View /></el-icon>
                      {{ item.views }}
                    </span>
                    <span class="modern-discover__card-stat">
                      <el-icon><Star /></el-icon>
                      {{ item.rating }}
                    </span>
                  </div>
                  <div class="modern-discover__card-tags">
                    <span 
                      v-for="tag in item.tags" 
                      :key="tag"
                      class="modern-discover__card-tag"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </template>
            </ModernCard>
          </div>
          
          <!-- 空状态 -->
          <div v-if="!loading && filteredItems.length === 0" class="modern-discover__empty">
            <div class="modern-discover__empty-content">
              <el-icon class="modern-discover__empty-icon">
                <Search />
              </el-icon>
              <h3 class="modern-discover__empty-title">未找到相关内容</h3>
              <p class="modern-discover__empty-description">
                尝试调整搜索条件或筛选器
              </p>
              <ModernButton
                variant="primary"
                @click="resetFilters"
              >
                重置筛选条件
              </ModernButton>
            </div>
          </div>
          
          <!-- 加载更多 -->
          <div v-if="hasMore && !loading" class="modern-discover__load-more">
            <ModernButton
              variant="outline"
              size="large"
              :loading="loadingMore"
              @click="loadMore"
            >
              {{ loadingMore ? '加载中...' : '加载更多' }}
            </ModernButton>
          </div>
        </div>
      </section>
    </div>
  </ModernLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import ModernLayout from '@/components/ui/ModernLayout.vue'
import ModernInput from '@/components/ui/ModernInput.vue'
import ModernButton from '@/components/ui/ModernButton.vue'
import ModernCard from '@/components/ui/ModernCard.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { Search, View, Star, Play } from '@element-plus/icons-vue'

export default {
  name: 'ModernDiscover',
  components: {
    ModernLayout,
    ModernInput,
    ModernButton,
    ModernCard,
    LoadingSpinner,
    Search,
    View,
    Star,
    Play
  },
  setup() {
    // 用户状态
    const userLoggedIn = ref(true)
    const userAvatar = ref('')
    const userName = ref('现代用户')
    const userEmail = ref('user@example.com')
    
    // 搜索和筛选状态
    const searchQuery = ref('')
    const selectedType = ref('all')
    const selectedSort = ref('latest')
    const loading = ref(false)
    const loadingMore = ref(false)
    const hasMore = ref(true)
    
    // 模拟数据
    const mediaItems = ref([])
    
    // 筛选选项
    const mediaTypes = [
      { value: 'all', label: '全部' },
      { value: 'video', label: '视频' },
      { value: 'audio', label: '音频' },
      { value: 'image', label: '图片' },
      { value: 'document', label: '文档' }
    ]
    
    const sortOptions = [
      { value: 'latest', label: '最新' },
      { value: 'popular', label: '热门' },
      { value: 'rating', label: '评分' },
      { value: 'duration', label: '时长' }
    ]
    
    // 计算属性：筛选后的项目
    const filteredItems = computed(() => {
      let items = mediaItems.value
      
      // 按类型筛选
      if (selectedType.value !== 'all') {
        items = items.filter(item => item.type === selectedType.value)
      }
      
      // 按搜索词筛选
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        items = items.filter(item => 
          item.title.toLowerCase().includes(query) ||
          item.description.toLowerCase().includes(query) ||
          item.tags.some(tag => tag.toLowerCase().includes(query))
        )
      }
      
      // 排序
      switch (selectedSort.value) {
        case 'latest':
          items.sort((a, b) => new Date(b.date) - new Date(a.date))
          break
        case 'popular':
          items.sort((a, b) => b.views - a.views)
          break
        case 'rating':
          items.sort((a, b) => b.rating - a.rating)
          break
        case 'duration':
          items.sort((a, b) => b.durationSeconds - a.durationSeconds)
          break
      }
      
      return items
    })
    
    // 模拟数据生成
    const generateMockData = () => {
      const types = ['video', 'audio', 'image', 'document']
      const titles = [
        '美丽的自然风光', '城市夜景延时摄影', '古典音乐精选', 
        '编程教程系列', '旅行摄影集', '播客访谈节目',
        '设计灵感分享', '科技新闻播报', '美食制作教程'
      ]
      
      return Array.from({ length: 12 }, (_, i) => ({
        id: i + 1,
        title: titles[i % titles.length] + ` ${i + 1}`,
        type: types[i % types.length],
        description: `这是关于${titles[i % titles.length]}的详细描述，包含了丰富的内容和精彩的展示。`,
        thumbnail: `https://picsum.photos/300/200?random=${i}`,
        duration: `${Math.floor(Math.random() * 30) + 5}:00`,
        durationSeconds: Math.floor(Math.random() * 1800) + 300,
        views: Math.floor(Math.random() * 10000) + 1000,
        rating: (Math.random() * 2 + 3).toFixed(1),
        date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000),
        tags: ['精选', '热门', '推荐'].slice(0, Math.floor(Math.random() * 3) + 1)
      }))
    }
    
    // 事件处理
    const handleSearch = () => {
      console.log('搜索功能触发')
    }
    
    const handleProfile = () => {
      console.log('查看个人资料')
    }
    
    const handleSettings = () => {
      console.log('打开设置')
    }
    
    const handleLogout = () => {
      userLoggedIn.value = false
      console.log('用户登出')
    }
    
    const handleLogin = () => {
      userLoggedIn.value = true
      console.log('用户登录')
    }
    
    const handleSearchInput = () => {
      // 防抖搜索逻辑
      console.log('搜索输入:', searchQuery.value)
    }
    
    const selectType = (type) => {
      selectedType.value = type
    }
    
    const selectSort = (sort) => {
      selectedSort.value = sort
    }
    
    const openItem = (item) => {
      console.log('打开项目:', item)
    }
    
    const playItem = (item) => {
      console.log('播放项目:', item)
    }
    
    const favoriteItem = (item) => {
      console.log('收藏项目:', item)
    }
    
    const resetFilters = () => {
      searchQuery.value = ''
      selectedType.value = 'all'
      selectedSort.value = 'latest'
    }
    
    const loadMore = async () => {
      loadingMore.value = true
      
      // 模拟加载更多数据
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const newItems = generateMockData()
      mediaItems.value = [...mediaItems.value, ...newItems]
      
      loadingMore.value = false
      hasMore.value = mediaItems.value.length < 50 // 限制最大数量
    }
    
    // 初始化数据
    onMounted(async () => {
      loading.value = true
      
      // 模拟数据加载
      await new Promise(resolve => setTimeout(resolve, 1500))
      mediaItems.value = generateMockData()
      
      loading.value = false
    })
    
    return {
      userLoggedIn,
      userAvatar,
      userName,
      userEmail,
      searchQuery,
      selectedType,
      selectedSort,
      loading,
      loadingMore,
      hasMore,
      mediaTypes,
      sortOptions,
      filteredItems,
      handleSearch,
      handleProfile,
      handleSettings,
      handleLogout,
      handleLogin,
      handleSearchInput,
      selectType,
      selectSort,
      openItem,
      playItem,
      favoriteItem,
      resetFilters,
      loadMore
    }
  }
}
</script>

<style scoped>
.modern-discover {
  min-height: 100vh;
}

/* 筛选区域 */
.modern-discover__filters {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  padding: var(--space-6) 0;
}

.modern-discover__filters-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-8);
}

.modern-discover__search {
  margin-bottom: var(--space-6);
}

.modern-discover__filter-options {
  display: flex;
  gap: var(--space-8);
  flex-wrap: wrap;
}

.modern-discover__filter-group {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.modern-discover__filter-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  min-width: 60px;
}

.modern-discover__filter-buttons {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

/* 内容区域 */
.modern-discover__content {
  padding: var(--space-8);
}

.modern-discover__content-container {
  max-width: 1200px;
  margin: 0 auto;
}

.modern-discover__loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.modern-discover__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-6);
}

.modern-discover__card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.modern-discover__card-image {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.modern-discover__card-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.modern-discover__card:hover .modern-discover__card-image img {
  transform: scale(1.05);
}

.modern-discover__card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modern-discover__card:hover .modern-discover__card-overlay {
  opacity: 1;
}

.modern-discover__card-actions {
  display: flex;
  gap: var(--space-2);
}

.modern-discover__card-meta {
  display: flex;
  gap: var(--space-3);
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.modern-discover__card-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.modern-discover__card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--space-4);
}

.modern-discover__card-stats {
  display: flex;
  gap: var(--space-4);
}

.modern-discover__card-stat {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

.modern-discover__card-tags {
  display: flex;
  gap: var(--space-1);
}

.modern-discover__card-tag {
  font-size: var(--font-size-xs);
  color: var(--primary-600);
  background: var(--primary-50);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
}

/* 空状态 */
.modern-discover__empty {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  text-align: center;
}

.modern-discover__empty-content {
  max-width: 400px;
}

.modern-discover__empty-icon {
  font-size: 4rem;
  color: var(--text-tertiary);
  margin-bottom: var(--space-4);
}

.modern-discover__empty-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.modern-discover__empty-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
}

/* 加载更多 */
.modern-discover__load-more {
  display: flex;
  justify-content: center;
  margin-top: var(--space-8);
  padding-top: var(--space-8);
  border-top: 1px solid var(--border-primary);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-discover__filters-container {
    padding: 0 var(--space-4);
  }
  
  .modern-discover__filter-options {
    flex-direction: column;
    gap: var(--space-4);
  }
  
  .modern-discover__filter-group {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .modern-discover__grid {
    grid-template-columns: 1fr;
  }
  
  .modern-discover__card-footer {
    flex-direction: column;
    gap: var(--space-3);
    align-items: flex-start;
  }
  
  .modern-discover__card-stats {
    order: 2;
  }
}

/* 深色主题适配 */
[data-theme="dark"] .modern-discover__filters {
  background: rgba(17, 24, 39, 0.8);
  border-bottom-color: var(--border-secondary);
}

[data-theme="dark"] .modern-discover__card-tag {
  background: rgba(59, 130, 246, 0.2);
  color: var(--primary-400);
}
</style>