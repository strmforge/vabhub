<template>
  <div id="app">
    <!-- 响应式布局 -->
    <ResponsiveLayout>
      <router-view />
    </ResponsiveLayout>
    
    <!-- 移动端底部导航 -->
    <MobileBottomNav />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import ResponsiveLayout from './components/ResponsiveLayout.vue'
import MobileBottomNav from './components/MobileBottomNav.vue'

export default {
  name: 'App',
  components: {
    ResponsiveLayout,
    MobileBottomNav
  },
  setup() {
    const isDarkMode = ref(false)

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
      initTheme()
    })

    return {
      isDarkMode,
      toggleTheme
    }
  }
}
</script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #3498db;
  --secondary-color: #2c3e50;
  --accent-color: #e74c3c;
  --text-primary: #2c3e50;
  --text-secondary: #7f8c8d;
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --border-color: #e1e5e9;
  --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  --radius: 8px;
}

[data-theme="dark"] {
  --primary-color: #3498db;
  --secondary-color: #34495e;
  --accent-color: #e74c3c;
  --text-primary: #ecf0f1;
  --text-secondary: #bdc3c7;
  --bg-primary: #2c3e50;
  --bg-secondary: #34495e;
  --border-color: #4a6278;
  --shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
  background-color: var(--bg-primary);
  transition: background-color 0.3s, color 0.3s;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 响应式设计增强 */
@media (max-width: 768px) {
  html {
    font-size: 14px;
  }
  
  body {
    -webkit-text-size-adjust: 100%;
    -webkit-tap-highlight-color: transparent;
  }
}

@media (max-width: 480px) {
  html {
    font-size: 13px;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .btn, .nav-btn, .bottom-nav-item {
    min-height: 44px;
    min-width: 44px;
  }
  
  .nav-link {
    padding: 12px 16px;
  }
}

/* 通用组件样式 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  border: none;
  border-radius: var(--radius);
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
  transform: translateY(-1px);
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--border-color);
}

.card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background: #fee;
  border: 1px solid #fcc;
  border-radius: var(--radius);
  padding: 15px;
  color: #c33;
  margin: 20px 0;
}

.success-message {
  background: #efe;
  border: 1px solid #cfc;
  border-radius: var(--radius);
  padding: 15px;
  color: #3c3;
  margin: 20px 0;
}

/* 响应式工具类 */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

.p-1 { padding: 0.5rem; }
.p-2 { padding: 1rem; }
.p-3 { padding: 1.5rem; }
.p-4 { padding: 2rem; }

.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }

.grid {
  display: grid;
  gap: 1rem;
}

.grid-cols-1 { grid-template-columns: 1fr; }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

/* 响应式网格系统 */
@media (max-width: 768px) {
  .grid-cols-2,
  .grid-cols-3,
  .grid-cols-4 {
    grid-template-columns: 1fr;
  }
  
  .grid {
    gap: 0.75rem;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .grid-cols-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 移动端优化类 */
.mobile-only {
  display: none;
}

.desktop-only {
  display: block;
}

@media (max-width: 768px) {
  .mobile-only {
    display: block;
  }
  
  .desktop-only {
    display: none;
  }
}

/* 安全区域适配 */
@supports (padding: max(0px)) {
  .safe-area-top {
    padding-top: max(12px, env(safe-area-inset-top));
  }
  
  .safe-area-bottom {
    padding-bottom: max(12px, env(safe-area-inset-bottom));
  }
  
  .safe-area-left {
    padding-left: max(12px, env(safe-area-inset-left));
  }
  
  .safe-area-right {
    padding-right: max(12px, env(safe-area-inset-right));
  }
}

/* 滚动条优化 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-secondary);
}

/* 选择文本优化 */
::selection {
  background: var(--primary-color);
  color: white;
}

/* 焦点样式 */
*:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* 减少动画（用户偏好） */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>