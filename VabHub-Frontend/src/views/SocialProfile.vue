<template>
  <div class="social-profile">
    <!-- 用户信息头部 -->
    <div class="profile-header">
      <div class="profile-avatar">
        <span class="avatar-icon">👤</span>
      </div>
      <div class="profile-info">
        <h1 class="profile-name">{{ userProfile.display_name }}</h1>
        <p class="profile-bio" v-if="userProfile.bio">{{ userProfile.bio }}</p>
        <p class="profile-joined" v-else>加入于 {{ formatDate(userProfile.joined_date) }}</p>
        
        <!-- 用户统计 -->
        <div class="profile-stats">
          <div class="stat-item">
            <span class="stat-value">{{ userProfile.ratings_count || 0 }}</span>
            <span class="stat-label">评分</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ userProfile.comments_count || 0 }}</span>
            <span class="stat-label">评论</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ userProfile.favorites_count || 0 }}</span>
            <span class="stat-label">收藏</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ userProfile.following_count || 0 }}</span>
            <span class="stat-label">关注</span>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="profile-actions" v-if="!isOwnProfile">
        <button 
          class="follow-btn"
          :class="{ following: isFollowing }"
          @click="toggleFollow"
        >
          {{ isFollowing ? '已关注' : '关注' }}
        </button>
        <button class="message-btn">私信</button>
      </div>
    </div>

    <!-- 导航标签 -->
    <div class="profile-nav">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        class="nav-tab"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.name }}
      </button>
    </div>

    <!-- 内容区域 -->
    <div class="profile-content">
      <!-- 动态页面 -->
      <div v-if="activeTab === 'activity'" class="tab-content">
        <div class="activity-feed">
          <div 
            v-for="activity in userActivities" 
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-avatar">
              <span class="avatar-icon">👤</span>
            </div>
            <div class="activity-content">
              <div class="activity-header">
                <span class="activity-user">{{ userProfile.display_name }}</span>
                <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
              </div>
              <div class="activity-text">{{ getActivityText(activity) }}</div>
              
              <!-- 活动内容预览 -->
              <div class="activity-preview" v-if="activity.content_data">
                <div class="preview-content">
                  <img 
                    v-if="activity.content_data.poster" 
                    :src="activity.content_data.poster" 
                    :alt="activity.content_data.title"
                    class="preview-image"
                  />
                  <div class="preview-info">
                    <h4 class="preview-title">{{ activity.content_data.title }}</h4>
                    <p class="preview-year" v-if="activity.content_data.year">
                      {{ activity.content_data.year }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div class="empty-state" v-if="userActivities.length === 0">
            <p>暂无动态</p>
          </div>
          
          <!-- 加载更多 -->
          <div class="load-more" v-if="hasMoreActivities">
            <button class="btn-load-more" @click="loadMoreActivities">
              加载更多动态
            </button>
          </div>
        </div>
      </div>

      <!-- 评分页面 -->
      <div v-if="activeTab === 'ratings'" class="tab-content">
        <div class="ratings-grid">
          <div 
            v-for="rating in userRatings" 
            :key="rating.content_id"
            class="rating-item"
          >
            <div class="rating-poster">
              <img 
                v-if="rating.poster" 
                :src="rating.poster" 
                :alt="rating.title"
              />
              <div v-else class="poster-placeholder">📽️</div>
            </div>
            <div class="rating-info">
              <h4 class="rating-title">{{ rating.title }}</h4>
              <div class="rating-score">
                <span class="user-rating">{{ rating.rating }}</span>
                <span class="avg-rating" v-if="rating.avg_rating">
                  平均: {{ rating.avg_rating }}
                </span>
              </div>
              <p class="rating-year" v-if="rating.year">{{ rating.year }}</p>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div class="empty-state" v-if="userRatings.length === 0">
          <p>暂无评分记录</p>
        </div>
      </div>

      <!-- 收藏页面 -->
      <div v-if="activeTab === 'favorites'" class="tab-content">
        <div class="favorites-grid">
          <div 
            v-for="favorite in userFavorites" 
            :key="favorite.content_id"
            class="favorite-item"
          >
            <div class="favorite-poster">
              <img 
                v-if="favorite.poster" 
                :src="favorite.poster" 
                :alt="favorite.title"
              />
              <div v-else class="poster-placeholder">❤️</div>
              <div class="favorite-overlay">
                <button class="overlay-btn" @click="removeFavorite(favorite.content_id)">
                  取消收藏
                </button>
              </div>
            </div>
            <div class="favorite-info">
              <h4 class="favorite-title">{{ favorite.title }}</h4>
              <p class="favorite-year" v-if="favorite.year">{{ favorite.year }}</p>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div class="empty-state" v-if="userFavorites.length === 0">
          <p>暂无收藏内容</p>
        </div>
      </div>

      <!-- 评论页面 -->
      <div v-if="activeTab === 'comments'" class="tab-content">
        <div class="comments-list">
          <div 
            v-for="comment in userComments" 
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-header">
              <h4 class="comment-title">{{ comment.content_title }}</h4>
              <span class="comment-time">{{ formatTime(comment.timestamp) }}</span>
            </div>
            <div class="comment-text">{{ comment.text }}</div>
            <div class="comment-actions">
              <span class="comment-likes">👍 {{ comment.likes || 0 }}</span>
              <button 
                v-if="isOwnProfile"
                class="delete-btn"
                @click="deleteComment(comment.id)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div class="empty-state" v-if="userComments.length === 0">
          <p>暂无评论记录</p>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div class="loading-overlay" v-if="loading">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'SocialProfile',
  setup() {
    const route = useRoute()
    const userId = ref(route.params.userId || 'current')
    const activeTab = ref('activity')
    const loading = ref(false)
    const isFollowing = ref(false)
    const hasMoreActivities = ref(false)
    const currentPage = ref(1)

    // 用户资料
    const userProfile = ref({
      display_name: '用户',
      bio: '',
      joined_date: new Date().toISOString(),
      ratings_count: 0,
      comments_count: 0,
      favorites_count: 0,
      following_count: 0
    })

    // 用户数据
    const userActivities = ref([])
    const userRatings = ref([])
    const userFavorites = ref([])
    const userComments = ref([])

    // 标签页配置
    const tabs = [
      { id: 'activity', name: '动态' },
      { id: 'ratings', name: '评分' },
      { id: 'favorites', name: '收藏' },
      { id: 'comments', name: '评论' }
    ]

    // 是否为自己的个人主页
    const isOwnProfile = computed(() => {
      return userId.value === 'current' || userId.value === 'anonymous'
    })

    // 监听标签页切换
    watch(activeTab, (newTab) => {
      loadTabData(newTab)
    })

    // 监听用户ID变化
    watch(() => route.params.userId, (newUserId) => {
      if (newUserId) {
        userId.value = newUserId
        loadUserProfile()
        loadTabData(activeTab.value)
      }
    })

    // 加载用户资料
    const loadUserProfile = async () => {
      try {
        const response = await fetch(`/api/social/profile/${userId.value}`)
        if (response.ok) {
          const data = await response.json()
          userProfile.value = data
        }
      } catch (error) {
        console.error('加载用户资料失败:', error)
      }
    }

    // 加载标签页数据
    const loadTabData = async (tab) => {
      if (loading.value) return
      
      loading.value = true
      try {
        switch (tab) {
          case 'activity':
            await loadUserActivities()
            break
          case 'ratings':
            await loadUserRatings()
            break
          case 'favorites':
            await loadUserFavorites()
            break
          case 'comments':
            await loadUserComments()
            break
        }
      } catch (error) {
        console.error(`加载${tab}数据失败:`, error)
      } finally {
        loading.value = false
      }
    }

    // 加载用户动态
    const loadUserActivities = async () => {
      const response = await fetch(`/api/social/activities/${userId.value}?page=${currentPage.value}`)
      if (response.ok) {
        const data = await response.json()
        userActivities.value = data.activities || []
        hasMoreActivities.value = data.has_more || false
      }
    }

    // 加载用户评分
    const loadUserRatings = async () => {
      const response = await fetch(`/api/social/ratings/${userId.value}`)
      if (response.ok) {
        const data = await response.json()
        userRatings.value = data.ratings || []
      }
    }

    // 加载用户收藏
    const loadUserFavorites = async () => {
      const response = await fetch(`/api/social/favorites/${userId.value}`)
      if (response.ok) {
        const data = await response.json()
        userFavorites.value = data.favorites || []
      }
    }

    // 加载用户评论
    const loadUserComments = async () => {
      const response = await fetch(`/api/social/comments/${userId.value}`)
      if (response.ok) {
        const data = await response.json()
        userComments.value = data.comments || []
      }
    }

    // 加载更多动态
    const loadMoreActivities = async () => {
      currentPage.value += 1
      await loadUserActivities()
    }

    // 切换关注状态
    const toggleFollow = async () => {
      if (isOwnProfile.value) {
        ElMessage.warning('不能关注自己')
        return
      }

      try {
        const response = await fetch('/api/social/follow', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: 'current', // 当前用户
            target_user_id: userId.value
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            isFollowing.value = !isFollowing.value
            ElMessage.success(result.message)
            
            // 更新关注统计
            if (isFollowing.value) {
              userProfile.value.following_count = (userProfile.value.following_count || 0) + 1
            } else {
              userProfile.value.following_count = Math.max(0, (userProfile.value.following_count || 1) - 1)
            }
          }
        }
      } catch (error) {
        console.error('关注操作失败:', error)
        ElMessage.error('操作失败')
      }
    }

    // 移除收藏
    const removeFavorite = async (contentId) => {
      if (!isOwnProfile.value) return

      try {
        await ElMessageBox.confirm('确定要取消收藏吗？', '确认取消', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        const response = await fetch('/api/social/favorite', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: 'current',
            content_id: contentId,
            action: 'remove'
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            // 从列表中移除
            userFavorites.value = userFavorites.value.filter(f => f.content_id !== contentId)
            userProfile.value.favorites_count = Math.max(0, (userProfile.value.favorites_count || 1) - 1)
            ElMessage.success('已取消收藏')
          }
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('取消收藏失败:', error)
          ElMessage.error('操作失败')
        }
      }
    }

    // 删除评论
    const deleteComment = async (commentId) => {
      if (!isOwnProfile.value) return

      try {
        await ElMessageBox.confirm('确定要删除这条评论吗？', '确认删除', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        const response = await fetch(`/api/social/comment/${commentId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            // 从列表中移除
            userComments.value = userComments.value.filter(c => c.id !== commentId)
            userProfile.value.comments_count = Math.max(0, (userProfile.value.comments_count || 1) - 1)
            ElMessage.success('评论删除成功')
          }
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除评论失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }

    // 格式化时间
    const formatTime = (timestamp) => {
      const now = new Date()
      const time = new Date(timestamp)
      const diff = now - time
      
      if (diff < 60000) return '刚刚'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
      if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
      
      return time.toLocaleDateString()
    }

    // 格式化日期
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    // 获取活动文本
    const getActivityText = (activity) => {
      const actions = {
        'rate': `评分为 ${activity.metadata?.rating} 分`,
        'comment': '发表了评论',
        'favorite': activity.metadata?.action === 'favorite' ? '收藏了内容' : '取消收藏',
        'watchlist': activity.metadata?.action === 'add' ? '添加到观看列表' : '从观看列表移除',
        'share': `分享到${activity.metadata?.platform}`
      }
      
      return actions[activity.action] || '进行了操作'
    }

    onMounted(() => {
      loadUserProfile()
      loadTabData(activeTab.value)
    })

    return {
      userProfile,
      activeTab,
      tabs,
      isFollowing,
      userActivities,
      userRatings,
      userFavorites,
      userComments,
      hasMoreActivities,
      loading,
      isOwnProfile,
      toggleFollow,
      removeFavorite,
      deleteComment,
      loadMoreActivities,
      formatTime,
      formatDate,
      getActivityText
    }
  }
}
</script>

<style scoped>
.social-profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  position: relative;
}

.profile-header {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #eee;
}

.profile-avatar {
  flex-shrink: 0;
}

.avatar-icon {
  font-size: 80px;
  display: block;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 32px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.profile-bio,
.profile-joined {
  color: #666;
  margin: 0 0 16px 0;
  font-size: 16px;
}

.profile-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 600;
  color: #3498db;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.profile-actions {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.follow-btn,
.message-btn {
  padding: 8px 16px;
  border: 1px solid #3498db;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.follow-btn {
  background: #3498db;
  color: white;
}

.follow-btn.following {
  background: #27ae60;
  border-color: #27ae60;
}

.message-btn {
  background: white;
  color: #3498db;
}

.profile-nav {
  display: flex;
  gap: 0;
  margin-bottom: 24px;
  border-bottom: 1px solid #eee;
}

.nav-tab {
  padding: 12px 24px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  transition: all 0.2s ease;
}

.nav-tab.active {
  color: #3498db;
  border-bottom-color: #3498db;
}

.nav-tab:hover {
  color: #3498db;
}

.tab-content {
  min-height: 400px;
}

.activity-item {
  display: flex;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-avatar .avatar-icon {
  font-size: 40px;
}

.activity-content {
  flex: 1;
}

.activity-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.activity-user {
  font-weight: 600;
  color: #333;
}

.activity-time {
  font-size: 14px;
  color: #999;
}

.activity-text {
  color: #333;
  margin-bottom: 12px;
}

.activity-preview {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 12px;
}

.preview-content {
  display: flex;
  gap: 12px;
  align-items: center;
}

.preview-image {
  width: 60px;
  height: 90px;
  object-fit: cover;
  border-radius: 4px;
}

.preview-info {
  flex: 1;
}

.preview-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: #333;
}

.preview-year {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.ratings-grid,
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.rating-item,
.favorite-item {
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s ease;
}

.rating-item:hover,
.favorite-item:hover {
  transform: translateY(-2px);
}

.rating-poster,
.favorite-poster {
  position: relative;
  height: 300px;
  overflow: hidden;
}

.rating-poster img,
.favorite-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  background: #e9ecef;
}

.favorite-overlay {
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
  transition: opacity 0.2s ease;
}

.favorite-item:hover .favorite-overlay {
  opacity: 1;
}

.overlay-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.rating-info,
.favorite-info {
  padding: 12px;
}

.rating-title,
.favorite-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #333;
}

.rating-score {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.user-rating {
  font-size: 18px;
  font-weight: 600;
  color: #ffc107;
}

.avg-rating {
  font-size: 12px;
  color: #666;
}

.rating-year,
.favorite-year {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.comment-text {
  line-height: 1.5;
  color: #333;
  margin-bottom: 8px;
}

.comment-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-likes {
  font-size: 12px;
  color: #666;
}

.delete-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.load-more {
  text-align: center;
  margin-top: 20px;
}

.btn-load-more {
  background: #f8f9fa;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  color: #666;
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
  z-index: 10;
}

.loading-spinner {
  width: 20px;
  height: 20px;
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
[data-theme="dark"] .social-profile {
  --bg-secondary: #2a2a2a;
  --text-color: #ffffff;
  --text-secondary: #b0b0b0;
  --border-color: #444;
}

[data-theme="dark"] .profile-header {
  border-bottom-color: var(--border-color);
}

[data-theme="dark"] .profile-name {
  color: var(--text-color);
}

[data-theme="dark"] .profile-bio,
[data-theme="dark"] .profile-joined {
  color: var(--text-secondary);
}

[data-theme="dark"] .profile-nav {
  border-bottom-color: var(--border-color);
}

[data-theme="dark"] .nav-tab {
  color: var(--text-secondary);
}

[data-theme="dark"] .activity-item {
  border-bottom-color: var(--border-color);
}

[data-theme="dark"] .activity-user {
  color: var(--text-color);
}

[data-theme="dark"] .activity-preview {
  background: var(--bg-secondary);
}

[data-theme="dark"] .preview-title {
  color: var(--text-color);
}

[data-theme="dark"] .rating-item,
[data-theme="dark"] .favorite-item,
[data-theme="dark"] .comment-item {
  background: var(--bg-secondary);
}

[data-theme="dark"] .rating-title,
[data-theme="dark"] .favorite-title,
[data-theme="dark"] .comment-title {
  color: var(--text-color);
}

[data-theme="dark"] .btn-load-more {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-color);
}

[data-theme="dark"] .loading-overlay {
  background: rgba(0, 0, 0, 0.8);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .social-profile {
    padding: 16px;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .profile-stats {
    justify-content: center;
  }
  
  .profile-actions {
    justify-content: center;
  }
  
  .ratings-grid,
  .favorites-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
  }
  
  .rating-poster,
  .favorite-poster {
    height: 200px;
  }
  
  .nav-tab {
    padding: 8px 16px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .profile-stats {
    flex-wrap: wrap;
    justify-content: space-around;
  }
  
  .ratings-grid,
  .favorites-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .profile-nav {
    flex-wrap: wrap;
  }
  
  .nav-tab {
    flex: 1;
    min-width: 80px;
    text-align: center;
  }
}
</style>