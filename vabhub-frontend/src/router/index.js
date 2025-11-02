import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 懒加载函数，添加加载状态和错误处理
const lazyLoad = (component) => {
  return () => ({
    component: component(),
    loading: {
      template: '<div class="loading-container"><div class="loading-spinner"></div><p>页面加载中...</p></div>'
    },
    error: {
      template: '<div class="error-container"><p>页面加载失败，请刷新重试</p></div>'
    },
    delay: 200,
    timeout: 10000
  })
}

// 预加载关键页面
const preloadCriticalPages = () => {
  // 预加载登录和仪表板页面
  const criticalPages = [
    () => import('@/pages/Login.vue'),
    () => import('@/pages/Dashboard.vue')
  ]
  
  criticalPages.forEach(load => {
    load().catch(err => console.warn('预加载失败:', err))
  })
}

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: lazyLoad(() => import('@/pages/Login.vue')),
    meta: { 
      requiresGuest: true,
      preload: true // 标记为需要预加载的关键页面
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: lazyLoad(() => import('@/pages/Dashboard.vue')),
    meta: { 
      requiresAuth: true,
      preload: true // 标记为需要预加载的关键页面
    }
  },
  {
    path: '/discover',
    name: 'Discover',
    component: lazyLoad(() => import('@/pages/Discover.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/recommendations',
    name: 'Recommendations',
    component: lazyLoad(() => import('@/pages/Recommendations.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/plugins',
    name: 'Plugins',
    component: lazyLoad(() => import('@/pages/Plugins.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: lazyLoad(() => import('@/pages/Settings.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/storage',
    name: 'Storage',
    component: lazyLoad(() => import('@/pages/Storage.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/logs',
    name: 'Logs',
    component: lazyLoad(() => import('@/pages/Logs.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/subscriptions',
    name: 'Subscriptions',
    component: lazyLoad(() => import('@/pages/SubscriptionManagement.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/site-bundles',
    name: 'SiteBundles',
    component: lazyLoad(() => import('@/pages/SiteBundleManagement.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/music',
    name: 'Music',
    component: lazyLoad(() => import('@/pages/Music.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/microfrontend-demo',
    name: 'MicroFrontendDemo',
    component: lazyLoad(() => import('@/pages/MicroFrontendDemo.vue')),
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: lazyLoad(() => import('@/pages/NotFound.vue'))
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // 滚动行为优化
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 预加载关键页面
  if (to.meta.preload) {
    preloadCriticalPages()
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 尝试检查认证状态
    const isAuthenticated = await authStore.checkAuth()
    if (!isAuthenticated) {
      next('/login')
      return
    }
  }
  
  // 检查是否需要访客状态（如登录页面）
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  next()
})

// 路由后置钩子 - 性能监控
router.afterEach((to, from) => {
  // 记录页面访问
  console.log(`路由跳转: ${from.path} -> ${to.path}`)
  
  // 发送性能指标（可集成到监控系统）
  if (window.performance && window.performance.mark) {
    performance.mark(`route-${to.name}-end`)
    
    // 计算路由切换时间
    const startMark = performance.getEntriesByName(`route-${to.name}-start`)[0]
    const endMark = performance.getEntriesByName(`route-${to.name}-end`)[0]
    
    if (startMark && endMark) {
      const duration = endMark.startTime - startMark.startTime
      console.log(`路由 ${to.name} 加载耗时: ${duration.toFixed(2)}ms`)
    }
  }
})

// 初始化时预加载关键页面
preloadCriticalPages()

export default router