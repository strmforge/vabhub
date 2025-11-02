<template>
  <div class="dashboard-config">
    <div class="config-modal" @click="closeModal">
      <div class="config-content" @click.stop>
        <!-- 配置头部 -->
        <div class="config-header">
          <h2>仪表板配置</h2>
          <p>自定义您的仪表板布局和组件</p>
          <button class="close-btn" @click="closeModal">×</button>
        </div>

        <!-- 配置标签页 -->
        <div class="config-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            class="tab-btn"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>

        <!-- 布局配置 -->
        <div v-if="activeTab === 'layout'" class="tab-content">
          <div class="layout-section">
            <h3>布局模板</h3>
            <div class="layout-grid">
              <div 
                v-for="layout in layoutTemplates" 
                :key="layout.id"
                class="layout-card"
                :class="{ active: selectedLayout === layout.id }"
                @click="selectLayout(layout)"
              >
                <div class="layout-preview">
                  <div 
                    v-for="area in layout.areas" 
                    :key="area.id"
                    class="layout-area"
                    :style="{ 
                      gridArea: area.gridArea,
                      backgroundColor: area.color
                    }"
                  ></div>
                </div>
                <div class="layout-info">
                  <h4>{{ layout.name }}</h4>
                  <p>{{ layout.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="grid-settings">
            <h3>网格设置</h3>
            <div class="settings-grid">
              <div class="setting-item">
                <label>列数:</label>
                <input 
                  type="number" 
                  v-model="gridSettings.columns" 
                  min="1" 
                  max="12"
                  class="setting-input"
                >
              </div>
              <div class="setting-item">
                <label>行数:</label>
                <input 
                  type="number" 
                  v-model="gridSettings.rows" 
                  min="1" 
                  max="20"
                  class="setting-input"
                >
              </div>
              <div class="setting-item">
                <label>间距:</label>
                <select v-model="gridSettings.gap" class="setting-select">
                  <option value="small">小</option>
                  <option value="medium">中</option>
                  <option value="large">大</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- 小部件配置 -->
        <div v-if="activeTab === 'widgets'" class="tab-content">
          <div class="widgets-section">
            <h3>可用小部件</h3>
            <div class="widgets-grid">
              <div 
                v-for="widget in availableWidgets" 
                :key="widget.type"
                class="widget-card"
                :class="{ 'widget-added': isWidgetAdded(widget.type) }"
                @click="toggleWidget(widget)"
              >
                <div class="widget-icon">{{ widget.icon }}</div>
                <div class="widget-info">
                  <h4>{{ widget.name }}</h4>
                  <p>{{ widget.description }}</p>
                  <div class="widget-meta">
                    <span class="widget-size">{{ widget.size }}</span>
                    <span class="widget-category">{{ widget.category }}</span>
                  </div>
                </div>
                <div class="widget-status">
                  <span v-if="isWidgetAdded(widget.type)" class="status-added">✓ 已添加</span>
                  <span v-else class="status-available">+ 添加</span>
                </div>
              </div>
            </div>
          </div>

          <div class="current-widgets">
            <h3>当前小部件</h3>
            <div 
              v-if="currentLayout.widgets.length === 0" 
              class="empty-widgets"
            >
              <div class="empty-icon">📊</div>
              <p>暂无小部件，请从上方添加</p>
            </div>
            <div v-else class="widgets-list">
              <div 
                v-for="widget in currentLayout.widgets" 
                :key="widget.id"
                class="current-widget"
              >
                <div class="widget-header">
                  <div class="widget-icon-small">{{ getWidgetIcon(widget.type) }}</div>
                  <div class="widget-title">
                    <h4>{{ getWidgetName(widget.type) }}</h4>
                    <span class="widget-position">
                      位置: {{ widget.rowStart }},{{ widget.colStart }}
                    </span>
                  </div>
                </div>
                <div class="widget-actions">
                  <button 
                    class="btn btn-small"
                    @click="configureWidget(widget)"
                    title="配置"
                  >
                    ⚙️
                  </button>
                  <button 
                    class="btn btn-small btn-danger"
                    @click="removeWidget(widget.id)"
                    title="删除"
                  >
                    ❌
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 主题配置 -->
        <div v-if="activeTab === 'theme'" class="tab-content">
          <div class="theme-section">
            <h3>主题设置</h3>
            <div class="theme-grid">
              <div 
                v-for="theme in themes" 
                :key="theme.id"
                class="theme-card"
                :class="{ active: selectedTheme === theme.id }"
                @click="selectTheme(theme)"
              >
                <div class="theme-preview" :style="{ backgroundColor: theme.primaryColor }">
                  <div class="theme-sample" :style="{ backgroundColor: theme.secondaryColor }"></div>
                </div>
                <div class="theme-info">
                  <h4>{{ theme.name }}</h4>
                  <p>{{ theme.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="custom-theme">
            <h3>自定义主题</h3>
            <div class="color-settings">
              <div class="color-item">
                <label>主色调:</label>
                <input 
                  type="color" 
                  v-model="customTheme.primaryColor"
                  class="color-input"
                >
                <span class="color-value">{{ customTheme.primaryColor }}</span>
              </div>
              <div class="color-item">
                <label>辅助色:</label>
                <input 
                  type="color" 
                  v-model="customTheme.secondaryColor"
                  class="color-input"
                >
                <span class="color-value">{{ customTheme.secondaryColor }}</span>
              </div>
              <div class="color-item">
                <label>背景色:</label>
                <input 
                  type="color" 
                  v-model="customTheme.backgroundColor"
                  class="color-input"
                >
                <span class="color-value">{{ customTheme.backgroundColor }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 配置操作 -->
        <div class="config-actions">
          <button class="btn btn-secondary" @click="resetConfig">
            重置配置
          </button>
          <button class="btn btn-secondary" @click="closeModal">
            取消
          </button>
          <button class="btn btn-primary" @click="saveConfig">
            保存配置
          </button>
        </div>
      </div>
    </div>

    <!-- 小部件配置模态框 -->
    <div v-if="configuringWidget" class="widget-config-modal" @click="closeWidgetConfig">
      <div class="widget-config-content" @click.stop>
        <div class="widget-config-header">
          <h3>配置小部件: {{ configuringWidget.name }}</h3>
          <button class="close-btn" @click="closeWidgetConfig">×</button>
        </div>
        <div class="widget-config-body">
          <div class="config-section">
            <h4>位置和大小</h4>
            <div class="position-settings">
              <div class="setting-group">
                <label>起始行:</label>
                <input 
                  type="number" 
                  v-model="configuringWidget.rowStart" 
                  min="1" 
                  :max="gridSettings.rows"
                  class="setting-input"
                >
              </div>
              <div class="setting-group">
                <label>起始列:</label>
                <input 
                  type="number" 
                  v-model="configuringWidget.colStart" 
                  min="1" 
                  :max="gridSettings.columns"
                  class="setting-input"
                >
              </div>
              <div class="setting-group">
                <label>行跨度:</label>
                <input 
                  type="number" 
                  v-model="configuringWidget.rowSpan" 
                  min="1" 
                  :max="gridSettings.rows"
                  class="setting-input"
                >
              </div>
              <div class="setting-group">
                <label>列跨度:</label>
                <input 
                  type="number" 
                  v-model="configuringWidget.colSpan" 
                  min="1" 
                  :max="gridSettings.columns"
                  class="setting-input"
                >
              </div>
            </div>
          </div>
          <div class="config-section">
            <h4>小部件设置</h4>
            <div class="widget-settings">
              <div class="setting-group">
                <label>标题:</label>
                <input 
                  type="text" 
                  v-model="configuringWidget.title"
                  class="setting-input"
                >
              </div>
              <div class="setting-group">
                <label>刷新间隔:</label>
                <select v-model="configuringWidget.refreshInterval" class="setting-select">
                  <option value="0">不自动刷新</option>
                  <option value="30">30秒</option>
                  <option value="60">1分钟</option>
                  <option value="300">5分钟</option>
                  <option value="600">10分钟</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        <div class="widget-config-actions">
          <button class="btn btn-secondary" @click="closeWidgetConfig">取消</button>
          <button class="btn btn-primary" @click="saveWidgetConfig">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardConfig',
  props: {
    widgets: {
      type: Array,
      default: () => []
    },
    layout: {
      type: Object,
      default: () => ({
        name: '默认布局',
        description: '基础网格布局',
        widgets: [],
        grid: { columns: 4, rows: 6, gap: 'medium' }
      })
    }
  },
  data() {
    return {
      activeTab: 'layout',
      selectedLayout: 'default',
      configuringWidget: null,
      tabs: [
        { id: 'layout', label: '布局' },
        { id: 'widgets', label: '小部件' },
        { id: 'theme', label: '主题' }
      ],
      layoutTemplates: [
        {
          id: 'default',
          name: '默认布局',
          description: '均衡的4列网格布局',
          areas: [
            { id: '1', gridArea: '1 / 1 / 3 / 3', color: '#3498db' },
            { id: '2', gridArea: '1 / 3 / 2 / 5', color: '#2ecc71' },
            { id: '3', gridArea: '2 / 3 / 3 / 5', color: '#e74c3c' },
            { id: '4', gridArea: '3 / 1 / 4 / 5', color: '#f39c12' }
          ]
        },
        {
          id: 'sidebar',
          name: '侧边栏布局',
          description: '左侧边栏加主内容区',
          areas: [
            { id: '1', gridArea: '1 / 1 / 4 / 2', color: '#3498db' },
            { id: '2', gridArea: '1 / 2 / 2 / 5', color: '#2ecc71' },
            { id: '3', gridArea: '2 / 2 / 3 / 4', color: '#e74c3c' },
            { id: '4', gridArea: '2 / 4 / 3 / 5', color: '#f39c12' },
            { id: '5', gridArea: '3 / 2 / 4 / 5', color: '#9b59b6' }
          ]
        },
        {
          id: 'centered',
          name: '居中布局',
          description: '内容居中的简洁布局',
          areas: [
            { id: '1', gridArea: '1 / 2 / 2 / 4', color: '#3498db' },
            { id: '2', gridArea: '2 / 1 / 3 / 3', color: '#2ecc71' },
            { id: '3', gridArea: '2 / 3 / 3 / 5', color: '#e74c3c' },
            { id: '4', gridArea: '3 / 2 / 4 / 4', color: '#f39c12' }
          ]
        }
      ],
      themes: [
        {
          id: 'light',
          name: '浅色主题',
          description: '明亮的浅色界面',
          primaryColor: '#3498db',
          secondaryColor: '#2ecc71'
        },
        {
          id: 'dark',
          name: '深色主题',
          description: '护眼的深色界面',
          primaryColor: '#34495e',
          secondaryColor: '#2c3e50'
        },
        {
          id: 'blue',
          name: '蓝色主题',
          description: '专业的蓝色调',
          primaryColor: '#2980b9',
          secondaryColor: '#3498db'
        },
        {
          id: 'green',
          name: '绿色主题',
          description: '清新的绿色调',
          primaryColor: '#27ae60',
          secondaryColor: '#2ecc71'
        }
      ],
      gridSettings: {
        columns: 4,
        rows: 6,
        gap: 'medium'
      },
      customTheme: {
        primaryColor: '#3498db',
        secondaryColor: '#2ecc71',
        backgroundColor: '#ffffff'
      },
      selectedTheme: 'light',
      currentLayout: {
        name: '默认布局',
        description: '基础网格布局',
        widgets: [],
        grid: { columns: 4, rows: 6, gap: 'medium' }
      }
    }
  },
  computed: {
    availableWidgets() {
      return [
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
        },
        {
          type: 'plugins',
          name: '插件状态',
          description: '显示已安装插件的状态',
          icon: '🔌',
          size: '1x1',
          category: '插件'
        },
        {
          type: 'notifications',
          name: '通知中心',
          description: '显示系统通知和提醒',
          icon: '🔔',
          size: '1x2',
          category: '通知'
        },
        {
          type: 'search',
          name: '快速搜索',
          description: '提供快速搜索功能',
          icon: '🔍',
          size: '1x1',
          category: '搜索'
        },
        {
          type: 'weather',
          name: '天气信息',
          description: '显示当地天气信息',
          icon: '☀️',
          size: '1x1',
          category: '工具'
        }
      ]
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    
    selectLayout(layout) {
      this.selectedLayout = layout.id
      this.currentLayout.name = layout.name
      this.currentLayout.description = layout.description
    },
    
    selectTheme(theme) {
      this.selectedTheme = theme.id
      this.customTheme.primaryColor = theme.primaryColor
      this.customTheme.secondaryColor = theme.secondaryColor
    },
    
    isWidgetAdded(widgetType) {
      return this.currentLayout.widgets.some(widget => widget.type === widgetType)
    },
    
    toggleWidget(widget) {
      if (this.isWidgetAdded(widget.type)) {
        this.removeWidgetByType(widget.type)
      } else {
        this.addWidget(widget)
      }
    },
    
    addWidget(widget) {
      const newWidget = {
        id: `${widget.type}-${Date.now()}`,
        type: widget.type,
        name: widget.name,
        title: widget.name,
        rowStart: 1,
        colStart: 1,
        rowSpan: 2,
        colSpan: 2,
        refreshInterval: 60,
        config: {}
      }
      
      // 根据小部件大小设置默认跨度
      const sizeMap = {
        '1x1': { rowSpan: 1, colSpan: 1 },
        '1x2': { rowSpan: 1, colSpan: 2 },
        '2x1': { rowSpan: 2, colSpan: 1 },
        '2x2': { rowSpan: 2, colSpan: 2 }
      }
      
      if (sizeMap[widget.size]) {
        newWidget.rowSpan = sizeMap[widget.size].rowSpan
        newWidget.colSpan = sizeMap[widget.size].colSpan
      }
      
      this.currentLayout.widgets.push(newWidget)
    },
    
    removeWidget(widgetId) {
      this.currentLayout.widgets = this.currentLayout.widgets.filter(w => w.id !== widgetId)
    },
    
    removeWidgetByType(widgetType) {
      this.currentLayout.widgets = this.currentLayout.widgets.filter(w => w.type !== widgetType)
    },
    
    configureWidget(widget) {
      this.configuringWidget = { ...widget }
    },
    
    closeWidgetConfig() {
      this.configuringWidget = null
    },
    
    saveWidgetConfig() {
      if (this.configuringWidget) {
        const index = this.currentLayout.widgets.findIndex(w => w.id === this.configuringWidget.id)
        if (index !== -1) {
          this.currentLayout.widgets[index] = { ...this.configuringWidget }
        }
        this.closeWidgetConfig()
      }
    },
    
    getWidgetIcon(widgetType) {
      const widget = this.availableWidgets.find(w => w.type === widgetType)
      return widget ? widget.icon : '🔌'
    },
    
    getWidgetName(widgetType) {
      const widget = this.availableWidgets.find(w => w.type === widgetType)
      return widget ? widget.name : '未知小部件'
    },
    
    resetConfig() {
      this.currentLayout = {
        name: '默认布局',
        description: '基础网格布局',
        widgets: [],
        grid: { columns: 4, rows: 6, gap: 'medium' }
      }
      this.selectedLayout = 'default'
      this.selectedTheme = 'light'
      this.gridSettings = { columns: 4, rows: 6, gap: 'medium' }
    },
    
    saveConfig() {
      const config = {
        layout: {
          ...this.currentLayout,
          grid: { ...this.gridSettings }
        },
        theme: {
          id: this.selectedTheme,
          custom: this.customTheme
        }
      }
      
      this.$emit('save', config)
      this.closeModal()
    }
  },
  mounted() {
    if (this.layout) {
      this.currentLayout = { ...this.layout }
    }
  }
}
</script>

<style scoped>
.dashboard-config {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

.config-modal {
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 2rem;
}

.config-content {
  background: white;
  border-radius: 12px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.config-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid #eee;
  position: relative;
}

.config-header h2 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.config-header p {
  margin: 0;
  color: #7f8c8d;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
}

.config-tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  padding: 0 2rem;
}

.tab-btn {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
  color: #7f8c8d;
}

.tab-btn.active {
  color: #3498db;
  border-bottom-color: #3498db;
}

.tab-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.layout-section, .widgets-section, .theme-section {
  margin-bottom: 2rem;
}

.layout-section h3, .widgets-section h3, .theme-section h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.layout-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.layout-card {
  border: 2px solid #eee;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.layout-card:hover, .layout-card.active {
  border-color: #3498db;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
}

.layout-card.active {
  background: #f8fafc;
}

.layout-preview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 20px);
  gap: 2px;
  margin-bottom: 1rem;
  height: 70px;
}

.layout-area {
  border-radius: 2px;
}

.layout-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.layout-info p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.grid-settings h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.setting-item label {
  font-weight: 500;
  color: #34495e;
}

.setting-input, .setting-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.widgets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.widget-card {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.widget-card:hover {
  border-color: #3498db;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
}

.widget-card.widget-added {
  border-color: #27ae60;
  background: #f8fff9;
}

.widget-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  text-align: center;
}

.widget-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.widget-info p {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  line-height: 1.4;
}

.widget-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #95a5a6;
}

.widget-status {
  margin-top: auto;
  text-align: center;
  padding-top: 1rem;
}

.status-added {
  color: #27ae60;
  font-weight: 500;
}

.status-available {
  color: #3498db;
  font-weight: 500;
}

.current-widgets h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.empty-widgets {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.widgets-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.current-widget {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #f8f9fa;
}

.widget-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.widget-icon-small {
  font-size: 1.5rem;
}

.widget-title h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.widget-position {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.widget-actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.btn-small {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
}

.theme-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.theme-card {
  border: 2px solid #eee;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.theme-card:hover, .theme-card.active {
  border-color: #3498db;
}

.theme-card.active {
  background: #f8fafc;
}

.theme-preview {
  height: 60px;
  border-radius: 4px;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
}

.theme-sample {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 40px;
  height: 40px;
  border-radius: 4px;
}

.theme-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.theme-info p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.custom-theme h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.color-settings {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.color-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.color-item label {
  font-weight: 500;
  color: #34495e;
  min-width: 80px;
}

.color-input {
  width: 50px;
  height: 30px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.color-value {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.config-actions {
  padding: 1.5rem 2rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.widget-config-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
  padding: 2rem;
}

.widget-config-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.widget-config-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  position: relative;
}

.widget-config-header h3 {
  margin: 0;
  color: #2c3e50;
}

.widget-config-body {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
}

.config-section {
  margin-bottom: 2rem;
}

.config-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.position-settings, .widget-settings {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.setting-group label {
  font-weight: 500;
  color: #34495e;
  font-size: 0.9rem;
}

.widget-config-actions {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .config-modal {
    padding: 1rem;
  }
  
  .config-content {
    max-height: 95vh;
  }
  
  .config-header {
    padding: 1rem;
  }
  
  .config-tabs {
    padding: 0 1rem;
  }
  
  .tab-content {
    padding: 1rem;
  }
  
  .layout-grid, .widgets-grid, .theme-grid {
    grid-template-columns: 1fr;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
  
  .position-settings, .widget-settings {
    grid-template-columns: 1fr;
  }
  
  .config-actions {
    padding: 1rem;
    flex-direction: column;
  }
  
  .widget-config-modal {
    padding: 1rem;
  }
}
</style>