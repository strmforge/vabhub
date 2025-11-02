<template>
  <aside class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <!-- 侧边栏头部 -->
    <div class="sidebar-header">
      <div class="logo-section">
        <h2 class="logo" v-if="!isCollapsed">VabHub</h2>
        <button class="toggle-btn" @click="toggleSidebar" :title="isCollapsed ? '展开菜单' : '折叠菜单'">
          <span class="toggle-icon">{{ isCollapsed ? '→' : '←' }}</span>
        </button>
      </div>
    </div>

    <!-- 导航菜单 -->
    <nav class="sidebar-nav">
      <!-- 核心功能 -->
      <div class="nav-section">
        <h3 class="section-title" v-if="!isCollapsed">核心功能</h3>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">🏠</span>
              <span class="nav-text" v-if="!isCollapsed">首页</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/dashboard" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">📊</span>
              <span class="nav-text" v-if="!isCollapsed">仪表板</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/discover" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">🔍</span>
              <span class="nav-text" v-if="!isCollapsed">内容发现</span>
            </router-link>
          </li>
        </ul>
      </div>

      <!-- 媒体管理 -->
      <div class="nav-section">
        <h3 class="section-title" v-if="!isCollapsed">媒体管理</h3>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/subscriptions" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">📺</span>
              <span class="nav-text" v-if="!isCollapsed">订阅管理</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/file-organizer" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">📁</span>
              <span class="nav-text" v-if="!isCollapsed">文件整理</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/music" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">🎵</span>
              <span class="nav-text" v-if="!isCollapsed">音乐管理</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/recommendations" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">🤖</span>
              <span class="nav-text" v-if="!isCollapsed">AI推荐</span>
            </router-link>
          </li>
        </ul>
      </div>

      <!-- 系统管理 -->
      <div class="nav-section">
        <h3 class="section-title" v-if="!isCollapsed">系统管理</h3>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/storage" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">💾</span>
              <span class="nav-text" v-if="!isCollapsed">存储管理</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/plugins" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">🔌</span>
              <span class="nav-text" v-if="!isCollapsed">插件管理</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/logs" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">📋</span>
              <span class="nav-text" v-if="!isCollapsed">实时日志</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/microfrontend-demo" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">🌐</span>
              <span class="nav-text" v-if="!isCollapsed">微前端演示</span>
            </router-link>
          </li>
        </ul>
      </div>

      <!-- 设置 -->
      <div class="nav-section">
        <h3 class="section-title" v-if="!isCollapsed">设置</h3>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/settings" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">⚙️</span>
              <span class="nav-text" v-if="!isCollapsed">系统设置</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/notifications" class="nav-link" @click="closeMobileMenu">
              <span class="nav-icon">🔔</span>
              <span class="nav-text" v-if="!isCollapsed">通知设置</span>
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- 侧边栏底部 -->
    <div class="sidebar-footer">
      <!-- 语言切换器 -->
      <div class="language-section" v-if="!isCollapsed">
        <LanguageSwitcher />
      </div>
      
      <div class="user-info" v-if="!isCollapsed">
        <div class="user-avatar">👤</div>
        <div class="user-details">
          <p class="username">管理员</p>
          <p class="user-status">在线</p>
        </div>
      </div>
      <div class="system-info" v-if="!isCollapsed">
        <p class="version">v{{ version }}</p>
      </div>
    </div>
  </aside>
</template>

<script>
import LanguageSwitcher from './LanguageSwitcher.vue'

export default {
  name: 'Sidebar',
  components: {
    LanguageSwitcher
  },
  props: {
    version: {
      type: String,
      default: '1.6.0'
    }
  },
  data() {
    return {
      isCollapsed: false
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
      this.$emit('sidebar-toggle', this.isCollapsed)
    },
    closeMobileMenu() {
      // 在移动端点击菜单项时关闭移动菜单
      if (window.innerWidth <= 768) {
        this.$emit('close-mobile-menu')
      }
    }
  },
  mounted() {
    // 监听窗口大小变化，自动调整侧边栏状态
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        this.isCollapsed = true
      }
    }
    
    window.addEventListener('resize', handleResize)
    handleResize() // 初始化时检查一次
    
    this.$on('hook:beforeDestroy', () => {
      window.removeEventListener('resize', handleResize)
    })
  }
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  overflow-y: auto;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  padding: 1.5rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
  color: #3498db;
}

.toggle-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.toggle-icon {
  font-size: 1rem;
  font-weight: bold;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.6);
  margin: 0 1rem 0.5rem 1rem;
  letter-spacing: 0.5px;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin: 0.25rem 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-link.router-link-active {
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
  border-left-color: #3498db;
}

.nav-icon {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
  margin-right: 1rem;
}

.nav-text {
  font-size: 0.95rem;
  font-weight: 500;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.1);
}

.language-section {
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.user-avatar {
  font-size: 2rem;
  margin-right: 0.75rem;
}

.user-details {
  flex: 1;
}

.username {
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  font-size: 0.95rem;
}

.user-status {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

.system-info {
  text-align: center;
}

.version {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .sidebar {
    width: 280px;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .sidebar.collapsed {
    width: 280px;
    transform: translateX(-100%);
  }
  
  .sidebar.collapsed.mobile-open {
    transform: translateX(0);
  }
}

/* 滚动条样式 */
.sidebar::-webkit-scrollbar {
  width: 4px;
}

.sidebar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.sidebar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>