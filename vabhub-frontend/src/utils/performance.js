/**
 * 性能监控和优化工具
 * 提供性能指标收集、监控和优化建议
 */

/**
 * 性能指标收集
 */
export class PerformanceMonitor {
  constructor() {
    this.metrics = new Map()
    this.observers = []
    this.isMonitoring = false
  }

  /**
   * 开始性能监控
   */
  start() {
    if (this.isMonitoring) return

    this.isMonitoring = true
    this.setupPerformanceObserver()
    this.setupNavigationTiming()
    this.setupResourceTiming()
    this.setupLongTaskObserver()

    console.log('性能监控已启动')
  }

  /**
   * 停止性能监控
   */
  stop() {
    this.isMonitoring = false
    this.observers.forEach(observer => observer.disconnect())
    this.observers = []
    console.log('性能监控已停止')
  }

  /**
   * 设置性能观察器
   */
  setupPerformanceObserver() {
    if (!('PerformanceObserver' in window)) return

    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        this.handlePerformanceEntry(entry)
      })
    })

    try {
      observer.observe({ entryTypes: ['navigation', 'resource', 'paint', 'largest-contentful-paint', 'layout-shift', 'first-input'] })
      this.observers.push(observer)
    } catch (e) {
      console.warn('PerformanceObserver 不支持:', e)
    }
  }

  /**
   * 设置导航计时
   */
  setupNavigationTiming() {
    const navigation = performance.getEntriesByType('navigation')[0]
    if (navigation) {
      this.metrics.set('navigation', navigation)
      this.emitMetric('navigation', navigation)
    }
  }

  /**
   * 设置资源计时
   */
  setupResourceTiming() {
    const resources = performance.getEntriesByType('resource')
    resources.forEach(resource => {
      this.metrics.set(`resource-${resource.name}`, resource)
    })
  }

  /**
   * 设置长任务观察器
   */
  setupLongTaskObserver() {
    if (!('PerformanceObserver' in window)) return

    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        if (entry.duration > 50) { // 超过50ms的任务视为长任务
          this.emitMetric('longtask', entry)
          console.warn('检测到长任务:', entry)
        }
      })
    })

    try {
      observer.observe({ entryTypes: ['longtask'] })
      this.observers.push(observer)
    } catch (e) {
      console.warn('LongTask Observer 不支持:', e)
    }
  }

  /**
   * 处理性能条目
   */
  handlePerformanceEntry(entry) {
    switch (entry.entryType) {
      case 'navigation':
        this.handleNavigationTiming(entry)
        break
      case 'paint':
        this.handlePaintTiming(entry)
        break
      case 'largest-contentful-paint':
        this.handleLCP(entry)
        break
      case 'layout-shift':
        this.handleCLS(entry)
        break
      case 'first-input':
        this.handleFID(entry)
        break
      case 'resource':
        this.handleResourceTiming(entry)
        break
    }
  }

  /**
   * 处理导航计时
   */
  handleNavigationTiming(entry) {
    const metrics = {
      dns: entry.domainLookupEnd - entry.domainLookupStart,
      tcp: entry.connectEnd - entry.connectStart,
      ssl: entry.connectEnd - entry.secureConnectionStart,
      ttfb: entry.responseStart - entry.requestStart,
      download: entry.responseEnd - entry.responseStart,
      domContentLoaded: entry.domContentLoadedEventEnd - entry.navigationStart,
      load: entry.loadEventEnd - entry.navigationStart
    }

    this.metrics.set('navigation-timing', metrics)
    this.emitMetric('navigation-timing', metrics)
  }

  /**
   * 处理绘制计时
   */
  handlePaintTiming(entry) {
    if (entry.name === 'first-paint') {
      this.metrics.set('first-paint', entry.startTime)
      this.emitMetric('first-paint', entry.startTime)
    } else if (entry.name === 'first-contentful-paint') {
      this.metrics.set('first-contentful-paint', entry.startTime)
      this.emitMetric('first-contentful-paint', entry.startTime)
    }
  }

  /**
   * 处理最大内容绘制
   */
  handleLCP(entry) {
    this.metrics.set('largest-contentful-paint', entry.startTime)
    this.emitMetric('largest-contentful-paint', entry.startTime)
  }

  /**
   * 处理累积布局偏移
   */
  handleCLS(entry) {
    const currentCLS = this.metrics.get('cumulative-layout-shift') || 0
    const newCLS = currentCLS + entry.value
    this.metrics.set('cumulative-layout-shift', newCLS)
    this.emitMetric('cumulative-layout-shift', newCLS)
  }

  /**
   * 处理首次输入延迟
   */
  handleFID(entry) {
    this.metrics.set('first-input-delay', entry.processingStart - entry.startTime)
    this.emitMetric('first-input-delay', entry.processingStart - entry.startTime)
  }

  /**
   * 处理资源计时
   */
  handleResourceTiming(entry) {
    const resourceMetrics = {
      name: entry.name,
      duration: entry.duration,
      size: entry.encodedBodySize || 0,
      type: entry.initiatorType
    }

    this.metrics.set(`resource-${entry.name}`, resourceMetrics)
    this.emitMetric('resource', resourceMetrics)
  }

  /**
   * 发射指标事件
   */
  emitMetric(name, data) {
    window.dispatchEvent(new CustomEvent('performance-metric', {
      detail: { name, data }
    }))
  }

  /**
   * 获取性能报告
   */
  getReport() {
    const report = {}
    this.metrics.forEach((value, key) => {
      report[key] = value
    })
    return report
  }

  /**
   * 发送性能数据到服务器
   */
  sendToAnalytics(endpoint = '/api/performance/metrics') {
    const report = this.getReport()
    
    // 使用 navigator.sendBeacon 发送数据
    if (navigator.sendBeacon) {
      const data = new Blob([JSON.stringify(report)], { type: 'application/json' })
      navigator.sendBeacon(endpoint, data)
    } else {
      // 降级方案：使用 fetch
      fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(report),
        headers: { 'Content-Type': 'application/json' },
        keepalive: true
      }).catch(console.error)
    }
  }
}

