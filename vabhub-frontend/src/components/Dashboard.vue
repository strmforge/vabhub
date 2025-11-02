<template>
  <div class="dashboard">
    <!-- 仪表板配置模态框 -->
    <DashboardConfig 
      v-if="showConfig" 
      :widgets="availableWidgets" 
      :layout="currentLayout"
      @save="saveDashboardConfig" 
      @close="showConfig = false"
    />
    
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-info">
          <h1>VabHub 仪表板</h1>
          <p>欢迎使用 VabHub 媒体管理系统</p>
          <div class="layout-info">
            <span class="layout-name">{{ currentLayout.name }}</span>
            <span class="layout-desc">{{ currentLayout.description }}</span>
          </div>
        </div>
        <div class="header-actions">
          <button class="config-btn" @click="showConfig = true">
            <span class="btn-icon">⚙️</span>
            <span class="btn-text">配置仪表板</span>
          </button>
          <button class="layout-btn" @click="toggleEditMode">
            <span class="btn-icon">{{ editMode ? '✅' : '📐' }}</span>
            <span class="btn-text">{{ editMode ? '完成编辑' : '编辑布局' }}</span>
          </button>
          <button class="refresh-btn" @click="refreshDashboard">
            <span class="btn-icon">🔄</span>
            <span class="btn-text">刷新</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 拖拽布局容器 -->
    <div 
      class="dashboard-layout" 
      :class="{ 'edit-mode': editMode }"
      @dragover.prevent
      @drop="handleDrop"
    >
      <!-- 网格布局 -->
      <div 
        v-for="(widget, index) in currentLayout.widgets" 
        :key="widget.id"
        class="widget-container"
        :style="{ 
          gridArea: `${widget.rowStart} / ${widget.colStart} / ${widget.rowEnd} / ${widget.colEnd}`
        }"
        :class="{ 
          'widget-dragging': draggingWidget === widget.id,
          'widget-editable': editMode 
        }"
        draggable="true"
        @dragstart="handleDragStart(widget.id)"
        @dragend="handleDragEnd"
        @click="editMode ? selectWidget(widget.id) : null"
      >
        <!-- 小部件内容 -->
        <component
          :is="getWidgetComponent(widget.type)"
          :data="widget.data"
          :config="widget.config"
          :class="{ 'widget-selected': selectedWidget === widget.id }"
        />
        
        <!-- 编辑模式控制 -->
        <div v-if="editMode" class="widget-controls">
          <button class="widget-btn" @click="removeWidget(widget.id)" title="删除">
            ❌
          </button>
          <button class="widget-btn" @click="configureWidget(widget.id)" title="配置">
            ⚙️
          </button>
          <button class="widget-btn" @click="resizeWidget(widget.id, 'increase')" title="放大">
            ➕
          </button>
          <button class="widget-btn" @click="resizeWidget(widget.id, 'decrease')" title="缩小">
            ➖
          </button>
        </div>
      </div>
      
      <!-- 空位提示 -->
      <div v-if="editMode && currentLayout.widgets.length === 0" class="empty-layout">
        <div class="empty-content">
          <div class="empty-icon">📊</div>
          <h3>添加小部件到仪表板</h3>
          <p>拖拽右侧的小部件到网格中，或点击"添加小部件"按钮</p>
          <button class="btn btn-primary" @click="showConfig = true">
            添加小部件
          </button>
        </div>
      </div>
    </div>

    <!-- 小部件库侧边栏 -->
    <div v-if="editMode" class="widget-library">
      <div class="library-header">
        <h3>小部件库</h3>
        <button class="close-library" @click="editMode = false">×</button>
      </div>
      <div class="widget-list">
        <div 
          v-for="widget in availableWidgets" 
          :key="widget.type"
          class="widget-item"
          draggable="true"
          @dragstart="handleLibraryDragStart(widget)"
        >
          <div class="widget-icon">{{ widget.icon }}</div>
          <div class="widget-info">
            <h4>{{ widget.name }}</h4>
            <p>{{ widget.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 系统状态概览 -->
    <div class="status-overview">
      <div class="status-card">
        <div class="status-icon">📊</div>
        <div class="status-info">
          <h3>系统状态</h3>
          <p class="status-value">{{ systemStatus }}</p>
        </div>
      </div>
      
      <div class="status-card">
        <div class="status-icon">⚡</div>
        <div class="status-info">
          <h3>CPU使用率</h3>
          <p class="status-value">{{ cpuUsage }}%</p>
        </div>
      </div>
      
      <div class="status-card">
        <div class="status-icon">💾</div>
        <div class="status-info">
          <h3>内存使用</h3>
          <p class="status-value">{{ memoryUsage }}%</p>
        </div>
      </div>
      
      <div class="status-card">
        <div class="status-icon">🔌</div>
        <div class="status-info">
          <h3>WebSocket连接</h3>
          <p class="status-value">{{ wsConnections }} 个</p>
        </div>
      </div>
    </div>

    <!-- 快速操作 -->
    <div class="quick-actions">
      <h2>快速操作</h2>
      <div class="action-grid">
        <router-link to="/plugins" class="action-card">
          <div class="action-icon">🔌</div>
          <h3>插件管理</h3>
          <p>管理功能扩展插件</p>
        </router-link>
        
        <router-link to="/logs" class="action-card">
          <div class="action-icon">📋</div>
          <h3>实时日志</h3>
          <p>查看系统运行日志</p>
        </router-link>
        
        <router-link to="/discover" class="action-card">
          <div class="action-icon">🔍</div>
          <h3>内容发现</h3>
          <p>搜索和发现媒体内容</p>
        </router-link>
        
        <router-link to="/recommendations" class="action-card">
          <div class="action-icon">🤖</div>
          <h3>AI推荐</h3>
          <p>智能推荐个性化内容</p>
        </router-link>
        
        <router-link to="/settings" class="action-card">
          <div class="action-icon">⚙️</div>
          <h3>系统设置</h3>
          <p>配置系统参数</p>
        </router-link>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="recent-activity">
      <h2>最近活动</h2>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon">{{ activity.icon }}</div>
          <div class="activity-content">
            <p class="activity-text">{{ activity.text }}</p>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DashboardConfig from './DashboardConfig.vue'

export default {
  name: 'Dashboard',
  components: {
    DashboardConfig
  },
  data() {
    return {
      showConfig: false,
      editMode: false,
      systemStatus: '运行中',
      cpuUsage: 0,
      memoryUsage: 0,
      wsConnections: 0,
      systemWebSocket: null,
      isConnected: false,
      currentLayout: {
        name: '默认布局',
        description: '基础网格布局',
        widgets: [],
        grid: { columns: 4, rows: 6, gap: 'medium' }
      },
      availableWidgets: [
        {
          type: 'system-status',
          name: '系统状态',
          description: '显示CPU、内存、网络等系统状态',
          icon: '⚡',
          size: '2x2',
          category: '系统'
        },
        {
          type: 'recent-activity',
          name: '最近活动',
          description: '显示最近的系统活动和事件',
          icon: '📋',
          size: '2x1',
          category: '活动'
        },
        {
          type: 'media-stats',
          name: '媒体统计',
          description: '显示媒体库的统计信息',
          icon: '🎬',
          size: '1x2',
          category: '媒体'
        },
        {
          type: 'downloads',
          name: '下载管理',
          description: '显示当前下载任务和进度',
          icon: '📥',
          size: '2x2',
          category: '下载'
        }
      ],
      recentActivities: [
        {
          id: 1,
          icon: '🔌',
          text: '媒体信息插件已启用',
          time: '2分钟前'
        },
        {
          id: 2,
          icon: '📥',
          text: '下载任务已完成',
          time: '5分钟前'
        },
        {
          id: 3,
          icon: '🔍',
          text: '发现新的媒体内容',
          time: '10分钟前'
        },
        {
          id: 4,
          icon: '⚙️',
          text: '系统配置已更新',
          time: '15分钟前'
        }
      ]
    }
  },
  mounted() {
    this.connectSystemWebSocket()
    this.fetchDashboardData()
    this.loadDashboardConfig()
  },
  
  beforeUnmount() {
    this.disconnectSystemWebSocket()
  },
  
  methods: {
    connectSystemWebSocket() {
      try {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const host = window.location.hostname || 'localhost'
        const port = window.location.port || '8000'
        const wsUrl = `${protocol}//${host}:${port}/ws/system`
        
        this.systemWebSocket = new WebSocket(wsUrl)
        
        this.systemWebSocket.onopen = () => {
          this.isConnected = true
          this.systemStatus = '已连接'
          console.log('系统状态WebSocket连接成功')
        }
        
        this.systemWebSocket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            if (data.type === 'system_status') {
              this.updateSystemStatus(data.status)
            }
          } catch (error) {
            console.error('Failed to parse system status message:', error)
          }
        }
        
        this.systemWebSocket.onclose = () => {
          this.isConnected = false
          this.systemStatus = '连接断开'
          console.log('系统状态WebSocket连接已断开')
        }
        
        this.systemWebSocket.onerror = (error) => {
          console.error('系统状态WebSocket错误:', error)
          this.systemStatus = '连接错误'
        }
        
      } catch (error) {
        console.error('系统状态WebSocket连接失败:', error)
        this.systemStatus = '连接失败'
      }
    },
    
    disconnectSystemWebSocket() {
      if (this.systemWebSocket) {
        this.systemWebSocket.close()
      }
    },
    
    updateSystemStatus(status) {
      // 更新CPU使用率
      if (status.performance && status.performance.cpu_usage) {
        this.cpuUsage = Math.round(status.performance.cpu_usage.last)
      }
      
      // 更新内存使用率
      if (status.performance && status.performance.memory_usage) {
        this.memoryUsage = Math.round(status.performance.memory_usage.last)
      }
      
      // 更新连接数
      if (status.connections) {
        const totalConnections = Object.values(status.connections).reduce((sum, count) => sum + count, 0)
        this.wsConnections = totalConnections
      }
    },
    
    fetchDashboardData() {
      // 模拟API调用获取初始数据
      console.log('获取仪表板数据...')
      
      // 如果没有WebSocket连接，使用模拟数据
      if (!this.isConnected) {
        this.cpuUsage = Math.floor(Math.random() * 30) + 10
        this.memoryUsage = Math.floor(Math.random() * 40) + 30
        this.wsConnections = 1
      }
    },
    
    toggleEditMode() {
      this.editMode = !this.editMode
    },
    
    saveDashboardConfig(config) {
      console.log('保存仪表板配置:', config)
      this.currentLayout = config.layout
      
      // 保存到localStorage
      localStorage.setItem('dashboard-config', JSON.stringify(config))
      
      // 显示保存成功提示
      this.showNotification('仪表板配置已保存', 'success')
    },
    
    loadDashboardConfig() {
      const savedConfig = localStorage.getItem('dashboard-config')
      if (savedConfig) {
        try {
          const config = JSON.parse(savedConfig)
          this.currentLayout = config.layout
          console.log('加载仪表板配置:', config)
        } catch (error) {
          console.error('加载仪表板配置失败:', error)
        }
      }
    },
    
    getWidgetComponent(widgetType) {
      // 这里应该返回对应的小部件组件
      // 暂时返回一个简单的占位符组件
      return {
        template: '<div class="widget-placeholder">{{ widgetType }}</div>',
        props: ['data', 'config'],
        data() {
          return {
            widgetType: widgetType
          }
        }
      }
    },
    
    handleDragStart(widgetId) {
      console.log('开始拖拽小部件:', widgetId)
    },
    
    handleDragEnd() {
      console.log('结束拖拽')
    },
    
    handleDrop(event) {
      event.preventDefault()
      console.log('放置小部件')
    },
    
    handleLibraryDragStart(widget) {
      event.dataTransfer.setData('text/plain', JSON.stringify(widget))
      console.log('开始拖拽小部件库中的小部件:', widget)
    },
    
    selectWidget(widgetId) {
      console.log('选择小部件:', widgetId)
    },
    
    removeWidget(widgetId) {
      this.currentLayout.widgets = this.currentLayout.widgets.filter(w => w.id !== widgetId)
      console.log('删除小部件:', widgetId)
    },
    
    configureWidget(widgetId) {
      console.log('配置小部件:', widgetId)
    },
    
    resizeWidget(widgetId, direction) {
      console.log('调整小部件大小:', widgetId, direction)
    },
    
    showNotification(message, type = 'info') {
      // 这里应该显示通知
      console.log(`通知 [${type}]: ${message}`)
    },
    
    refreshDashboard() {
      console.log('刷新仪表板')
      this.fetchDashboardData()
      this.showNotification('仪表板已刷新', 'success')
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.dashboard-header p {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.status-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.status-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.3s;
}

.status-card:hover {
  transform: translateY(-2px);
}

.status-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.status-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #7f8c8d;
  font-weight: 500;
}

.status-value {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.quick-actions {
  margin-bottom: 3rem;
}

.quick-actions h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  color: inherit;
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.action-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  color: #2c3e50;
}

.action-card p {
  margin: 0;
  color: #7f8c8d;
  line-height: 1.4;
}

.recent-activity h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.activity-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f1f3f4;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.5rem;
}

.activity-content {
  flex: 1;
}

.activity-text {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.activity-time {
  font-size: 0.8rem;
  color: #95a5a6;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .status-overview {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-item {
    padding: 1rem;
  }
}
</style>