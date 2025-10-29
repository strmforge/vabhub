<template>
  <div :class="containerClasses">
    <!-- 标签 -->
    <label v-if="label" :for="id" class="modern-input__label">
      {{ label }}
      <span v-if="required" class="modern-input__required">*</span>
    </label>
    
    <!-- 输入容器 -->
    <div :class="inputContainerClasses">
      <!-- 前缀图标 -->
      <div v-if="prefixIcon" class="modern-input__prefix">
        <el-icon>
          <component :is="prefixIcon" />
        </el-icon>
      </div>
      
      <!-- 输入框 -->
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :maxlength="maxlength"
        :minlength="minlength"
        :pattern="pattern"
        :autocomplete="autocomplete"
        :autofocus="autofocus"
        :step="step"
        :min="min"
        :max="max"
        :class="inputClasses"
        @input="handleInput"
        @change="handleChange"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown="handleKeydown"
        @keyup="handleKeyup"
        @keypress="handleKeypress"
      />
      
      <!-- 后缀图标 -->
      <div v-if="suffixIcon" class="modern-input__suffix">
        <el-icon>
          <component :is="suffixIcon" />
        </el-icon>
      </div>
      
      <!-- 清除按钮 -->
      <button
        v-if="clearable && modelValue && !disabled"
        class="modern-input__clear"
        @click="handleClear"
        type="button"
        aria-label="清除输入"
      >
        <el-icon>
          <Close />
        </el-icon>
      </button>
      
      <!-- 密码显示切换 -->
      <button
        v-if="type === 'password' && showPasswordToggle"
        class="modern-input__password-toggle"
        @click="togglePasswordVisibility"
        type="button"
        :aria-label="passwordVisible ? '隐藏密码' : '显示密码'"
      >
        <el-icon>
          <component :is="passwordVisible ? 'View' : 'Hide'" />
        </el-icon>
      </button>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="modern-input__loading">
        <LoadingSpinner size="small" />
      </div>
    </div>
    
    <!-- 帮助文本 -->
    <div v-if="helpText" class="modern-input__help">
      {{ helpText }}
    </div>
    
    <!-- 错误信息 -->
    <div v-if="error" class="modern-input__error">
      <el-icon class="modern-input__error-icon">
        <Warning />
      </el-icon>
      <span>{{ error }}</span>
    </div>
    
    <!-- 字符计数 -->
    <div v-if="showCount && maxlength" class="modern-input__count">
      {{ modelValue ? modelValue.length : 0 }} / {{ maxlength }}
    </div>
  </div>
</template>

<script>
import { ref, computed, nextTick } from 'vue'
import LoadingSpinner from './LoadingSpinner.vue'
import { Close, View, Hide, Warning } from '@element-plus/icons-vue'

export default {
  name: 'ModernInput',
  components: {
    LoadingSpinner
  },
  props: {
    // 双向绑定值
    modelValue: {
      type: [String, Number],
      default: ''
    },
    
    // 输入类型
    type: {
      type: String,
      default: 'text',
      validator: (value) => ['text', 'password', 'email', 'tel', 'url', 'number', 'search'].includes(value)
    },
    
    // 标签
    label: {
      type: String,
      default: ''
    },
    
    // 占位符
    placeholder: {
      type: String,
      default: ''
    },
    
    // 尺寸
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
    
    // 是否只读
    readonly: {
      type: Boolean,
      default: false
    },
    
    // 是否必填
    required: {
      type: Boolean,
      default: false
    },
    
    // 错误信息
    error: {
      type: String,
      default: ''
    },
    
    // 帮助文本
    helpText: {
      type: String,
      default: ''
    },
    
    // 前缀图标
    prefixIcon: {
      type: String,
      default: ''
    },
    
    // 后缀图标
    suffixIcon: {
      type: String,
      default: ''
    },
    
    // 是否可清除
    clearable: {
      type: Boolean,
      default: false
    },
    
    // 是否显示密码切换
    showPasswordToggle: {
      type: Boolean,
      default: true
    },
    
    // 是否显示字符计数
    showCount: {
      type: Boolean,
      default: false
    },
    
    // 最大长度
    maxlength: {
      type: Number,
      default: null
    },
    
    // 最小长度
    minlength: {
      type: Number,
      default: null
    },
    
    // 正则模式
    pattern: {
      type: String,
      default: ''
    },
    
    // 自动完成
    autocomplete: {
      type: String,
      default: 'off'
    },
    
    // 自动聚焦
    autofocus: {
      type: Boolean,
      default: false
    },
    
    // 步长（数字输入）
    step: {
      type: [String, Number],
      default: null
    },
    
    // 最小值
    min: {
      type: [String, Number],
      default: null
    },
    
    // 最大值
    max: {
      type: [String, Number],
      default: null
    },
    
    // 是否加载中
    loading: {
      type: Boolean,
      default: false
    },
    
    // 输入框ID
    id: {
      type: String,
      default: ''
    }
  },
  emits: [
    'update:modelValue',
    'input',
    'change',
    'focus',
    'blur',
    'keydown',
    'keyup',
    'keypress',
    'clear'
  ],
  setup(props, { emit }) {
    // 响应式状态
    const isFocused = ref(false)
    const passwordVisible = ref(false)
    
    // 计算属性
    const containerClasses = computed(() => ({
      'modern-input': true,
      'modern-input--focused': isFocused.value,
      'modern-input--disabled': props.disabled,
      'modern-input--error': props.error,
      'modern-input--loading': props.loading
    }))
    
    const inputContainerClasses = computed(() => ({
      'modern-input__container': true,
      [`modern-input__container--${props.size}`]: true,
      'modern-input__container--focused': isFocused.value,
      'modern-input__container--disabled': props.disabled,
      'modern-input__container--error': props.error,
      'modern-input__container--with-prefix': props.prefixIcon,
      'modern-input__container--with-suffix': props.suffixIcon || props.clearable || (props.type === 'password' && props.showPasswordToggle)
    }))
    
    const inputClasses = computed(() => ({
      'modern-input__field': true,
      [`modern-input__field--${props.size}`]: true
    }))
    
    const actualType = computed(() => {
      if (props.type === 'password' && passwordVisible.value) {
        return 'text'
      }
      return props.type
    })
    
    // 方法
    const handleInput = (event) => {
      const value = event.target.value
      emit('update:modelValue', value)
      emit('input', value, event)
    }
    
    const handleChange = (event) => {
      emit('change', event.target.value, event)
    }
    
    const handleFocus = (event) => {
      isFocused.value = true
      emit('focus', event)
    }
    
    const handleBlur = (event) => {
      isFocused.value = false
      emit('blur', event)
    }
    
    const handleKeydown = (event) => {
      emit('keydown', event)
    }
    
    const handleKeyup = (event) => {
      emit('keyup', event)
    }
    
    const handleKeypress = (event) => {
      emit('keypress', event)
    }
    
    const handleClear = () => {
      emit('update:modelValue', '')
      emit('clear')
      
      // 聚焦输入框
      nextTick(() => {
        const input = document.getElementById(props.id)
        if (input) {
          input.focus()
        }
      })
    }
    
    const togglePasswordVisibility = () => {
      passwordVisible.value = !passwordVisible.value
    }
    
    // 生成唯一ID
    const generateId = () => {
      return `modern-input-${Math.random().toString(36).substr(2, 9)}`
    }
    
    // 设置ID
    const inputId = props.id || generateId()
    
    return {
      isFocused,
      passwordVisible,
      containerClasses,
      inputContainerClasses,
      inputClasses,
      actualType,
      inputId,
      handleInput,
      handleChange,
      handleFocus,
      handleBlur,
      handleKeydown,
      handleKeyup,
      handleKeypress,
      handleClear,
      togglePasswordVisibility
    }
  }
}
</script>

