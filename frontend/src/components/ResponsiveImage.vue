<template>
  <div class="responsive-image" :class="{ 'loading': isLoading, 'error': hasError }">
    <!-- 图片容器 -->
    <img
      :src="finalSrc"
      :alt="alt"
      :class="imageClass"
      :style="imageStyle"
      @load="handleLoad"
      @error="handleError"
      loading="lazy"
    />
    
    <!-- 加载状态 -->
    <div v-if="isLoading && !hasError" class="image-loading">
      <div class="loading-spinner"></div>
    </div>
    
    <!-- 错误状态 -->
    <div v-if="hasError" class="image-error">
      <el-icon class="error-icon">
        <Picture />
      </el-icon>
      <span class="error-text">图片加载失败</span>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { Picture } from '@element-plus/icons-vue'
import { responsiveImageSize, loadResponsiveImage } from '../utils/responsive'

export default {
  name: 'ResponsiveImage',
  components: {
    Picture
  },
  props: {
    src: {
      type: String,
      required: true
    },
    alt: {
      type: String,
      default: ''
    },
    width: {
      type: [Number, String],
      default: null
    },
    height: {
      type: [Number, String],
      default: null
    },
    maxWidth: {
      type: [Number, String],
      default: null
    },
    maxHeight: {
      type: [Number, String],
      default: null
    },
    objectFit: {
      type: String,
      default: 'cover',
      validator: (value) => ['cover', 'contain', 'fill', 'none', 'scale-down'].includes(value)
    },
    lazy: {
      type: Boolean,
      default: true
    },
    placeholder: {
      type: String,
      default: null
    }
  },
  setup(props) {
    const isLoading = ref(true)
    const hasError = ref(false)
    const finalSrc = ref(props.placeholder || props.src)

    // 响应式图片尺寸
    const responsiveWidth = computed(() => {
      if (props.width) {
        return responsiveImageSize(parseInt(props.width))
      }
      return null
    })

    const responsiveHeight = computed(() => {
      if (props.height) {
        return responsiveImageSize(parseInt(props.height))
      }
      return null
    })

    // 图片样式
    const imageStyle = computed(() => {
      const style = {
        objectFit: props.objectFit
      }

      if (responsiveWidth.value) {
        style.width = `${responsiveWidth.value}px`
      }

      if (responsiveHeight.value) {
        style.height = `${responsiveHeight.value}px`
      }

      if (props.maxWidth) {
        style.maxWidth = typeof props.maxWidth === 'number' ? `${props.maxWidth}px` : props.maxWidth
      }

      if (props.maxHeight) {
        style.maxHeight = typeof props.maxHeight === 'number' ? `${props.maxHeight}px` : props.maxHeight
      }

      return style
    })

    // 图片类名
    const imageClass = computed(() => ({
      'image-loaded': !isLoading.value && !hasError.value
    }))

    // 图片加载处理
    const handleLoad = () => {
      isLoading.value = false
      hasError.value = false
      
      // 如果使用了占位图，加载完成后替换为实际图片
      if (props.placeholder && finalSrc.value === props.placeholder) {
        finalSrc.value = props.src
      }
    }

    // 图片错误处理
    const handleError = () => {
      isLoading.value = false
      hasError.value = true
      
      // 如果加载失败且没有占位图，使用默认占位图
      if (!props.placeholder) {
        finalSrc.value = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjBGMEYwIi8+CjxwYXRoIGQ9Ik04MCA3MEgxMjBWMTMwSDgwVjcwWiIgZmlsbD0iI0RERERERCIvPgo8L3N2Zz4K'
      }
    }

    // 监听src变化
    watch(() => props.src, (newSrc) => {
      if (newSrc) {
        isLoading.value = true
        hasError.value = false
        finalSrc.value = props.placeholder || newSrc
      }
    })

    // 组件挂载时加载图片
    onMounted(async () => {
      if (props.src) {
        try {
          await loadResponsiveImage(props.src)
          finalSrc.value = props.src
        } catch (error) {
          handleError()
        }
      }
    })

    return {
      isLoading,
      hasError,
      finalSrc,
      imageStyle,
      imageClass,
      handleLoad,
      handleError
    }
  }
}
</script>

<style scoped>
.responsive-image {
  position: relative;
  display: inline-block;
  overflow: hidden;
}

.responsive-image img {
  display: block;
  width: 100%;
  height: auto;
  transition: opacity 0.3s ease;
}

.responsive-image.loading img {
  opacity: 0;
}

.responsive-image .image-loaded {
  opacity: 1;
}

/* 加载状态 */
.image-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-color);
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 错误状态 */
.image-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

.error-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.error-text {
  font-size: 0.875rem;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .error-icon {
    font-size: 1.5rem;
  }
  
  .error-text {
    font-size: 0.75rem;
  }
  
  .loading-spinner {
    width: 24px;
    height: 24px;
    border-width: 2px;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>