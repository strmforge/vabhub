<template>
  <div class="dashboard-widget">
    <el-card class="widget-card" shadow="hover">
      <template #header>
        <div class="widget-header">
          <div class="header-left">
            <el-icon><component :is="widget.icon" /></el-icon>
            <span class="widget-title">{{ widget.title }}</span>
          </div>
          <div class="header-right">
            <el-button-group size="small">
              <el-button @click="$emit('refresh')" :loading="loading">
                <el-icon><Refresh /></el-icon>
              </el-button>
              <el-button @click="$emit('configure')">
                <el-icon><Setting /></el-icon>
              </el-button>
              <el-button @click="$emit('remove')" type="danger">
                <el-icon><Close /></el-icon>
              </el-button>
            </el-button-group>
          </div>
        </div>
      </template>
      
      <div class="widget-content">
        <div v-if="loading" class="loading-container">
          <el-icon class="loading-icon"><Loading /></el-icon>
          <span>加载中...</span>
        </div>
        
        <div v-else-if="error" class="error-container">
          <el-icon class="error-icon"><Warning /></el-icon>
          <span>{{ error }}</span>
        </div>
        
        <div v-else class="data-container">
          <!-- 根据组件类型显示不同的内容 -->
          <div v-if="widget.id === 'stats'" class="stats-widget">
            <div class="stat-item">
              <span class="stat-value">{{ data?.total || 0 }}</span>
              <span class="stat-label">总数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ data?.active || 0 }}</span>
              <span class="stat-label">活跃</span>
            </div>
          </div>
          
          <div v-else-if="widget.id === 'chart'" class="chart-widget">
            <div class="chart-placeholder">
              <el-icon><TrendCharts /></el-icon>
              <span>图表组件</span>
            </div>
          </div>
          
          <div v-else class="default-widget">
            <p>{{ widget.description }}</p>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Refresh, Setting, Close, Loading, Warning } from '@element-plus/icons-vue'

// 定义 props
interface Widget {
  id: string
  title: string
  description: string
  icon: string
  category: string
  minW: number
  minH: number
  defaultW: number
  defaultH: number
}

interface Props {
  widget: Widget
  data?: any
}

const props = defineProps<Props>()

// 定义 emits
defineEmits<{
  refresh: []
  configure: []
  remove: []
}>()

// 响应式数据
const loading = ref(false)
const error = ref('')

// 模拟数据加载
const loadData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // 模拟 API 调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 根据组件类型返回模拟数据
    if (props.widget.id === 'stats') {
      return { total: 150, active: 87 }
    } else if (props.widget.id === 'chart') {
      return { data: [10, 20, 30, 40, 50] }
    }
    
    return { message: '组件数据加载成功' }
  } catch (err) {
    error.value = '数据加载失败'
    throw err
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadData()
})

// 暴露方法给父组件
const refresh = () => {
  loadData()
}

defineExpose({
  refresh
})
</script>

<style scoped>
.dashboard-widget {
  height: 100%;
}

.widget-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.widget-title {
  font-weight: 600;
}

.widget-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--el-color-info);
}

.loading-icon {
  animation: spin 1s linear infinite;
}

.error-icon {
  color: var(--el-color-error);
}

.stats-widget {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.chart-placeholder,
.default-widget {
  text-align: center;
  color: var(--el-text-color-secondary);
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>