// 现代化UI工具函数

/**
 * 生成唯一ID
 * @param {string} prefix - ID前缀
 * @returns {string} 唯一ID
 */
export const generateId = (prefix = 'modern') => {
  return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {number} wait - 等待时间
 * @returns {Function} 防抖后的函数
 */
export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {number} limit - 限制时间
 * @returns {Function} 节流后的函数
 */
export const throttle = (func, limit) => {
  let inThrottle
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

/**
 * 深拷贝对象
 * @param {any} obj - 要拷贝的对象
 * @returns {any} 深拷贝后的对象
 */
export const deepClone = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime())
  if (obj instanceof Array) return obj.map(item => deepClone(item))
  if (typeof obj === 'object') {
    const clonedObj = {}
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj
  }
}

/**
 * 格式化文件大小
 * @param {number} bytes - 字节数
 * @returns {string} 格式化后的文件大小
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 格式化时间
 * @param {number} seconds - 秒数
 * @returns {string} 格式化后的时间
 */
export const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

/**
 * 截断文本
 * @param {string} text - 要截断的文本
 * @param {number} length - 最大长度
 * @returns {string} 截断后的文本
 */
export const truncateText = (text, length = 50) => {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

/**
 * 生成随机颜色
 * @returns {string} 随机颜色值
 */
export const generateRandomColor = () => {
  const colors = [
    '#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6',
    '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1'
  ]
  return colors[Math.floor(Math.random() * colors.length)]
}

/**
 * 检查元素是否在视口中
 * @param {Element} element - 要检查的元素
 * @returns {boolean} 是否在视口中
 */
export const isElementInViewport = (element) => {
  const rect = element.getBoundingClientRect()
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  )
}

/**
 * 平滑滚动到元素
 * @param {Element} element - 要滚动到的元素
 * @param {Object} options - 滚动选项
 */
export const smoothScrollToElement = (element, options = {}) => {
  const {
    behavior = 'smooth',
    block = 'start',
    inline = 'nearest'
  } = options
  
  element.scrollIntoView({
    behavior,
    block,
    inline
  })
}

/**
 * 复制文本到剪贴板
 * @param {string} text - 要复制的文本
 * @returns {Promise<boolean>} 是否复制成功
 */
export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (err) {
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = text
    document.body.appendChild(textArea)
    textArea.select()
    const result = document.execCommand('copy')
    document.body.removeChild(textArea)
    return result
  }
}

/**
 * 获取CSS变量值
 * @param {string} variableName - CSS变量名
 * @returns {string} CSS变量值
 */
export const getCssVariable = (variableName) => {
  return getComputedStyle(document.documentElement).getPropertyValue(variableName)
}

/**
 * 设置CSS变量值
 * @param {string} variableName - CSS变量名
 * @param {string} value - CSS变量值
 */
export const setCssVariable = (variableName, value) => {
  document.documentElement.style.setProperty(variableName, value)
}

/**
 * 检测设备类型
 * @returns {string} 设备类型
 */
export const detectDeviceType = () => {
  const ua = navigator.userAgent
  if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
    return 'tablet'
  }
  if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
    return 'mobile'
  }
  return 'desktop'
}

/**
 * 检测触摸设备
 * @returns {boolean} 是否是触摸设备
 */
export const isTouchDevice = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0
}

/**
 * 生成渐变背景
 * @param {string[]} colors - 颜色数组
 * @param {string} direction - 渐变方向
 * @returns {string} 渐变CSS值
 */
export const generateGradient = (colors, direction = 'to right') => {
  const gradientColors = colors.join(', ')
  return `linear-gradient(${direction}, ${gradientColors})`
}

/**
 * 添加CSS动画
 * @param {Element} element - 要添加动画的元素
 * @param {string} animationName - 动画名称
 * @param {number} duration - 动画时长
 */
export const addAnimation = (element, animationName, duration = 1000) => {
  element.style.animation = `${animationName} ${duration}ms ease-in-out`
  
  // 动画结束后移除样式
  const handleAnimationEnd = () => {
    element.style.animation = ''
    element.removeEventListener('animationend', handleAnimationEnd)
  }
  
  element.addEventListener('animationend', handleAnimationEnd)
}

/**
 * 验证邮箱格式
 * @param {string} email - 邮箱地址
 * @returns {boolean} 是否有效
 */
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * 验证URL格式
 * @param {string} url - URL地址
 * @returns {boolean} 是否有效
 */
export const validateUrl = (url) => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * 生成数据图表颜色
 * @param {number} index - 数据索引
 * @returns {string} 图表颜色
 */
export const getChartColor = (index) => {
  const colors = [
    '#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6',
    '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1'
  ]
  return colors[index % colors.length]
}

/**
 * 格式化数字
 * @param {number} num - 要格式化的数字
 * @param {number} decimals - 小数位数
 * @returns {string} 格式化后的数字
 */
export const formatNumber = (num, decimals = 0) => {
  return num.toLocaleString(undefined, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  })
}

/**
 * 计算百分比
 * @param {number} value - 当前值
 * @param {number} total - 总值
 * @returns {number} 百分比
 */
export const calculatePercentage = (value, total) => {
  if (total === 0) return 0
  return Math.round((value / total) * 100)
}

/**
 * 生成UUID
 * @returns {string} UUID
 */
export const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

/**
 * 检测浏览器支持的特性
 * @returns {Object} 支持的特性
 */
export const detectBrowserFeatures = () => {
  return {
    cssGrid: 'grid' in document.documentElement.style,
    flexbox: 'flex' in document.documentElement.style,
    webp: (() => {
      const canvas = document.createElement('canvas')
      if (canvas.getContext && canvas.getContext('2d')) {
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0
      }
      return false
    })(),
    serviceWorker: 'serviceWorker' in navigator,
    pushManager: 'PushManager' in window
  }
}