/**
 * 性能优化建议
 */
export class PerformanceOptimizer {
  /**
   * 分析性能瓶颈
   */
  static analyzeBottlenecks(metrics) {
    const suggestions = []

    // 分析导航时间
    if (metrics['navigation-timing']) {
      const nav = metrics['navigation-timing']
      
      if (nav.dns > 100) {
        suggestions.push('DNS查询时间过长，考虑使用DNS预解析')
      }
      
      if (nav.ttfb > 500) {
        suggestions.push('首字节时间过长，优化服务器响应时间')
      }
      
      if (nav.download > 1000) {
        suggestions.push('资源下载时间过长，考虑压缩资源或使用CDN')
      }
    }

    // 分析资源加载
    const resources = Object.keys(metrics).filter(key => key.startsWith('resource-'))
    resources.forEach(key => {
      const resource = metrics[key]
      if (resource.duration > 1000) {
        suggestions.push(`资源 ${resource.name} 加载过慢，考虑优化`)
      }
    })

    return suggestions
  }

  /**
   * 获取优化建议
   */
  static getOptimizationSuggestions(metrics) {
    const suggestions = []

    // Core Web Vitals 建议
    if (metrics['largest-contentful-paint'] > 2500) {
      suggestions.push('LCP超过2.5秒，优化关键资源加载')
    }

    if (metrics['cumulative-layout-shift'] > 0.1) {
      suggestions.push('CLS过高，确保元素有固定尺寸')
    }

    if (metrics['first-input-delay'] > 100) {
      suggestions.push('FID过高，优化JavaScript执行')
    }

    // 资源优化建议
    const largeResources = Object.keys(metrics)
      .filter(key => key.startsWith('resource-'))
      .map(key => metrics[key])
      .filter(resource => resource.size > 100000) // 大于100KB的资源

    largeResources.forEach(resource => {
      suggestions.push(`资源 ${resource.name} 过大(${Math.round(resource.size / 1024)}KB)，考虑压缩`)
    })

    return suggestions
  }
}