<style scoped>
.modern-input {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;
}

/* 标签 */
.modern-input__label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.modern-input__required {
  color: var(--danger-500);
  margin-left: var(--space-1);
}

/* 输入容器 */
.modern-input__container {
  position: relative;
  display: flex;
  align-items: center;
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  transition: all 0.2s ease;
  overflow: hidden;
}

.modern-input__container--focused {
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px var(--primary-100);
}

.modern-input__container--error {
  border-color: var(--danger-500);
  box-shadow: 0 0 0 3px var(--danger-100);
}

.modern-input__container--disabled {
  background: var(--bg-tertiary);
  border-color: var(--border-primary);
  opacity: 0.6;
  cursor: not-allowed;
}

/* 尺寸 */
.modern-input__container--small {
  height: 32px;
}

.modern-input__container--medium {
  height: 40px;
}

.modern-input__container--large {
  height: 48px;
}

/* 前缀/后缀图标 */
.modern-input__prefix,
.modern-input__suffix {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.modern-input__prefix {
  padding-left: var(--space-3);
  padding-right: var(--space-2);
}

.modern-input__suffix {
  padding-left: var(--space-2);
  padding-right: var(--space-3);
}

.modern-input__container--small .modern-input__prefix,
.modern-input__container--small .modern-input__suffix {
  font-size: 1rem;
}

.modern-input__container--medium .modern-input__prefix,
.modern-input__container--medium .modern-input__suffix {
  font-size: 1.125rem;
}

.modern-input__container--large .modern-input__prefix,
.modern-input__container--large .modern-input__suffix {
  font-size: 1.25rem;
}

/* 输入框 */
.modern-input__field {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  color: var(--text-primary);
  font-family: inherit;
  font-size: inherit;
  width: 100%;
  height: 100%;
  padding: 0 var(--space-3);
}

.modern-input__container--with-prefix .modern-input__field {
  padding-left: var(--space-2);
}

.modern-input__container--with-suffix .modern-input__field {
  padding-right: var(--space-2);
}

.modern-input__field--small {
  font-size: var(--font-size-sm);
}

.modern-input__field--medium {
  font-size: var(--font-size-base);
}

.modern-input__field--large {
  font-size: var(--font-size-lg);
}

.modern-input__field::placeholder {
  color: var(--text-tertiary);
}

.modern-input__field:disabled {
  cursor: not-allowed;
}

/* 清除按钮 */
.modern-input__clear {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
  margin-right: var(--space-1);
}

.modern-input__clear:hover {
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

.modern-input__clear:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 密码切换按钮 */
.modern-input__password-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
  margin-right: var(--space-1);
}

.modern-input__password-toggle:hover {
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

.modern-input__password-toggle:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 加载状态 */
.modern-input__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--space-2);
}

/* 帮助文本 */
.modern-input__help {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-top: var(--space-1);
}

/* 错误信息 */
.modern-input__error {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--danger-600);
  margin-top: var(--space-1);
}

.modern-input__error-icon {
  font-size: 0.875rem;
}

/* 字符计数 */
.modern-input__count {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  text-align: right;
  margin-top: var(--space-1);
}

.modern-input--error .modern-input__count {
  color: var(--danger-600);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-input__container--medium {
    height: 36px;
  }
  
  .modern-input__container--large {
    height: 44px;
  }
  
  .modern-input__field--medium {
    font-size: var(--font-size-sm);
  }
  
  .modern-input__field--large {
    font-size: var(--font-size-base);
  }
}

/* 无障碍支持 */
.modern-input__container:focus-within {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .modern-input__container {
    transition: none;
  }
}
</style>