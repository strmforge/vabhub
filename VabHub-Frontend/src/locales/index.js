import { createI18n } from 'vue-i18n'
import zhCN from './zh-CN.json'
import enUS from './en-US.json'

// 可用语言列表
export const availableLocales = [
  { code: 'zh-CN', name: '简体中文' },
  { code: 'en-US', name: 'English' }
]

// 默认语言
const defaultLocale = 'zh-CN'

// 获取浏览器语言设置
const getBrowserLocale = () => {
  const browserLang = navigator.language || navigator.userLanguage
  return availableLocales.find(locale => locale.code === browserLang) ? browserLang : defaultLocale
}

// 创建 i18n 实例
const i18n = createI18n({
  legacy: false,
  locale: getBrowserLocale(),
  fallbackLocale: defaultLocale,
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
        weekday: 'long',
        hour: 'numeric',
        minute: 'numeric'
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
        weekday: 'long',
        hour: 'numeric',
        minute: 'numeric'
      }
    }
  },
  numberFormats: {
    'zh-CN': {
      currency: {
        style: 'currency',
        currency: 'CNY',
        notation: 'standard'
      },
      decimal: {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      },
      percent: {
        style: 'percent',
        useGrouping: false
      }
    },
    'en-US': {
      currency: {
        style: 'currency',
        currency: 'USD',
        notation: 'standard'
      },
      decimal: {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      },
      percent: {
        style: 'percent',
        useGrouping: false
      }
    }
  }
})

// 切换语言
export const changeLocale = (locale) => {
  i18n.global.locale.value = locale
  localStorage.setItem('vabhub-locale', locale)
}

// 获取当前语言
export const getCurrentLocale = () => {
  return i18n.global.locale.value
}

// 初始化语言设置
export const initLocale = () => {
  const savedLocale = localStorage.getItem('vabhub-locale')
  if (savedLocale && availableLocales.find(locale => locale.code === savedLocale)) {
    i18n.global.locale.value = savedLocale
  }
}

export default i18n