<template>
  <!-- 移动端导航栏 -->
  <nav class="mobile-nav" :class="{ 'nav-open': isMenuOpen }">
    <!-- 顶部导航栏 -->
    <div class="mobile-nav-header">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-icon">🎬</span>
          <span class="brand-text">VabHub</span>
        </router-link>
      </div>
      
      <div class="nav-actions">
        <button class="nav-btn theme-toggle" @click="toggleTheme">
          {{ isDarkMode ? '🌙' : '☀️' }}
        </button>
        <button class="nav-btn menu-toggle" @click="toggleMenu">
          <span class="hamburger" :class="{ 'hamburger-open': isMenuOpen }">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
      </div>
    </div>

    <!-- 移动端菜单 -->
    <div class="mobile-menu" :class="{ 'menu-open': isMenuOpen }">
      <div class="menu-content">
        <router-link 
          v-for="item in menuItems" 
          :key="item.path"
          :to="item.path"
          class="mobile-menu-item"
          @click="closeMenu"
        >
          <el-icon class="menu-icon">
            <component :is="item.icon" />
          </el-icon>
          <span class="menu-text">{{ item.text }}</span>
        </router-link>
      </div>
    </div>

    <!-- 遮罩层 -->
    <div 
      class="menu-overlay" 
      :class="{ 'overlay-visible': isMenuOpen }"
      @click="closeMenu"
    ></div>
  </nav>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  House,
  Search,
  Compass,
  Collection,
  Setting,
  User
} from '@element-plus/icons-vue'

export default {
  name: 'MobileNav',
  components: {
    House,
    Search,
    Compass,
    Collection,
    Setting,
    User
  },
  setup() {
    const isMenuOpen = ref(false)
    const isDarkMode = ref(false)
    const router = useRouter()

    const menuItems = [
      { path: '/', text: '首页', icon: 'House' },
      { path: '/discover', text: '发现', icon: 'Compass' },
      { path: '/search', text: '搜索', icon: 'Search' },
      { path: '/library', text: '媒体库', icon: 'Collection' },
      { path: '/social', text: '社交', icon: 'User' },
      { path: '/settings', text: '设置', icon: 'Setting' }
    ]

    // 切换菜单
    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value
      if (isMenuOpen.value) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }

    // 关闭菜单
    const closeMenu = () => {
      isMenuOpen.value = false
      document.body.style.overflow = ''
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

    // 监听窗口大小变化
    const handleResize = () => {
      if (window.innerWidth > 768 && isMenuOpen.value) {
        closeMenu()
      }
    }

    onMounted(() => {
      initTheme()
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      document.body.style.overflow = ''
    })

    return {
      isMenuOpen,
      isDarkMode,
      menuItems,
      toggleMenu,
      closeMenu,
      toggleTheme
    }
  }
}
</script>

<style scoped>
.mobile-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow);
}

.mobile-nav-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 16px;
  background: var(--bg-primary);
}

.nav-brand .brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text-primary);
  font-weight: bold;
  font-size: 1.25rem;
}

.brand-icon {
  font-size: 1.5rem;
  margin-right: 8px;
}

.brand-text {
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-btn {
  background: none;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-btn:hover {
  background: var(--bg-secondary);
  border-color: var(--primary-color);
}

.theme-toggle {
  font-size: 1.2rem;
}

.menu-toggle {
  width: 40px;
  height: 40px;
}

.hamburger {
  display: flex;
  flex-direction: column;
  width: 20px;
  height: 16px;
  position: relative;
  transition: all 0.3s;
}

.hamburger span {
  display: block;
  height: 2px;
  width: 100%;
  background: var(--text-primary);
  border-radius: 1px;
  transition: all 0.3s;
  transform-origin: center;
}

.hamburger span:nth-child(1) {
  margin-bottom: 5px;
}

.hamburger span:nth-child(2) {
  margin-bottom: 5px;
}

.hamburger-open span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.hamburger-open span:nth-child(2) {
  opacity: 0;
}

.hamburger-open span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -6px);
}

/* 移动端菜单 */
.mobile-menu {
  position: fixed;
  top: 60px;
  left: -100%;
  width: 280px;
  height: calc(100vh - 60px);
  background: var(--bg-primary);
  border-right: 1px solid var(--border-color);
  transition: left 0.3s ease;
  z-index: 1001;
}

.menu-open {
  left: 0;
}

.menu-content {
  padding: 20px 0;
}

.mobile-menu-item {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.mobile-menu-item:hover,
.mobile-menu-item.router-link-active {
  background: var(--bg-secondary);
  border-left-color: var(--primary-color);
  color: var(--primary-color);
}

.menu-icon {
  margin-right: 12px;
  font-size: 1.2rem;
}

.menu-text {
  font-weight: 500;
}

/* 遮罩层 */
.menu-overlay {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  z-index: 1000;
}

.overlay-visible {
  opacity: 1;
  visibility: visible;
}

/* 响应式适配 */
@media (min-width: 769px) {
  .mobile-nav {
    display: none;
  }
}

@media (max-width: 480px) {
  .mobile-nav-header {
    height: 56px;
    padding: 0 12px;
  }
  
  .mobile-menu {
    top: 56px;
    height: calc(100vh - 56px);
  }
  
  .menu-overlay {
    top: 56px;
  }
  
  .brand-text {
    font-size: 1.1rem;
  }
}

/* 深色主题适配 */
[data-theme="dark"] .menu-overlay {
  background: rgba(0, 0, 0, 0.7);
}
</style>