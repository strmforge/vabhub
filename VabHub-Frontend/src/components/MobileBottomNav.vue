<template>
  <!-- 移动端底部导航 -->
  <nav v-if="isMobile" class="mobile-bottom-nav">
    <router-link 
      v-for="item in navItems" 
      :key="item.path"
      :to="item.path"
      class="bottom-nav-item"
      :class="{ active: $route.path === item.path }"
    >
      <el-icon class="nav-icon">
        <component :is="item.icon" />
      </el-icon>
      <span class="nav-text">{{ item.text }}</span>
    </router-link>
  </nav>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  House,
  Search,
  Compass,
  Collection,
  User
} from '@element-plus/icons-vue'

export default {
  name: 'MobileBottomNav',
  components: {
    House,
    Search,
    Compass,
    Collection,
    User
  },
  setup() {
    const isMobile = ref(false)
    const route = useRoute()

    const navItems = [
      { path: '/', text: '首页', icon: 'House' },
      { path: '/discover', text: '发现', icon: 'Compass' },
      { path: '/search', text: '搜索', icon: 'Search' },
      { path: '/library', text: '媒体库', icon: 'Collection' },
      { path: '/social', text: '社交', icon: 'User' }
    ]

    // 检测移动端
    const checkMobile = () => {
      isMobile.value = window.innerWidth <= 768
    }

    onMounted(() => {
      checkMobile()
      window.addEventListener('resize', checkMobile)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkMobile)
    })

    return {
      isMobile,
      navItems
    }
  }
}
</script>

<style scoped>
.mobile-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: var(--bg-primary);
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 1000;
  padding: 0 8px;
}

.bottom-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  height: 100%;
  text-decoration: none;
  color: var(--text-secondary);
  transition: all 0.3s;
  padding: 8px 4px;
  border-radius: 8px;
  min-width: 0;
}

.bottom-nav-item:hover,
.bottom-nav-item.active {
  color: var(--primary-color);
  background: var(--bg-secondary);
}

.nav-icon {
  font-size: 1.4rem;
  margin-bottom: 4px;
}

.nav-text {
  font-size: 0.7rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

/* 响应式适配 */
@media (max-width: 480px) {
  .mobile-bottom-nav {
    height: 56px;
  }
  
  .nav-icon {
    font-size: 1.2rem;
  }
  
  .nav-text {
    font-size: 0.65rem;
  }
  
  .bottom-nav-item {
    padding: 6px 2px;
  }
}

/* 平板适配 */
@media (min-width: 481px) and (max-width: 768px) {
  .mobile-bottom-nav {
    height: 64px;
  }
  
  .nav-icon {
    font-size: 1.5rem;
  }
  
  .nav-text {
    font-size: 0.75rem;
  }
}

/* 深色主题适配 */
[data-theme="dark"] .mobile-bottom-nav {
  background: var(--bg-primary);
  border-top-color: var(--border-color);
}

/* 安全区域适配（iPhone X及以上） */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .mobile-bottom-nav {
    padding-bottom: env(safe-area-inset-bottom);
    height: calc(60px + env(safe-area-inset-bottom));
  }
  
  @media (max-width: 480px) {
    .mobile-bottom-nav {
      height: calc(56px + env(safe-area-inset-bottom));
    }
  }
  
  @media (min-width: 481px) and (max-width: 768px) {
    .mobile-bottom-nav {
      height: calc(64px + env(safe-area-inset-bottom));
    }
  }
}
</style>