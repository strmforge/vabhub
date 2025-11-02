import { createI18n } from 'vue-i18n'
import { DEFAULT_LANGUAGE, LANGUAGE_STORAGE_KEY, SupportedLocale, SUPPORTED_LANGUAGES } from '@/types/i18n'
import zhCN from '@/locales/zh-CN.json'
import enUS from '@/locales/en-US.json'

// 创建 i18n 实例
export const i18n = createI18n({
  legacy: false,
  locale: getStoredLanguage(),
  fallbackLocale: DEFAULT_LANGUAGE,
  messages: {
    'zh-CN': zhCN,
    'en-US': enUS
  },
  datetimeFormats: {
    'zh-CN': {
      short: {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      },
      long: {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      }
    },
    'en-US': {
      short: {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      },
      long: {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      }
    }
  },
  numberFormats: {
    'zh-CN': {
      currency: {
        style: 'currency',
        currency: 'CNY',
        currencyDisplay: 'symbol'
      }
    },
    'en-US': {
      currency: {
        style: 'currency',
        currency: 'USD',
        currencyDisplay: 'symbol'
      }
    }
  }
})

// 获取存储的语言设置
export function getStoredLanguage(): SupportedLocale {
  const stored = localStorage.getItem(LANGUAGE_STORAGE_KEY)
  return (stored as SupportedLocale) || getBrowserLocale()
}

// 获取浏览器语言
export function getBrowserLocale(): SupportedLocale {
  const browserLang = navigator.language || (navigator as any).userLanguage
  
  // 检查是否支持浏览器语言
  const supported = SUPPORTED_LANGUAGES.find(lang => 
    browserLang.startsWith(lang.code)
  )
  
  return supported ? supported.code : DEFAULT_LANGUAGE
}

// 设置语言
export function setI18nLanguage(locale: SupportedLocale): void {
  i18n.global.locale.value = locale
  localStorage.setItem(LANGUAGE_STORAGE_KEY, locale)
  
  // 更新 HTML lang 属性
  document.documentElement.lang = locale
}

// 切换语言
export function toggleLanguage(): SupportedLocale {
  const current = i18n.global.locale.value as SupportedLocale
  const nextIndex = (SUPPORTED_LANGUAGES.findIndex(lang => lang.code === current) + 1) % SUPPORTED_LANGUAGES.length
  const nextLang = SUPPORTED_LANGUAGES[nextIndex].code
  
  setI18nLanguage(nextLang)
  return nextLang
}

// 获取当前语言配置
export function getCurrentLanguageConfig() {
  const current = i18n.global.locale.value as SupportedLocale
  return SUPPORTED_LANGUAGES.find(lang => lang.code === current)
}

// 翻译函数（简化版）
export function t(key: string, params?: Record<string, any>): string {
  return i18n.global.t(key, params)
}

// 格式化日期
export function formatDate(date: Date, formatType: 'short' | 'long' = 'short'): string {
  return i18n.global.d(date, formatType)
}

// 格式化数字
export function formatNumber(value: number, formatType: 'currency' = 'currency'): string {
  return i18n.global.n(value, formatType)
}

export default i18n