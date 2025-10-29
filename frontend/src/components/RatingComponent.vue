<template>
  <div class="rating-component">
    <!-- 评分显示 -->
    <div class="rating-display" v-if="!isEditing">
      <div class="rating-stars">
        <span 
          v-for="star in 10" 
          :key="star"
          class="star"
          :class="{ active: star <= currentRating }"
          @click="startEditing"
        >
          ★
        </span>
      </div>
      <div class="rating-info">
        <span class="rating-value">{{ currentRating || '未评分' }}</span>
        <span class="rating-count" v-if="stats.ratings_count > 0">
          ({{ stats.ratings_count }}人评分)
        </span>
        <span class="avg-rating" v-if="stats.avg_rating > 0">
          平均: {{ stats.avg_rating }}
        </span>
      </div>
    </div>

    <!-- 评分编辑 -->
    <div class="rating-edit" v-if="isEditing">
      <div class="edit-stars">
        <span 
          v-for="star in 10" 
          :key="star"
          class="edit-star"
          :class="{ active: star <= tempRating, hover: star <= hoverRating }"
          @click="rateContent(star)"
          @mouseenter="hoverRating = star"
          @mouseleave="hoverRating = 0"
        >
          ★
        </span>
      </div>
      <div class="edit-actions">
        <span class="rating-hint">{{ tempRating || '请选择评分' }}</span>
        <button class="btn-cancel" @click="cancelEditing">取消</button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div class="loading" v-if="loading">
      <span>评分中...</span>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'RatingComponent',
  props: {
    contentId: {
      type: String,
      required: true
    },
    contentData: {
      type: Object,
      default: () => ({})
    },
    userId: {
      type: String,
      default: 'anonymous'
    }
  },
  setup(props) {
    const isEditing = ref(false)
    const tempRating = ref(0)
    const hoverRating = ref(0)
    const loading = ref(false)
    const userRating = ref(0)
    const stats = ref({
      ratings_count: 0,
      avg_rating: 0
    })

    // 当前评分（用户评分或平均分）
    const currentRating = computed(() => {
      return userRating.value || stats.value.avg_rating
    })

    // 开始编辑评分
    const startEditing = () => {
      isEditing.value = true
      tempRating.value = userRating.value
    }

    // 取消编辑
    const cancelEditing = () => {
      isEditing.value = false
      tempRating.value = 0
      hoverRating.value = 0
    }

    // 评分内容
    const rateContent = async (rating) => {
      if (loading.value) return
      
      loading.value = true
      try {
        // 调用后端API进行评分
        const response = await fetch(`/api/social/rate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: props.userId,
            content_id: props.contentId,
            rating: rating,
            content_data: props.contentData
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            userRating.value = rating
            stats.value = result.content_stats
            ElMessage.success('评分成功')
            isEditing.value = false
            
            // 触发评分事件
            window.dispatchEvent(new CustomEvent('content-rated', {
              detail: {
                contentId: props.contentId,
                rating: rating,
                userId: props.userId
              }
            }))
          } else {
            ElMessage.error(result.message)
          }
        } else {
          throw new Error('评分请求失败')
        }
      } catch (error) {
        console.error('评分失败:', error)
        ElMessage.error('评分失败，请重试')
      } finally {
        loading.value = false
      }
    }

    // 获取评分统计
    const fetchStats = async () => {
      try {
        const response = await fetch(`/api/social/stats/${props.contentId}`)
        if (response.ok) {
          const data = await response.json()
          stats.value = data
        }
      } catch (error) {
        console.error('获取评分统计失败:', error)
      }
    }

    // 获取用户评分
    const fetchUserRating = async () => {
      try {
        const response = await fetch(`/api/social/user-rating/${props.userId}/${props.contentId}`)
        if (response.ok) {
          const data = await response.json()
          userRating.value = data.rating || 0
        }
      } catch (error) {
        console.error('获取用户评分失败:', error)
      }
    }

    onMounted(() => {
      fetchStats()
      if (props.userId !== 'anonymous') {
        fetchUserRating()
      }
    })

    return {
      isEditing,
      tempRating,
      hoverRating,
      loading,
      stats,
      currentRating,
      startEditing,
      cancelEditing,
      rateContent
    }
  }
}
</script>

<style scoped>
.rating-component {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rating-stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 20px;
  color: #ddd;
  cursor: pointer;
  transition: color 0.2s ease;
}

.star.active {
  color: #ffc107;
}

.star:hover {
  color: #ffc107;
}

.rating-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.rating-value {
  font-weight: 600;
  color: #333;
}

.rating-count, .avg-rating {
  font-size: 12px;
  color: #999;
}

.rating-edit {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.edit-stars {
  display: flex;
  gap: 2px;
}

.edit-star {
  font-size: 24px;
  color: #ddd;
  cursor: pointer;
  transition: color 0.2s ease;
}

.edit-star.active {
  color: #ffc107;
}

.edit-star.hover {
  color: #ffeb3b;
}

.edit-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rating-hint {
  font-size: 14px;
  color: #666;
  min-width: 100px;
}

.btn-cancel {
  padding: 4px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-cancel:hover {
  background: #f5f5f5;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #666;
}

/* 暗色主题支持 */
[data-theme="dark"] .rating-component {
  --text-color: #ffffff;
  --text-secondary: #b0b0b0;
  --border-color: #444;
}

[data-theme="dark"] .rating-value {
  color: var(--text-color);
}

[data-theme="dark"] .rating-count,
[data-theme="dark"] .avg-rating {
  color: var(--text-secondary);
}

[data-theme="dark"] .btn-cancel {
  border-color: var(--border-color);
  background: #2a2a2a;
  color: var(--text-color);
}

[data-theme="dark"] .btn-cancel:hover {
  background: #3a3a3a;
}
</style>