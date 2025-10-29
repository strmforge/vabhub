<template>
  <nav :class="navClasses">
    <!-- 桌面端导航 -->
    <div v-if="!isMobile" class="modern-nav__desktop">
      <div class="modern-nav__container">
        <!-- 品牌标识 -->
        <div class="modern-nav__brand">
          <router-link to="/" class="modern-nav__brand-link">
            <div class="modern-nav__logo">
              <slot name="logo">
                <el-icon class="modern-nav__logo-icon">
                  <VideoCamera />
                </el-icon>
              </slot>
            </div>
            <span class="modern-nav__brand-text">{{ brandName }}</span>
          </router-link>
        </div>

        <!-- 主导航 -->
        <div class="modern-nav__menu">
          <div class="modern-nav__menu-items">
            <router-link
              v-for="item in navigationItems"
              :key="item.path"
              :to="item.path"
              :class="navItemClasses(item)"
            >
              <el-icon class="modern-nav__item-icon">
                <component :is="item.icon" />
              </el-icon>
              <span class="modern-nav__item-text">{{ item.name }}</span>
              <span v-if="item.badge" class="modern-nav__item-badge">{{ item.badge }}</span>
            </router-link>
          </div>
        </div>

        <!-- 导航操作 -->
        <div class="modern-nav__actions">
          <!-- 搜索按钮 -->
          <button
            v-if="showSearch"
            class="modern-nav__action-btn"
            @click="$emit('search')"
            aria-label="搜索"
          >
            <el-icon><Search /></el-icon>
          </button>

          <!-- 主题切换 -->
          <button
            class="modern-nav__action-btn"
            @click="toggleTheme"
            :aria-label="isDarkMode ? '切换到亮色主题' : '切换到深色主题'"
          >
            <el-icon v-if="isDarkMode"><Sunny /></el-icon>
            <el-icon v-else><Moon /></el-icon>
          </button>

          <!-- 用户菜单 -->
          <div v-if="showUserMenu" class="modern-nav__user-menu">
            <el-dropdown trigger="click" placement="bottom-end">
              <button class="modern-nav__user-btn">
                <el-avatar :size="32" :src="userAvatar" />
                <el-icon class="modern-nav__user-arrow"><ArrowDown /></el-icon>
              </button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="$emit('profile')">
                    <el-icon><User /></el-icon>
                    个人资料
                  </el-dropdown-item>
                  <el-dropdown-item @click="$emit('settings')">
                    <el-icon><Setting /></el-icon>
                    设置
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="$emit('logout')">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>

          <!-- 登录按钮 -->
          <button
            v-else-if="showLogin"
            class="modern-nav__login-btn"
            @click="$emit('login')"
          >
            登录
          </button>
        </div>
      </div>
    </div>

    <!-- 移动端导航 -->
    <div v-else class="modern-nav__mobile">
      <div class="modern-nav__mobile-header">
        <!-- 汉堡菜单 -->
        <button
          class="modern-nav__mobile-toggle"
          @click="mobileMenuOpen = !mobileMenuOpen"
          :aria-expanded="mobileMenuOpen"
          aria-label="切换菜单"
        >
          <span class="modern-nav__mobile-toggle-bar"></span>
          <span class="modern-nav__mobile-toggle-bar"></span>
          <span class="modern-nav__mobile-toggle-bar"></span>
        </button>

        <!-- 品牌标识 -->
        <div class="modern-nav__mobile-brand">
          <router-link to="/" class="modern-nav__mobile-brand-link">
            <div class="modern-nav__mobile-logo">
              <slot name="logo">
                <el-icon class="modern-nav__mobile-logo-icon">
                  <VideoCamera />
                </el-icon>
              </slot>
            </div>
            <span class="modern-nav__mobile-brand-text">{{ brandName }}</span>
          </router-link>
        </div>

        <!-- 移动端操作 -->
        <div class="modern-nav__mobile-actions">
          <button
            v-if="showSearch"
            class="modern-nav__mobile-action-btn"
            @click="$emit('search')"
            aria-label="搜索"
          >
            <el-icon><Search /></el-icon>
          </button>
        </div>
      </div>

      <!-- 移动端菜单 -->
      <transition name="slide-down">
        <div v-if="mobileMenuOpen" class="modern-nav__mobile-menu">
          <div class="modern-nav__mobile-menu-content">
            <!-- 导航项 -->
            <div class="modern-nav__mobile-items">
              <router-link
                v-for="item in navigationItems"
                :key="item.path"
                :to="item.path"
                :class="navItemClasses(item)"
                @click="mobileMenuOpen = false"
              >
                <el-icon class="modern-nav__mobile-item-icon">
                  <component :is="item.icon" />
                </el-icon>
                <span class="modern-nav__mobile-item-text">{{ item.name }}</span>
                <span v-if="item.badge" class="modern-nav__mobile-item-badge">{{ item.badge }}</span>
              </router-link>
            </div>

            <!-- 移动端底部操作 -->
            <div class="modern-nav__mobile-footer">
              <!-- 主题切换 -->
              <button
                class="modern-nav__mobile-theme-btn"
                @click="toggleTheme"
              >
                <el-icon v-if="isDarkMode"><Sunny /></el-icon>
                <el-icon v-else><Moon /></el-icon>
                <span>{{ isDarkMode ? '亮色主题' : '深色主题' }}</span>
              </button>

              <!-- 用户相关 -->
              <div v-if="showUserMenu" class="modern-nav__mobile-user">
                <div class="modern-nav__mobile-user-info">
                  <el-avatar :size="40" :src="userAvatar" />
                  <div class="modern-nav__mobile-user-details">
                    <span class="modern-nav__mobile-user-name">{{ userName }}</span>
                    <span class="modern-nav__mobile-user-email">{{ userEmail }}</span>
                  </div>
                </div>
                <div class="modern-nav__mobile-user-actions">
                  <button @click="$emit('profile'); mobileMenuOpen = false">
                    <el-icon><User /></el-icon>
                    个人资料
                  </button>
                  <button @click="$emit('settings'); mobileMenuOpen = false">
                    <el-icon><Setting /></el-icon>
                    设置
                  </button>
                  <button @click="$emit('logout'); mobileMenuOpen = false">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </button>
                </div>
              </div>

              <button
                v-else-if="showLogin"
                class="modern-nav__mobile-login-btn"
                @click="$emit('login'); mobileMenuOpen = false"
              >
                登录
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 移动端菜单遮罩 -->
    <transition name="fade">
      <div
        v-if="mobileMenuOpen && isMobile"
        class="modern-nav__mobile-overlay"
        @click="mobileMenuOpen = false"
      ></div>
    </transition>
  </nav>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  VideoCamera,
  Search,
  Sunny,
  Moon,
  ArrowDown,
  User,
  Setting,
  SwitchButton,
  House,
  Compass,
  Collection
} from '@element-plus/icons-vue'

