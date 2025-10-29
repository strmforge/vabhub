// UI组件库入口文件

// 导入所有UI组件
import ModernButton from './ModernButton.vue'
import ModernInput from './ModernInput.vue'
import ModernLayout from './ModernLayout.vue'
import ModernCard from './ModernCard.vue'
import LoadingSpinner from './LoadingSpinner.vue'
import ThemeToggle from './ThemeToggle.vue'
import ModernNavigation from './ModernNavigation.vue'
import InteractiveFeedback from './InteractiveFeedback.vue'
import ErrorBoundary from './ErrorBoundary.vue'

// 组件列表
export {
  ModernButton,
  ModernInput,
  ModernLayout,
  ModernCard,
  LoadingSpinner,
  ThemeToggle,
  ModernNavigation,
  InteractiveFeedback,
  ErrorBoundary
}

// 默认导出（用于插件安装）
const components = {
  ModernButton,
  ModernInput,
  ModernLayout,
  ModernCard,
  LoadingSpinner,
  ThemeToggle,
  ModernNavigation,
  InteractiveFeedback,
  ErrorBoundary
}

// 安装函数
export function install(app) {
  Object.keys(components).forEach(key => {
    app.component(key, components[key])
  })
}

// 默认导出（用于Vue.use()）
export default {
  install,
  ...components
}

// 类型定义导出（用于TypeScript）
export * from './types.js'

// 工具函数导出
export * from './utils.js'