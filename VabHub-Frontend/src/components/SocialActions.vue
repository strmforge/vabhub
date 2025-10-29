<template>
  <div class="social-actions">
    <!-- 主要社交操作 -->
    <div class="actions-primary">
      <!-- 评分组件 -->
      <RatingComponent 
        :content-id="contentId" 
        :content-data="contentData"
        :user-id="userId"
        class="action-item"
      />
      
      <!-- 收藏按钮 -->
      <button 
        class="action-btn favorite-btn"
        :class="{ active: isFavorited }"
        @click="toggleFavorite"
      >
        <span class="action-icon">{{ isFavorited ? '❤️' : '🤍' }}</span>
        <span class="action-text">{{ isFavorited ? '已收藏' : '收藏' }}</span>
      </button>

      <!-- 观看列表按钮 -->
      <button 
        class="action-btn watchlist-btn"
        :class="{ active: inWatchlist }"
        @click="toggleWatchlist"
      >
        <span class="action-icon">{{ inWatchlist ? '✅' : '📺' }}</span>
        <span class="action-text">{{ inWatchlist ? '已添加' : '想看' }}</span>
      </button>

      <!-- 分享组件 -->
      <ShareComponent 
        :content-id="contentId" 
        :content-data="contentData"
        :user-id="userId"
        class="action-item"
      />
    </div>

    <!-- 次要社交操作 -->
    <div class="actions-secondary" v-if="showSecondaryActions">
      <button class="secondary-btn" @click="$emit('view-comments')">
        💬 评论
      </button>
      <button class="secondary-btn" @click="$emit('view-details')">
        📖 详情
      </button>
      <button class="secondary-btn" @click="$emit('view-similar')">
        🔍 相似内容
      </button>
    </div>

    <!-- 操作统计 -->
    <div class="action-stats" v-if="showStats">
      <div class="stat-item">
        <span class="stat-icon">⭐</span>
        <span class="stat-value">{{ stats.ratings_count || 0 }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-icon">💬</span>
        <span class="stat-value">{{ stats.comments_count || 0 }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-icon">❤️</span>
        <span class="stat-value">{{ stats.favorites_count || 0 }}</span>
      </div>
    </div>

    <!-- 加载状态 -->
    <div class="loading-overlay" v-if="loading">
      <div class="loading-spinner"></div>
      <span>操作中...</span>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import RatingComponent from './RatingComponent.vue'
import ShareComponent from './ShareComponent.vue'

export default {
  name: 'SocialActions',
  components: {
    RatingComponent,
    ShareComponent
  },
  props: {
    contentId: {
      type: String,
      required: true
    },
    contentData: {
      type: Object,
      default: () => ({
        title: '',
        type: '',
        year: ''
      })
    },
    userId: {
      type: String,
      default: 'anonymous'
    },
    showSecondaryActions: {
      type: Boolean,
      default: true
    },
    showStats: {
      type: Boolean,
      default: true
    }
  },
  emits: ['view-comments', 'view-details', 'view-similar'],
  setup(props) {
    const isFavorited = ref(false)
    const inWatchlist = ref(false)
    const loading = ref(false)
    const stats = ref({})

    // 监听内容ID变化
    watch(() => props.contentId, () => {
      if (props.contentId) {
        loadUserActions()
        loadStats()
      }
    })

    // 加载用户操作状态
    const loadUserActions = async () => {
      if (props.userId === 'anonymous') return
      
      try {
        // 获取收藏状态
        const favoriteResponse = await fetch(`/api/social/favorite-status/${props.userId}/${props.contentId}`)
        if (favoriteResponse.ok) {
          const favoriteData = await favoriteResponse.json()
          isFavorited.value = favoriteData.is_favorited || false
        }

        // 获取观看列表状态
        const watchlistResponse = await fetch(`/api/social/watchlist-status/${props.userId}/${props.contentId}`)
        if (watchlistResponse.ok) {
          const watchlistData = await watchlistResponse.json()
          inWatchlist.value = watchlistData.in_watchlist || false
        }
      } catch (error) {
        console.error('加载用户操作状态失败:', error)
      }
    }

    // 加载统计信息
    const loadStats = async () => {
      try {
        const response = await fetch(`/api/social/stats/${props.contentId}`)
        if (response.ok) {
          const data = await response.json()
          stats.value = data
        }
      } catch (error) {
        console.error('加载统计信息失败:', error)
      }
    }

    // 切换收藏状态
    const toggleFavorite = async () => {
      if (props.userId === 'anonymous') {
        ElMessage.warning('请登录后收藏内容')
        return
      }

      if (loading.value) return
      
      loading.value = true
      try {
        const response = await fetch('/api/social/favorite', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: props.userId,
            content_id: props.contentId,
            content_data: props.contentData
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            isFavorited.value = !isFavorited.value
            ElMessage.success(result.message)
            
            // 更新统计信息
            await loadStats()
            
            // 触发收藏事件
            window.dispatchEvent(new CustomEvent('content-favorited', {
              detail: {
                contentId: props.contentId,
                favorited: isFavorited.value,
                userId: props.userId
              }
            }))
          } else {
            ElMessage.error(result.message)
          }
        } else {
          throw new Error('收藏操作失败')
        }
      } catch (error) {
        console.error('收藏操作失败:', error)
        ElMessage.error('操作失败，请重试')
      } finally {
        loading.value = false
      }
    }

    // 切换观看列表状态
    const toggleWatchlist = async () => {
      if (props.userId === 'anonymous') {
        ElMessage.warning('请登录后管理观看列表')
        return
      }

      if (loading.value) return
      
      loading.value = true
      try {
        const response = await fetch('/api/social/watchlist', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: props.userId,
            content_id: props.contentId,
            content_data: props.contentData
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            inWatchlist.value = !inWatchlist.value
            ElMessage.success(result.message)
            
            // 触发观看列表事件
            window.dispatchEvent(new CustomEvent('watchlist-updated', {
              detail: {
                contentId: props.contentId,
                inWatchlist: inWatchlist.value,
                userId: props.userId
              }
            }))
          } else {
            ElMessage.error(result.message)
          }
        } else {
          throw new Error('观看列表操作失败')
        }
      } catch (error) {
        console.error('观看列表操作失败:', error)
        ElMessage.error('操作失败，请重试')
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      if (props.contentId) {
        loadUserActions()
        loadStats()
      }
    })

    return {
      isFavorited,
      inWatchlist,
      loading,
      stats,
      toggleFavorite,
      toggleWatchlist
    }
  }
}
</script>

