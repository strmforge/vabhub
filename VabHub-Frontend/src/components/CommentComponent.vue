<template>
  <div class="comment-component">
    <!-- 评论输入框 -->
    <div class="comment-input-section" v-if="userId !== 'anonymous'">
      <div class="input-header">
        <span class="input-title">发表评论</span>
        <span class="char-count">{{ commentText.length }}/1000</span>
      </div>
      <textarea
        v-model="commentText"
        class="comment-textarea"
        placeholder="写下你的想法..."
        maxlength="1000"
        rows="3"
      ></textarea>
      <div class="input-actions">
        <button 
          class="btn-submit" 
          :disabled="!commentText.trim() || submitting"
          @click="submitComment"
        >
          {{ submitting ? '发表中...' : '发表评论' }}
        </button>
      </div>
    </div>

    <!-- 未登录提示 -->
    <div class="login-prompt" v-else>
      <p>请登录后发表评论</p>
      <button class="btn-login" @click="$emit('login-required')">登录</button>
    </div>

    <!-- 评论列表 -->
    <div class="comments-section">
      <div class="comments-header">
        <h3 class="comments-title">评论 ({{ comments.length }})</h3>
        <div class="sort-options">
          <button 
            class="sort-btn" 
            :class="{ active: sortBy === 'time' }"
            @click="sortBy = 'time'"
          >
            最新
          </button>
          <button 
            class="sort-btn" 
            :class="{ active: sortBy === 'hot' }"
            @click="sortBy = 'hot'"
          >
            热门
          </button>
        </div>
      </div>

      <!-- 评论列表 -->
      <div class="comments-list">
        <div 
          v-for="comment in sortedComments" 
          :key="comment.id"
          class="comment-item"
        >
          <div class="comment-avatar">
            <span class="avatar-icon">👤</span>
          </div>
          <div class="comment-content">
            <div class="comment-header">
              <span class="comment-author">{{ comment.user_display_name }}</span>
              <span class="comment-time">{{ formatTime(comment.timestamp) }}</span>
            </div>
            <div class="comment-text">{{ comment.text }}</div>
            <div class="comment-actions">
              <button 
                class="action-btn"
                :class="{ liked: comment.likes > 0 }"
                @click="likeComment(comment.id)"
              >
                👍 {{ comment.likes || '' }}
              </button>
              <button class="action-btn" @click="replyToComment(comment)">回复</button>
              <button 
                v-if="comment.user_id === userId"
                class="action-btn delete-btn"
                @click="deleteComment(comment.id)"
              >
                删除
              </button>
            </div>

            <!-- 回复列表 -->
            <div class="replies-section" v-if="comment.replies && comment.replies.length > 0">
              <div 
                v-for="reply in comment.replies" 
                :key="reply.id"
                class="reply-item"
              >
                <div class="reply-avatar">
                  <span class="avatar-icon">👤</span>
                </div>
                <div class="reply-content">
                  <div class="reply-header">
                    <span class="reply-author">{{ reply.user_display_name }}</span>
                    <span class="reply-time">{{ formatTime(reply.timestamp) }}</span>
                  </div>
                  <div class="reply-text">{{ reply.text }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div class="empty-state" v-if="comments.length === 0">
          <p>暂无评论，快来发表第一条评论吧！</p>
        </div>
      </div>

      <!-- 加载更多 -->
      <div class="load-more" v-if="hasMoreComments">
        <button class="btn-load-more" @click="loadMoreComments">
          加载更多评论
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'CommentComponent',
  props: {
    contentId: {
      type: String,
      required: true
    },
    userId: {
      type: String,
      default: 'anonymous'
    }
  },
  emits: ['login-required'],
  setup(props) {
    const commentText = ref('')
    const submitting = ref(false)
    const comments = ref([])
    const sortBy = ref('time')
    const currentPage = ref(1)
    const hasMoreComments = ref(true)
    const pageSize = 10

    // 排序后的评论
    const sortedComments = computed(() => {
      const sorted = [...comments.value]
      
      if (sortBy.value === 'time') {
        return sorted.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      } else if (sortBy.value === 'hot') {
        return sorted.sort((a, b) => (b.likes || 0) - (a.likes || 0))
      }
      
      return sorted
    })

    // 格式化时间
    const formatTime = (timestamp) => {
      const now = new Date()
      const commentTime = new Date(timestamp)
      const diff = now - commentTime
      
      if (diff < 60000) return '刚刚'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
      if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
      
      return commentTime.toLocaleDateString()
    }

    // 提交评论
    const submitComment = async () => {
      if (submitting.value || !commentText.value.trim()) return
      
      submitting.value = true
      try {
        const response = await fetch('/api/social/comment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: props.userId,
            content_id: props.contentId,
            text: commentText.value.trim()
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            // 添加新评论到列表开头
            comments.value.unshift(result.comment)
            commentText.value = ''
            ElMessage.success('评论发表成功')
            
            // 触发评论事件
            window.dispatchEvent(new CustomEvent('comment-added', {
              detail: {
                contentId: props.contentId,
                comment: result.comment
              }
            }))
          } else {
            ElMessage.error(result.message)
          }
        } else {
          throw new Error('评论请求失败')
        }
      } catch (error) {
        console.error('评论失败:', error)
        ElMessage.error('评论失败，请重试')
      } finally {
        submitting.value = false
      }
    }

    // 点赞评论
    const likeComment = async (commentId) => {
      if (props.userId === 'anonymous') {
        ElMessage.warning('请登录后点赞')
        return
      }

      try {
        const response = await fetch('/api/social/like-comment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: props.userId,
            comment_id: commentId
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            // 更新评论点赞数
            const comment = comments.value.find(c => c.id === commentId)
            if (comment) {
              comment.likes = result.likes
            }
            ElMessage.success(result.message)
          }
        }
      } catch (error) {
        console.error('点赞失败:', error)
        ElMessage.error('点赞失败')
      }
    }

    // 回复评论
    const replyToComment = (comment) => {
      if (props.userId === 'anonymous') {
        ElMessage.warning('请登录后回复')
        return
      }
      
      // 简化实现：将回复内容添加到评论输入框
      commentText.value = `@${comment.user_display_name} `
      
      // 在实际项目中，这里应该实现完整的回复功能
      ElMessage.info('回复功能开发中...')
    }

    // 删除评论
    const deleteComment = async (commentId) => {
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
          },
          body: JSON.stringify({
            user_id: props.userId
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            // 从列表中移除评论
            comments.value = comments.value.filter(c => c.id !== commentId)
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

    // 加载评论
    const loadComments = async (page = 1) => {
      try {
        const response = await fetch(`/api/social/comments/${props.contentId}?page=${page}&size=${pageSize}`)
        
        if (response.ok) {
          const data = await response.json()
          
          if (page === 1) {
            comments.value = data.comments || []
          } else {
            comments.value.push(...(data.comments || []))
          }
          
          hasMoreComments.value = data.has_more || false
          currentPage.value = page
        }
      } catch (error) {
        console.error('加载评论失败:', error)
      }
    }

    // 加载更多评论
    const loadMoreComments = () => {
      loadComments(currentPage.value + 1)
    }

    onMounted(() => {
      loadComments(1)
    })

    return {
      commentText,
      submitting,
      comments,
      sortBy,
      hasMoreComments,
      sortedComments,
      formatTime,
      submitComment,
      likeComment,
      replyToComment,
      deleteComment,
      loadMoreComments
    }
  }
}
</script>

