/**
 * Axios 类型扩展
 * 扩展 InternalAxiosRequestConfig 以支持自定义字段
 */
import 'axios'

declare module 'axios' {
  export interface InternalAxiosRequestConfig {
    /** 标记是否已重试（防止无限重试） */
    __retry?: boolean
  }
}