export default {
  name: 'ModernNavigation',
  components: {
    VideoCamera,
    Search,
    Sunny,
    Moon,
    ArrowDown,
    User,
    Setting,
    SwitchButton,
    House,
    Compass,
    Collection
  },
  props: {
    brandName: {
      type: String,
      default: 'VabHub'
    },
    navigationItems: {
      type: Array,
      default: () => [
        { path: '/', name: '首页', icon: House },
        { path: '/discover', name: '发现', icon: Compass },
        { path: '/library', name: '媒体库', icon: Collection }
      ]
    },
    showSearch: {
      type: Boolean,
      default: true
    },
    showUserMenu: {
      type: Boolean,
      default: false
    },
    showLogin: {
      type: Boolean,
      default: true
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
  setup(props) {
    const route = useRoute()
    const isMobile = ref(false)
    const isDarkMode = ref(false)
    const mobileMenuOpen = ref(false)

    // 检测移动端
    const checkMobile = () => {
      isMobile.value = window.innerWidth <= 768
      if (!isMobile.value) {
        mobileMenuOpen.value = false
      }
    }

    // 切换主题
    const toggleTheme = () => {
      isDarkMode.value = !isDarkMode.value
      document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light')
      localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
    }

    // 初始化主题
    const initTheme = () => {
      const savedTheme = localStorage.getItem('theme') || 'light'
      isDarkMode.value = savedTheme === 'dark'
      document.documentElement.setAttribute('data-theme', savedTheme)
    }

    // 导航项类名
    const navItemClasses = (item) => ({
      'modern-nav__item': true,
      'modern-nav__item--active': route.path === item.path,
      'modern-nav__item--mobile': isMobile.value
    })

    // 导航类名
    const navClasses = computed(() => ({
      'modern-nav': true,
      'modern-nav--mobile': isMobile.value,
      'modern-nav--scrolled': false, // 可以添加滚动检测
      'modern-nav--dark': isDarkMode.value
    }))

    onMounted(() => {
      checkMobile()
      initTheme()
      window.addEventListener('resize', checkMobile)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkMobile)
    })

    return {
      isMobile,
      isDarkMode,
      mobileMenuOpen,
      navClasses,
      navItemClasses,
      toggleTheme
    }
  }
}
</script>

<style scoped>
.modern-nav {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  backdrop-filter: blur(10px);
  transition: all var(--transition-normal);
}

/* 桌面端导航 */
.modern-nav__desktop {
  padding: 0 var(--space-4);
}

.modern-nav__container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

/* 品牌标识 */
.modern-nav__brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text-primary);
  gap: var(--space-3);
}

.modern-nav__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  border-radius: var(--radius-md);
  color: white;
}

.modern-nav__logo-icon {
  font-size: 1.25rem;
}

.modern-nav__brand-text {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 主导航菜单 */
.modern-nav__menu {
  flex: 1;
  display: flex;
  justify-content: center;
}

.modern-nav__menu-items {
  display: flex;
  gap: var(--space-1);
  background: var(--bg-tertiary);
  border-radius: var(--radius-lg);
  padding: var(--space-1);
}

.modern-nav__item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  text-decoration: none;
  color: var(--text-secondary);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  font-weight: var(--font-weight-medium);
  position: relative;
}

