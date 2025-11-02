// 懒加载工具函数

/**
 * 图片懒加载
 * @param {string} selector - 图片选择器
 */
export const lazyLoadImages = (selector = 'img[data-src]') => {
  const images = document.querySelectorAll(selector)
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target
        img.src = img.dataset.src
        img.removeAttribute('data-src')
        imageObserver.unobserve(img)
      }
    })
  })

  images.forEach(img => imageObserver.observe(img))
}

/**
 * 组件懒加载
 * @param {Function} importFn - 组件导入函数
 * @returns {Promise} 组件Promise
 */
export const lazyLoadComponent = (importFn) => {
  return new Promise((resolve, reject) => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          importFn()
            .then(resolve)
            .catch(reject)
          observer.disconnect()
        }
      })
    })

    // 创建一个占位元素来触发观察
    const placeholder = document.createElement('div')
    placeholder.style.height = '1px'
    document.body.appendChild(placeholder)
    observer.observe(placeholder)
  })
}

/**
 * 预加载关键资源
 */
export const preloadCriticalResources = () => {
  const criticalResources = [
    '/src/styles/ui-components.css',
    '/src/styles/dark-theme.css'
  ]

  criticalResources.forEach(resource => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.href = resource
    link.as = 'style'
    document.head.appendChild(link)
  })
}

/**
 * 初始化懒加载
 */
export const initLazyLoading = () => {
  // 预加载关键资源
  preloadCriticalResources()
  
  // 监听DOM变化，动态懒加载新图片
  const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      if (mutation.type === 'childList') {
        lazyLoadImages()
      }
    })
  })

  observer.observe(document.body, {
    childList: true,
    subtree: true
  })

  // 初始加载现有图片
  lazyLoadImages()
}