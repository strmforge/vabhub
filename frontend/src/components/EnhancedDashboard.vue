<template>
  <div class="enhanced-dashboard">
    <!-- 顶部导航栏 -->
    <el-header class="dashboard-header">
      <div class="header-left">
        <h1 class="dashboard-title">VabHub 仪表盘</h1>
        <el-tag type="success" size="small">v{{ version }}</el-tag>
      </div>
      <div class="header-right">
        <el-button-group>
          <el-button 
            :type="refreshMode === 'auto' ? 'primary' : 'default'"
            @click="toggleRefreshMode"
            size="small"
          >
            <el-icon><Refresh /></el-icon>
            {{ refreshMode === 'auto' ? '自动刷新' : '手动刷新' }}
          </el-button>
          <el-button @click="toggleTheme" size="small">
            <el-icon><Moon v-if="isDarkTheme" /><Sunny v-else /></el-icon>
            {{ isDarkTheme ? '暗色' : '亮色' }}
          </el-button>
          <el-button @click="exportDashboard" size="small">
            <el-icon><Download /></el-icon>
            导出
          </el-button>
        </el-button-group>
      </div>
    </el-header>

    <!-- 可拖拽仪表盘 -->
    <grid-layout
      :layout.sync="dashboardLayout"
      :col-num="12"
      :row-height="30"
      :is-draggable="true"
      :is-resizable="true"
      :vertical-compact="true"
      :margin="[10, 10]"
      :use-css-transforms="true"
      @layout-updated="onLayoutUpdated"
    >
      <grid-item
        v-for="item in dashboardLayout"
        :key="item.i"
        :x="item.x"
        :y="item.y"
        :w="item.w"
        :h="item.h"
        :i="item.i"
        @resized="onItemResized"
        @dragged="onItemDragged"
      >
        <dashboard-widget
          :widget="getWidgetConfig(item.i)"
          :data="widgetData[item.i]"
          @refresh="refreshWidget"
          @configure="configureWidget"
          @remove="removeWidget"
        />
      </grid-item>
    </grid-layout>

    <!-- 添加组件面板 -->
    <el-drawer
      v-model="widgetDrawerVisible"
      title="添加组件"
      direction="rtl"
      size="300px"
    >
      <div class="widget-panel">
        <el-input
          v-model="widgetSearch"
          placeholder="搜索组件..."
          prefix-icon="Search"
          clearable
        />
        <div class="widget-categories">
          <el-collapse v-model="activeCategories">
            <el-collapse-item
              v-for="category in widgetCategories"
              :key="category.name"
              :title="category.label"
              :name="category.name"
            >
              <div class="widget-list">
                <el-card
                  v-for="widget in getCategoryWidgets(category.name)"
                  :key="widget.id"
                  shadow="hover"
                  class="widget-card"
                  @click="addWidget(widget)"
                >
                  <template #header>
                    <div class="widget-header">
                      <el-icon><component :is="widget.icon" /></el-icon>
                      <span>{{ widget.title }}</span>
                    </div>
                  </template>
                  <div class="widget-description">
                    {{ widget.description }}
                  </div>
                </el-card>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>
    </el-drawer>

    <!-- 浮动操作按钮 -->
    <div class="floating-actions">
      <el-tooltip content="添加组件" placement="left">
        <el-button
          type="primary"
          circle
          size="large"
          @click="widgetDrawerVisible = true"
          class="floating-btn"
        >
          <el-icon><Plus /></el-icon>
        </el-button>
      </el-tooltip>
      <el-tooltip content="重置布局" placement="left">
        <el-button
          circle
          size="large"
          @click="resetLayout"
          class="floating-btn"
        >
          <el-icon><Setting /></el-icon>
        </el-button>
      </el-tooltip>
    </div>

    <!-- 实时通知 -->
    <el-notification
      v-for="notification in notifications"
      :key="notification.id"
      :title="notification.title"
      :message="notification.message"
      :type="notification.type"
      :duration="notification.duration"
      @close="removeNotification(notification.id)"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { GridLayout, GridItem } from 'vue3-grid-layout-next'
import DashboardWidget from './DashboardWidget.vue'

// 图标导入
import {
  Refresh,
  Moon,
  Sunny,
  Download,
  Plus,
  Setting
} from '@element-plus/icons-vue'

// 类型定义
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

interface LayoutItem {
  i: string
  x: number
  y: number
  w: number
  h: number
}

interface Notification {
  id: string
  title: string
  message: string
  type: 'success' | 'warning' | 'info' | 'error'
  duration: number
}

