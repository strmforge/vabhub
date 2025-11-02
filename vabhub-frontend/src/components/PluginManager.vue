<template>
  <div class="plugin-manager">
    <div class="plugin-header">
      <h2>插件管理</h2>
      <p>管理VabHub的功能扩展插件</p>
      <div class="plugin-stats">
        <span class="stat-item">
          <span class="stat-value">{{ enabledPluginsCount }}</span>
          <span class="stat-label">已启用</span>
        </span>
        <span class="stat-item">
          <span class="stat-value">{{ totalPluginsCount }}</span>
          <span class="stat-label">总数</span>
        </span>
        <span class="stat-item">
          <span class="stat-value">{{ availablePluginsCount }}</span>
          <span class="stat-label">可安装</span>
        </span>
      </div>
    </div>

    <!-- 插件搜索和筛选 -->
    <div class="plugin-controls">
      <div class="search-section">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="搜索插件..." 
          class="search-input"
        >
        <select v-model="filterStatus" class="filter-select">
          <option value="all">全部状态</option>
          <option value="enabled">已启用</option>
          <option value="disabled">已禁用</option>
          <option value="error">错误</option>
        </select>
      </div>
      <button class="btn btn-primary" @click="refreshPlugins">
        🔄 刷新
      </button>
    </div>

    <!-- 插件列表 -->
    <div class="plugin-list">
      <div 
        v-for="plugin in filteredPlugins" 
        :key="plugin.id" 
        class="plugin-card"
        :class="{ 
          'plugin-enabled': plugin.enabled, 
          'plugin-error': plugin.status === 'error' 
        }"
      >
        <div class="plugin-icon">{{ getPluginIcon(plugin.type) }}</div>
        
        <div class="plugin-info">
          <h3 class="plugin-name">{{ plugin.name }}</h3>
          <p class="plugin-description">{{ plugin.description }}</p>
          <div class="plugin-meta">
            <span class="plugin-version">v{{ plugin.version }}</span>
            <span class="plugin-author">作者: {{ plugin.author }}</span>
          </div>
          <div class="plugin-status">
            <span class="status-badge" :class="plugin.status">
              {{ getStatusText(plugin.status) }}
            </span>
            <span class="plugin-updated">
              更新: {{ formatDate(plugin.updatedAt) }}
            </span>
          </div>
        </div>

        <div class="plugin-actions">
          <button 
            v-if="plugin.enabled" 
            class="btn btn-secondary" 
            @click="disablePlugin(plugin.id)"
          >
            🔴 禁用
          </button>
          <button 
            v-else 
            class="btn btn-primary" 
            @click="enablePlugin(plugin.id)"
          >
            🟢 启用
          </button>
          
          <button 
            class="btn btn-secondary" 
            @click="showPluginDetails(plugin)"
          >
            📋 详情
          </button>
          
          <button 
            v-if="plugin.configurable" 
            class="btn btn-secondary" 
            @click="configurePlugin(plugin.id)"
          >
            ⚙️ 配置
          </button>
        </div>
      </div>
    </div>

    <!-- 插件详情模态框 -->
    <div v-if="selectedPlugin" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedPlugin.name }} 详情</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="detail-section">
            <h4>基本信息</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <label>版本:</label>
                <span>v{{ selectedPlugin.version }}</span>
              </div>
              <div class="detail-item">
                <label>作者:</label>
                <span>{{ selectedPlugin.author }}</span>
              </div>
              <div class="detail-item">
                <label>状态:</label>
                <span :class="selectedPlugin.status">
                  {{ getStatusText(selectedPlugin.status) }}
                </span>
              </div>
              <div class="detail-item">
                <label>更新时间:</label>
                <span>{{ formatDate(selectedPlugin.updatedAt) }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>描述</h4>
            <p>{{ selectedPlugin.description }}</p>
          </div>
          
          <div v-if="selectedPlugin.dependencies" class="detail-section">
            <h4>依赖项</h4>
            <ul class="dependencies-list">
              <li v-for="dep in selectedPlugin.dependencies" :key="dep">
                {{ dep }}
              </li>
            </ul>
          </div>
          
          <div class="detail-section">
            <h4>配置信息</h4>
            <pre class="config-preview">{{ JSON.stringify(selectedPlugin.config, null, 2) }}</pre>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeModal">关闭</button>
          <button 
            v-if="selectedPlugin.configurable" 
            class="btn btn-primary" 
            @click="configurePlugin(selectedPlugin.id)"
          >
            编辑配置
          </button>
        </div>
      </div>
    </div>

    <!-- 插件市场 -->
    <div class="plugin-market">
      <h3>插件市场</h3>
      <div class="market-grid">
        <div 
          v-for="plugin in availablePlugins" 
          :key="plugin.id" 
          class="market-card"
        >
          <div class="market-icon">{{ getPluginIcon(plugin.type) }}</div>
          <h4>{{ plugin.name }}</h4>
          <p>{{ plugin.description }}</p>
          <button 
            class="btn btn-primary" 
            @click="installPlugin(plugin.id)"
            :disabled="plugin.installed"
          >
            {{ plugin.installed ? '已安装' : '安装' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PluginManager',
  data() {
    return {
      searchQuery: '',
      filterStatus: 'all',
      selectedPlugin: null,
      plugins: [
        {
          id: 'media-info',
          name: '媒体信息插件',
          description: '自动获取和解析媒体文件信息',
          version: '1.0.0',
          author: 'VabHub Team',
          type: 'media',
          enabled: true,
          status: 'running',
          configurable: true,
          updatedAt: new Date('2024-01-15'),
          config: { autoScan: true, cacheSize: 1000 }
        },
        {
          id: 'download-manager',
          name: '下载管理器',
          description: '管理下载任务和进度',
          version: '1.0.0',
          author: 'VabHub Team',
          type: 'download',
          enabled: true,
          status: 'running',
          configurable: true,
          updatedAt: new Date('2024-01-14'),
          config: { maxConcurrent: 3, retryCount: 3 }
        },
        {
          id: 'notification',
          name: '通知插件',
          description: '发送系统通知和提醒',
          version: '1.0.0',
          author: 'VabHub Team',
          type: 'notification',
          enabled: false,
          status: 'stopped',
          configurable: true,
          updatedAt: new Date('2024-01-13'),
          config: { channels: ['web', 'email'] }
        },
        {
          id: 'search',
          name: '搜索插件',
          description: '提供媒体内容搜索功能',
          version: '1.0.0',
          author: 'VabHub Team',
          type: 'search',
          enabled: true,
          status: 'error',
          configurable: true,
          updatedAt: new Date('2024-01-12'),
          config: { sources: ['tmdb', 'douban'] }
        }
      ],
      availablePlugins: [
        {
          id: 'backup',
          name: '备份插件',
          description: '自动备份系统数据和配置',
          type: 'backup',
          installed: false
        },
        {
          id: 'analytics',
          name: '分析插件',
          description: '提供系统使用统计和分析',
          type: 'analytics',
          installed: false
        },
        {
          id: 'sync',
          name: '同步插件',
          description: '多设备间数据同步',
          type: 'sync',
          installed: false
        }
      ]
    }
  },
  computed: {
    filteredPlugins() {
      return this.plugins.filter(plugin => {
        const matchesSearch = plugin.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                            plugin.description.toLowerCase().includes(this.searchQuery.toLowerCase())
        
        const matchesFilter = this.filterStatus === 'all' || 
                            (this.filterStatus === 'enabled' && plugin.enabled) ||
                            (this.filterStatus === 'disabled' && !plugin.enabled) ||
                            (this.filterStatus === 'error' && plugin.status === 'error')
        
        return matchesSearch && matchesFilter
      })
    }
  },
  methods: {
    getPluginIcon(type) {
      const icons = {
        media: '🎬',
        download: '📥',
        notification: '🔔',
        search: '🔍',
        backup: '💾',
        analytics: '📊',
        sync: '🔄'
      }
      return icons[type] || '🔌'
    },
    
    getStatusText(status) {
      const statusMap = {
        running: '运行中',
        stopped: '已停止',
        error: '错误',
        loading: '加载中'
      }
      return statusMap[status] || '未知'
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-CN')
    },
    
    refreshPlugins() {
      console.log('刷新插件列表')
      // 这里应该调用后端API获取最新插件状态
    },
    
    enablePlugin(pluginId) {
      const plugin = this.plugins.find(p => p.id === pluginId)
      if (plugin) {
        plugin.enabled = true
        plugin.status = 'running'
        console.log(`启用插件: ${plugin.name}`)
        // 这里应该调用后端API启用插件
      }
    },
    
    disablePlugin(pluginId) {
      const plugin = this.plugins.find(p => p.id === pluginId)
      if (plugin) {
        plugin.enabled = false
        plugin.status = 'stopped'
        console.log(`禁用插件: ${plugin.name}`)
        // 这里应该调用后端API禁用插件
      }
    },
    
    showPluginDetails(plugin) {
      this.selectedPlugin = { ...plugin }
    },
    
    closeModal() {
      this.selectedPlugin = null
    },
    
    configurePlugin(pluginId) {
      console.log(`配置插件: ${pluginId}`)
      // 这里应该打开插件配置界面
    },
    
    installPlugin(pluginId) {
      const plugin = this.availablePlugins.find(p => p.id === pluginId)
      if (plugin) {
        plugin.installed = true
        console.log(`安装插件: ${plugin.name}`)
        // 这里应该调用后端API安装插件
      }
    }
  },
  mounted() {
    this.refreshPlugins()
  }
}
</script>

<style scoped>
.plugin-manager {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.plugin-header {
  text-align: center;
  margin-bottom: 2rem;
}

.plugin-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.plugin-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.search-section {
  display: flex;
  gap: 1rem;
  flex: 1;
  max-width: 400px;
}

.search-input, .filter-select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
}

.search-input {
  flex: 1;
}

.plugin-list {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.plugin-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.3s, box-shadow 0.3s;
}

.plugin-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.plugin-card.plugin-enabled {
  border-left: 4px solid #27ae60;
}

.plugin-card.plugin-error {
  border-left: 4px solid #e74c3c;
}

.plugin-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.plugin-info {
  flex: 1;
}

.plugin-name {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.plugin-description {
  color: #7f8c8d;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.plugin-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #95a5a6;
  margin-bottom: 0.5rem;
}

.plugin-status {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.running {
  background: #d4edda;
  color: #155724;
}

.status-badge.stopped {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.error {
  background: #fff3cd;
  color: #856404;
}

.plugin-updated {
  font-size: 0.8rem;
  color: #95a5a6;
}

.plugin-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
}

.modal-body {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f3f4;
}

.detail-item label {
  font-weight: 500;
  color: #34495e;
}

.dependencies-list {
  list-style: none;
  padding: 0;
}

.dependencies-list li {
  padding: 0.25rem 0;
  color: #7f8c8d;
}

.config-preview {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  max-height: 200px;
  overflow: auto;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.plugin-market {
  border-top: 2px solid #eee;
  padding-top: 2rem;
}

.plugin-market h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.market-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.market-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.market-card:hover {
  transform: translateY(-2px);
}

.market-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.market-card h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.market-card p {
  color: #7f8c8d;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .plugin-manager {
    padding: 1rem;
  }
  
  .plugin-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-section {
    max-width: none;
  }
  
  .plugin-card {
    flex-direction: column;
    text-align: center;
  }
  
  .plugin-actions {
    justify-content: center;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .market-grid {
    grid-template-columns: 1fr;
  }
}
</style>