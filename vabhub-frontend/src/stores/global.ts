import { defineStore } from 'pinia'
import { ref } from 'vue'

interface GlobalSettings {
  language: string
  theme: string
  autoUpdate: boolean
  notifications: boolean
  privacyMode: boolean
  performanceMode: 'balanced' | 'performance' | 'battery'
}

export const useGlobalSettingsStore = defineStore('globalSettings', () => {
  // 状态
  const settings = ref<GlobalSettings>({
    language: 'zh-CN',
    theme: 'light',
    autoUpdate: true,
    notifications: true,
    privacyMode: false,
    performanceMode: 'balanced'
  })

  const isInitialized = ref(false)
  const isLoading = ref(false)

  // 动作
  const initialize = async (): Promise<void> => {
    if (isInitialized.value || isLoading.value) {
      return
    }

    isLoading.value = true
    
    try {
      // 从localStorage加载设置
      const savedSettings = localStorage.getItem('global-settings')
      if (savedSettings) {
        const parsedSettings = JSON.parse(savedSettings)
        settings.value = { ...settings.value, ...parsedSettings }
      }

      // 应用设置
      applySettings()
      
      isInitialized.value = true
    } catch (error) {
      console.error('Failed to initialize global settings:', error)
    } finally {
      isLoading.value = false
    }
  }

  const updateSettings = (newSettings: Partial<GlobalSettings>): void => {
    settings.value = { ...settings.value, ...newSettings }
    
    // 保存到localStorage
    localStorage.setItem('global-settings', JSON.stringify(settings.value))
    
    // 应用更新后的设置
    applySettings()
  }

  const applySettings = (): void => {
    // 应用主题
    document.documentElement.setAttribute('data-theme', settings.value.theme)
    
    // 应用语言
    document.documentElement.lang = settings.value.language
    
    // 应用性能模式
    applyPerformanceMode(settings.value.performanceMode)
  }

  const applyPerformanceMode = (mode: 'balanced' | 'performance' | 'battery'): void => {
    // 移除现有的性能模式类
    document.body.classList.remove('performance-mode-balanced', 'performance-mode-performance', 'performance-mode-battery')
    
    // 添加新的性能模式类
    document.body.classList.add(`performance-mode-${mode}`)
    
    // 根据性能模式调整动画和视觉效果
    switch (mode) {
      case 'performance':
        // 禁用部分动画以提升性能
        document.body.style.setProperty('--animation-duration', '0.1s')
        break
      case 'battery':
        // 进一步减少动画和视觉效果
        document.body.style.setProperty('--animation-duration', '0.05s')
        document.body.style.setProperty('--blur-intensity', '2px')
        break
      default:
        // 平衡模式使用默认值
        document.body.style.removeProperty('--animation-duration')
        document.body.style.removeProperty('--blur-intensity')
    }
  }

  const resetToDefaults = (): void => {
    const defaultSettings: GlobalSettings = {
      language: 'zh-CN',
      theme: 'light',
      autoUpdate: true,
      notifications: true,
      privacyMode: false,
      performanceMode: 'balanced'
    }
    
    settings.value = defaultSettings
    localStorage.setItem('global-settings', JSON.stringify(defaultSettings))
    applySettings()
  }

  // 获取特定设置
  const getSetting = <K extends keyof GlobalSettings>(key: K): GlobalSettings[K] => {
    return settings.value[key]
  }

  return {
    // 状态
    settings,
    isInitialized,
    isLoading,
    
    // 动作
    initialize,
    updateSettings,
    resetToDefaults,
    getSetting
  }
})