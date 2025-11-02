<template>
  <div v-if="hasError" class="error-boundary">
    <div class="error-content">
      <div class="error-icon">⚠️</div>
      <h2 class="error-title">页面加载失败</h2>
      <p class="error-message">{{ errorMessage }}</p>
      <div class="error-actions">
        <button @click="reloadPage" class="btn btn-primary">重新加载</button>
        <button @click="goHome" class="btn btn-secondary">返回首页</button>
        <button v-if="showDetails" @click="toggleDetails" class="btn btn-outline">
          {{ showDetails ? '隐藏详情' : '显示详情' }}
        </button>
      </div>
      
      <div v-if="showDetails" class="error-details">
        <h3>错误详情</h3>
        <pre class="error-stack">{{ errorStack }}</pre>
        <div class="error-info">
          <p><strong>错误类型:</strong> {{ errorType }}</p>
          <p><strong>发生时间:</strong> {{ errorTime }}</p>
          <p><strong>页面路径:</strong> {{ currentPath }}</p>
        </div>
      </div>
    </div>
  </div>
  <slot v-else></slot>
</template>

<script>
import { errorHandler } from '../utils/errorHandler'

export default {
  name: 'ErrorBoundary',
  props: {
    fallback: {
      type: Function,
      default: null
    }
  },
  data() {
    return {
      hasError: false,
      error: null,
      errorInfo: null,
      showDetails: false
    }
  },
  computed: {
    errorMessage() {
      if (this.fallback) {
        return this.fallback(this.error, this.errorInfo)
      }
      
      return errorHandler.createUserFriendlyMessage(this.error || {})
    },
    errorStack() {
      return this.error?.stack || '无堆栈信息'
    },
    errorType() {
      return this.error?.name || 'Unknown'
    },
    errorTime() {
      return new Date().toLocaleString()
    },
    currentPath() {
      return this.$route?.path || window.location.pathname
    }
  },
  errorCaptured(error, vm, info) {
    this.hasError = true
    this.error = error
    this.errorInfo = info
    
    // 记录错误
    errorHandler.handleError(error, {
      component: this.$options.name,
      lifecycleHook: info,
      boundary: true
    })
    
    // 阻止错误继续向上传播
    return false
  },
  methods: {
    reloadPage() {
      window.location.reload()
    },
    goHome() {
      if (this.$router) {
        this.$router.push('/')
      } else {
        window.location.href = '/'
      }
    },
    toggleDetails() {
      this.showDetails = !this.showDetails
    },
    resetError() {
      this.hasError = false
      this.error = null
      this.errorInfo = null
      this.showDetails = false
    }
  },
  watch: {
    '$route.path'() {
      // 路由变化时重置错误状态
      this.resetError()
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
  padding: 2rem;
  background: var(--bg-primary);
}

.error-content {
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.error-message {
  color: var(--text-secondary);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.error-details {
  text-align: left;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.error-details h3 {
  margin: 0 0 1rem 0;
  color: var(--text-primary);
  font-size: 1.1rem;
}

.error-stack {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 1rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  overflow-x: auto;
  margin-bottom: 1rem;
  max-height: 200px;
  overflow-y: auto;
}

.error-info p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.error-info strong {
  color: var(--text-primary);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .error-boundary {
    padding: 1rem;
    min-height: 300px;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .error-actions .btn {
    width: 100%;
    max-width: 200px;
  }
  
  .error-details {
    padding: 1rem;
  }
}

/* 暗色主题适配 */
[data-theme="dark"] .error-boundary {
  background: var(--bg-primary);
}

[data-theme="dark"] .error-stack {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}
</style>