/**
 * 核心工具函数
 */

/**
 * 检查用户偏好的颜色方案是否为深色模式
 * @returns 是否为深色模式
 */
export function checkPrefersColorSchemeIsDark(): boolean {
  if (typeof window === 'undefined') {
    return false
  }
  
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
}

/**
 * 检查用户偏好的颜色方案是否为浅色模式
 * @returns 是否为浅色模式
 */
export function checkPrefersColorSchemeIsLight(): boolean {
  if (typeof window === 'undefined') {
    return true
  }
  
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches
}

/**
 * 获取用户偏好的颜色方案
 * @returns 'dark' | 'light' | 'no-preference'
 */
export function getPreferredColorScheme(): 'dark' | 'light' | 'no-preference' {
  if (typeof window === 'undefined') {
    return 'no-preference'
  }
  
  if (window.matchMedia) {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark'
    }
    if (window.matchMedia('(prefers-color-scheme: light)').matches) {
      return 'light'
    }
  }
  
  return 'no-preference'
}

/**
 * 监听颜色方案变化
 * @param callback 回调函数
 * @returns 取消监听函数
 */
export function watchColorScheme(callback: (scheme: 'dark' | 'light') => void): () => void {
  if (typeof window === 'undefined' || !window.matchMedia) {
    return () => {}
  }
  
  const darkMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  const lightMediaQuery = window.matchMedia('(prefers-color-scheme: light)')
  
  const handleChange = () => {
    if (darkMediaQuery.matches) {
      callback('dark')
    } else if (lightMediaQuery.matches) {
      callback('light')
    }
  }
  
  darkMediaQuery.addEventListener('change', handleChange)
  lightMediaQuery.addEventListener('change', handleChange)
  
  return () => {
    darkMediaQuery.removeEventListener('change', handleChange)
    lightMediaQuery.removeEventListener('change', handleChange)
  }
}

/**
 * 防抖函数
 * @param func 要防抖的函数
 * @param wait 等待时间
 * @returns 防抖后的函数
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null
  
  return (...args: Parameters<T>) => {
    if (timeoutId) {
      clearTimeout(timeoutId)
    }
    
    timeoutId = setTimeout(() => {
      func.apply(null, args)
    }, wait)
  }
}

/**
 * 节流函数
 * @param func 要节流的函数
 * @param limit 时间限制
 * @returns 节流后的函数
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean = false
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func.apply(null, args)
      inThrottle = true
      setTimeout(() => {
        inThrottle = false
      }, limit)
    }
  }
}

/**
 * 深度克隆对象
 * @param obj 要克隆的对象
 * @returns 克隆后的对象
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime()) as unknown as T
  }
  
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item)) as unknown as T
  }
  
  if (obj instanceof Object) {
    const cloned = {} as T
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        cloned[key] = deepClone(obj[key])
      }
    }
    return cloned
  }
  
  return obj
}

/**
 * 生成唯一ID
 * @param prefix 前缀
 * @returns 唯一ID
 */
export function generateId(prefix: string = 'id'): string {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

/**
 * 格式化文件大小
 * @param bytes 字节数
 * @returns 格式化后的文件大小
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 检查是否为移动设备
 * @returns 是否为移动设备
 */
export function isMobileDevice(): boolean {
  if (typeof window === 'undefined') {
    return false
  }
  
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  )
}

/**
 * 检查是否为触摸设备
 * @returns 是否为触摸设备
 */
export function isTouchDevice(): boolean {
  if (typeof window === 'undefined') {
    return false
  }
  
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0
}

/**
 * 获取浏览器信息
 * @returns 浏览器信息
 */
export function getBrowserInfo(): {
  name: string
  version: string
  os: string
  isMobile: boolean
} {
  if (typeof window === 'undefined') {
    return {
      name: 'Unknown',
      version: 'Unknown',
      os: 'Unknown',
      isMobile: false
    }
  }
  
  const ua = navigator.userAgent
  let name = 'Unknown'
  let version = 'Unknown'
  let os = 'Unknown'
  
  // 检测浏览器
  if (ua.indexOf('Firefox') > -1) {
    name = 'Firefox'
    version = ua.match(/Firefox\/([0-9.]+)/)?.[1] || 'Unknown'
  } else if (ua.indexOf('Chrome') > -1) {
    name = 'Chrome'
    version = ua.match(/Chrome\/([0-9.]+)/)?.[1] || 'Unknown'
  } else if (ua.indexOf('Safari') > -1) {
    name = 'Safari'
    version = ua.match(/Version\/([0-9.]+)/)?.[1] || 'Unknown'
  } else if (ua.indexOf('Edge') > -1) {
    name = 'Edge'
    version = ua.match(/Edge\/([0-9.]+)/)?.[1] || 'Unknown'
  }
  
  // 检测操作系统
  if (ua.indexOf('Win') > -1) os = 'Windows'
  else if (ua.indexOf('Mac') > -1) os = 'macOS'
  else if (ua.indexOf('Linux') > -1) os = 'Linux'
  else if (ua.indexOf('Android') > -1) os = 'Android'
  else if (ua.indexOf('iOS') > -1 || ua.indexOf('iPhone') > -1) os = 'iOS'
  
  return {
    name,
    version,
    os,
    isMobile: isMobileDevice()
  }
}