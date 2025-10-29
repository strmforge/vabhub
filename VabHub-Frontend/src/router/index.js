import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/media',
    name: 'Media',
    component: () => import('@/views/Media.vue'),
    meta: { title: '媒体库' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { title: '设置' }
  },
  {
    path: '/plugins',
    name: 'Plugins',
    component: () => import('@/views/Plugins.vue'),
    meta: { title: '插件管理' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/SearchPage.vue'),
    meta: { title: '搜索' }
  },
  {
    path: '/search-test',
    name: 'SearchTest',
    component: () => import('@/views/SearchTest.vue'),
    meta: { title: '搜索功能测试' }
  },
  {
    path: '/discover',
    name: 'Discover',
    component: () => import('@/views/DiscoverPage.vue'),
    meta: { title: '发现推荐' }
  },
  
  // 现代化UI路由
  {
    path: '/modern',
    name: 'ModernHome',
    component: () => import('@/views/ModernHome.vue'),
    meta: { title: 'VabHub - 现代化界面' }
  },
  {
    path: '/modern/discover',
    name: 'ModernDiscover',
    component: () => import('@/views/ModernDiscover.vue'),
    meta: { title: '发现 - VabHub' }
  },
  {
    path: '/modern/library',
    name: 'ModernLibrary',
    component: () => import('@/views/ModernLibrary.vue'),
    meta: { title: '媒体库 - VabHub' }
  },
  {
    path: '/modern/settings',
    name: 'ModernSettings',
    component: () => import('@/views/ModernSettings.vue'),
    meta: { title: '设置 - VabHub' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - VabHub`
  }
  
  // 检查认证状态
  const token = localStorage.getItem('token')
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router