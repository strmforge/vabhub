<template>
  <div class="share-component">
    <!-- 分享按钮 -->
    <button class="share-btn" @click="showSharePanel = true">
      <span class="share-icon">📤</span>
      <span class="share-text">分享</span>
    </button>

    <!-- 分享面板 -->
    <div class="share-panel" v-if="showSharePanel" @click.self="showSharePanel = false">
      <div class="share-modal">
        <div class="share-header">
          <h3 class="share-title">分享内容</h3>
          <button class="close-btn" @click="showSharePanel = false">×</button>
        </div>
        
        <div class="share-content">
          <!-- 分享平台选择 -->
          <div class="platforms-section">
            <h4 class="section-title">分享到</h4>
            <div class="platforms-grid">
              <button 
                v-for="platform in sharePlatforms" 
                :key="platform.id"
                class="platform-btn"
                @click="shareToPlatform(platform.id)"
              >
                <span class="platform-icon">{{ platform.icon }}</span>
                <span class="platform-name">{{ platform.name }}</span>
              </button>
            </div>
          </div>

          <!-- 链接分享 -->
          <div class="link-section">
            <h4 class="section-title">复制链接</h4>
            <div class="link-input-group">
              <input 
                ref="shareLinkInput"
                type="text" 
                :value="shareLink" 
                readonly
                class="link-input"
              />
              <button class="copy-btn" @click="copyShareLink">
                {{ copyStatus === 'copied' ? '已复制' : '复制' }}
              </button>
            </div>
          </div>

          <!-- 分享统计 -->
          <div class="stats-section" v-if="shareStats.total > 0">
            <h4 class="section-title">分享统计</h4>
            <div class="stats-grid">
              <div class="stat-item">
                <span class="stat-value">{{ shareStats.total }}</span>
                <span class="stat-label">总分享</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ shareStats.wechat || 0 }}</span>
                <span class="stat-label">微信</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ shareStats.weibo || 0 }}</span>
                <span class="stat-label">微博</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ shareStats.qq || 0 }}</span>
                <span class="stat-label">QQ</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 分享成功提示 -->
        <div class="share-success" v-if="shareSuccess">
          <div class="success-icon">✅</div>
          <p class="success-message">分享成功！</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'ShareComponent',
  props: {
    contentId: {
      type: String,
      required: true
    },
    contentData: {
      type: Object,
      default: () => ({
        title: '',
        description: '',
        image: ''
      })
    },
    userId: {
      type: String,
      default: 'anonymous'
    }
  },
  setup(props) {
    const showSharePanel = ref(false)
    const copyStatus = ref('idle') // idle, copying, copied
    const shareSuccess = ref(false)
    const shareLinkInput = ref(null)
    const shareStats = ref({
      total: 0,
      wechat: 0,
      weibo: 0,
      qq: 0
    })

    // 分享平台配置
    const sharePlatforms = [
      { id: 'wechat', name: '微信', icon: '💬' },
      { id: 'weibo', name: '微博', icon: '📱' },
      { id: 'qq', name: 'QQ', icon: '💙' },
      { id: 'qzone', name: 'QQ空间', icon: '🏠' },
      { id: 'douban', name: '豆瓣', icon: '📚' },
      { id: 'link', name: '复制链接', icon: '🔗' }
    ]

    // 生成分享链接
    const shareLink = computed(() => {
      const baseUrl = window.location.origin
      return `${baseUrl}/content/${props.contentId}`
    })

    // 分享到平台
    const shareToPlatform = async (platformId) => {
      if (platformId === 'link') {
        copyShareLink()
        return
      }

      try {
        const response = await fetch('/api/social/share', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: props.userId,
            content_id: props.contentId,
            platform: platformId,
            content_data: props.contentData
          })
        })

        if (response.ok) {
          const result = await response.json()
          
          if (result.success) {
            // 打开分享链接
            window.open(result.share_url, '_blank', 'noopener,noreferrer')
            
            // 显示成功提示
            shareSuccess.value = true
            setTimeout(() => {
              shareSuccess.value = false
              showSharePanel.value = false
            }, 2000)
            
            // 更新分享统计
            await fetchShareStats()
            
            ElMessage.success(`分享到${getPlatformName(platformId)}成功`)
            
            // 触发分享事件
            window.dispatchEvent(new CustomEvent('content-shared', {
              detail: {
                contentId: props.contentId,
                platform: platformId,
                userId: props.userId
              }
            }))
          } else {
            ElMessage.error(result.message)
          }
        } else {
          throw new Error('分享请求失败')
        }
      } catch (error) {
        console.error('分享失败:', error)
        
        // 降级处理：直接打开平台分享页面
        openPlatformShare(platformId)
      }
    }

    // 降级分享：直接打开平台分享页面
    const openPlatformShare = (platformId) => {
      const title = encodeURIComponent(props.contentData.title || 'VabHub内容分享')
      const url = encodeURIComponent(shareLink.value)
      const desc = encodeURIComponent(props.contentData.description || '发现精彩内容')
      
      let shareUrl = ''
      
      switch (platformId) {
        case 'weibo':
          shareUrl = `http://service.weibo.com/share/share.php?url=${url}&title=${title}`
          break
        case 'qq':
          shareUrl = `http://connect.qq.com/widget/shareqq/index.html?url=${url}&title=${title}&desc=${desc}`
          break
        case 'qzone':
          shareUrl = `https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=${url}&title=${title}&desc=${desc}`
          break
        default:
          shareUrl = shareLink.value
      }
      
      if (shareUrl) {
        window.open(shareUrl, '_blank', 'noopener,noreferrer')
        ElMessage.success('分享窗口已打开')
      }
    }

    // 复制分享链接
    const copyShareLink = async () => {
      if (!shareLinkInput.value) return
      
      copyStatus.value = 'copying'
      
      try {
        shareLinkInput.value.select()
        const successful = document.execCommand('copy')
        
        if (successful) {
          copyStatus.value = 'copied'
          ElMessage.success('链接已复制到剪贴板')
          
          // 记录分享行为
          if (props.userId !== 'anonymous') {
            await recordShare('link')
          }
          
          setTimeout(() => {
            copyStatus.value = 'idle'
            showSharePanel.value = false
          }, 2000)
        } else {
          throw new Error('复制失败')
        }
      } catch (error) {
        // 使用现代 Clipboard API
        try {
          await navigator.clipboard.writeText(shareLink.value)
          copyStatus.value = 'copied'
          ElMessage.success('链接已复制到剪贴板')
          
          if (props.userId !== 'anonymous') {
            await recordShare('link')
          }
          
          setTimeout(() => {
            copyStatus.value = 'idle'
            showSharePanel.value = false
          }, 2000)
        } catch (clipboardError) {
          console.error('复制失败:', clipboardError)
          ElMessage.error('复制失败，请手动复制链接')
          copyStatus.value = 'idle'
        }
      }
    }

    // 记录分享行为
    const recordShare = async (platform) => {
      try {
        await fetch('/api/social/share', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: props.userId,
            content_id: props.contentId,
            platform: platform
          })
        })
      } catch (error) {
        console.error('记录分享失败:', error)
      }
    }

    // 获取分享统计
    const fetchShareStats = async () => {
      try {
        const response = await fetch(`/api/social/share-stats/${props.contentId}`)
        
        if (response.ok) {
          const data = await response.json()
          shareStats.value = data
        }
      } catch (error) {
        console.error('获取分享统计失败:', error)
      }
    }

    // 获取平台名称
    const getPlatformName = (platformId) => {
      const platform = sharePlatforms.find(p => p.id === platformId)
      return platform ? platform.name : platformId
    }

    onMounted(() => {
      if (props.userId !== 'anonymous') {
        fetchShareStats()
      }
    })

    return {
      showSharePanel,
      copyStatus,
      shareSuccess,
      shareLinkInput,
      shareStats,
      sharePlatforms,
      shareLink,
      shareToPlatform,
      copyShareLink
    }
  }
}
</script>

