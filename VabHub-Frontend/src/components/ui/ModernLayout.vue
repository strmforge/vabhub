<template>
  <div class="modern-layout" :class="layoutClasses">
    <!-- 顶部导航栏 -->
    <header class="modern-layout__header">
      <div class="modern-layout__header-container">
        <!-- Logo和标题 -->
        <div class="modern-layout__brand">
          <div class="modern-layout__logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <path d="M16 2L22 8L16 14L10 8L16 2Z" fill="var(--primary-600)"/>
              <path d="M2 16L8 22L14 16L8 10L2 16Z" fill="var(--primary-500)"/>
              <path d="M16 30L22 24L16 18L10 24L16 30Z" fill="var(--primary-400)"/>
              <path d="M30 16L24 10L18 16L24 22L30 16Z" fill="var(--primary-300)"/>
            </svg>
          </div>
          <div class="modern-layout__title">
            <h1 class="modern-layout__app-name">VabHub</h1>
            <p class="modern-layout__page-title">{{ pageTitle }}</p>
          </div>
        </div>

        <!-- 搜索框 -->
        <div class="modern-layout__search">
          <div class="modern-layout__search-container">
            <el-icon class="modern-layout__search-icon">
              <Search />
            </el-icon>
            <input
              type="text"
              class="modern-layout__search-input"
              placeholder="搜索媒体、插件..."
              @focus="handleSearchFocus"
              @blur="handleSearchBlur"
              @input="handleSearchInput"
            />
            <div v-if="searchQuery" class="modern-layout__search-clear" @click="clearSearch">
              <el-icon><Close /></el-icon>
            </div>
          </div>
        </div>

        <!-- 用户操作区域 -->
        <div class="modern-layout__actions">
          <!-- 主题切换 -->
          <ThemeToggle class="modern-layout__theme-toggle" />
          
          <!-- 通知 -->
          <div class="modern-layout__notification" @click="handleNotification">
            <el-icon class="modern-layout__notification-icon">
              <Bell />
            </el-icon>
            <span v-if="unreadCount > 0" class="modern-layout__notification-badge">
              {{ unreadCount > 99 ? '99+' : unreadCount }}
            </span>
          </div>

          <!-- 用户菜单 -->
          <div class="modern-layout__user-menu" v-click-outside="closeUserMenu">
            <div class="modern-layout__user-trigger" @click="toggleUserMenu">
              <div class="modern-layout__user-avatar">
                <img v-if="userAvatar" :src="userAvatar" :alt="userName" />
                <el-icon v-else class="modern-layout__user-avatar-placeholder">
                  <User />
                </el-icon>
              </div>
              <span class="modern-layout__user-name">{{ userName }}</span>
              <el-icon class="modern-layout__user-arrow">
                <ArrowDown />
              </el-icon>
            </div>

            <transition name="slide-down">
              <div v-if="showUserMenu" class="modern-layout__user-dropdown">
                <div class="modern-layout__user-info">
                  <div class="modern-layout__user-avatar-large">
                    <img v-if="userAvatar" :src="userAvatar" :alt="userName" />
                    <el-icon v-else class="modern-layout__user-avatar-placeholder-large">
                      <User />
                    </el-icon>
                  </div>
                  <div class="modern-layout__user-details">
                    <div class="modern-layout__user-display-name">{{ userName }}</div>
                    <div class="modern-layout__user-email">{{ userEmail }}</div>
                  </div>
                </div>

                <div class="modern-layout__user-actions">
                  <div class="modern-layout__user-action" @click="handleProfile">
                    <el-icon><User /></el-icon>
                    <span>个人资料</span>
                  </div>
                  <div class="modern-layout__user-action" @click="handleSettings">
                    <el-icon><Setting /></el-icon>
                    <span>设置</span>
                  </div>
                  <div class="modern-layout__user-action" @click="handleHelp">
                    <el-icon><QuestionFilled /></el-icon>
                    <span>帮助中心</span>
                  </div>
                  <div class="modern-layout__user-divider"></div>
                  <div class="modern-layout__user-action modern-layout__user-action--logout" @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>
                    <span>退出登录</span>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </header>

    <!-- 侧边栏 -->
    <aside class="modern-layout__sidebar" :class="{ 'modern-layout__sidebar--collapsed': sidebarCollapsed }">
      <div class="modern-layout__sidebar-container">
        <!-- 侧边栏切换按钮 -->
        <div class="modern-layout__sidebar-toggle" @click="toggleSidebar">
          <el-icon>
            <component :is="sidebarCollapsed ? 'Menu' : 'Fold'" />
          </el-icon>
        </div>

        <!-- 导航菜单 -->
        <nav class="modern-layout__navigation">
          <ul class="modern-layout__nav-list">
            <li v-for="item in navigationItems" :key="item.name" class="modern-layout__nav-item">
              <router-link
                :to="{ name: item.name }"
                class="modern-layout__nav-link"
                :class="{ 
                  'modern-layout__nav-link--active': $route.name === item.name,
                  'modern-layout__nav-link--collapsed': sidebarCollapsed
                }"
                @click="handleNavigation(item)"
              >
                <el-icon class="modern-layout__nav-icon">
                  <component :is="item.icon" />
                </el-icon>
                <span class="modern-layout__nav-label">{{ item.label }}</span>
                <span v-if="item.badge" class="modern-layout__nav-badge">{{ item.badge }}</span>
              </router-link>
            </li>
          </ul>
        </nav>

        <!-- 底部操作 -->
        <div class="modern-layout__sidebar-footer">
          <div class="modern-layout__sidebar-actions">
            <div class="modern-layout__sidebar-action" @click="handleFeedback">
              <el-icon><ChatDotRound /></el-icon>
              <span v-if="!sidebarCollapsed">反馈</span>
            </div>
            <div class="modern-layout__sidebar-action" @click="handleAbout">
              <el-icon><InfoFilled /></el-icon>
              <span v-if="!sidebarCollapsed">关于</span>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 主内容区域 -->
    <main class="modern-layout__main">
      <div class="modern-layout__main-container">
        <!-- 页面标题和操作 -->
        <div class="modern-layout__page-header">
          <div class="modern-layout__page-header-content">
            <h2 class="modern-layout__page-heading">{{ pageTitle }}</h2>
            <p class="modern-layout__page-description" v-if="pageDescription">
              {{ pageDescription }}
            </p>
          </div>
          
          <div class="modern-layout__page-actions" v-if="$slots.actions">
            <slot name="actions"></slot>
          </div>
        </div>

        <!-- 页面内容 -->
        <div class="modern-layout__content">
          <slot></slot>
        </div>
      </div>
    </main>

    <!-- 全局加载状态 -->
    <transition name="fade">
      <div v-if="globalLoading" class="modern-layout__loading-overlay">
        <LoadingSpinner size="large" />
        <p class="modern-layout__loading-text">加载中...</p>
      </div>
    </transition>

    <!-- 全局通知 -->
    <div class="modern-layout__notifications">
      <transition-group name="slide-up">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="modern-layout__notification-item"
          :class="`modern-layout__notification-item--${notification.type}`"
        >
          <div class="modern-layout__notification-content">
            <el-icon class="modern-layout__notification-type-icon">
              <component :is="getNotificationIcon(notification.type)" />
            </el-icon>
            <div class="modern-layout__notification-message">
              <div class="modern-layout__notification-title">{{ notification.title }}</div>
              <div class="modern-layout__notification-description">{{ notification.message }}</div>
            </div>
          </div>
          <button
            class="modern-layout__notification-close"
            @click="removeNotification(notification.id)"
          >
            <el-icon><Close /></el-icon>
          </button>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import ThemeToggle from './ThemeToggle.vue'
