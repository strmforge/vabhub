<template>
  <el-card
    :header="header"
    :body-style="bodyStyle"
    :shadow="shadow"
    class="vab-card"
    :class="customClass"
  >
    <template #header v-if="$slots.header || header">
      <div class="vab-card-header">
        <slot name="header">
          {{ header }}
        </slot>
        <div v-if="showActions" class="vab-card-actions">
          <slot name="actions"></slot>
        </div>
      </div>
    </template>
    
    <div class="vab-card-content">
      <slot></slot>
    </div>
    
    <template v-if="$slots.footer" #footer>
      <div class="vab-card-footer">
        <slot name="footer"></slot>
      </div>
    </template>
  </el-card>
</template>

<script>
import { ElCard } from 'element-plus'

export default {
  name: 'VabCard',
  components: {
    ElCard
  },
  props: {
    header: {
      type: String,
      default: ''
    },
    bodyStyle: {
      type: Object,
      default: () => ({ padding: '20px' })
    },
    shadow: {
      type: String,
      default: 'hover',
      validator: (value) => {
        return ['always', 'hover', 'never'].includes(value)
      }
    },
    showActions: {
      type: Boolean,
      default: false
    },
    customClass: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.vab-card {
  position: relative;
  border-radius: 12px;
  transition: all 0.3s ease-in-out;
  overflow: hidden;
}

.vab-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--el-color-primary), var(--el-color-success));
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.vab-card:hover::before {
  opacity: 1;
}

.vab-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
  font-weight: 600;
  font-size: 16px;
  color: var(--el-text-color-primary);
}

.vab-card-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.vab-card-content {
  padding: 20px;
}

.vab-card-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--el-border-color-light);
  background-color: var(--el-fill-color-light);
}

/* 无阴影版本 */
.vab-card.is-never-shadow {
  box-shadow: none;
  border: 1px solid var(--el-border-color-light);
}

.vab-card.is-never-shadow:hover {
  border-color: var(--el-border-color);
}

/* 始终显示阴影版本 */
.vab-card.is-always-shadow {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.vab-card.is-always-shadow:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

/* 悬停阴影版本（默认） */
.vab-card.is-hover-shadow {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.vab-card.is-hover-shadow:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* 紧凑版本 */
.vab-card.is-compact .vab-card-header {
  padding: 12px 16px;
}

.vab-card.is-compact .vab-card-content {
  padding: 16px;
}

.vab-card.is-compact .vab-card-footer {
  padding: 12px 16px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .vab-card {
    border-radius: 8px;
    margin: 8px;
  }
  
  .vab-card-header {
    padding: 12px 16px;
    font-size: 14px;
  }
  
  .vab-card-content {
    padding: 16px;
  }
  
  .vab-card-footer {
    padding: 12px 16px;
  }
  
  .vab-card-actions {
    flex-direction: column;
    gap: 4px;
  }
}

/* 暗色主题适配 */
[data-theme="dark"] .vab-card {
  background-color: var(--el-bg-color);
  border-color: var(--el-border-color);
}

[data-theme="dark"] .vab-card-header {
  border-bottom-color: var(--el-border-color);
}

[data-theme="dark"] .vab-card-footer {
  background-color: var(--el-fill-color-dark);
  border-top-color: var(--el-border-color);
}

/* 动画效果 */
@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.vab-card {
  animation: cardFadeIn 0.4s ease-out;
}

/* 特殊样式变体 */
.vab-card.is-primary::before {
  background: linear-gradient(90deg, var(--el-color-primary), var(--el-color-primary-light-3));
}

.vab-card.is-success::before {
  background: linear-gradient(90deg, var(--el-color-success), var(--el-color-success-light-3));
}

.vab-card.is-warning::before {
  background: linear-gradient(90deg, var(--el-color-warning), var(--el-color-warning-light-3));
}

.vab-card.is-danger::before {
  background: linear-gradient(90deg, var(--el-color-danger), var(--el-color-danger-light-3));
}

.vab-card.is-info::before {
  background: linear-gradient(90deg, var(--el-color-info), var(--el-color-info-light-3));
}
</style>