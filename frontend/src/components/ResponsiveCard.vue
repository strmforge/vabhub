<template>
  <div class="responsive-card" :class="cardClass" :style="cardStyle">
    <!-- 卡片头部 -->
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <h3 class="card-title">{{ title }}</h3>
        <div v-if="showActions" class="card-actions">
          <slot name="actions"></slot>
        </div>
      </slot>
    </div>
    
    <!-- 卡片内容 -->
    <div class="card-content">
      <slot></slot>
    </div>
    
    <!-- 卡片底部 -->
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { responsiveSpacing } from '../utils/responsive'

export default {
  name: 'ResponsiveCard',
  props: {
    title: {
      type: String,
      default: ''
    },
    padding: {
      type: [Number, String],
      default: 'medium'
    },
    shadow: {
      type: Boolean,
      default: true
    },
    border: {
      type: Boolean,
      default: true
    },
    hover: {
      type: Boolean,
      default: true
    },
    radius: {
      type: [Number, String],
      default: 'medium'
    },
    background: {
      type: String,
      default: 'primary'
    }
  },
  setup(props) {
    const showActions = computed(() => {
      return !!this.$slots.actions
    })

    // 响应式间距
    const responsivePadding = computed(() => {
      const basePadding = {
        small: 12,
        medium: 20,
        large: 32
      }[props.padding] || parseInt(props.padding) || 20
      
      return responsiveSpacing(basePadding)
    })

    // 响应式圆角
    const responsiveRadius = computed(() => {
      const baseRadius = {
        small: 4,
        medium: 8,
        large: 16
      }[props.radius] || parseInt(props.radius) || 8
      
      return responsiveSpacing(baseRadius, { mobileRatio: 0.8, tabletRatio: 0.9 })
    })

    // 卡片样式
    const cardStyle = computed(() => {
      return {
        padding: `${responsivePadding.value}px`,
        borderRadius: `${responsiveRadius.value}px`
      }
    })

    // 卡片类名
    const cardClass = computed(() => ({
      'card-shadow': props.shadow,
      'card-border': props.border,
      'card-hover': props.hover,
      [`card-bg-${props.background}`]: true
    }))

    return {
      showActions,
      responsivePadding,
      responsiveRadius,
      cardStyle,
      cardClass
    }
  }
}
</script>

<style scoped>
.responsive-card {
  background: var(--bg-primary);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

/* 阴影效果 */
.responsive-card.card-shadow {
  box-shadow: var(--shadow);
}

/* 边框效果 */
.responsive-card.card-border {
  border: 1px solid var(--border-color);
}

/* 悬停效果 */
.responsive-card.card-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* 背景变体 */
.responsive-card.card-bg-primary {
  background: var(--bg-primary);
}

.responsive-card.card-bg-secondary {
  background: var(--bg-secondary);
}

/* 卡片头部 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.card-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.card-actions {
  display: flex;
  gap: 8px;
}

/* 卡片内容 */
.card-content {
  flex: 1;
}

/* 卡片底部 */
.card-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;
    padding-bottom: 8px;
  }
  
  .card-title {
    font-size: 1.125rem;
  }
  
  .card-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .card-footer {
    margin-top: 12px;
    padding-top: 8px;
  }
}

@media (max-width: 480px) {
  .card-title {
    font-size: 1rem;
  }
  
  .responsive-card.card-hover:hover {
    transform: none;
    box-shadow: var(--shadow);
  }
}

/* 平板适配 */
@media (min-width: 769px) and (max-width: 1024px) {
  .card-title {
    font-size: 1.125rem;
  }
}

/* 减少动画（用户偏好） */
@media (prefers-reduced-motion: reduce) {
  .responsive-card {
    transition: none;
  }
  
  .responsive-card.card-hover:hover {
    transform: none;
  }
}
</style>