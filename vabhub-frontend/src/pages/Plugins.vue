<template>
  <div class="plugins-page">
    <div class="page-header">
      <h1>插件管理</h1>
      <p>管理 VabHub 功能扩展插件</p>
    </div>
    
    <div class="plugins-content">
      <!-- 插件市场 -->
      <div class="section">
        <div class="section-header">
          <h2>插件市场</h2>
          <div class="section-actions">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="搜索插件..." 
              class="search-input"
            />
            <button class="btn btn-primary" @click="refreshPlugins">
              <span class="btn-icon">🔄</span>
              刷新
            </button>
          </div>
        </div>
        
        <div class="plugins-grid">
          <div 
            v-for="plugin in filteredPlugins" 
            :key="plugin.id"
            class="plugin-card"
            :class="{ 'installed': plugin.installed }"
          >
            <div class="plugin-header">
              <div class="plugin-icon">{{ plugin.icon }}</div>
              <div class="plugin-info">
                <h3>{{ plugin.name }}</h3>
                <span class="plugin-version">v{{ plugin.version }}</span>
              </div>
              <div class="plugin-status">
                <span v-if="plugin.installed" class="status-badge installed">已安装</span>
                <span v-else class="status-badge available">可用</span>
              </div>
            </div>
            
            <div class="plugin-description">
              <p>{{ plugin.description }}</p>
            </div>
            
            <div class="plugin-meta">
              <span class="meta-item">作者: {{ plugin.author }}</span>
              <span class="meta-item">分类: {{ plugin.category }}</span>
            </div>
            
            <div class="plugin-actions">
              <button 
                v-if="!plugin.installed" 
                class="btn btn-primary"
                @click="installPlugin(plugin)"
                :disabled="plugin.installing"
              >
                <span v-if="plugin.installing">安装中...</span>
                <span v-else>安装</span>
              </button>
              
              <div v-else class="installed-actions">
                <button 
                  class="btn btn-secondary"
                  @click="configurePlugin(plugin)"
                >
                  配置
                </button>
                <button 
                  class="btn btn-danger"
                  @click="uninstallPlugin(plugin)"
                >
                  卸载
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 已安装插件 -->
      <div class="section">
        <div class="section-header">
          <h2>已安装插件</h2>
          <div class="section-actions">
            <button class="btn btn-secondary" @click="updateAllPlugins">
              <span class="btn-icon">🔄</span>
              更新全部
            </button>
          </div>
        </div>
        
        <div class="installed-plugins">
          <div 
            v-for="plugin in installedPlugins" 
            :key="plugin.id"
            class="installed-plugin"
          >
            <div class="plugin-main">
              <div class="plugin-icon">{{ plugin.icon }}</div>
              <div class="plugin-details">
                <h3>{{ plugin.name }}</h3>
                <p>{{ plugin.description }}</p>
                <div class="plugin-meta">
                  <span>版本: v{{ plugin.version }}</span>
                  <span>状态: {{ plugin.enabled ? '已启用' : '已禁用' }}</span>
                </div>
              </div>
            </div>
            
            <div class="plugin-controls">
              <button 
                class="btn btn-secondary"
                @click="togglePlugin(plugin)"
              >
                {{ plugin.enabled ? '禁用' : '启用' }}
              </button>
              <button 
                class="btn btn-primary"
                @click="configurePlugin(plugin)"
              >
                配置
              </button>
              <button 
                class="btn btn-danger"
                @click="uninstallPlugin(plugin)"
              >
                卸载
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAppStore } from '@/stores/app'

