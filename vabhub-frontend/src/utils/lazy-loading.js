/**
 * 懒加载工具函数
 * 提供组件懒加载、图片懒加载等功能
 */

import { onMounted, onUnmounted, ref } from 'vue'

/**
 * 组件懒加载
 * @param {Function} importFn - 导入函数
 * @param {Object} options - 配置选项
 * @returns {Promise}
 */
export const lazyLoadComponent = (importFn, options = {}) => {
  const {
    loadingComponent = null,
    errorComponent = null,
    delay = 200,
    timeout = 10000
  } = options

  return () => ({
    component: importFn(),
    loading: loadingComponent,
    error: errorComponent,
    delay,
    timeout
  })
}

/**
 * 图片懒加载指令
 */
export const vLazyLoad = {
  mounted(el, binding) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target
          img.src = binding.value
          observer.unobserve(img)
        }
      })
    }, {
      rootMargin: '0px',
      threshold: 0.1
    })

    observer.observe(el)
    el._lazyLoadObserver = observer
  },
  
  unmounted(el) {
    if (el._lazyLoadObserver) {
      el._lazyLoadObserver.unobserve(el)
      el._lazyLoadObserver = null
    }
  }
}

/**
 * 使用Intersection Observer实现懒加载
 * @param {HTMLElement} element - 要观察的元素
 * @param {Function} callback - 回调函数
 * @param {Object} options - 观察器选项
 */
export const useIntersectionObserver = (element, callback, options = {}) => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        callback(entry)
      }
    })
  }, {
    root: null,
    rootMargin: '0px',
    threshold: 0.1,
    ...options
  })

  if (element.value) {
    observer.observe(element.value)
  }

  return {
    disconnect: () => observer.disconnect(),
    unobserve: (el) => observer.unobserve(el)
  }
}

/**
 * 图片预加载
 * @param {string} src - 图片URL
 * @returns {Promise}
 */
export const preloadImage = (src) => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = reject
    img.src = src
  })
}

/**
 * 批量预加载图片
 * @param {string[]} urls - 图片URL数组
 * @returns {Promise}
 */
export const preloadImages = (urls) => {
  return Promise.all(urls.map(url => preloadImage(url)))
}

/**
 * 组件懒加载组合式函数
 * @param {Function} importFn - 导入函数
 * @param {Object} options - 配置选项
 */
export const useLazyComponent = (importFn, options = {}) => {
  const component = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const loadComponent = async () => {
    if (component.value || loading.value) return

    loading.value = true
    error.value = null

    try {
      const module = await importFn()
      component.value = module.default || module
    } catch (err) {
      error.value = err
      console.error('组件懒加载失败:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    component,
    loading,
    error,
    loadComponent
  }
}

/**
 * 路由预加载
 * @param {string} routeName - 路由名称
 */
export const preloadRoute = (routeName) => {
  const router = window.__VUE_APP_ROUTER__
  if (!router) return

  const route = router.getRoutes().find(r => r.name === routeName)
  if (route && route.components) {
    // 预加载路由组件
    Object.values(route.components).forEach(component => {
      if (typeof component === 'function') {
        component().catch(() => {}) // 静默处理错误
      }
    })
  }
}

/**
 * 关键资源预加载
 */
export const preloadCriticalResources = () => {
  // 预加载关键CSS
  const criticalStyles = [
    '/css/element-plus.css',
    '/css/app.css'
  ]

  criticalStyles.forEach(href => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.as = 'style'
    link.href = href
    document.head.appendChild(link)
  })

  // 预加载关键字体
  const criticalFonts = [
    '/fonts/inter-var.woff2'
  ]

  criticalFonts.forEach(href => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.as = 'font'
    link.type = 'font/woff2'
    link.crossOrigin = 'anonymous'
    link.href = href
    document.head.appendChild(link)
  })
}

/**
 * 延迟加载非关键资源
 */
export const loadNonCriticalResources = () => {
  // 延迟加载非关键CSS
  const nonCriticalStyles = [
    '/css/third-party.css'
  ]

  nonCriticalStyles.forEach(href => {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = href
    link.media = 'print'
    link.onload = () => {
      link.media = 'all'
    }
    document.head.appendChild(link)
  })

  // 延迟加载非关键脚本
  const nonCriticalScripts = [
    '/js/analytics.js'
  ]

  nonCriticalScripts.forEach(src => {
    const script = document.createElement('script')
    script.src = src
    script.async = true
    document.body.appendChild(script)
  })
}

/**
 * 初始化懒加载
 */
export const initLazyLoading = () => {
  // 预加载关键资源
  preloadCriticalResources()

  // 在空闲时间加载非关键资源
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      loadNonCriticalResources()
    })
  } else {
    // 降级方案：延迟加载
    setTimeout(loadNonCriticalResources, 2000)
  }
}

export default {
  lazyLoadComponent,
  vLazyLoad,
  useIntersectionObserver,
  preloadImage,
  preloadImages,
  useLazyComponent,
  preloadRoute,
  preloadCriticalResources,
  loadNonCriticalResources,
  initLazyLoading
}