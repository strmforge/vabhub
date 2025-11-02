import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import i18n from './plugins/i18n'
import 'virtual:uno.css'
import 'nprogress/nprogress.css'
import './styles/main.scss'

// 创建应用实例
const app = createApp(App)

// 配置 Pinia 状态管理
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// 注册插件
app.use(pinia)
app.use(router)
app.use(i18n)

// 挂载应用
app.mount('#app')