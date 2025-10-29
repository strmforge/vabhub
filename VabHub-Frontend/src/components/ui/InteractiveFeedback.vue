<template>
  <div class="interactive-feedback">
    <!-- 悬停效果容器 -->
    <div
      v-if="enableHover"
      class="interactive-feedback__hover"
      :class="hoverClasses"
      @mouseenter="handleHoverEnter"
      @mouseleave="handleHoverLeave"
    >
      <slot name="hover">
        <div class="interactive-feedback__hover-content">
          <el-icon v-if="hoverIcon" class="interactive-feedback__hover-icon">
            <component :is="hoverIcon" />
          </el-icon>
          <span class="interactive-feedback__hover-text">{{ hoverText }}</span>
        </div>
      </slot>
    </div>

    <!-- 点击效果容器 -->
    <div
      v-if="enableClick"
      class="interactive-feedback__click"
      :class="clickClasses"
      @click="handleClick"
      @mousedown="handleMouseDown"
      @mouseup="handleMouseUp"
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
    >
      <slot name="click">
        <button class="interactive-feedback__click-btn">
          <el-icon v-if="clickIcon" class="interactive-feedback__click-icon">
            <component :is="clickIcon" />
          </el-icon>
          <span class="interactive-feedback__click-text">{{ clickText }}</span>
        </button>
      </slot>
    </div>

    <!-- 加载状态 -->
    <div
      v-if="loading"
      class="interactive-feedback__loading"
      :class="loadingClasses"
    >
      <slot name="loading">
        <LoadingSpinner
          :size="loadingSize"
          :color="loadingColor"
          :message="loadingMessage"
        />
      </slot>
    </div>

    <!-- 成功状态 -->
    <div
      v-if="success"
      class="interactive-feedback__success"
      :class="successClasses"
    >
      <slot name="success">
        <div class="interactive-feedback__success-content">
          <el-icon class="interactive-feedback__success-icon">
            <Check />
          </el-icon>
          <span class="interactive-feedback__success-text">{{ successText }}</span>
        </div>
      </slot>
    </div>

    <!-- 错误状态 -->
    <div
      v-if="error"
      class="interactive-feedback__error"
      :class="errorClasses"
    >
      <slot name="error">
        <div class="interactive-feedback__error-content">
          <el-icon class="interactive-feedback__error-icon">
            <Close />
          </el-icon>
          <span class="interactive-feedback__error-text">{{ errorText }}</span>
        </div>
      </slot>
    </div>

    <!-- 波纹效果 -->
    <div
      v-if="showRipple"
      class="interactive-feedback__ripple"
      :style="rippleStyle"
    ></div>

    <!-- 脉冲效果 -->
    <div
      v-if="showPulse"
      class="interactive-feedback__pulse"
      :style="pulseStyle"
    ></div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import LoadingSpinner from './LoadingSpinner.vue'
import { Check, Close } from '@element-plus/icons-vue'