import LoadingSpinner from './LoadingSpinner.vue'
import {
  Search,
  Close,
  Bell,
  User,
  ArrowDown,
  Setting,
  QuestionFilled,
  SwitchButton,
  Menu,
  Fold,
  ChatDotRound,
  InfoFilled,
  SuccessFilled,
  WarningFilled,
  CircleCloseFilled
} from '@element-plus/icons-vue'

export default {
  name: 'ModernLayout',
  components: {
    ThemeToggle,
    LoadingSpinner
  },
  props: {
    pageTitle: {
      type: String,
      default: 'VabHub'
    },
    pageDescription: {
      type: String,
      default: ''
    },
    userLoggedIn: {
      type: Boolean,
      default: false
    },
    userAvatar: {
      type: String,
      default: ''
    },
    userName: {
      type: String,
      default: '用户'
    },
    userEmail: {
      type: String,
      default: ''
    }
  },
  emits: ['search', 'profile', 'settings', 'logout', 'login'],
  setup(props, { emit }) {
    const router = useRouter()
    
    // 响应式状态
    const searchQuery = ref('')
    const searchFocused = ref(false)
    const showUserMenu = ref(false)
    const sidebarCollapsed = ref(false)
    const globalLoading = ref(false)
    const unreadCount = ref(3)
    const notifications = ref([])
    
    // 导航项
    const navigationItems = [
      { name: 'ModernHome', label: '首页', icon: 'House' },
      { name: 'ModernDiscover', label: '发现', icon: 'Compass' },
      { name: 'ModernLibrary', label: '媒体库', icon: 'Collection' },
      { name: 'ModernSettings', label: '设置', icon: 'Setting' }
    ]

    // 计算属性
    const layoutClasses = computed(() => ({
      'modern-layout--search-focused': searchFocused.value,
      'modern-layout--sidebar-collapsed': sidebarCollapsed.value,
      'modern-layout--user-menu-open': showUserMenu.value
    }))

    // 方法
    const handleSearchFocus = () => {
      searchFocused.value = true
    }

    const handleSearchBlur = () => {
      searchFocused.value = false
    }

    const handleSearchInput = (event) => {
      searchQuery.value = event.target.value
      emit('search', searchQuery.value)
    }

    const clearSearch = () => {
      searchQuery.value = ''
    }

    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
    }

    const closeUserMenu = () => {
      showUserMenu.value = false
    }

    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
    }

    const handleNotification = () => {
      // 处理通知点击
      console.log('打开通知面板')
    }

    const handleProfile = () => {
      closeUserMenu()
      emit('profile')
    }

    const handleSettings = () => {
      closeUserMenu()
      emit('settings')
      router.push({ name: 'ModernSettings' })
    }

    const handleHelp = () => {
      closeUserMenu()
      console.log('打开帮助中心')
    }

    const handleLogout = () => {
      closeUserMenu()
      emit('logout')
    }

    const handleNavigation = (item) => {
      // 处理导航点击
      console.log('导航到:', item.name)
    }

    const handleFeedback = () => {
      console.log('打开反馈表单')
    }

    const handleAbout = () => {
      console.log('打开关于页面')
    }

    const getNotificationIcon = (type) => {
      const icons = {
        success: 'SuccessFilled',
        warning: 'WarningFilled',
        error: 'CircleCloseFilled',
        info: 'InfoFilled'
      }
      return icons[type] || 'InfoFilled'
    }

    const removeNotification = (id) => {
      notifications.value = notifications.value.filter(n => n.id !== id)
    }

    const addNotification = (notification) => {
      const id = Date.now()
      notifications.value.push({
        id,
        ...notification
      })
      
      // 自动移除通知
      setTimeout(() => {
        removeNotification(id)
      }, 5000)
    }

    // 全局事件监听
    const handleGlobalLoading = (loading) => {
      globalLoading.value = loading
    }

    // 生命周期
    onMounted(() => {
      // 监听全局事件
      window.addEventListener('global-loading', (event) => {
        handleGlobalLoading(event.detail.loading)
      })
      
      // 添加示例通知
      addNotification({
        type: 'info',
        title: '欢迎使用 VabHub',
        message: '现代化媒体管理平台已准备就绪'
      })
    })

    onUnmounted(() => {
      window.removeEventListener('global-loading', handleGlobalLoading)
    })

    return {
      searchQuery,
      searchFocused,
      showUserMenu,
      sidebarCollapsed,
      globalLoading,
      unreadCount,
      notifications,
      navigationItems,
      layoutClasses,
      handleSearchFocus,
      handleSearchBlur,
      handleSearchInput,
      clearSearch,
      toggleUserMenu,
      closeUserMenu,
      toggleSidebar,
      handleNotification,
      handleProfile,
      handleSettings,
      handleHelp,
      handleLogout,
      handleNavigation,
      handleFeedback,
      handleAbout,
      getNotificationIcon,
      removeNotification
    }
  }
}
</script>

