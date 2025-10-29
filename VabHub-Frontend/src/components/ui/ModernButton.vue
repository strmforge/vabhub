<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    @mousedown="handleMouseDown"
    @mouseup="handleMouseUp"
    @focus="handleFocus"
    @blur="handleBlur"
    :type="nativeType"
    :aria-label="ariaLabel"
    :aria-disabled="disabled || loading"
  >
    <!-- 加载状态 -->
    <span v-if="loading" class="modern-button__loading">
      <LoadingSpinner :size="spinnerSize" />
    </span>
    
    <!-- 图标 -->
    <span v-if="icon && !loading" class="modern-button__icon">
      <el-icon>
        <component :is="icon" />
      </el-icon>
    </span>
    
    <!-- 内容 -->
    <span class="modern-button__content">
      <slot></slot>
    </span>
    
    <!-- 右侧图标 -->
    <span v-if="rightIcon && !loading" class="modern-button__right-icon">
      <el-icon>
        <component :is="rightIcon" />
      </el-icon>
    </span>
    
    <!-- 波纹效果 -->
    <span v-if="showRipple" class="modern-button__ripple" :style="rippleStyle"></span>
  </button>
</template>

<script>
import { ref, computed, nextTick } from 'vue'
import LoadingSpinner from './LoadingSpinner.vue'

export default {
  name: 'ModernButton',
  components: {
    LoadingSpinner
  },
  props: {
    // 按钮变体
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'outline', 'ghost', 'danger', 'success', 'warning'].includes(value)
    },
    
    // 按钮尺寸
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false
    },
    
    // 是否加载中
    loading: {
      type: Boolean,
      default: false
    },
    
    // 是否块级元素
    block: {
      type: Boolean,
      default: false
    },
    
    // 是否圆形按钮
    circle: {
      type: Boolean,
      default: false
    },
    
    // 左侧图标
    icon: {
      type: String,
      default: ''
    },
    
    // 右侧图标
    rightIcon: {
      type: String,
      default: ''
    },
    
    // 原生按钮类型
    nativeType: {
      type: String,
      default: 'button',
      validator: (value) => ['button', 'submit', 'reset'].includes(value)
    },
    
    // 无障碍标签
    ariaLabel: {
      type: String,
      default: ''
    },
    
    // 是否启用波纹效果
    ripple: {
      type: Boolean,
      default: true
    },
    
    // 波纹颜色
    rippleColor: {
      type: String,
      default: 'rgba(255, 255, 255, 0.6)'
    }
  },
  emits: ['click', 'mouseenter', 'mouseleave', 'mousedown', 'mouseup', 'focus', 'blur'],
  setup(props, { emit }) {
    // 响应式状态
    const isHovered = ref(false)
    const isFocused = ref(false)
    const isActive = ref(false)
    const showRipple = ref(false)
    const rippleStyle = ref({})
    
    // 计算属性
    const buttonClasses = computed(() => ({
      'modern-button': true,
      [`modern-button--${props.variant}`]: true,
      [`modern-button--${props.size}`]: true,
      'modern-button--disabled': props.disabled,
      'modern-button--loading': props.loading,
      'modern-button--block': props.block,
      'modern-button--circle': props.circle,
      'modern-button--hovered': isHovered.value,
      'modern-button--focused': isFocused.value,
      'modern-button--active': isActive.value,
      'modern-button--icon-only': !props.$slots.default && props.icon && !props.rightIcon
    }))
    
    const spinnerSize = computed(() => {
      const sizes = {
        small: 'small',
        medium: 'small',
        large: 'medium'
      }
      return sizes[props.size]
    })
    
    // 方法
    const handleClick = (event) => {
      if (props.disabled || props.loading) return
      
      // 触发波纹效果
      if (props.ripple) {
        triggerRipple(event)
      }
      
      emit('click', event)
    }
    
    const handleMouseEnter = (event) => {
      isHovered.value = true
      emit('mouseenter', event)
    }
    
    const handleMouseLeave = (event) => {
      isHovered.value = false
      emit('mouseleave', event)
    }
    
    const handleMouseDown = (event) => {
      isActive.value = true
      emit('mousedown', event)
    }
    
    const handleMouseUp = (event) => {
      isActive.value = false
      emit('mouseup', event)
    }
    
    const handleFocus = (event) => {
      isFocused.value = true
      emit('focus', event)
    }
    
    const handleBlur = (event) => {
      isFocused.value = false
      emit('blur', event)
    }
    
    const triggerRipple = (event) => {
      const button = event.currentTarget
      const rect = button.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height)
      const x = event.clientX - rect.left - size / 2
      const y = event.clientY - rect.top - size / 2
      
      rippleStyle.value = {
        width: `${size}px`,
        height: `${size}px`,
        left: `${x}px`,
        top: `${y}px`,
        '--ripple-color': props.rippleColor
      }
      
      showRipple.value = true
      
      // 自动隐藏波纹
      nextTick(() => {
        setTimeout(() => {
          showRipple.value = false
        }, 600)
      })
    }
    
    return {
      isHovered,
      isFocused,
      isActive,
      showRipple,
      rippleStyle,
      buttonClasses,
      spinnerSize,
      handleClick,
      handleMouseEnter,
      handleMouseLeave,
      handleMouseDown,
      handleMouseUp,
      handleFocus,
      handleBlur
    }
  }
}
</script>

<style scoped>
.modern-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border: none;
  border-radius: var(--radius-lg);
  font-family: inherit;
  font-weight: var(--font-weight-medium);
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  overflow: hidden;
  user-select: none;
  outline: none;
}

/* 尺寸 */
.modern-button--small {
  height: 32px;
  padding: 0 var(--space-3);
  font-size: var(--font-size-sm);
}

