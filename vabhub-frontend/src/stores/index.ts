import { createPinia } from 'pinia'

// 创建 Pinia 实例
export const pinia = createPinia()

// 导出所有 store
export * from './auth'
export * from './app'

// 默认导出
export default pinia