<style scoped>
.social-actions {
  position: relative;
}

.actions-primary {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.action-item {
  flex-shrink: 0;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.action-btn:hover {
  background: #e9ecef;
  border-color: #adb5bd;
}

.action-btn.active {
  background: #e3f2fd;
  border-color: #3498db;
  color: #3498db;
}

.action-icon {
  font-size: 16px;
}

.actions-secondary {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.secondary-btn {
  background: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 12px;
  color: #666;
  transition: all 0.2s ease;
}

.secondary-btn:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}

.action-stats {
  display: flex;
  gap: 16px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #666;
}

.stat-icon {
  font-size: 14px;
}

.stat-value {
  font-weight: 600;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 8px;
  z-index: 10;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 暗色主题支持 */
[data-theme="dark"] .social-actions {
  --bg-secondary: #2a2a2a;
  --text-color: #ffffff;
  --text-secondary: #b0b0b0;
  --border-color: #444;
}

[data-theme="dark"] .action-btn {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-color);
}

[data-theme="dark"] .action-btn.active {
  background: #1a3a5a;
  border-color: #3498db;
  color: #3498db;
}

[data-theme="dark"] .secondary-btn {
  border-color: var(--border-color);
  color: var(--text-color);
}

[data-theme="dark"] .secondary-btn:hover {
  background: var(--bg-secondary);
}

[data-theme="dark"] .action-stats {
  border-top-color: var(--border-color);
}

[data-theme="dark"] .loading-overlay {
  background: rgba(0, 0, 0, 0.8);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .actions-primary {
    gap: 12px;
  }
  
  .action-btn {
    padding: 6px 10px;
    font-size: 12px;
  }
  
  .actions-secondary {
    gap: 6px;
  }
  
  .secondary-btn {
    font-size: 11px;
    padding: 3px 6px;
  }
  
  .action-stats {
    gap: 12px;
  }
  
  .stat-item {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .actions-primary {
    justify-content: space-between;
  }
  
  .action-btn {
    flex: 1;
    justify-content: center;
    min-width: 0;
  }
  
  .action-text {
    display: none;
  }
}
</style>