<style scoped>
.share-component {
  display: inline-block;
}

.share-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.2s ease;
}

.share-btn:hover {
  background: #e9ecef;
  border-color: #adb5bd;
}

.share-icon {
  font-size: 16px;
}

.share-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.share-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.share-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #eee;
}

.share-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.share-content {
  padding: 24px;
  max-height: 400px;
  overflow-y: auto;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.platforms-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.platform-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.platform-btn:hover {
  background: #e9ecef;
  border-color: #adb5bd;
  transform: translateY(-2px);
}

.platform-icon {
  font-size: 24px;
}

.platform-name {
  font-size: 12px;
  color: #666;
}

.link-input-group {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.link-input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  background: #f8f9fa;
}

.copy-btn {
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  min-width: 60px;
}

.copy-btn:hover {
  background: #2980b9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: 600;
  color: #3498db;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

.share-success {
  text-align: center;
  padding: 20px;
  background: #f0f9f0;
  border: 1px solid #d4edda;
  border-radius: 8px;
  margin-top: 16px;
}

.success-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.success-message {
  color: #155724;
  margin: 0;
  font-weight: 600;
}

/* 暗色主题支持 */
[data-theme="dark"] .share-component {
  --bg-secondary: #2a2a2a;
  --text-color: #ffffff;
  --text-secondary: #b0b0b0;
  --border-color: #444;
}

[data-theme="dark"] .share-btn {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-color);
}

[data-theme="dark"] .share-modal {
  background: #1a1a1a;
}

[data-theme="dark"] .share-title {
  color: var(--text-color);
}

[data-theme="dark"] .platform-btn {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-color);
}

[data-theme="dark"] .link-input {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-color);
}

[data-theme="dark"] .stat-item {
  background: var(--bg-secondary);
}

[data-theme="dark"] .stat-value {
  color: #3498db;
}

[data-theme="dark"] .share-success {
  background: #1a3a1a;
  border-color: #2d5a2d;
}

[data-theme="dark"] .success-message {
  color: #90ee90;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .platforms-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .share-modal {
    width: 95%;
    margin: 20px;
  }
}
</style>