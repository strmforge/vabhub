<template>
  <div v-if="showPrompt" class="pwa-install-prompt">
    <div class="pwa-prompt-overlay" @click="dismissPrompt"></div>
    <div class="pwa-prompt-content">
      <div class="pwa-prompt-header">
        <h3>安装应用</h3>
        <button class="close-button" @click="dismissPrompt" aria-label="关闭">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 6.586L13.657.929l1.414 1.414L9.414 8l5.657 5.657-1.414 1.414L8 9.414l-5.657 5.657-1.414-1.414L6.586 8 .929 2.343 2.343.929 8 6.586z"/>
          </svg>
        </button>
      </div>
      
      <div class="pwa-prompt-body">
        <div class="app-info">
          <div class="app-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="currentColor">
              <path d="M24 4C12.954 4 4 12.954 4 24s8.954 20 20 20 20-8.954 20-20S35.046 4 24 4zm0 36c-8.837 0-16-7.163-16-16S15.163 8 24 8s16 7.163 16 16-7.163 16-16 16z"/>
              <path d="M24 12c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm0 20c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8z"/>
            </svg>
          </div>
          <div class="app-details">
            <h4>VabHub</h4>
            <p>更好的应用体验</p>
          </div>
        </div>
        
        <div class="pwa-benefits">
          <div class="benefit-item">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2C5.582 2 2 5.582 2 10s3.582 8 8 8 8-3.582 8-8-3.582-8-8-8zm0 14c-3.314 0-6-2.686-6-6s2.686-6 6-6 6 2.686 6 6-2.686 6-6 6z"/>
              <path d="M10 6c-2.209 0-4 1.791-4 4s1.791 4 4 4 4-1.791 4-4-1.791-4-4-4zm0 6c-1.105 0-2-.895-2-2s.895-2 2-2 2 .895 2 2-.895 2-2 2z"/>
            </svg>
            <span>快速启动</span>
          </div>
          <div class="benefit-item">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2C5.582 2 2 5.582 2 10s3.582 8 8 8 8-3.582 8-8-3.582-8-8-8zm0 14c-3.314 0-6-2.686-6-6s2.686-6 6-6 6 2.686 6 6-2.686 6-6 6z"/>
              <path d="M10 6c-2.209 0-4 1.791-4 4s1.791 4 4 4 4-1.791 4-4-1.791-4-4-4zm0 6c-1.105 0-2-.895-2-2s.895-2 2-2 2 .895 2 2-.895 2-2 2z"/>
            </svg>
            <span>离线使用</span>
          </div>
          <div class="benefit-item">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2C5.582 2 2 5.582 2 10s3.582 8 8 8 8-3.582 8-8-3.582-8-8-8zm0 14c-3.314 0-6-2.686-6-6s2.686-6 6-6 6 2.686 6 6-2.686 6-6 6z"/>
              <path d="M10 6c-2.209 0-4 1.791-4 4s1.791 4 4 4 4-1.791 4-4-1.791-4-4-4zm0 6c-1.105 0-2-.895-2-2s.895-2 2-2 2 .895 2 2-.895 2-2 2z"/>
            </svg>
            <span>桌面快捷方式</span>
          </div>
        </div>
      </div>
      
      <div class="pwa-prompt-footer">
        <button class="secondary-button" @click="dismissPrompt">
          稍后再说
        </button>
        <button class="primary-button" @click="installApp">
          安装应用
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const showPrompt = ref(false)
let deferredPrompt = null

// 监听 beforeinstallprompt 事件
const handleBeforeInstallPrompt = (event) => {
  // 阻止默认的安装提示
  event.preventDefault()
  // 保存事件对象
  deferredPrompt = event
  // 显示自定义安装提示
  showPrompt.value = true
}

// 安装应用
const installApp = async () => {
  if (!deferredPrompt) return
  
  try {
    // 触发安装流程
    deferredPrompt.prompt()
    
    // 等待用户选择
    const { outcome } = await deferredPrompt.userChoice
    
    console.log(`用户选择: ${outcome}`)
    
    // 无论用户选择什么，都隐藏提示
    showPrompt.value = false
    deferredPrompt = null
    
    // 保存用户选择到本地存储
    localStorage.setItem('pwaInstallPromptShown', 'true')
    
  } catch (error) {
    console.error('安装失败:', error)
    showPrompt.value = false
    deferredPrompt = null
  }
}

// 关闭提示
const dismissPrompt = () => {
  showPrompt.value = false
  deferredPrompt = null
  
  // 保存用户选择到本地存储
  localStorage.setItem('pwaInstallPromptShown', 'true')
}

// 检查是否已经显示过提示
const shouldShowPrompt = () => {
  const shown = localStorage.getItem('pwaInstallPromptShown')
  return !shown || shown === 'false'
}

onMounted(() => {
  // 添加事件监听器
  window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
  
  // 检查应用是否已经安装
  window.addEventListener('appinstalled', () => {
    console.log('应用已安装')
    showPrompt.value = false
    deferredPrompt = null
  })
})

onUnmounted(() => {
  // 移除事件监听器
  window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
})
</script>

<style scoped>
.pwa-install-prompt {
  position: fixed;
  z-index: 1000;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pwa-prompt-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.pwa-prompt-content {
  position: relative;
  background: var(--surface-color);
  border-radius: 12px;
  padding: 0;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.pwa-prompt-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 20px 0;
  margin-bottom: 16px;
}

.pwa-prompt-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
}

.close-button {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-secondary);
  transition: all 0.2s;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-color);
}

.pwa-prompt-body {
  padding: 0 20px 20px;
}

.app-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.app-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.app-details h4 {
  margin: 0 0 4px 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-color);
}

.app-details p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.pwa-benefits {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.benefit-item svg {
  flex-shrink: 0;
}

.pwa-prompt-footer {
  display: flex;
  gap: 12px;
  padding: 0 20px 20px;
}

.primary-button,
.secondary-button {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.primary-button {
  background: var(--primary-color);
  color: white;
}

.primary-button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.secondary-button {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-color);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.secondary-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .pwa-prompt-content {
    margin: 20px;
    width: calc(100% - 40px);
  }
  
  .pwa-prompt-footer {
    flex-direction: column;
  }
}
</style>