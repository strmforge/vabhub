<template>
  <div :class="spinnerClasses" :style="spinnerStyle">
    <div class="modern-spinner__container">
      <div class="modern-spinner__circle"></div>
      <div class="modern-spinner__circle"></div>
      <div class="modern-spinner__circle"></div>
      <div class="modern-spinner__circle"></div>
    </div>
    
    <!-- 加载文本 -->
    <span v-if="text" class="modern-spinner__text">{{ text }}</span>
    
    <!-- 进度指示器 -->
    <div v-if="showProgress" class="modern-spinner__progress">
      <div class="modern-spinner__progress-bar" :style="{ width: progress + '%' }"></div>
      <span class="modern-spinner__progress-text">{{ progress }}%</span>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'LoadingSpinner',
  props: {
    // 尺寸
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large', 'xlarge'].includes(value)
    },
    
    // 颜色
    color: {
      type: String,
      default: 'primary'
    },
    
    // 类型
    type: {
      type: String,
      default: 'default',
      validator: (value) => ['default', 'dots', 'ring', 'pulse', 'progress'].includes(value)
    },
    
    // 加载文本
    text: {
      type: String,
      default: ''
    },
    
    // 是否显示进度
    showProgress: {
      type: Boolean,
      default: false
    },
    
    // 进度值 (0-100)
    progress: {
      type: Number,
      default: 0,
      validator: (value) => value >= 0 && value <= 100
    },
    
    // 是否居中
    center: {
      type: Boolean,
      default: false
    },
    
    // 是否块级显示
    block: {
      type: Boolean,
      default: false
    },
    
    // 自定义尺寸
    customSize: {
      type: String,
      default: ''
    },
    
    // 自定义颜色
    customColor: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    // 计算属性
    const spinnerClasses = computed(() => ({
      'modern-spinner': true,
      [`modern-spinner--${props.size}`]: true,
      [`modern-spinner--${props.type}`]: true,
      [`modern-spinner--${props.color}`]: true,
      'modern-spinner--center': props.center,
      'modern-spinner--block': props.block,
      'modern-spinner--with-text': props.text,
      'modern-spinner--with-progress': props.showProgress
    }))
    
    const spinnerStyle = computed(() => ({
      '--spinner-size': props.customSize || '',
      '--spinner-color': props.customColor || ''
    }))
    
    return {
      spinnerClasses,
      spinnerStyle
    }
  }
}
</script>

<style scoped>
.modern-spinner {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.modern-spinner--center {
  justify-content: center;
  align-items: center;
}

.modern-spinner--block {
  width: 100%;
}

/* 默认加载器 */
.modern-spinner__container {
  position: relative;
  width: var(--spinner-size, 40px);
  height: var(--spinner-size, 40px);
}

.modern-spinner--small .modern-spinner__container {
  width: var(--spinner-size, 24px);
  height: var(--spinner-size, 24px);
}

.modern-spinner--medium .modern-spinner__container {
  width: var(--spinner-size, 40px);
  height: var(--spinner-size, 40px);
}

.modern-spinner--large .modern-spinner__container {
  width: var(--spinner-size, 56px);
  height: var(--spinner-size, 56px);
}

.modern-spinner--xlarge .modern-spinner__container {
  width: var(--spinner-size, 80px);
  height: var(--spinner-size, 80px);
}

.modern-spinner__circle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: var(--spinner-color, var(--primary-500));
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.modern-spinner__circle:nth-child(2) {
  border: 3px solid transparent;
  border-right-color: var(--spinner-color, var(--primary-400));
  animation-delay: 0.1s;
}

.modern-spinner__circle:nth-child(3) {
  border: 3px solid transparent;
  border-bottom-color: var(--spinner-color, var(--primary-300));
  animation-delay: 0.2s;
}

.modern-spinner__circle:nth-child(4) {
  border: 3px solid transparent;
  border-left-color: var(--spinner-color, var(--primary-200));
  animation-delay: 0.3s;
}

/* 点状加载器 */
.modern-spinner--dots .modern-spinner__container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.modern-spinner--dots .modern-spinner__circle {
  position: static;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--spinner-color, var(--primary-500));
  animation: bounce 1.4s ease-in-out infinite both;
  border: none;
}