// 响应式数据
const version = ref('1.3.0')
const refreshMode = ref<'auto' | 'manual'>('auto')
const isDarkTheme = ref(false)
const dashboardLayout = ref<LayoutItem[]>([])
const widgetData = ref<Record<string, any>>({})
const widgetDrawerVisible = ref(false)
const widgetSearch = ref('')
const activeCategories = ref<string[]>([])
const notifications = ref<Notification[]>([])

// 组件配置
const widgetCategories = [
  { name: 'system', label: '系统监控' },
  { name: 'media', label: '媒体管理' },
  { name: 'download', label: '下载管理' },
  { name: 'plugins', label: '插件管理' }
]

const availableWidgets: Widget[] = [
  {
    id: 'system-monitor',
    title: '系统监控',
    description: '实时监控CPU、内存、磁盘使用情况',
    icon: 'Monitor',
    category: 'system',
    minW: 4,
    minH: 6,
    defaultW: 6,
    defaultH: 8
  },
  {
    id: 'download-status',
    title: '下载状态',
    description: '显示当前下载任务和速度',
    icon: 'Download',
    category: 'download',
    minW: 4,
    minH: 6,
    defaultW: 6,
    defaultH: 8
  },
  {
    id: 'media-library',
    title: '媒体库概览',
    description: '显示媒体库统计信息',
    icon: 'Film',
    category: 'media',
    minW: 4,
    minH: 6,
    defaultW: 6,
    defaultH: 8
  },
  {
    id: 'plugin-manager',
    title: '插件管理',
    description: '管理已安装的插件',
    icon: 'Puzzle',
    category: 'plugins',
    minW: 4,
    minH: 6,
    defaultW: 6,
    defaultH: 8
  }
]

// 计算属性
const filteredWidgets = computed(() => {
  if (!widgetSearch.value) {
    return availableWidgets
  }
  return availableWidgets.filter(widget =>
    widget.title.toLowerCase().includes(widgetSearch.value.toLowerCase()) ||
    widget.description.toLowerCase().includes(widgetSearch.value.toLowerCase())
  )
})

// 方法
const toggleRefreshMode = () => {
  refreshMode.value = refreshMode.value === 'auto' ? 'manual' : 'auto'
  addNotification({
    title: '刷新模式',
    message: `已切换到${refreshMode.value === 'auto' ? '自动' : '手动'}刷新模式`,
    type: 'success',
    duration: 3000
  })
}

const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value
  document.documentElement.setAttribute('data-theme', isDarkTheme.value ? 'dark' : 'light')
}

const exportDashboard = async () => {
  try {
    const layoutData = {
      version: version.value,
      layout: dashboardLayout.value,
      theme: isDarkTheme.value ? 'dark' : 'light',
      timestamp: new Date().toISOString()
    }
    
    const blob = new Blob([JSON.stringify(layoutData, null, 2)], {
      type: 'application/json'
    })
    
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `vabhub-dashboard-${new Date().getTime()}.json`
    a.click()
    URL.revokeObjectURL(url)
    
    addNotification({
      title: '导出成功',
      message: '仪表盘配置已导出',
      type: 'success',
      duration: 3000
    })
  } catch (error) {
    addNotification({
      title: '导出失败',
      message: '导出过程中出现错误',
      type: 'error',
      duration: 3000
    })
  }
}

const onLayoutUpdated = (newLayout: LayoutItem[]) => {
  console.log('布局更新:', newLayout)
  saveLayout()
}

const onItemResized = (i: string | number, newH: number, newW: number, _height: number, _width: number) => {
  console.log(`组件 ${i} 大小调整: ${newW}x${newH}`)
}

const onItemDragged = (i: string | number, newX: number, newY: number) => {
  console.log(`组件 ${i} 位置移动: ${newX},${newY}`)
}

const getWidgetConfig = (widgetId: string): Widget => {
  const widget = availableWidgets.find(w => w.id === widgetId)
  if (!widget) {
    throw new Error(`Widget with id ${widgetId} not found`)
  }
  return widget
}

const refreshWidget = () => {
  console.log('刷新组件')
  // 实现组件数据刷新逻辑
}

const configureWidget = () => {
  console.log('配置组件')
  // 实现组件配置逻辑
}

const removeWidget = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要移除这个组件吗？',
      '确认移除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 实现组件移除逻辑
    addNotification({
      title: '组件移除',
      message: '组件已成功移除',
      type: 'success',
      duration: 3000
    })
  } catch (error) {
    // 用户取消操作
  }
}

const getCategoryWidgets = (category: string) => {
  return filteredWidgets.value.filter(widget => widget.category === category)
}

