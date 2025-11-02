<template>
  <div class="media-card" @click="$emit('click', media)">
    <el-card shadow="hover" class="card-container">
      <div class="media-poster-container">
        <img 
          :src="media.poster" 
          :alt="media.title" 
          class="media-poster"
          @error="handleImageError"
        />
        <div class="media-overlay">
          <div class="media-actions">
            <el-button 
              type="primary" 
              size="small" 
              circle
              @click.stop="handlePlay"
            >
              <el-icon><VideoPlay /></el-icon>
            </el-button>
            <el-button 
              type="info" 
              size="small" 
              circle
              @click.stop="handleInfo"
            >
              <el-icon><InfoFilled /></el-icon>
            </el-button>
          </div>
        </div>
        
        <!-- 评分标签 -->
        <div v-if="media.rating" class="rating-badge">
          <span>{{ media.rating.toFixed(1) }}</span>
        </div>
        
        <!-- 类型标签 -->
        <div class="type-badge">
          <el-tag 
            :type="getTypeColor(media.type)" 
            size="small"
          >
            {{ getTypeLabel(media.type) }}
          </el-tag>
        </div>
      </div>
      
      <div class="media-info">
        <h4 class="media-title" :title="media.title">
          {{ media.title }}
        </h4>
        
        <p class="media-year">{{ media.year }}</p>
        
        <!-- 推荐原因 -->
        <div v-if="media.reason" class="recommendation-reason">
          <el-tooltip 
            :content="media.reason" 
            placement="top"
          >
            <span class="reason-text">{{ media.reason }}</span>
          </el-tooltip>
        </div>
        
        <!-- 相似度 -->
        <div v-if="media.similarity" class="similarity-indicator">
          <el-progress 
            :percentage="Math.round(media.similarity * 100)" 
            :show-text="false"
            :stroke-width="4"
          />
          <span class="similarity-text">
            相似度: {{ (media.similarity * 100).toFixed(0) }}%
          </span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { VideoPlay, InfoFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Media {
  id: number
  title: string
  year: string
  rating: number
  poster: string
  type: string
  reason?: string
  similarity?: number
}

interface Props {
  media: Media
}

const props = defineProps<Props>()
const emit = defineEmits<{
  click: [media: Media]
}>()

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = '/images/posters/default.jpg'
}

const handlePlay = () => {
  ElMessage.info(`播放: ${props.media.title}`)
  // 这里可以触发播放逻辑
}

const handleInfo = () => {
  ElMessage.info(`查看详情: ${props.media.title}`)
  // 这里可以跳转到详情页面
}

const getTypeColor = (type: string) => {
  const colors = {
    movie: 'primary',
    tv: 'success',
    anime: 'warning',
    documentary: 'info'
  }
  return colors[type as keyof typeof colors] || 'default'
}

const getTypeLabel = (type: string) => {
  const labels = {
    movie: '电影',
    tv: '电视剧',
    anime: '动漫',
    documentary: '纪录片'
  }
  return labels[type as keyof typeof labels] || type
}
</script>

<style scoped>
.media-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.media-card:hover {
  transform: translateY(-5px);
}

.card-container {
  height: 100%;
  border: none;
}

.media-poster-container {
  position: relative;
  overflow: hidden;
  border-radius: 4px;
}

.media-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.media-card:hover .media-poster {
  transform: scale(1.05);
}

.media-overlay {
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

.media-card:hover .media-overlay {
  opacity: 1;
}

.media-actions {
  display: flex;
  gap: 10px;
}

.rating-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.type-badge {
  position: absolute;
  top: 10px;
  left: 10px;
}

.media-info {
  padding: 15px 0 0 0;
}

.media-title {
  margin: 0 0 8px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.media-year {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 10px 0;
}

.recommendation-reason {
  margin-bottom: 10px;
}

.reason-text {
  color: #888;
  font-size: 0.8rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.similarity-indicator {
  margin-top: 8px;
}

.similarity-text {
  display: block;
  font-size: 0.75rem;
  color: #999;
  margin-top: 4px;
}

:deep(.el-card__body) {
  padding: 0;
}

:deep(.el-card) {
  border: 1px solid #f0f0f0;
}

:deep(.el-card:hover) {
  border-color: #409eff;
}

@media (max-width: 768px) {
  .media-poster {
    height: 250px;
  }
  
  .media-title {
    font-size: 0.9rem;
  }
  
  .media-actions {
    flex-direction: column;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .media-poster {
    height: 200px;
  }
  
  .rating-badge {
    font-size: 0.7rem;
    padding: 2px 6px;
  }
}
</style>