<style scoped>
.modern-layout {
  min-height: 100vh;
  display: grid;
  grid-template-areas: 
    "header header"
    "sidebar main";
  grid-template-columns: auto 1fr;
  grid-template-rows: auto 1fr;
  background: var(--bg-primary);
  transition: all 0.3s ease;
}

/* 头部样式 */
.modern-layout__header {
  grid-area: header;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.modern-layout__header-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.modern-layout__brand {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  min-width: 280px;
}

.modern-layout__logo {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modern-layout__title {
  display: flex;
  flex-direction: column;
}

.modern-layout__app-name {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0;
  line-height: 1.2;
}

.modern-layout__page-title {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.2;
}

.modern-layout__search {
  flex: 1;
  max-width: 480px;
  margin: 0 var(--space-8);
}

.modern-layout__search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.modern-layout__search-icon {
  position: absolute;
  left: var(--space-3);
  color: var(--text-tertiary);
  font-size: 1.25rem;
  z-index: 1;
}

.modern-layout__search-input {
  width: 100%;
  height: 40px;
  padding: 0 var(--space-3) 0 40px;
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.modern-layout__search-input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px var(--primary-100);
}

.modern-layout__search-clear {
  position: absolute;
  right: var(--space-3);
  color: var(--text-tertiary);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.modern-layout__search-clear:hover {
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

.modern-layout__actions {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  min-width: 280px;
  justify-content: flex-end;
}

.modern-layout__theme-toggle {
  margin-right: var(--space-2);
}

.modern-layout__notification {
  position: relative;
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.modern-layout__notification:hover {
  background: var(--bg-tertiary);
}

.modern-layout__notification-icon {
  font-size: 1.25rem;
  color: var(--text-secondary);
}

.modern-layout__notification-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: var(--danger-500);
  color: white;
  font-size: var(--font-size-xs);
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
  line-height: 1;
}

.modern-layout__user-menu {
  position: relative;
}

.modern-layout__user-trigger {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.2s ease;
}

.modern-layout__user-trigger:hover {
  background: var(--bg-tertiary);
}

.modern-layout__user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.modern-layout__user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modern-layout__user-avatar-placeholder {
  font-size: 1.25rem;
  color: var(--text-tertiary);
}

.modern-layout__user-name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.modern-layout__user-arrow {
  color: var(--text-tertiary);
  transition: transform 0.2s ease;
}

.modern-layout--user-menu-open .modern-layout__user-arrow {
  transform: rotate(180deg);
}

.modern-layout__user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 280px;
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  margin-top: var(--space-2);
  overflow: hidden;
  z-index: 1001;
}

.modern-layout__user-info {
  padding: var(--space-6);
  border-bottom: 1px solid var(--border-primary);
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.modern-layout__user-avatar-large {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.modern-layout__user-avatar-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modern-layout__user-avatar-placeholder-large {
  font-size: 1.5rem;
  color: var(--text-tertiary);
}

.modern-layout__user-details {
  flex: 1;
}

.modern-layout__user-display-name {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.modern-layout__user-email {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.modern-layout__user-actions {
  padding: var(--space-2);
}

.modern-layout__user-action {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-primary);
}

.modern-layout__user-action:hover {
  background: var(--bg-tertiary);
}

.modern-layout__user-action--logout {
  color: var(--danger-600);
}

.modern-layout__user-action--logout:hover {
  background: var(--danger-50);
}

.modern-layout__user-divider {
  height: 1px;
  background: var(--border-primary);
  margin: var(--space-2) 0;
}

/* 侧边栏样式 */
.modern-layout__sidebar {
  grid-area: sidebar;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-primary);
  transition: width 0.3s ease;
  width: 280px;
  position: sticky;
  top: 64px;
  height: calc(100vh - 64px);
  overflow-y: auto;
}

.modern-layout__sidebar--collapsed {
  width: 64px;
}

.modern-layout__sidebar-container {
  padding: var(--space-4);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.modern-layout__sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  cursor: pointer;
  margin-bottom: var(--space-4);
  transition: all 0.2s ease;
  color: var(--text-secondary);
}

.modern-layout__sidebar-toggle:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.modern-layout__navigation {
  flex: 1;
}

.modern-layout__nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.modern-layout__nav-item {
  margin-bottom: var(--space-1);
}

.modern-layout__nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: var(--text-secondary);
  transition: all 0.2s ease;
  position: relative;
}

.modern-layout__nav-link:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.modern-layout__nav-link--active {
  background: var(--primary-50);
  color: var(--primary-600);
  font-weight: var(--font-weight-medium);
}

.modern-layout__nav-link--collapsed {
  justify-content: center;
  padding: var(--space-3);
}

.modern-layout__nav-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.modern-layout__nav-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: opacity 0.3s ease;
}

.modern-layout__sidebar--collapsed .modern-layout__nav-label {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

.modern-layout__nav-badge {
  background: var(--danger-500);
  color: white;
  font-size: var(--font-size-xs);
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: auto;
}

.modern-layout__sidebar-footer {
  margin-top: auto;
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-primary);
}

.modern-layout__sidebar-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.modern-layout__sidebar-action {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
}

.modern-layout__sidebar-action:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.modern-layout__sidebar--collapsed .modern-layout__sidebar-action {
  justify-content: center;
  padding: var(--space-3);
}

.modern-layout__sidebar-action span {
  font-size: var(--font-size-sm);
  transition: opacity 0.3s ease;
}

.modern-layout__sidebar--collapsed .modern-layout__sidebar-action span {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

/* 主内容区域 */
.modern-layout__main {
  grid-area: main;
  background: var(--bg-primary);
  overflow-y: auto;
}

.modern-layout__main-container {
  max-width: 100%;
  margin: 0 auto;
  padding: var(--space-8);
  min-height: calc(100vh - 64px);
}

.modern-layout__page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-8);
}

.modern-layout__page-header-content {
  flex: 1;
}

.modern-layout__page-heading {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0 0 var(--space-2) 0;
}

.modern-layout__page-description {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin: 0;
}

.modern-layout__page-actions {
  display: flex;
  gap: var(--space-3);
  align-items: center;
}

.modern-layout__content {
  min-height: 400px;
}

/* 加载状态 */
.modern-layout__loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modern-layout__loading-text {
  color: white;
  margin-top: var(--space-4);
  font-size: var(--font-size-lg);
}

/* 通知样式 */
.modern-layout__notifications {
  position: fixed;
  top: var(--space-8);
  right: var(--space-8);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.modern-layout__notification-item {
  min-width: 320px;
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  padding: var(--space-4);
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
}

.modern-layout__notification-item--success {
  border-left: 4px solid var(--success-500);
}

.modern-layout__notification-item--warning {
  border-left: 4px solid var(--warning-500);
}

.modern-layout__notification-item--error {
  border-left: 4px solid var(--danger-500);
}

.modern-layout__notification-item--info {
  border-left: 4px solid var(--primary-500);
}

.modern-layout__notification-content {
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
}

.modern-layout__notification-type-icon {
  font-size: 1.25rem;
  margin-top: 2px;
  flex-shrink: 0;
}

.modern-layout__notification-item--success .modern-layout__notification-type-icon {
  color: var(--success-500);
}

.modern-layout__notification-item--warning .modern-layout__notification-type-icon {
  color: var(--warning-500);
}

.modern-layout__notification-item--error .modern-layout__notification-type-icon {
  color: var(--danger-500);
}

.modern-layout__notification-item--info .modern-layout__notification-type-icon {
  color: var(--primary-500);
}

.modern-layout__notification-message {
  flex: 1;
}

.modern-layout__notification-title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.modern-layout__notification-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.modern-layout__notification-close {
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.modern-layout__notification-close:hover {
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .modern-layout__sidebar {
    position: fixed;
    top: 64px;
    left: 0;
    z-index: 999;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .modern-layout__sidebar--mobile-open {
    transform: translateX(0);
  }
  
  .modern-layout__main {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .modern-layout__header-container {
    padding: 0 var(--space-4);
  }
  
  .modern-layout__brand {
    min-width: auto;
  }
  
  .modern-layout__page-title {
    display: none;
  }
  
  .modern-layout__search {
    margin: 0 var(--space-4);
    max-width: 200px;
  }
  
  .modern-layout__actions {
    min-width: auto;
  }
  
  .modern-layout__user-name {
    display: none;
  }
  
  .modern-layout__main-container {
    padding: var(--space-6);
  }
  
  .modern-layout__page-header {
    flex-direction: column;
    gap: var(--space-4);
  }
  
  .modern-layout__notifications {
    right: var(--space-4);
    left: var(--space-4);
  }
  
  .modern-layout__notification-item {
    min-width: auto;
    width: 100%;
  }
}

/* 动画 */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>