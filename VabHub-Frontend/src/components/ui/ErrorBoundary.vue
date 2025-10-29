<template>
  <div>
    <slot v-if="!hasError" />
    
    <div v-else class="error-boundary">
      <div class="error-boundary__content">
        <!-- 错误图标 -->
        <div class="error-boundary__icon">
          <el-icon class="error-boundary__icon-svg">
            <Warning />
          </el-icon>
        </div>
        
        <!-- 错误信息 -->
        <div class="error-boundary__info">
          <h2 class="error-boundary__title">{{ errorTitle }}</h2>
          <p class="error-boundary__message">{{ errorMessage }}</p>
          
          <!-- 错误详情（开发模式显示） -->
          <details v-if="showDetails" class="error-boundary__details">
            <summary class="error-boundary__details-summary">
              查看错误详情
            </summary>
            <pre class="error-boundary__details-content">{{ errorDetails }}</pre>
          </details>
        </div>
        
        <!-- 操作按钮 -->
        <div class="error-boundary__actions">
          <button
            class="error-boundary__btn error-boundary__btn--primary"
            @click="handleRetry"
          >
            <el-icon><Refresh /></el-icon>
            重试
          </button>
          
          <button
            class="error-boundary__btn error-boundary__btn--secondary"
            @click="handleReport"
          >
            <el-icon><ChatDotRound /></el-icon>
            报告问题
          </button>
          
          <button
            class="error-boundary__btn error-boundary__btn--text"
            @click="handleGoHome"
          >
            <el-icon><HomeFilled /></el-icon>
            返回首页
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onErrorCaptured, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Warning, 
  Refresh, 
  ChatDotRound, 
  HomeFilled 
} from '@element-plus/icons-vue'

export default {
  name: 'ErrorBoundary',
  components: {
    Warning,
    Refresh,
    ChatDotRound,
    HomeFilled
  },
  props: {
    fallback: {
      type: Function,
      default: null
    },
    showDetails: {
      type: Boolean,
      default: process.env.NODE_ENV === 'development'
    },
    autoRetry: {
      type: Boolean,
      default: false
    },
    retryDelay: {
      type: Number,
      default: 3000
    },
    maxRetries: {
      type: Number,
      default: 3
    }
  },
  emits: ['error', 'retry', 'report'],
  setup(props, { emit, slots }) {
    const router = useRouter()
    const hasError = ref(false)
    const error = ref(null)
    const errorInfo = ref(null)
    const retryCount = ref(0)

    // 错误标题映射
    const errorTitles = {
      'Network Error': '网络连接错误',
      'Timeout': '请求超时',
      '404': '页面未找到',
      '500': '服务器错误',
      '403': '访问被拒绝',
      '401': '未授权访问'
    }

    // 错误消息映射
    const errorMessages = {
      'Network Error': '请检查您的网络连接，然后重试。',
      'Timeout': '请求超时，请稍后重试。',
      '404': '抱歉，您访问的页面不存在。',
      '500': '服务器内部错误，请稍后重试。',
      '403': '您没有权限访问此页面。',
      '401': '请先登录以访问此页面。'
    }

    // 获取错误标题
    const errorTitle = ref('发生错误')
    const errorMessage = ref('抱歉，发生了意外错误。')
    const errorDetails = ref('')

    // 更新错误信息
    const updateErrorInfo = (err, info) => {
      error.value = err
      errorInfo.value = info
      
      // 设置错误标题和消息
      const errorKey = err.message || err.toString()
      errorTitle.value = errorTitles[errorKey] || '发生错误'
      errorMessage.value = errorMessages[errorKey] || '抱歉，发生了意外错误。'
      
      // 构建错误详情
      errorDetails.value = `错误: ${err.toString()}\n\n`
      if (info) {
        errorDetails.value += `组件栈: ${info.componentStack}\n`
      }
      errorDetails.value += `时间: ${new Date().toLocaleString()}`
    }

    // 错误处理
    const handleError = (err, info) => {
      hasError.value = true
      updateErrorInfo(err, info)
      retryCount.value++
      
      // 触发错误事件
      emit('error', { error: err, info, retryCount: retryCount.value })
      
      // 自动重试逻辑
      if (props.autoRetry && retryCount.value < props.maxRetries) {
        setTimeout(() => {
          handleRetry()
        }, props.retryDelay)
      }
    }

    // 重试
    const handleRetry = () => {
      hasError.value = false
      error.value = null
      errorInfo.value = null
      
      emit('retry', { retryCount: retryCount.value })
    }

    // 报告问题
    const handleReport = () => {
      const reportData = {
        error: error.value?.toString(),
        componentStack: errorInfo.value?.componentStack,
        userAgent: navigator.userAgent,
        url: window.location.href,
        timestamp: new Date().toISOString()
      }
      
      emit('report', reportData)
      
      // 在实际应用中，这里可以发送错误报告到服务器
      console.error('错误报告:', reportData)
      
      // 显示反馈
      alert('感谢您的反馈！错误信息已记录。')
    }

    // 返回首页
    const handleGoHome = () => {
      router.push('/')
    }

    // 捕获错误
    onErrorCaptured((err, instance, info) => {
      handleError(err, info)
      return false // 阻止错误继续向上传播
    })

    // 全局错误处理
    onMounted(() => {
      // 监听未处理的 Promise 拒绝
      window.addEventListener('unhandledrejection', (event) => {
        handleError(event.reason, { type: 'unhandledrejection' })
      })

      // 监听全局错误
      window.addEventListener('error', (event) => {
        handleError(event.error, { type: 'global', filename: event.filename })
      })
    })

    return {
      hasError,
      errorTitle,
      errorMessage,
      errorDetails,
      handleRetry,
      handleReport,
      handleGoHome
    }
  }
}
</script>

