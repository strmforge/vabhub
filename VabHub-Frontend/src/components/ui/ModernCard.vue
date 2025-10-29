<template>
  <div :class="cardClasses" :style="cardStyle">
    <!-- 卡片头部 -->
    <div v-if="showHeader" class="modern-card__header">
      <slot name="header">
        <div v-if="title || subtitle" class="modern-card__header-content">
          <h3 v-if="title" class="modern-card__title">{{ title }}</h3>
          <p v-if="subtitle" class="modern-card__subtitle">{{ subtitle }}</p>
        </div>
        <div v-if="showActions" class="modern-card__actions">
          <slot name="actions"></slot>
        </div>
      </slot>
    </div>
    
    <!-- 卡片内容 -->
    <div class="modern-card__content" :style="contentStyle">
      <slot></slot>
    </div>
    
    <!-- 卡片底部 -->
    <div v-if="showFooter" class="modern-card__footer">
      <slot name="footer"></slot>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="modern-card__loading">
      <div class="modern-card__loading-spinner"></div>
      <span v-if="loadingText" class="modern-card__loading-text">{{ loadingText }}</span>
    </div>
    
    <!-- 悬停遮罩 -->
    <div v-if="hoverable" class="modern-card__hover-mask"></div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'ModernCard',
  props: {
    title: {
      type: String,
      default: ''
    },
    subtitle: {
      type: String,
      default: ''
    },
    variant: {
      type: String,
      default: 'default',
      validator: (value) => ['default', 'elevated', 'outline', 'filled'].includes(value)
    },
    padding: {
      type: String,
      default: 'md',
      validator: (value) => ['none', 'sm', 'md', 'lg'].includes(value)
    },
    hoverable: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    loadingText: {
      type: String,
      default: ''
    },
    radius: {
      type: String,
      default: 'md',
      validator: (value) => ['none', 'sm', 'md', 'lg', 'xl'].includes(value)
    },
    shadow: {
      type: Boolean,
      default: true
    },
    border: {
      type: Boolean,
      default: true
    }
  },
  setup(props, { slots }) {
    const showHeader = computed(() => {
      return slots.header || props.title || props.subtitle
    })

    const showFooter = computed(() => {
      return slots.footer
    })

    const showActions = computed(() => {
      return slots.actions
    })

    const cardClasses = computed(() => ({
      'modern-card': true,
      [`modern-card--${props.variant}`]: true,
      [`modern-card--padding-${props.padding}`]: true,
      [`modern-card--radius-${props.radius}`]: true,
      'modern-card--hoverable': props.hoverable,
      'modern-card--loading': props.loading,
      'modern-card--shadow': props.shadow,
      'modern-card--border': props.border
    }))

    const cardStyle = computed(() => ({
      '--card-radius': {
        none: '0',
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-xl)'
      }[props.radius]
    }))

    const contentStyle = computed(() => ({
      '--content-padding': {
        none: '0',
        sm: 'var(--space-4)',
        md: 'var(--space-6)',
        lg: 'var(--space-8)'
      }[props.padding]
    }))

    return {
      showHeader,
      showFooter,
      showActions,
      cardClasses,
      cardStyle,
      contentStyle
    }
  }
}
</script>

<style scoped>
.modern-card {
  position: relative;
  background: var(--bg-secondary);
  border-radius: var(--card-radius, var(--radius-md));
  transition: all var(--transition-normal);
  overflow: hidden;
  isolation: isolate;
}

/* 变体样式 */
.modern-card--default {
  background: var(--bg-secondary);
}

.modern-card--elevated {
  background: var(--bg-secondary);
  box-shadow: var(--shadow-lg);
}

.modern-card--outline {
  background: transparent;
  border: 1px solid var(--border-primary);
}

.modern-card--filled {
  background: var(--bg-tertiary);
}

/* 阴影 */
.modern-card--shadow {
  box-shadow: var(--shadow-sm);
}

.modern-card--shadow.modern-card--elevated {
  box-shadow: var(--shadow-lg);
}

/* 边框 */
.modern-card--border:not(.modern-card--outline) {
  border: 1px solid var(--border-primary);
}

/* 悬停效果 */
.modern-card--hoverable:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}

.modern-card--hoverable.modern-card--outline:hover {
  border-color: var(--primary-300);
}

/* 卡片头部 */
.modern-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--content-padding, var(--space-6));
  padding-bottom: 0;
  border-bottom: 1px solid var(--border-primary);
}

.modern-card__header-content {
  flex: 1;
  min-width: 0;
}

.modern-card__title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0 0 var(--space-1) 0;
  line-height: var(--line-height-tight);
}

.modern-card__subtitle {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: 0;
  line-height: var(--line-height-normal);
}

.modern-card__actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

/* 卡片内容 */
.modern-card__content {
  padding: var(--content-padding, var(--space-6));
  position: relative;
  z-index: 1;
}

.modern-card__header + .modern-card__content {
  padding-top: var(--space-4);
}

/* 卡片底部 */
.modern-card__footer {
  padding: var(--content-padding, var(--space-6));
  padding-top: 0;
  border-top: 1px solid var(--border-primary);
  margin-top: var(--space-4);
}

/* 加载状态 */
.modern-card__loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  z-index: 10;
  border-radius: inherit;
}

[data-theme="dark"] .modern-card__loading {
  background: rgba(0, 0, 0, 0.6);
}

.modern-card__loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-primary);
  border-top: 3px solid var(--primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.modern-card__loading-text {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* 悬停遮罩 */
.modern-card__hover-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--primary-500);
  opacity: 0;
  transition: opacity var(--transition-normal);
  z-index: 0;
  border-radius: inherit;
}

.modern-card--hoverable:hover .modern-card__hover-mask {
  opacity: 0.03;
}

/* 动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-card__header {
    flex-direction: column;
    align-items: stretch;
    gap: var(--space-3);
  }
  
  .modern-card__actions {
    justify-content: flex-end;
  }
  
  .modern-card--hoverable:hover {
    transform: none;
  }
  
  .modern-card--hoverable:active {
    transform: scale(0.98);
  }
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .modern-card {
    transition: none;
  }
  
  .modern-card--hoverable:hover {
    transform: none;
  }
  
  .modern-card__loading-spinner {
    animation: none;
  }
}

/* 深色主题适配 */
[data-theme="dark"] {
  .modern-card--outline {
    border-color: var(--border-secondary);
  }
  
  .modern-card--filled {
    background: var(--bg-tertiary);
  }
}

/* 无障碍访问 */
.modern-card:focus-within {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
</style>