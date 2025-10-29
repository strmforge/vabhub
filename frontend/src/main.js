import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'

// 导入现代化UI样式
import '@/styles/design-system.css'
import '@/styles/animations.css'
import '@/styles/accessibility.css'

// 导入Element Plus图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用插件
app.use(store)
app.use(router)
app.use(ElementPlus)

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue错误:', err)
  console.error('组件:', vm)
  console.error('信息:', info)
  
  // 在实际应用中，这里可以发送错误报告到服务器
  // 或者显示用户友好的错误信息
}

// 全局属性
app.config.globalProperties.$filters = {
  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  },
  
  formatTime(seconds) {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = Math.floor(seconds % 60)
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  },
  
  truncateText(text, length = 50) {
    if (text.length <= length) return text
    return text.substring(0, length) + '...'
  }
}

// 全局指令
app.directive('focus', {
  mounted(el) {
    el.focus()
  }
})

app.directive('click-outside', {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
})

// 挂载应用
app.mount('#app')

// 初始化主题
const initTheme = () => {
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme)
  } else {
    document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light')
  }
}

// 监听系统主题变化
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (!localStorage.getItem('theme')) {
    document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light')
  }
})

// 初始化
initTheme()

console.log('🚀 VabHub 现代化UI已启动')