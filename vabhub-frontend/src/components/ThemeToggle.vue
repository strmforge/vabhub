<template>
  <button 
    class="theme-toggle"
    @click="toggleTheme"
    :title="currentTheme === 'dark' ? '切换到亮色主题' : '切换到暗色主题'"
    aria-label="切换主题"
  >
    <span class="theme-icon">
      {{ currentTheme === 'dark' ? '☀️' : '🌙' }}
    </span>
    <span class="theme-text">
      {{ currentTheme === 'dark' ? '亮色' : '暗色' }}
    </span>
  </button>
</template>

<script>
export default {
  name: 'ThemeToggle',
  data() {
    return {
      currentTheme: 'light'
    }
  },
  mounted() {
    // 从本地存储加载主题设置
    const savedTheme = localStorage.getItem('vabhub-theme')
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    
    if (savedTheme) {
      this.currentTheme = savedTheme
    } else if (systemPrefersDark) {
      this.currentTheme = 'dark'
    }
    
    this.applyTheme()
    
    // 监听系统主题变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('vabhub-theme')) {
        this.currentTheme = e.matches ? 'dark' : 'light'
        this.applyTheme()
      }
    })
  },
  methods: {
    toggleTheme() {
      this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('vabhub-theme', this.currentTheme)
      this.applyTheme()
    },
    applyTheme() {
      document.documentElement.setAttribute('data-theme', this.currentTheme)
      
      // 触发主题变化事件
      this.$emit('theme-change', this.currentTheme)
    }
  }
}
</script>

<style scoped>
.theme-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--bg-secondary, #f8f9fa);
  border: 1px solid var(--border-color, #e9ecef);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-primary, #2c3e50);
}

.theme-toggle:hover {
  background: var(--bg-tertiary, #e9ecef);
  transform: translateY(-1px);
}

.theme-icon {
  font-size: 1.2rem;
}

.theme-text {
  font-size: 0.9rem;
  font-weight: 500;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .theme-toggle {
    padding: 0.375rem 0.75rem;
  }
  
  .theme-text {
    display: none;
  }
}
</style>