/**
 * 内存监控
 */
export class MemoryMonitor {
  constructor() {
    this.memoryUsage = []
    this.maxEntries = 100
  }

  /**
   * 记录内存使用情况
   */
  recordMemoryUsage() {
    if (!('memory' in performance)) return

    const memory = performance.memory
    const usage = {
      timestamp: Date.now(),
      used: memory.usedJSHeapSize,
      total: memory.totalJSHeapSize,
      limit: memory.jsHeapSizeLimit
    }

    this.memoryUsage.push(usage)
    
    // 保持最大记录数
    if (this.memoryUsage.length > this.maxEntries) {
      this.memoryUsage.shift()
    }

    // 检查内存泄漏
    this.checkMemoryLeak()
  }

  /**
   * 检查内存泄漏
   */
  checkMemoryLeak() {
    if (this.memoryUsage.length < 10) return

    const recent = this.memoryUsage.slice(-10)
    const avgUsage = recent.reduce((sum, entry) => sum + entry.used, 0) / recent.length
    
    // 如果平均使用量持续增长，可能存在内存泄漏
    if (avgUsage > this.memoryUsage[0].used * 1.5) {
      console.warn('检测到可能的内存泄漏')
      this.emitMemoryWarning()
    }
  }

  /**
   * 发射内存警告
   */
  emitMemoryWarning() {
    window.dispatchEvent(new CustomEvent('memory-warning', {
      detail: { usage: this.memoryUsage }
    }))
  }

  /**
   * 开始内存监控
   */
  start() {
    this.interval = setInterval(() => {
      this.recordMemoryUsage()
    }, 5000) // 每5秒记录一次
  }

  /**
   * 停止内存监控
   */
  stop() {
    if (this.interval) {
      clearInterval(this.interval)
    }
  }
}

/**
 * 性能工具函数
 */

/**
 * 节流函数
 */
export const throttle = (func, delay) => {
  let timeoutId
  let lastExecTime = 0
  
  return function (...args) {
    const currentTime = Date.now()
    
    if (currentTime - lastExecTime > delay) {
      func.apply(this, args)
      lastExecTime = currentTime
    } else {
      clearTimeout(timeoutId)
      timeoutId = setTimeout(() => {
        func.apply(this, args)
        lastExecTime = Date.now()
      }, delay - (currentTime - lastExecTime))
    }
  }
}

/**
 * 防抖函数
 */
export const debounce = (func, delay) => {
  let timeoutId
  
  return function (...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      func.apply(this, args)
    }, delay)
  }
}

/**
 * 测量函数执行时间
 */
export const measureExecutionTime = (func, label = 'Function') => {
  return function (...args) {
    const start = performance.now()
    const result = func.apply(this, args)
    const end = performance.now()
    
    console.log(`${label} 执行时间: ${(end - start).toFixed(2)}ms`)
    return result
  }
}

/**
 * 初始化性能监控
 */
export const initPerformanceMonitoring = () => {
  const monitor = new PerformanceMonitor()
  const memoryMonitor = new MemoryMonitor()
  
  monitor.start()
  memoryMonitor.start()
  
  // 页面卸载前发送性能数据
  window.addEventListener('beforeunload', () => {
    monitor.sendToAnalytics()
  })
  
  return {
    monitor,
    memoryMonitor,
    stop: () => {
      monitor.stop()
      memoryMonitor.stop()
    }
  }
}

export default {
  PerformanceMonitor,
  PerformanceOptimizer,
  MemoryMonitor,
  throttle,
  debounce,
  measureExecutionTime,
  initPerformanceMonitoring
}