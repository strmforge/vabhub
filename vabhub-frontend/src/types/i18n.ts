// 支持的语言类型
export type SupportedLocale = 'zh-CN' | 'en-US'

// 语言配置接口
export interface LanguageConfig {
  code: SupportedLocale
  name: string
  nativeName: string
  flag: string
}

// 语言包接口
export interface I18nMessages {
  [key: string]: string | I18nMessages
}

// 语言配置列表
export const SUPPORTED_LANGUAGES: LanguageConfig[] = [
  {
    code: 'zh-CN',
    name: 'Chinese',
    nativeName: '中文',
    flag: '🇨🇳'
  },
  {
    code: 'en-US',
    name: 'English',
    nativeName: 'English',
    flag: '🇺🇸'
  }
]

// 默认语言
export const DEFAULT_LANGUAGE: SupportedLocale = 'zh-CN'

// 语言存储键
export const LANGUAGE_STORAGE_KEY = 'vabhub-language'