export default {
  name: 'InteractiveFeedback',
  components: {
    LoadingSpinner,
    Check,
    Close
  },
  props: {
    // 悬停效果配置
    enableHover: {
      type: Boolean,
      default: true
    },
    hoverEffect: {
      type: String,
      default: 'scale', // 'scale', 'glow', 'shadow', 'border'
      validator: (value) => ['scale', 'glow', 'shadow', 'border'].includes(value)
    },
    hoverIcon: {
      type: [String, Object],
      default: null
    },
    hoverText: {
      type: String,
      default: '悬停效果'
    },

    // 点击效果配置
    enableClick: {
      type: Boolean,
      default: true
    },
    clickEffect: {
      type: String,
      default: 'ripple', // 'ripple', 'pulse', 'bounce', 'press'
      validator: (value) => ['ripple', 'pulse', 'bounce', 'press'].includes(value)
    },
    clickIcon: {
      type: [String, Object],
      default: null
    },
    clickText: {
      type: String,
      default: '点击效果'
    },

    // 状态配置
    loading: {
      type: Boolean,
      default: false
    },
    loadingSize: {
      type: String,
      default: 'small'
    },
    loadingColor: {
      type: String,
      default: 'primary'
    },
    loadingMessage: {
      type: String,
      default: '加载中...'
    },

    success: {
      type: Boolean,
      default: false
    },
    successText: {
      type: String,
      default: '操作成功'
    },

    error: {
      type: Boolean,
      default: false
    },
    errorText: {
      type: String,
      default: '操作失败'
    },

    // 动画配置
    animationDuration: {
      type: Number,
      default: 400
    },
    rippleColor: {
      type: String,
      default: 'rgba(255, 255, 255, 0.6)'
    }
  },
  emits: ['hover', 'click'],
  setup(props, { emit }) {
    // 状态管理
    const isHovering = ref(false)
    const isClicking = ref(false)
    const showRipple = ref(false)
    const showPulse = ref(false)
    const ripplePosition = ref({ x: 0, y: 0 })
    const pulsePosition = ref({ x: 0, y: 0 })

    // 悬停类名
    const hoverClasses = computed(() => ({
      'interactive-feedback__hover--active': isHovering.value,
      'interactive-feedback__hover--scale': props.hoverEffect === 'scale',
      'interactive-feedback__hover--glow': props.hoverEffect === 'glow',
      'interactive-feedback__hover--shadow': props.hoverEffect === 'shadow',
      'interactive-feedback__hover--border': props.hoverEffect === 'border'
    }))

    // 点击类名
    const clickClasses = computed(() => ({
      'interactive-feedback__click--active': isClicking.value,
      'interactive-feedback__click--ripple': props.clickEffect === 'ripple',
      'interactive-feedback__click--pulse': props.clickEffect === 'pulse',
      'interactive-feedback__click--bounce': props.clickEffect === 'bounce',
      'interactive-feedback__click--press': props.clickEffect === 'press'
    }))

    // 加载类名
    const loadingClasses = computed(() => ({
      'interactive-feedback__loading--active': props.loading
    }))

    // 成功类名
    const successClasses = computed(() => ({
      'interactive-feedback__success--active': props.success
    }))

    // 错误类名
    const errorClasses = computed(() => ({
      'interactive-feedback__error--active': props.error
    }))

    // 波纹样式
    const rippleStyle = computed(() => ({
      left: ripplePosition.value.x + 'px',
      top: ripplePosition.value.y + 'px',
      '--ripple-color': props.rippleColor,
      '--animation-duration': props.animationDuration + 'ms'
    }))

    // 脉冲样式
    const pulseStyle = computed(() => ({
      left: pulsePosition.value.x + 'px',
      top: pulsePosition.value.y + 'px',
      '--animation-duration': props.animationDuration + 'ms'
    }))

    // 悬停事件处理
    const handleHoverEnter = (event) => {
      isHovering.value = true
      emit('hover', { type: 'enter', event })
    }

    const handleHoverLeave = (event) => {
      isHovering.value = false
      emit('hover', { type: 'leave', event })
    }

    // 点击事件处理
    const handleClick = (event) => {
      emit('click', { event, state: 'clicked' })
    }

    const handleMouseDown = (event) => {
      isClicking.value = true
      
      if (props.clickEffect === 'ripple') {
        showRippleEffect(event)
      } else if (props.clickEffect === 'pulse') {
        showPulseEffect(event)
      }
    }

    const handleMouseUp = () => {
      isClicking.value = false
    }

    const handleTouchStart = (event) => {
      isClicking.value = true
      
      if (props.clickEffect === 'ripple') {
        showRippleEffect(event.touches[0])
      } else if (props.clickEffect === 'pulse') {
        showPulseEffect(event.touches[0])
      }
    }

    const handleTouchEnd = () => {
      isClicking.value = false
    }

    // 显示波纹效果
    const showRippleEffect = (event) => {
      const rect = event.currentTarget.getBoundingClientRect()
      ripplePosition.value = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
      }
      showRipple.value = true
      
      setTimeout(() => {
        showRipple.value = false
      }, props.animationDuration)
    }

    // 显示脉冲效果
    const showPulseEffect = (event) => {
      const rect = event.currentTarget.getBoundingClientRect()
      pulsePosition.value = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
      }
      showPulse.value = true
      
      setTimeout(() => {
        showPulse.value = false
      }, props.animationDuration)
    }

    return {
      isHovering,
      isClicking,
      showRipple,
      showPulse,
      hoverClasses,
      clickClasses,
      loadingClasses,
      successClasses,
      errorClasses,
      rippleStyle,
      pulseStyle,
      handleHoverEnter,
      handleHoverLeave,
      handleClick,
      handleMouseDown,
      handleMouseUp,
      handleTouchStart,
      handleTouchEnd
    }
  }
}
</script>