.modern-nav__item:hover {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

.modern-nav__item--active {
  color: var(--primary-600);
  background: var(--bg-secondary);
  box-shadow: var(--shadow-sm);
}

.modern-nav__item-icon {
  font-size: 1.1rem;
}

.modern-nav__item-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--error-500);
  color: white;
  font-size: var(--font-size-xs);
  padding: 2px 6px;
  border-radius: var(--radius-full);
  min-width: 18px;
  text-align: center;
  line-height: 1;
}

/* 导航操作 */
.modern-nav__actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.modern-nav__action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.modern-nav__action-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.modern-nav__user-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.modern-nav__user-btn:hover {
  background: var(--bg-tertiary);
}

.modern-nav__user-arrow {
  font-size: 0.875rem;
  color: var(--text-tertiary);
}

.modern-nav__login-btn {
  padding: var(--space-2) var(--space-4);
  background: var(--primary-600);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.modern-nav__login-btn:hover {
  background: var(--primary-700);
  transform: translateY(-1px);
}

/* 移动端导航 */
.modern-nav__mobile {
  position: relative;
}

.modern-nav__mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-4);
  height: 56px;
}

.modern-nav__mobile-toggle {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: var(--space-2);
}

.modern-nav__mobile-toggle-bar {
  width: 20px;
  height: 2px;
  background: var(--text-primary);
  transition: all var(--transition-fast);
  border-radius: 1px;
}

.modern-nav__mobile-toggle[aria-expanded="true"] .modern-nav__mobile-toggle-bar:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.modern-nav__mobile-toggle[aria-expanded="true"] .modern-nav__mobile-toggle-bar:nth-child(2) {
  opacity: 0;
}

.modern-nav__mobile-toggle[aria-expanded="true"] .modern-nav__mobile-toggle-bar:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -6px);
}

.modern-nav__mobile-brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text-primary);
  gap: var(--space-2);
}

.modern-nav__mobile-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  border-radius: var(--radius-md);
  color: white;
}

.modern-nav__mobile-brand-text {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
}

.modern-nav__mobile-actions {
  display: flex;
  gap: var(--space-2);
}

.modern-nav__mobile-action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: var(--radius-md);
  cursor: pointer;
}

/* 移动端菜单 */
.modern-nav__mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  max-height: calc(100vh - 56px);
  overflow-y: auto;
}

.modern-nav__mobile-menu-content {
  padding: var(--space-4);
}

.modern-nav__mobile-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  margin-bottom: var(--space-6);
}

.modern-nav__mobile-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  text-decoration: none;
  color: var(--text-secondary);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  font-weight: var(--font-weight-medium);
}

.modern-nav__mobile-item:hover,
.modern-nav__mobile-item--active {
  color: var(--primary-600);
  background: var(--bg-tertiary);
}

.modern-nav__mobile-item-badge {
  margin-left: auto;
  background: var(--error-500);
  color: white;
  font-size: var(--font-size-xs);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  min-width: 20px;
  text-align: center;
}

/* 移动端底部 */
.modern-nav__mobile-footer {
  border-top: 1px solid var(--border-primary);
  padding-top: var(--space-4);
}

.modern-nav__mobile-theme-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.modern-nav__mobile-theme-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.modern-nav__mobile-user {
  margin-top: var(--space-4);
}

.modern-nav__mobile-user-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
}

.modern-nav__mobile-user-details {
  display: flex;
  flex-direction: column;
}

.modern-nav__mobile-user-name {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.modern-nav__mobile-user-email {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.modern-nav__mobile-user-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  margin-top: var(--space-2);
}

.modern-nav__mobile-user-actions button {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-4);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.modern-nav__mobile-user-actions button:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.modern-nav__mobile-login-btn {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: var(--primary-600);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.modern-nav__mobile-login-btn:hover {
  background: var(--primary-700);
}

/* 移动端遮罩 */
.modern-nav__mobile-overlay {
  position: fixed;
  top: 56px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-nav__desktop {
    display: none;
  }
}

@media (min-width: 769px) {
  .modern-nav__mobile {
    display: none;
  }
}

/* 深色主题适配 */
[data-theme="dark"] .modern-nav {
  background: rgba(17, 24, 39, 0.8);
  border-bottom-color: var(--border-secondary);
}

/* 无障碍访问 */
.modern-nav__item:focus-visible,
.modern-nav__action-btn:focus-visible,
.modern-nav__mobile-toggle:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .modern-nav,
  .modern-nav__item,
  .modern-nav__action-btn,
  .modern-nav__mobile-toggle-bar,
  .modern-nav__mobile-item {
    transition: none;
  }
  
  .modern-nav__mobile-toggle[aria-expanded="true"] .modern-nav__mobile-toggle-bar {
    transform: none;
  }
}
</style>