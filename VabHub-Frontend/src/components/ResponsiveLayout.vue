<template>
  <div class="responsive-layout">
    <!-- 桌面端导航 -->
    <nav v-if="!isMobile" class="desktop-nav">
      <div class="nav-container">
        <div class="nav-brand">
          <router-link to="/" class="brand-link">
            <span class="brand-icon">🎬</span>
            <span class="brand-text">VabHub</span>
          </router-link>
        </div>
        
        <div class="nav-menu">
          <router-link to="/" class="nav-link">
            <el-icon class="nav-icon">
              <House />
            </el-icon>
            首页
          </router-link>
          <router-link to="/discover" class="nav-link">
            <el-icon class="nav-icon">
              <Compass />
            </el-icon>
            发现
          </router-link>
          <router-link to="/search" class="nav-link">
            <el-icon class="nav-icon">
              <Search />
            </el-icon>
            搜索
          </router-link>
          <router-link to="/library" class="nav-link">
            <el-icon class="nav-icon">
              <Collection />
            </el-icon>
            媒体库
          </router-link>
          <router-link to="/social" class="nav-link">
            <el-icon class="nav-icon">
              <User />
            </el-icon>
            社交
          </router-link>
        </div>
        
        <div class="nav-actions">
          <button class="nav-btn" @click="toggleTheme">
            {{ isDarkMode ? '🌙' : '☀️' }}
          </button>
        </div>
      </div>
    </nav>

    <!-- 移动端导航 -->
    <MobileNav v-else />

    <!-- 主要内容区域 -->
    <main class="main-content" :class="{ 'mobile-padding': isMobile }">
      <div class="content-container">
        <slot></slot>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer" :class="{ 'mobile-footer': isMobile }">
      <div class="footer-content">
        <p>&copy; 2024 VabHub. 智能媒体管理系统</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import MobileNav from './MobileNav.vue'
import {
  House,
  Search,
  Compass,
  Collection,
  User
} from '@element-plus/icons-vue'

export default {
  name: 'ResponsiveLayout',
  components: {
    MobileNav,
    House,
    Search,
    Compass,
    Collection,
    User
  },
  setup() {
    const isMobile = ref(false)
    const isDarkMode = ref(false)

    // 检测移动端
    const checkMobile = () => {
      isMobile.value = window.innerWidth <= 768
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
      toggleTheme
    }
  }
}
</script>

<style scoped>
.responsive-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 桌面端导航 */
.desktop-nav {
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.desktop-nav .nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.nav-brand .brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text-primary);
  font-weight: bold;
  font-size: 1.5rem;
}

.brand-icon {
  font-size: 2rem;
  margin-right: 10px;
}

.brand-text {
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.nav-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  padding: 8px 16px;
  border-radius: var(--radius);
  transition: all 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary-color);
  background: var(--bg-secondary);
}

.nav-icon {
  margin-right: 8px;
  font-size: 1.2rem;
}

.nav-actions {
  display: flex;
  gap: 10px;
}

.nav-btn {
  background: none;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 8px 12px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: var(--bg-secondary);
  border-color: var(--primary-color);
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  padding: 0;
}

.mobile-padding {
  padding-top: 60px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 页脚 */
.footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  padding: 20px 0;
  margin-top: auto;
}

.mobile-footer {
  padding-bottom: 80px; /* 为移动端底部导航留出空间 */
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
  color: var(--text-secondary);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }
  
  .content-container {
    padding: 16px;
  }
  
  .mobile-padding {
    padding-top: 56px;
  }
}

@media (max-width: 480px) {
  .content-container {
    padding: 12px;
  }
  
  .mobile-padding {
    padding-top: 56px;
  }
}

/* 平板适配 */
@media (min-width: 769px) and (max-width: 1024px) {
  .desktop-nav .nav-container {
    padding: 0 16px;
  }
  
  .nav-menu {
    gap: 20px;
  }
  
  .nav-link {
    padding: 8px 12px;
    font-size: 0.9rem;
  }
  
  .content-container {
    padding: 16px;
  }
}
</style>