<style scoped>
.interactive-feedback {
  position: relative;
  display: inline-block;
}

/* 悬停效果 */
.interactive-feedback__hover {
  transition: all var(--transition-normal);
  cursor: pointer;
}

.interactive-feedback__hover--scale {
  transform: scale(1);
}

.interactive-feedback__hover--scale.interactive-feedback__hover--active {
  transform: scale(1.05);
}

.interactive-feedback__hover--glow {
  box-shadow: 0 0 0 rgba(0, 0, 0, 0);
}

.interactive-feedback__hover--glow.interactive-feedback__hover--active {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}

.interactive-feedback__hover--shadow {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.interactive-feedback__hover--shadow.interactive-feedback__hover--active {
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.2));
}

.interactive-feedback__hover--border {
  border: 2px solid transparent;
}

.interactive-feedback__hover--border.interactive-feedback__hover--active {
  border-color: var(--primary-500);
}

.interactive-feedback__hover-content {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
}

.interactive-feedback__hover-icon {
  font-size: 1.1rem;
}

/* 点击效果 */
.interactive-feedback__click {
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.interactive-feedback__click-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--primary-600);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.interactive-feedback__click-btn:hover {
  background: var(--primary-700);
}

.interactive-feedback__click--ripple.interactive-feedback__click--active {
  transform: scale(0.98);
}

.interactive-feedback__click--pulse.interactive-feedback__click--active {
  animation: pulse var(--animation-duration) ease-out;
}

.interactive-feedback__click--bounce.interactive-feedback__click--active {
  animation: bounce var(--animation-duration) ease-out;
}

.interactive-feedback__click--press.interactive-feedback__click--active {
  transform: translateY(2px);
}

/* 波纹效果 */
.interactive-feedback__ripple {
  position: absolute;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: var(--ripple-color);
  transform: translate(-50%, -50%);
  animation: ripple var(--animation-duration) ease-out;
  pointer-events: none;
}

@keyframes ripple {
  0% {
    width: 0;
    height: 0;
    opacity: 0.8;
  }
  100% {
    width: 200px;
    height: 200px;
    opacity: 0;
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translateY(0);
  }
  40%, 43% {
    transform: translateY(-10px);
  }
  70% {
    transform: translateY(-5px);
  }
  90% {
    transform: translateY(-2px);
  }
}

/* 状态样式 */
.interactive-feedback__loading,
.interactive-feedback__success,
.interactive-feedback__error {
  transition: all var(--transition-normal);
}

.interactive-feedback__success-content,
.interactive-feedback__error-content {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
}

.interactive-feedback__success-content {
  background: var(--success-100);
  color: var(--success-700);
  border: 1px solid var(--success-300);
}

.interactive-feedback__error-content {
  background: var(--error-100);
  color: var(--error-700);
  border: 1px solid var(--error-300);
}

.interactive-feedback__success-icon {
  color: var(--success-500);
}

.interactive-feedback__error-icon {
  color: var(--error-500);
}

/* 无障碍访问 */
.interactive-feedback__hover:focus-visible,
.interactive-feedback__click-btn:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .interactive-feedback__hover,
  .interactive-feedback__click,
  .interactive-feedback__click-btn {
    transition: none;
  }
  
  .interactive-feedback__ripple,
  .interactive-feedback__click--pulse,
  .interactive-feedback__click--bounce {
    animation: none;
  }
  
  .interactive-feedback__hover--scale.interactive-feedback__hover--active,
  .interactive-feedback__click--press.interactive-feedback__click--active {
    transform: none;
  }
}

/* 深色主题适配 */
[data-theme="dark"] .interactive-feedback__hover-content {
  background: var(--bg-secondary);
}

[data-theme="dark"] .interactive-feedback__success-content {
  background: var(--success-900);
  color: var(--success-300);
  border-color: var(--success-700);
}

[data-theme="dark"] .interactive-feedback__error-content {
  background: var(--error-900);
  color: var(--error-300);
  border-color: var(--error-700);
}
</style>