// 现代化UI路由配置
import { createRouter, createWebHistory } from 'vue-router'
import ModernHome from '@/views/ModernHome.vue'

const routes = [
  {
    path: '/modern',
    name: 'ModernHome',
    component: ModernHome,
    meta: {
      title: 'VabHub - 现代化界面',
      description: '体验最新的UI设计语言和交互技术'
    }
  },
  {
    path: '/modern/discover',
    name: 'ModernDiscover',
    component: () => import('@/views/ModernDiscover.vue'),
    meta: {
      title: '发现 - VabHub',
      description: '探索丰富的媒体内容'
    }
  },
  {
    path: '/modern/library',
    name: 'ModernLibrary',
    component: () => import('@/views/ModernLibrary.vue'),
    meta: {
      title: '媒体库 - VabHub',
      description: '管理您的媒体收藏'
    }
  },
  {
    path: '/modern/settings',
    name: 'ModernSettings',
    component: () => import('@/views/ModernSettings.vue'),
    meta: {
      title: '设置 - VabHub',
      description: '个性化您的使用体验'
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 平滑滚动到顶部
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// 路由守卫 - 页面标题设置
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // 设置页面描述
  if (to.meta.description) {
    const metaDescription = document.querySelector('meta[name="description"]')
    if (metaDescription) {
      metaDescription.setAttribute('content', to.meta.description)
    }
  }
  
  next()
})

// 路由守卫 - 无障碍访问增强
router.afterEach((to, from) => {
  // 延迟执行以确保DOM已更新
  setTimeout(() => {
    // 聚焦到主要内容区域
    const mainContent = document.querySelector('main')
    if (mainContent && !to.meta.noFocus) {
      mainContent.setAttribute('tabindex', '-1')
      mainContent.focus()
    }
    
    // 发送路由变化事件（用于屏幕阅读器）
    const routeChangeEvent = new CustomEvent('routeChange', {
      detail: { 
        to: to.path, 
        from: from.path,
        title: to.meta.title || document.title
      }
    })
    window.dispatchEvent(routeChangeEvent)
  }, 100)
})

export default router