<template>
  <el-button
    :type="type"
    :size="size"
    :plain="plain"
    :round="round"
    :circle="circle"
    :disabled="disabled"
    :loading="loading"
    :icon="icon"
    :autofocus="autofocus"
    :native-type="nativeType"
    @click="handleClick"
    class="vab-button"
    :class="customClass"
  >
    <slot></slot>
  </el-button>
</template>

<script>
import { ElButton } from 'element-plus'

export default {
  name: 'VabButton',
  components: {
    ElButton
  },
  props: {
    type: {
      type: String,
      default: 'default',
      validator: (value) => {
        return ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
      }
    },
    size: {
      type: String,
      default: 'default',
      validator: (value) => {
        return ['large', 'default', 'small'].includes(value)
      }
    },
    plain: {
      type: Boolean,
      default: false
    },
    round: {
      type: Boolean,
      default: false
    },
    circle: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: ''
    },
    autofocus: {
      type: Boolean,
      default: false
    },
    nativeType: {
      type: String,
      default: 'button',
      validator: (value) => {
        return ['button', 'submit', 'reset'].includes(value)
      }
    },
    customClass: {
      type: String,
      default: ''
    }
  },
  emits: ['click'],
  methods: {
    handleClick(event) {
      this.$emit('click', event)
    }
  }
}
</script>

<style scoped>
.vab-button {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease-in-out;
}

.vab-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.vab-button:hover::before {
  left: 100%;
}

/* 主按钮特殊效果 */
.vab-button.el-button--primary {
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.vab-button.el-button--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.vab-button.el-button--primary:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
}

/* 成功按钮效果 */
.vab-button.el-button--success {
  box-shadow: 0 2px 8px rgba(103, 194, 58, 0.3);
}

.vab-button.el-button--success:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.4);
}

/* 警告按钮效果 */
.vab-button.el-button--warning {
  box-shadow: 0 2px 8px rgba(230, 162, 60, 0.3);
}

.vab-button.el-button--warning:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(230, 162, 60, 0.4);
}

/* 危险按钮效果 */
.vab-button.el-button--danger {
  box-shadow: 0 2px 8px rgba(245, 108, 108, 0.3);
}

.vab-button.el-button--danger:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.4);
}

/* 加载状态 */
.vab-button.is-loading {
  pointer-events: none;
}

/* 禁用状态 */
.vab-button.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 圆形按钮 */
.vab-button.is-circle {
  border-radius: 50%;
}

/* 圆角按钮 */
.vab-button.is-round {
  border-radius: 20px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .vab-button {
    font-size: 14px;
    padding: 8px 16px;
  }
  
  .vab-button.el-button--large {
    font-size: 16px;
    padding: 12px 24px;
  }
  
  .vab-button.el-button--small {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>