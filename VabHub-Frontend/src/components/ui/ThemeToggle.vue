<template>
  <button
    :class="toggleClasses"
    @click="toggleTheme"
    :aria-label="toggleLabel"
    :title="toggleLabel"
  >
    <!-- 图标容器 -->
    <div class="modern-theme-toggle__icon-container">
      <!-- 太阳图标（浅色模式） -->
      <div class="modern-theme-toggle__icon modern-theme-toggle__icon--sun">
        <el-icon>
          <Sunny />
        </el-icon>
      </div>
      
      <!-- 月亮图标（深色模式） -->
      <div class="modern-theme-toggle__icon modern-theme-toggle__icon--moon">
        <el-icon>
          <Moon />
        </el-icon>
      </div>
      
      <!-- 系统图标（自动模式） -->
      <div class="modern-theme-toggle__icon modern-theme-toggle__icon--system">
        <el-icon>
          <Monitor />
        </el-icon>
      </div>
    </div>
    
    <!-- 切换滑块 -->
    <div class="modern-theme-toggle__slider">
      <div class="modern-theme-toggle__slider-track"></div>
      <div 
        class="modern-theme-toggle__slider-thumb" 
        :class="sliderThumbClass"
      ></div>
    </div>
    
    <!-- 当前主题标签 -->
    <span v-if="showLabel" class="modern-theme-toggle__label">
      {{ currentThemeLabel }}
    </span>
  </button>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { Sunny, Moon, Monitor } from '@element-plus/icons-vue'

export default {
  name: 'ThemeToggle',
  components: {
    Sunny,
    Moon,
    Monitor
  },
  props: {
    // 是否显示标签
    showLabel: {
      type: Boolean,
      default: false
    },
    
    // 尺寸
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    
    // 变体
    variant: {
      type: String,
      default: 'default',
      validator: (value) => ['default', 'minimal', 'outline'].includes(value)
    },
    
    // 初始主题
    initialTheme: {
      type: String,
      default: '',
      validator: (value) => ['', 'light', 'dark', 'auto'].includes(value)
    }
  },
  emits: ['theme-change'],
  setup(props, { emit }) {
    // 响应式状态
    const currentTheme = ref('auto')
    const prefersDark = ref(false)
    
    // 计算属性
    const toggleClasses = computed(() => ({
      'modern-theme-toggle': true,
      [`modern-theme-toggle--${props.size}`]: true,
      [`modern-theme-toggle--${props.variant}`]: true,
      'modern-theme-toggle--with-label': props.showLabel,
      'modern-theme-toggle--light': currentTheme.value === 'light',
      'modern-theme-toggle--dark': currentTheme.value === 'dark',
      'modern-theme-toggle--auto': currentTheme.value === 'auto'
    }))
    
    const toggleLabel = computed(() => {
      const labels = {
        light: '切换到深色模式',
        dark: '切换到浅色模式',
        auto: '切换到系统主题'
      }
      return labels[currentTheme.value] || '切换主题'
    })
    
    const currentThemeLabel = computed(() => {
      const labels = {
        light: '浅色',
        dark: '深色',
        auto: '自动'
      }
      return labels[currentTheme.value] || '自动'
    })
    
    const sliderThumbClass = computed(() => ({
      'modern-theme-toggle__slider-thumb--light': currentTheme.value === 'light',
      'modern-theme-toggle__slider-thumb--dark': currentTheme.value === 'dark',
      'modern-theme-toggle__slider-thumb--auto': currentTheme.value === 'auto'
    }))
    
    // 方法
    const toggleTheme = () => {
      const themes = ['light', 'dark', 'auto']
      const currentIndex = themes.indexOf(currentTheme.value)
      const nextIndex = (currentIndex + 1) % themes.length
      
      setTheme(themes[nextIndex])
    }
    
    const setTheme = (theme) => {
      currentTheme.value = theme
      
      // 更新文档属性
      if (theme === 'auto') {
        document.documentElement.setAttribute('data-theme', prefersDark.value ? 'dark' : 'light')
        localStorage.removeItem('theme')
      } else {
        document.documentElement.setAttribute('data-theme', theme)
        localStorage.setItem('theme', theme)
      }
      
      // 触发事件
      emit('theme-change', theme)
    }
    
    const checkSystemPreference = () => {
      prefersDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      
      // 如果当前是自动模式，更新主题
      if (currentTheme.value === 'auto') {
        document.documentElement.setAttribute('data-theme', prefersDark.value ? 'dark' : 'light')
      }
    }
    
    // 初始化主题
    const initTheme = () => {
      // 从本地存储获取保存的主题
      const savedTheme = localStorage.getItem('theme')
      
      // 检查系统偏好
      checkSystemPreference()
      
      // 确定初始主题
      if (props.initialTheme) {
        setTheme(props.initialTheme)
      } else if (savedTheme) {
        setTheme(savedTheme)
      } else {
        setTheme('auto')
      }
    }
    
    // 监听系统主题变化
    const setupSystemThemeListener = () => {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      
      const handleSystemThemeChange = (e) => {
        prefersDark.value = e.matches
        
        // 如果当前是自动模式，更新主题
        if (currentTheme.value === 'auto') {
          document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light')
        }
      }
      
      mediaQuery.addEventListener('change', handleSystemThemeChange)
      
      // 清理函数
      return () => {
        mediaQuery.removeEventListener('change', handleSystemThemeChange)
      }
    }
    
    // 生命周期
    onMounted(() => {
      initTheme()
      setupSystemThemeListener()
    })
    
    // 监听主题变化
    watch(currentTheme, (newTheme) => {
      // 可以在这里添加主题变化后的额外逻辑
      console.log('主题已切换至:', newTheme)
    })
    
    return {
      currentTheme,
      toggleClasses,
      toggleLabel,
      currentThemeLabel,
      sliderThumbClass,
      toggleTheme,
      setTheme
    }
  }
}
</script>

