// 错误处理工具

/**
 * 错误类型枚举
 */
export const ErrorTypes = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  API_ERROR: 'API_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  AUTH_ERROR: 'AUTH_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR'
}

/**
 * 自定义错误类
 */
export class AppError extends Error {
  constructor(message, type = ErrorTypes.UNKNOWN_ERROR, details = {}) {
    super(message)
    this.name = 'AppError'
    this.type = type
    this.details = details
    this.timestamp = new Date().toISOString()
  }
}

/**
 * 错误处理器
 */
export class ErrorHandler {
  constructor() {
    this.listeners = []
    this.setupGlobalErrorHandling()
  }

  /**
   * 设置全局错误处理
   */
  setupGlobalErrorHandling() {
    // Vue错误处理
    if (window.Vue && window.Vue.config) {
      window.Vue.config.errorHandler = (err, vm, info) => {
        this.handleError(err, {
          component: vm?.$options?.name,
          lifecycleHook: info,
          isVueError: true
        })
      }
    }

    // 全局错误处理
    window.addEventListener('error', (event) => {
      this.handleError(event.error || new Error(event.message), {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        isGlobalError: true
      })
    })

    // Promise rejection处理
    window.addEventListener('unhandledrejection', (event) => {
      this.handleError(event.reason, {
        isPromiseRejection: true
      })
    })
  }

  /**
   * 处理错误
   */
  handleError(error, context = {}) {
    const errorInfo = {
      message: error.message,
      stack: error.stack,
      name: error.name,
      ...context,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href
    }

    // 通知监听器
    this.notifyListeners(errorInfo)

    // 开发环境输出到控制台
    if (import.meta.env.DEV) {
      console.error('捕获到错误:', errorInfo)
    }

    // 生产环境发送到错误收集服务
    if (import.meta.env.PROD) {
      this.reportToServer(errorInfo)
    }

    return errorInfo
  }

  /**
   * 报告错误到服务器
   */
  async reportToServer(errorInfo) {
    try {
      // 这里可以集成错误收集服务，如Sentry、Bugsnag等
      // 暂时使用console.log模拟
      console.log('错误报告:', errorInfo)
    } catch (reportError) {
      console.warn('错误报告失败:', reportError)
    }
  }

  /**
   * 添加错误监听器
   */
  addListener(listener) {
    this.listeners.push(listener)
  }

  /**
   * 移除错误监听器
   */
  removeListener(listener) {
    const index = this.listeners.indexOf(listener)
    if (index > -1) {
      this.listeners.splice(index, 1)
    }
  }

  /**
   * 通知所有监听器
   */
  notifyListeners(errorInfo) {
    this.listeners.forEach(listener => {
      try {
        listener(errorInfo)
      } catch (listenerError) {
        console.warn('错误监听器执行失败:', listenerError)
      }
    })
  }

  /**
   * 创建友好的错误消息
   */
  createFriendlyMessage(error) {
    const messages = {
      [ErrorTypes.NETWORK_ERROR]: '网络连接失败，请检查网络设置',
      [ErrorTypes.API_ERROR]: '服务器请求失败，请稍后重试',
      [ErrorTypes.VALIDATION_ERROR]: '输入数据格式不正确',
      [ErrorTypes.AUTH_ERROR]: '身份验证失败，请重新登录',
      [ErrorTypes.UNKNOWN_ERROR]: '系统发生未知错误'
    }

    return messages[error.type] || messages[ErrorTypes.UNKNOWN_ERROR]
  }
}

/**
 * 全局错误处理器实例
 */
export const globalErrorHandler = new ErrorHandler()

/**
 * 错误边界工具函数
 */
export const withErrorBoundary = (component, fallbackComponent) => {
  return {
    name: `ErrorBoundary${component.name || ''}`,
    components: { Component: component, Fallback: fallbackComponent },
    data() {
      return {
        hasError: false,
        error: null
      }
    },
    errorCaptured(err, vm, info) {
      this.hasError = true
      this.error = err
      globalErrorHandler.handleError(err, {
        component: vm?.$options?.name,
        lifecycleHook: info,
        boundary: true
      })
      return false // 阻止错误继续向上传播
    },
    render(h) {
      if (this.hasError) {
        return h('Fallback', { props: { error: this.error } })
      }
      return h('Component', this.$attrs, this.$slots.default)
    }
  }
}

/**
 * 创建友好的错误消息（独立函数）
 */
export function createFriendlyMessage(error) {
  const messages = {
    [ErrorTypes.NETWORK_ERROR]: '网络连接失败，请检查网络设置',
    [ErrorTypes.API_ERROR]: '服务器请求失败，请稍后重试',
    [ErrorTypes.VALIDATION_ERROR]: '输入数据格式不正确',
    [ErrorTypes.AUTH_ERROR]: '身份验证失败，请重新登录',
    [ErrorTypes.UNKNOWN_ERROR]: '系统发生未知错误'
  }

  return messages[error.type] || messages[ErrorTypes.UNKNOWN_ERROR]
}