<style scoped>
.comment-component {
  max-width: 800px;
  margin: 0 auto;
}

.comment-input-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.input-title {
  font-weight: 600;
  color: #333;
}

.char-count {
  font-size: 12px;
  color: #999;
}

.comment-textarea {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 12px;
  font-size: 14px;
  resize: vertical;
  font-family: inherit;
}

.comment-textarea:focus {
  outline: none;
  border-color: #3498db;
}

.input-actions {
  margin-top: 12px;
  text-align: right;
}

.btn-submit {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.login-prompt {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 24px;
}

.btn-login {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 8px;
}

.comments-section {
  border-top: 1px solid #eee;
  padding-top: 24px;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.comments-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.sort-options {
  display: flex;
  gap: 8px;
}

.sort-btn {
  padding: 4px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.sort-btn.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.comment-avatar {
  flex-shrink: 0;
}

.avatar-icon {
  font-size: 24px;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.comment-author {
  font-weight: 600;
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
  gap: 12px;
}

.action-btn {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 12px;
  padding: 2px 6px;
}

.action-btn:hover {
  color: #3498db;
}

.action-btn.liked {
  color: #e74c3c;
}

.delete-btn {
  color: #e74c3c;
}

.replies-section {
  margin-top: 12px;
  padding-left: 20px;
  border-left: 2px solid #f0f0f0;
}

.reply-item {
  display: flex;
  gap: 8px;
  padding: 8px 0;
}

.reply-avatar .avatar-icon {
  font-size: 16px;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 2px;
}

.reply-author {
  font-size: 12px;
  font-weight: 600;
}

.reply-time {
  font-size: 10px;
  color: #999;
}

.reply-text {
  font-size: 12px;
  line-height: 1.4;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
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

.btn-load-more:hover {
  background: #e9ecef;
}

/* 暗色主题支持 */
[data-theme="dark"] .comment-component {
  --bg-secondary: #2a2a2a;
  --text-color: #ffffff;
  --text-secondary: #b0b0b0;
  --border-color: #444;
}

[data-theme="dark"] .comment-input-section {
  background: var(--bg-secondary);
}

[data-theme="dark"] .comment-textarea {
  background: #1a1a1a;
  border-color: var(--border-color);
  color: var(--text-color);
}

[data-theme="dark"] .login-prompt {
  background: var(--bg-secondary);
}

[data-theme="dark"] .comments-section {
  border-top-color: var(--border-color);
}

[data-theme="dark"] .comment-item {
  border-bottom-color: var(--border-color);
}

[data-theme="dark"] .btn-load-more {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-color);
}
</style>