<style scoped>
.error-boundary {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: var(--space-8);
  background: var(--bg-primary);
}

.error-boundary__content {
  max-width: 480px;
  text-align: center;
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-primary);
}

.error-boundary__icon {
  margin-bottom: var(--space-6);
}

.error-boundary__icon-svg {
  font-size: 4rem;
  color: var(--error-500);
}

.error-boundary__info {
  margin-bottom: var(--space-6);
}

.error-boundary__title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0 0 var(--space-3) 0;
}

.error-boundary__message {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.error-boundary__details {
  margin-top: var(--space-4);
  text-align: left;
}

.error-boundary__details-summary {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.error-boundary__details-summary:hover {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.error-boundary__details-content {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  white-space: pre-wrap;
  word-break: break-all;
  margin-top: var(--space-2);
  max-height: 200px;
  overflow-y: auto;
}

.error-boundary__actions {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
  flex-wrap: wrap;
}

.error-boundary__btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: var(--font-size-sm);
}

.error-boundary__btn--primary {
  background: var(--primary-600);
  border-color: var(--primary-600);
  color: white;
}

.error-boundary__btn--primary:hover {
  background: var(--primary-700);
  border-color: var(--primary-700);
  transform: translateY(-1px);
}

.error-boundary__btn--secondary {
  background: var(--bg-tertiary);
  border-color: var(--border-primary);
  color: var(--text-secondary);
}

.error-boundary__btn--secondary:hover {
  background: var(--bg-secondary);
  border-color: var(--border-secondary);
  color: var(--text-primary);
}

.error-boundary__btn--text {
  background: transparent;
  border-color: transparent;
  color: var(--text-tertiary);
}

.error-boundary__btn--text:hover {
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .error-boundary {
    padding: var(--space-4);
    min-height: 300px;
  }
  
  .error-boundary__content {
    padding: var(--space-6);
  }
  
  .error-boundary__icon-svg {
    font-size: 3rem;
  }
  
  .error-boundary__title {
    font-size: var(--font-size-xl);
  }
  
  .error-boundary__actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .error-boundary__btn {
    justify-content: center;
  }
}

/* 深色主题适配 */
[data-theme="dark"] .error-boundary__content {
  background: rgba(17, 24, 39, 0.8);
  border-color: var(--border-secondary);
}

/* 无障碍访问 */
.error-boundary__btn:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

.error-boundary__details-summary:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .error-boundary__btn {
    transition: none;
  }
  
  .error-boundary__btn:hover {
    transform: none;
  }
}
</style>