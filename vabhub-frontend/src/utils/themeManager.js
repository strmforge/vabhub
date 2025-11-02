/**
 * 主题管理器
 * 统一管理应用主题切换和持久化
 */

class ThemeManager {
  constructor() {
    this.currentTheme = 'light'
    this.availableThemes = ['light', 'dark', 'transparent']
    this.themeChangeCallbacks = []
    
    // 初始化主题
    this.initialize()
  }

  /**
   * 初始化主题管理器
   */
  initialize() {
    // 从本地存储加载主题设置
    const savedTheme = localStorage.getItem('theme')
    
    if (savedTheme && this.availableThemes.includes(savedTheme)) {
      this.currentTheme = savedTheme
    } else {
      // 使用系统偏好
      this.currentTheme = this.getSystemPreferredTheme()
    }

    // 应用初始主题
    this.applyTheme(this.currentTheme)
  }

  /**
   * 获取系统偏好主题
   * @returns {string} 系统偏好主题
   */
  getSystemPreferredTheme() {
    if (typeof window !== 'undefined' && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
    return 'light'
  }

  /**
   * 设置主题
   * @param {string} theme 主题名称
   * @returns {Promise<void>}
   */
  async setTheme(theme) {
    if (!this.availableThemes.includes(theme)) {
      console.warn(`不支持的主题: ${theme}`)
      return
    }

    // 保存到本地存储
    localStorage.setItem('theme', theme)
    
    // 应用主题
    this.applyTheme(theme)
    
    // 更新当前主题
    this.currentTheme = theme
    
    // 触发主题变化回调
    this.notifyThemeChange(theme)

    console.log(`主题已切换为: ${theme}`)
  }

  /**
   * 应用主题到页面
   * @param {string} theme 主题名称
   */
  applyTheme(theme) {
    if (typeof document === 'undefined') return

    // 移除所有主题类
    document.documentElement.classList.remove(...this.availableThemes)
    document.body.classList.remove(...this.availableThemes)
    
    // 添加当前主题类
    document.documentElement.classList.add(theme)
    document.body.classList.add(theme)
    
    // 更新data-theme属性
    document.documentElement.setAttribute('data-theme', theme)
    document.body.setAttribute('data-theme', theme)

    // 更新CSS变量
    this.updateCSSVariables(theme)
  }

  /**
   * 更新CSS变量
   * @param {string} theme 主题名称
   */
  updateCSSVariables(theme) {
    const root = document.documentElement
    
    // 根据主题设置CSS变量
    switch (theme) {
      case 'dark':
        root.style.setProperty('--primary-color', '#1976d2')
        root.style.setProperty('--background-color', '#121212')
        root.style.setProperty('--surface-color', '#1e1e1e')
        root.style.setProperty('--text-color', '#ffffff')
        root.style.setProperty('--text-secondary', 'rgba(255, 255, 255, 0.7)')
        break
      
      case 'transparent':
        root.style.setProperty('--primary-color', '#1976d2')
        root.style.setProperty('--background-color', 'transparent')
        root.style.setProperty('--surface-color', 'rgba(30, 30, 30, 0.8)')
        root.style.setProperty('--text-color', '#ffffff')
        root.style.setProperty('--text-secondary', 'rgba(255, 255, 255, 0.7)')
        break
      
      case 'light':
      default:
        root.style.setProperty('--primary-color', '#1976d2')
        root.style.setProperty('--background-color', '#f5f5f5')
        root.style.setProperty('--surface-color', '#ffffff')
        root.style.setProperty('--text-color', '#000000')
        root.style.setProperty('--text-secondary', 'rgba(0, 0, 0, 0.6)')
        break
    }
  }

  /**
   * 获取当前主题
   * @returns {string} 当前主题
   */
  getCurrentTheme() {
    return this.currentTheme
  }

  /**
   * 获取可用主题列表
   * @returns {string[]} 可用主题列表
   */
  getAvailableThemes() {
    return [...this.availableThemes]
  }

  /**
   * 切换主题
   * @returns {Promise<string>} 切换后的主题
   */
  async toggleTheme() {
    const currentIndex = this.availableThemes.indexOf(this.currentTheme)
    const nextIndex = (currentIndex + 1) % this.availableThemes.length
    const nextTheme = this.availableThemes[nextIndex]
    
    await this.setTheme(nextTheme)
    return nextTheme
  }

  /**
   * 监听主题变化
   * @param {Function} callback 回调函数
   * @returns {Function} 取消监听函数
   */
  onThemeChange(callback) {
    this.themeChangeCallbacks.push(callback)
    
    // 返回取消监听函数
    return () => {
      const index = this.themeChangeCallbacks.indexOf(callback)
      if (index > -1) {
        this.themeChangeCallbacks.splice(index, 1)
      }
    }
  }

  /**
   * 通知主题变化
   * @param {string} theme 新主题
   */
  notifyThemeChange(theme) {
    this.themeChangeCallbacks.forEach(callback => {
      try {
        callback(theme)
      } catch (error) {
        console.warn('主题变化回调执行失败:', error)
      }
    })
  }

  /**
   * 检查是否为暗色主题
   * @returns {boolean} 是否为暗色主题
   */
  isDarkTheme() {
    return this.currentTheme === 'dark' || this.currentTheme === 'transparent'
  }

  /**
   * 检查是否为透明主题
   * @returns {boolean} 是否为透明主题
   */
  isTransparentTheme() {
    return this.currentTheme === 'transparent'
  }
}

// 创建全局实例
export const themeManager = new ThemeManager()

export default themeManager