export default {
  name: 'Plugins',
  data() {
    return {
      searchQuery: '',
      plugins: [
        {
          id: 1,
          name: '媒体信息刮削器',
          description: '自动获取电影、电视剧的元数据信息',
          version: '1.2.0',
          author: 'VabHub Team',
          category: '媒体处理',
          icon: '🎬',
          installed: true,
          enabled: true,
          installing: false
        },
        {
          id: 2,
          name: '下载管理器',
          description: '管理下载任务和进度监控',
          version: '1.1.0',
          author: 'VabHub Team',
          category: '下载管理',
          icon: '📥',
          installed: true,
          enabled: true,
          installing: false
        },
        {
          id: 3,
          name: '文件整理器',
          description: '自动整理媒体文件到指定目录结构',
          version: '1.0.0',
          author: 'VabHub Team',
          category: '文件管理',
          icon: '📁',
          installed: false,
          enabled: false,
          installing: false
        },
        {
          id: 4,
          name: '通知中心',
          description: '发送系统通知和提醒',
          version: '1.0.0',
          author: 'VabHub Team',
          category: '系统工具',
          icon: '🔔',
          installed: false,
          enabled: false,
          installing: false
        }
      ]
    }
  },
  computed: {
    filteredPlugins() {
      if (!this.searchQuery) {
        return this.plugins
      }
      
      const query = this.searchQuery.toLowerCase()
      return this.plugins.filter(plugin => 
        plugin.name.toLowerCase().includes(query) ||
        plugin.description.toLowerCase().includes(query) ||
        plugin.category.toLowerCase().includes(query)
      )
    },
    
    installedPlugins() {
      return this.plugins.filter(plugin => plugin.installed)
    }
  },
  methods: {
    async installPlugin(plugin) {
      plugin.installing = true
      
      try {
        // 模拟安装过程
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        plugin.installed = true
        plugin.enabled = true
        
        this.showNotification(`插件 "${plugin.name}" 安装成功`, 'success')
      } catch (error) {
        console.error('安装插件失败:', error)
        this.showNotification('安装插件失败', 'error')
      } finally {
        plugin.installing = false
      }
    },
    
    async uninstallPlugin(plugin) {
      if (!confirm(`确定要卸载插件 "${plugin.name}" 吗？`)) {
        return
      }
      
      try {
        // 模拟卸载过程
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        plugin.installed = false
        plugin.enabled = false
        
        this.showNotification(`插件 "${plugin.name}" 卸载成功`, 'success')
      } catch (error) {
        console.error('卸载插件失败:', error)
        this.showNotification('卸载插件失败', 'error')
      }
    },
    
    togglePlugin(plugin) {
      plugin.enabled = !plugin.enabled
      const status = plugin.enabled ? '启用' : '禁用'
      this.showNotification(`插件 "${plugin.name}" 已${status}`, 'success')
    },
    
    configurePlugin(plugin) {
      this.showNotification(`正在配置插件: ${plugin.name}`, 'info')
      // 这里应该打开插件配置页面
    },
    
    refreshPlugins() {
      this.showNotification('插件列表已刷新', 'success')
    },
    
    updateAllPlugins() {
      this.showNotification('正在检查插件更新...', 'info')
    },
    
    showNotification(message, type) {
      // 这里应该显示通知组件
      console.log(`[${type}] ${message}`)
    }
  }
}
</script>

<style scoped>
.plugins-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.page-header p {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.section {
  margin-bottom: 3rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.section-header h2 {
  margin: 0;
  color: #2c3e50;
}

.section-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  width: 200px;
}

.plugins-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.plugin-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.plugin-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.plugin-card.installed {
  border-color: #3498db;
  background: #f8fbfd;
}

.plugin-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.plugin-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.plugin-info {
  flex: 1;
}

.plugin-info h3 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.plugin-version {
  font-size: 0.875rem;
  color: #7f8c8d;
}

.plugin-status {
  margin-left: auto;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.installed {
  background: #d4edda;
  color: #155724;
}

.status-badge.available {
  background: #d1ecf1;
  color: #0c5460;
}

.plugin-description {
  margin-bottom: 1rem;
}

.plugin-description p {
  margin: 0;
  color: #6c757d;
  line-height: 1.5;
}

.plugin-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.plugin-actions {
  text-align: center;
}

.installed-plugins {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.installed-plugin {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plugin-main {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.plugin-icon {
  font-size: 2rem;
}

.plugin-details h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.plugin-details p {
  margin: 0 0 0.5rem 0;
  color: #6c757d;
}

.plugin-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #7f8c8d;
}

.plugin-controls {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background 0.3s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
}

.btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-icon {
  margin-right: 0.5rem;
}

@media (max-width: 768px) {
  .plugins-page {
    padding: 1rem;
  }
  
  .plugins-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .installed-plugin {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .plugin-controls {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>