const addWidget = (widget: Widget) => {
  if (dashboardLayout.value.some(item => item.i === widget.id)) {
    ElMessage.warning('该组件已存在')
    return
  }
  
  const newItem: LayoutItem = {
    i: widget.id,
    x: 0,
    y: findNextYPosition(),
    w: widget.defaultW,
    h: widget.defaultH
  }
  
  dashboardLayout.value.push(newItem)
  widgetDrawerVisible.value = false
  saveLayout()
  
  addNotification({
    title: '组件添加',
    message: `${widget.title} 已添加到仪表盘`,
    type: 'success',
    duration: 3000
  })
}

const findNextYPosition = (): number => {
  if (dashboardLayout.value.length === 0) return 0
  
  const maxY = Math.max(...dashboardLayout.value.map(item => item.y + item.h))
  return maxY
}

const resetLayout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要重置仪表盘布局吗？所有自定义设置将丢失。',
      '确认重置',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    loadDefaultLayout()
    addNotification({
      title: '布局重置',
      message: '仪表盘布局已重置为默认设置',
      type: 'success',
      duration: 3000
    })
  } catch (error) {
    // 用户取消操作
  }
}

const addNotification = (notification: Omit<Notification, 'id'>) => {
  const id = Date.now().toString()
  notifications.value.push({
    id,
    ...notification,
    duration: notification.duration || 3000
  })
}

const removeNotification = (id: string) => {
  notifications.value = notifications.value.filter(n => n.id !== id)
}

// 布局持久化
const saveLayout = () => {
  const layoutData = {
    layout: dashboardLayout.value,
    theme: isDarkTheme.value,
    refreshMode: refreshMode.value
  }
  localStorage.setItem('vabhub-dashboard-layout', JSON.stringify(layoutData))
}

const loadLayout = () => {
  const saved = localStorage.getItem('vabhub-dashboard-layout')
  if (saved) {
    try {
      const data = JSON.parse(saved)
      dashboardLayout.value = data.layout || []
      isDarkTheme.value = data.theme || false
      refreshMode.value = data.refreshMode || 'auto'
    } catch (error) {
      console.error('加载布局失败:', error)
      loadDefaultLayout()
    }
  } else {
    loadDefaultLayout()
  }
}

const loadDefaultLayout = () => {
  dashboardLayout.value = [
    { i: 'system-monitor', x: 0, y: 0, w: 6, h: 8 },
    { i: 'download-status', x: 6, y: 0, w: 6, h: 8 },
    { i: 'media-library', x: 0, y: 8, w: 6, h: 8 },
    { i: 'plugin-manager', x: 6, y: 8, w: 6, h: 8 }
  ]
}

// 生命周期
onMounted(() => {
  loadLayout()
  
  // 设置主题
  document.documentElement.setAttribute('data-theme', isDarkTheme.value ? 'dark' : 'light')
  
  // 自动刷新逻辑
  if (refreshMode.value === 'auto') {
    startAutoRefresh()
  }
})

onUnmounted(() => {
  // 清理自动刷新
  if (refreshMode.value === 'auto') {
    stopAutoRefresh()
  }
})

// 自动刷新逻辑
let refreshInterval: number | null = null

const startAutoRefresh = () => {
  refreshInterval = setInterval(() => {
    // 实现自动刷新逻辑
    console.log('自动刷新数据...')
  }, 30000) // 30秒刷新一次
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

// 监听刷新模式变化
watch(refreshMode, (newMode) => {
  if (newMode === 'auto') {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
})
</script>

<style scoped>
.enhanced-dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--el-bg-color-page);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color);
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dashboard-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.vue-grid-layout {
  flex: 1;
  padding: 20px;
  overflow: auto;
}

.widget-panel {
  padding: 20px;
}

.widget-categories {
  margin-top: 20px;
}

.widget-list {
  display: grid;
  gap: 12px;
  margin-top: 12px;
}

.widget-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.widget-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--el-box-shadow-light);
}

.widget-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.widget-description {
  font-size: 0.875rem;
  color: var(--el-text-color-secondary);
  line-height: 1.4;
}

.floating-actions {
  position: fixed;
  right: 30px;
  bottom: 30px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
}

.floating-btn {
  box-shadow: var(--el-box-shadow-light);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    height: auto;
    padding: 12px;
    gap: 12px;
  }
  
  .vue-grid-layout {
    padding: 10px;
  }
  
  .floating-actions {
    right: 15px;
    bottom: 15px;
  }
}

/* 暗色主题支持 */
[data-theme="dark"] {
  --el-bg-color-page: #1a1a1a;
  --el-bg-color: #2d2d2d;
}

[data-theme="light"] {
  --el-bg-color-page: #f5f7fa;
  --el-bg-color: #ffffff;
}
</style>