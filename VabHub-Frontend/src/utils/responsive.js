/**
 * 响应式工具函数
 * 提供设备检测、屏幕适配、触摸优化等功能
 */

// 设备类型检测
const DeviceType = {
  MOBILE: 'mobile',
  TABLET: 'tablet',
  DESKTOP: 'desktop'
}

// 屏幕断点配置
const BREAKPOINTS = {
  mobile: 768,
  tablet: 1024,
  desktop: 1200
}

/**
 * 检测设备类型
 * @returns {string} 设备类型
 */
export const detectDeviceType = () => {
  const width = window.innerWidth
  
  if (width < BREAKPOINTS.mobile) {
    return DeviceType.MOBILE
  } else if (width < BREAKPOINTS.tablet) {
    return DeviceType.TABLET
  } else {
    return DeviceType.DESKTOP
  }
}

/**
 * 检测是否为移动设备
 * @returns {boolean}
 */
export const isMobile = () => {
  return detectDeviceType() === DeviceType.MOBILE
}

/**
 * 检测是否为平板设备
 * @returns {boolean}
 */
export const isTablet = () => {
  return detectDeviceType() === DeviceType.TABLET
}

/**
 * 检测是否为桌面设备
 * @returns {boolean}
 */
export const isDesktop = () => {
  return detectDeviceType() === DeviceType.DESKTOP
}

/**
 * 检测触摸设备
 * @returns {boolean}
 */
export const isTouchDevice = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0
}

/**
 * 检测iOS设备
 * @returns {boolean}
 */
export const isIOS = () => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream
}

/**
 * 检测Android设备
 * @returns {boolean}
 */
export const isAndroid = () => {
  return /Android/.test(navigator.userAgent)
}

/**
 * 获取安全区域信息
 * @returns {Object}
 */
export const getSafeArea = () => {
  return {
    top: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-top') || '0'),
    bottom: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-bottom') || '0'),
    left: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-left') || '0'),
    right: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-right') || '0')
  }
}

/**
 * 响应式图片尺寸计算
 * @param {number} baseSize 基础尺寸
 * @param {Object} options 配置选项
 * @returns {number}
 */
export const responsiveImageSize = (baseSize, options = {}) => {
  const deviceType = detectDeviceType()
  const { mobileRatio = 0.8, tabletRatio = 0.9, desktopRatio = 1 } = options
  
  switch (deviceType) {
    case DeviceType.MOBILE:
      return Math.round(baseSize * mobileRatio)
    case DeviceType.TABLET:
      return Math.round(baseSize * tabletRatio)
    default:
      return Math.round(baseSize * desktopRatio)
  }
}

/**
 * 响应式字体大小计算
 * @param {number} baseSize 基础字体大小
 * @param {Object} options 配置选项
 * @returns {string}
 */
export const responsiveFontSize = (baseSize, options = {}) => {
  const deviceType = detectDeviceType()
  const { mobileRatio = 0.85, tabletRatio = 0.95, desktopRatio = 1 } = options
  
  let size = baseSize
  
  switch (deviceType) {
    case DeviceType.MOBILE:
      size = baseSize * mobileRatio
      break
    case DeviceType.TABLET:
      size = baseSize * tabletRatio
      break
    default:
      size = baseSize * desktopRatio
  }
  
  return `clamp(${Math.round(size * 0.8)}px, ${size}px, ${Math.round(size * 1.2)}px)`
}

/**
 * 响应式间距计算
 * @param {number} baseSpacing 基础间距
 * @param {Object} options 配置选项
 * @returns {number}
 */
export const responsiveSpacing = (baseSpacing, options = {}) => {
  const deviceType = detectDeviceType()
  const { mobileRatio = 0.7, tabletRatio = 0.85, desktopRatio = 1 } = options
  
  switch (deviceType) {
    case DeviceType.MOBILE:
      return Math.round(baseSpacing * mobileRatio)
    case DeviceType.TABLET:
      return Math.round(baseSpacing * tabletRatio)
    default:
      return Math.round(baseSpacing * desktopRatio)
  }
}

/**
 * 响应式网格列数计算
 * @param {number} baseColumns 基础列数
 * @param {Object} options 配置选项
 * @returns {number}
 */
export const responsiveGridColumns = (baseColumns, options = {}) => {
  const deviceType = detectDeviceType()
  const { mobileColumns = 1, tabletColumns = 2, desktopColumns = baseColumns } = options
  
  switch (deviceType) {
    case DeviceType.MOBILE:
      return mobileColumns
    case DeviceType.TABLET:
      return tabletColumns
    default:
      return desktopColumns
  }
}

/**
 * 防抖函数，用于窗口大小变化监听
 * @param {Function} func 要执行的函数
 * @param {number} wait 等待时间
 * @returns {Function}
 */
export const debounce = (func, wait = 250) => {
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
 * 监听窗口大小变化
 * @param {Function} callback 回调函数
 * @param {number} debounceWait 防抖等待时间
 * @returns {Function} 取消监听函数
 */
export const onWindowResize = (callback, debounceWait = 250) => {
  const debouncedCallback = debounce(callback, debounceWait)
  window.addEventListener('resize', debouncedCallback)
  
  return () => {
    window.removeEventListener('resize', debouncedCallback)
  }
}

/**
 * 响应式Vue组合式函数
 * @returns {Object}
 */
export const useResponsive = () => {
  const deviceType = ref(detectDeviceType())
  const isMobileDevice = ref(isMobile())
  const isTabletDevice = ref(isTablet())
  const isDesktopDevice = ref(isDesktop())
  const isTouch = ref(isTouchDevice())
  
  const updateDeviceInfo = () => {
    deviceType.value = detectDeviceType()
    isMobileDevice.value = isMobile()
    isTabletDevice.value = isTablet()
    isDesktopDevice.value = isDesktop()
    isTouch.value = isTouchDevice()
  }
  
  onMounted(() => {
    const cleanup = onWindowResize(updateDeviceInfo)
    onUnmounted(cleanup)
  })
  
  return {
    deviceType: readonly(deviceType),
    isMobile: readonly(isMobileDevice),
    isTablet: readonly(isTabletDevice),
    isDesktop: readonly(isDesktopDevice),
    isTouch: readonly(isTouch)
  }
}

/**
 * 响应式图片加载优化
 * @param {string} src 图片源
 * @param {Object} options 配置选项
 * @returns {Promise}
 */
export const loadResponsiveImage = (src, options = {}) => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    
    img.onload = () => resolve(img)
    img.onerror = reject
    
    // 根据设备类型选择合适尺寸的图片
    const deviceType = detectDeviceType()
    const { mobileSuffix = '_mobile', tabletSuffix = '_tablet', desktopSuffix = '' } = options
    
    let finalSrc = src
    
    switch (deviceType) {
      case DeviceType.MOBILE:
        finalSrc = src.replace(/(\.[^.]+)$/, mobileSuffix + '$1')
        break
      case DeviceType.TABLET:
        finalSrc = src.replace(/(\.[^.]+)$/, tabletSuffix + '$1')
        break
      default:
        finalSrc = src.replace(/(\.[^.]+)$/, desktopSuffix + '$1')
    }
    
    img.src = finalSrc
  })
}

export default {
  DeviceType,
  BREAKPOINTS,
  detectDeviceType,
  isMobile,
  isTablet,
  isDesktop,
  isTouchDevice,
  isIOS,
  isAndroid,
  getSafeArea,
  responsiveImageSize,
  responsiveFontSize,
  responsiveSpacing,
  responsiveGridColumns,
  debounce,
  onWindowResize,
  useResponsive,
  loadResponsiveImage
}