.modern-button--medium {
  height: 40px;
  padding: 0 var(--space-4);
  font-size: var(--font-size-base);
}

.modern-button--large {
  height: 48px;
  padding: 0 var(--space-5);
  font-size: var(--font-size-lg);
}

/* 变体 */
.modern-button--primary {
  background: var(--primary-600);
  color: white;
}

.modern-button--primary:hover:not(.modern-button--disabled) {
  background: var(--primary-700);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.modern-button--primary:focus:not(.modern-button--disabled) {
  box-shadow: 0 0 0 3px var(--primary-100);
}

.modern-button--primary:active:not(.modern-button--disabled) {
  background: var(--primary-800);
  transform: translateY(0);
}

.modern-button--secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
}

.modern-button--secondary:hover:not(.modern-button--disabled) {
  background: var(--bg-secondary);
  border-color: var(--border-secondary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.modern-button--secondary:focus:not(.modern-button--disabled) {
  box-shadow: 0 0 0 3px var(--primary-100);
}

.modern-button--secondary:active:not(.modern-button--disabled) {
  background: var(--bg-primary);
  transform: translateY(0);
}

.modern-button--outline {
  background: transparent;
  color: var(--primary-600);
  border: 1px solid var(--primary-600);
}

.modern-button--outline:hover:not(.modern-button--disabled) {
  background: var(--primary-600);
  color: white;
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.modern-button--outline:focus:not(.modern-button--disabled) {
  box-shadow: 0 0 0 3px var(--primary-100);
}

.modern-button--outline:active:not(.modern-button--disabled) {
  background: var(--primary-700);
  transform: translateY(0);
}

.modern-button--ghost {
  background: transparent;
  color: var(--text-primary);
}

.modern-button--ghost:hover:not(.modern-button--disabled) {
  background: var(--bg-tertiary);
  transform: translateY(-1px);
}

.modern-button--ghost:focus:not(.modern-button--disabled) {
  box-shadow: 0 0 0 3px var(--primary-100);
}

.modern-button--ghost:active:not(.modern-button--disabled) {
  background: var(--bg-secondary);
  transform: translateY(0);
}

.modern-button--danger {
  background: var(--danger-600);
  color: white;
}

.modern-button--danger:hover:not(.modern-button--disabled) {
  background: var(--danger-700);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.modern-button--danger:focus:not(.modern-button--disabled) {
  box-shadow: 0 0 0 3px var(--danger-100);
}

.modern-button--danger:active:not(.modern-button--disabled) {
  background: var(--danger-800);
  transform: translateY(0);
}

.modern-button--success {
  background: var(--success-600);
  color: white;
}

.modern-button--success:hover:not(.modern-button--disabled) {
  background: var(--success-700);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.modern-button--success:focus:not(.modern-button--disabled) {
  box-shadow: 0 0 0 3px var(--success-100);
}

.modern-button--success:active:not(.modern-button--disabled) {
  background: var(--success-800);
  transform: translateY(0);
}

.modern-button--warning {
  background: var(--warning-600);
  color: white;
}

.modern-button--warning:hover:not(.modern-button--disabled) {
  background: var(--warning-700);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.modern-button--warning:focus:not(.modern-button--disabled) {
  box-shadow: 0 0 0 3px var(--warning-100);
}

.modern-button--warning:active:not(.modern-button--disabled) {
  background: var(--warning-800);
  transform: translateY(0);
}

/* 禁用状态 */
.modern-button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.modern-button--disabled:hover {
  transform: none !important;
  box-shadow: none !important;
}

/* 加载状态 */
.modern-button--loading {
  cursor: wait;
}

.modern-button--loading .modern-button__content {
  opacity: 0.7;
}

/* 块级按钮 */
.modern-button--block {
  width: 100%;
}

/* 圆形按钮 */
.modern-button--circle {
  border-radius: 50%;
  aspect-ratio: 1;
  padding: 0;
}

.modern-button--circle.modern-button--small {
  width: 32px;
}

.modern-button--circle.modern-button--medium {
  width: 40px;
}

.modern-button--circle.modern-button--large {
  width: 48px;
}

/* 仅图标按钮 */
.modern-button--icon-only {
  padding: 0;
  aspect-ratio: 1;
}

.modern-button--icon-only.modern-button--small {
  width: 32px;
}

.modern-button--icon-only.modern-button--medium {
  width: 40px;
}

.modern-button--icon-only.modern-button--large {
  width: 48px;
}

/* 按钮内部元素 */
.modern-button__loading {
  display: flex;
  align-items: center;
}

.modern-button__icon,
.modern-button__right-icon {
  display: flex;
  align-items: center;
  font-size: 1.125rem;
}

.modern-button--small .modern-button__icon,
.modern-button--small .modern-button__right-icon {
  font-size: 1rem;
}

.modern-button--large .modern-button__icon,
.modern-button--large .modern-button__right-icon {
  font-size: 1.25rem;
}

.modern-button__content {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

/* 波纹效果 */
.modern-button__ripple {
  position: absolute;
  border-radius: 50%;
  background: var(--ripple-color, rgba(255, 255, 255, 0.6));
  transform: scale(0);
  animation: ripple 0.6s linear;
  pointer-events: none;
}

@keyframes ripple {
  to {
    transform: scale(4);
    opacity: 0;
  }
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-button--medium {
    height: 36px;
    padding: 0 var(--space-3);
    font-size: var(--font-size-sm);
  }
  
  .modern-button--large {
    height: 44px;
    padding: 0 var(--space-4);
    font-size: var(--font-size-base);
  }
}

/* 无障碍支持 */
.modern-button:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .modern-button {
    transition: none;
  }
  
  .modern-button__ripple {
    animation: none;
    display: none;
  }
}
</style>