.modern-spinner--dots .modern-spinner__circle:nth-child(1) {
  animation-delay: -0.32s;
}

.modern-spinner--dots .modern-spinner__circle:nth-child(2) {
  animation-delay: -0.16s;
}

.modern-spinner--dots .modern-spinner__circle:nth-child(3) {
  animation-delay: 0s;
}

/* 环形加载器 */
.modern-spinner--ring .modern-spinner__container {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 3px solid var(--spinner-color, var(--primary-500));
  animation: spin 1s linear infinite;
}

.modern-spinner--ring .modern-spinner__circle {
  display: none;
}

/* 脉冲加载器 */
.modern-spinner--pulse .modern-spinner__container {
  background: var(--spinner-color, var(--primary-500));
  border-radius: 50%;
  animation: pulse 1.5s ease-in-out infinite both;
}

.modern-spinner--pulse .modern-spinner__circle {
  display: none;
}

/* 进度加载器 */
.modern-spinner--progress .modern-spinner__container {
  width: 100%;
  height: 4px;
  background: var(--bg-tertiary);
  border-radius: 2px;
  overflow: hidden;
}

.modern-spinner--progress .modern-spinner__circle {
  display: none;
}

.modern-spinner__progress {
  width: 100%;
  max-width: 200px;
}

.modern-spinner__progress-bar {
  height: 100%;
  background: var(--spinner-color, var(--primary-500));
  border-radius: 2px;
  transition: width 0.3s ease;
}

.modern-spinner__progress-text {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-top: var(--space-1);
}

/* 加载文本 */
.modern-spinner__text {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  text-align: center;
}

.modern-spinner--small .modern-spinner__text {
  font-size: var(--font-size-xs);
}

.modern-spinner--large .modern-spinner__text,
.modern-spinner--xlarge .modern-spinner__text {
  font-size: var(--font-size-base);
}

/* 颜色变体 */
.modern-spinner--primary .modern-spinner__circle,
.modern-spinner--primary .modern-spinner__container {
  border-top-color: var(--primary-500);
}

.modern-spinner--secondary .modern-spinner__circle,
.modern-spinner--secondary .modern-spinner__container {
  border-top-color: var(--gray-500);
}

.modern-spinner--success .modern-spinner__circle,
.modern-spinner--success .modern-spinner__container {
  border-top-color: var(--success-500);
}

.modern-spinner--warning .modern-spinner__circle,
.modern-spinner--warning .modern-spinner__container {
  border-top-color: var(--warning-500);
}

.modern-spinner--danger .modern-spinner__circle,
.modern-spinner--danger .modern-spinner__container {
  border-top-color: var(--danger-500);
}

.modern-spinner--white .modern-spinner__circle,
.modern-spinner--white .modern-spinner__container {
  border-top-color: white;
}

/* 动画 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
  100% {
    transform: scale(0.8);
    opacity: 0.8;
  }
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-spinner--medium .modern-spinner__container {
    width: var(--spinner-size, 32px);
    height: var(--spinner-size, 32px);
  }
  
  .modern-spinner--large .modern-spinner__container {
    width: var(--spinner-size, 48px);
    height: var(--spinner-size, 48px);
  }
  
  .modern-spinner--xlarge .modern-spinner__container {
    width: var(--spinner-size, 64px);
    height: var(--spinner-size, 64px);
  }
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .modern-spinner__circle,
  .modern-spinner__container {
    animation: none;
  }
  
  .modern-spinner--dots .modern-spinner__circle {
    animation: none;
    opacity: 0.6;
  }
  
  .modern-spinner--dots .modern-spinner__circle:nth-child(1) {
    opacity: 0.3;
  }
  
  .modern-spinner--dots .modern-spinner__circle:nth-child(2) {
    opacity: 0.6;
  }
  
  .modern-spinner--dots .modern-spinner__circle:nth-child(3) {
    opacity: 0.9;
  }
}
</style>