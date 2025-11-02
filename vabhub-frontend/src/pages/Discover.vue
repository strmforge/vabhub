<template>
  <div class="discover-page">
    <div class="page-header">
      <h1>发现内容</h1>
      <p>探索和发现新的媒体内容</p>
    </div>
    
    <div class="discover-content">
      <el-row :gutter="20">
        <el-col :span="18">
          <el-card class="discover-main">
            <template #header>
              <div class="card-header">
                <span>热门推荐</span>
                <el-button type="primary" size="small">刷新</el-button>
              </div>
            </template>
            
            <div class="media-grid">
              <div v-for="item in mediaList" :key="item.id" class="media-item">
                <el-card shadow="hover" class="media-card">
                  <img :src="item.poster" :alt="item.title" class="media-poster" />
                  <div class="media-info">
                    <h4>{{ item.title }}</h4>
                    <p class="media-year">{{ item.year }}</p>
                    <p class="media-rating">
                      <el-rate
                        v-model="item.rating"
                        disabled
                        show-score
                        text-color="#ff9900"
                        score-template="{value}"
                      />
                    </p>
                  </div>
                </el-card>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="discover-sidebar">
            <template #header>
              <span>筛选条件</span>
            </template>
            
            <div class="filter-section">
              <h4>类型</h4>
              <el-checkbox-group v-model="selectedTypes">
                <el-checkbox label="movie">电影</el-checkbox>
                <el-checkbox label="tv">电视剧</el-checkbox>
                <el-checkbox label="anime">动漫</el-checkbox>
              </el-checkbox-group>
            </div>
            
            <div class="filter-section">
              <h4>评分</h4>
              <el-slider
                v-model="ratingRange"
                range
                :min="0"
                :max="10"
                :step="0.1"
                show-stops
              />
            </div>
            
            <div class="filter-section">
              <h4>年份</h4>
              <el-date-picker
                v-model="yearRange"
                type="yearrange"
                range-separator="至"
                start-placeholder="开始年份"
                end-placeholder="结束年份"
                value-format="YYYY"
              />
            </div>
            
            <el-button type="primary" style="width: 100%; margin-top: 20px;">
              应用筛选
            </el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

interface MediaItem {
  id: number
  title: string
  year: string
  rating: number
  poster: string
  type: string
}

const mediaList = ref<MediaItem[]>([])
const selectedTypes = ref<string[]>(['movie', 'tv', 'anime'])
const ratingRange = ref([6, 10])
const yearRange = ref(['2000', '2024'])

const loadMediaData = async () => {
  try {
    // 模拟数据加载
    await new Promise(resolve => setTimeout(resolve, 500))
    
    mediaList.value = [
      {
        id: 1,
        title: '流浪地球2',
        year: '2023',
        rating: 8.3,
        poster: '/images/posters/wandering-earth-2.jpg',
        type: 'movie'
      },
      {
        id: 2,
        title: '漫长的季节',
        year: '2023',
        rating: 9.4,
        poster: '/images/posters/the-long-season.jpg',
        type: 'tv'
      },
      {
        id: 3,
        title: '铃芽之旅',
        year: '2022',
        rating: 7.9,
        poster: '/images/posters/suzume.jpg',
        type: 'anime'
      },
      {
        id: 4,
        title: '狂飙',
        year: '2023',
        rating: 8.5,
        poster: '/images/posters/the-knockout.jpg',
        type: 'tv'
      }
    ]
    
    ElMessage.success('数据加载成功')
  } catch (error) {
    ElMessage.error('数据加载失败')
    console.error('加载发现数据失败:', error)
  }
}

onMounted(() => {
  loadMediaData()
})
</script>

<style scoped>
.discover-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-header h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

.page-header p {
  color: #666;
  font-size: 1rem;
}

.discover-main {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.media-item {
  transition: transform 0.3s ease;
}

.media-item:hover {
  transform: translateY(-5px);
}

.media-card {
  height: 100%;
}

.media-poster {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 4px;
}

.media-info {
  padding: 10px 0;
}

.media-info h4 {
  margin: 0 0 8px 0;
  font-size: 1rem;
  color: #333;
}

.media-year {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 8px 0;
}

.media-rating {
  margin: 0;
}

.discover-sidebar {
  position: sticky;
  top: 20px;
}

.filter-section {
  margin-bottom: 20px;
}

.filter-section h4 {
  margin-bottom: 10px;
  color: #333;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .media-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
  
  .media-poster {
    height: 200px;
  }
}
</style>