<style scoped>
.modern-theme-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-lg);
  transition: all 0.3s ease;
  color: var(--text-secondary);
  outline: none;
}

.modern-theme-toggle:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.modern-theme-toggle:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 尺寸 */
.modern-theme-toggle--small {
  padding: var(--space-1);
  gap: var(--space-2);
}

.modern-theme-toggle--large {
  padding: var(--space-3);
  gap: var(--space-4);
}

/* 变体 */
.modern-theme-toggle--outline {
  border: 1px solid var(--border-primary);
  background: var(--bg-primary);
}

.modern-theme-toggle--minimal {
  background: transparent;
}

.modern-theme-toggle--minimal:hover {
  background: var(--bg-tertiary);
}

/* 图标容器 */
.modern-theme-toggle__icon-container {
  position: relative;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modern-theme-toggle--small .modern-theme-toggle__icon-container {
  width: 16px;
  height: 16px;
}

.modern-theme-toggle--large .modern-theme-toggle__icon-container {
  width: 24px;
  height: 24px;
}

.modern-theme-toggle__icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modern-theme-toggle--light .modern-theme-toggle__icon--sun {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
}

.modern-theme-toggle--dark .modern-theme-toggle__icon--moon {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
}

.modern-theme-toggle--auto .modern-theme-toggle__icon--system {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
}

/* 滑块 */
.modern-theme-toggle__slider {
  position: relative;
  width: 48px;
  height: 24px;
  background: var(--bg-tertiary);
  border-radius: 12px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.modern-theme-toggle--small .modern-theme-toggle__slider {
  width: 40px;
  height: 20px;
}

.modern-theme-toggle--large .modern-theme-toggle__slider {
  width: 56px;
  height: 28px;
}

.modern-theme-toggle__slider-track {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, 
    var(--primary-300) 0%, 
    var(--primary-500) 33%, 
    var(--gray-500) 66%, 
    var(--gray-700) 100%
  );
  opacity: 0.3;
  transition: opacity 0.3s ease;
}

.modern-theme-toggle:hover .modern-theme-toggle__slider-track {
  opacity: 0.6;
}

.modern-theme-toggle__slider-thumb {
  position: absolute;
  top: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modern-theme-toggle--small .modern-theme-toggle__slider-thumb {
  width: 16px;
  height: 16px;
  top: 2px;
}

.modern-theme-toggle--large .modern-theme-toggle__slider-thumb {
  width: 24px;
  height: 24px;
  top: 2px;
}

.modern-theme-toggle__slider-thumb--light {
  left: 2px;
  background: var(--warning-400);
}

.modern-theme-toggle__slider-thumb--dark {
  left: 26px;
  background: var(--indigo-400);
}

.modern-theme-toggle__slider-thumb--auto {
  left: 14px;
  background: var(--primary-500);
}

.modern-theme-toggle--small .modern-theme-toggle__slider-thumb--light {
  left: 2px;
}

.modern-theme-toggle--small .modern-theme-toggle__slider-thumb--dark {
  left: 22px;
}

.modern-theme-toggle--small .modern-theme-toggle__slider-thumb--auto {
  left: 12px;
}

.modern-theme-toggle--large .modern-theme-toggle__slider-thumb--light {
  left: 2px;
}

.modern-theme-toggle--large .modern-theme-toggle__slider-thumb--dark {
  left: 30px;
}

.modern-theme-toggle--large .modern-theme-toggle__slider-thumb--auto {
  left: 16px;
}

/* 标签 */
.modern-theme-toggle__label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  transition: color 0.3s ease;
}

.modern-theme-toggle:hover .modern-theme-toggle__label {
  color: var(--text-primary);
}

.modern-theme-toggle--small .modern-theme-toggle__label {
  font-size: var(--font-size-xs);
}

.modern-theme-toggle--large .modern-theme-toggle__label {
  font-size: var(--font-size-base);
}

/* 深色主题适配 */
[data-theme="dark"] .modern-theme-toggle {
  color: var(--text-secondary);
}

[data-theme="dark"] .modern-theme-toggle:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .modern-theme-toggle--outline {
  border-color: var(--border-secondary);
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .modern-theme-toggle__slider {
  background: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .modern-theme-toggle__slider-thumb {
  background: var(--gray-300);
}

/* 动画 */
.modern-theme-toggle__slider-thumb {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-theme-toggle__label {
    display: none;
  }
  
  .modern-theme-toggle--with-label .modern-theme-toggle__label {
    display: inline;
  }
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .modern-theme-toggle,
  .modern-theme-toggle__icon,
  .modern-theme-toggle__slider-thumb {
    transition: none;
  }
}
</style>