<template>
  <div class="storage-page">
    <div class="page-header">
      <h1>存储管理</h1>
      <p>管理媒体文件存储和云盘配置</p>
    </div>
    
    <div class="storage-content">
      <!-- 存储概览 -->
      <div class="storage-overview">
        <div class="overview-card">
          <div class="overview-icon">💾</div>
          <div class="overview-info">
            <h3>总存储空间</h3>
            <p class="overview-value">{{ formatBytes(totalSpace) }}</p>
          </div>
        </div>
        
        <div class="overview-card">
          <div class="overview-icon">📊</div>
          <div class="overview-info">
            <h3>已使用空间</h3>
            <p class="overview-value">{{ formatBytes(usedSpace) }}</p>
          </div>
        </div>
        
        <div class="overview-card">
          <div class="overview-icon">🔄</div>
          <div class="overview-info">
            <h3>可用空间</h3>
            <p class="overview-value">{{ formatBytes(freeSpace) }}</p>
          </div>
        </div>
        
        <div class="overview-card">
          <div class="overview-icon">📁</div>
          <div class="overview-info">
            <h3>文件数量</h3>
            <p class="overview-value">{{ fileCount }} 个</p>
          </div>
        </div>
      </div>
      
      <!-- 存储提供商 -->
      <div class="section">
        <div class="section-header">
          <h2>存储提供商</h2>
          <button class="btn btn-primary" @click="addStorageProvider">
            <span class="btn-icon">➕</span>
            添加提供商
          </button>
        </div>
        
        <div class="storage-providers">
          <div 
            v-for="provider in storageProviders" 
            :key="provider.id"
            class="provider-card"
            :class="{ 'connected': provider.connected }"
          >
            <div class="provider-header">
              <div class="provider-icon">{{ provider.icon }}</div>
              <div class="provider-info">
                <h3>{{ provider.name }}</h3>
                <p>{{ provider.description }}</p>
                <div class="provider-status">
                  <span class="status-badge" :class="provider.connected ? 'connected' : 'disconnected'">
                    {{ provider.connected ? '已连接' : '未连接' }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="provider-details">
              <div class="detail-item">
                <span class="detail-label">存储空间:</span>
                <span class="detail-value">{{ formatBytes(provider.space) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">文件数量:</span>
                <span class="detail-value">{{ provider.fileCount }} 个</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">最后同步:</span>
                <span class="detail-value">{{ provider.lastSync }}</span>
              </div>
            </div>
            
            <div class="provider-actions">
              <button 
                class="btn btn-secondary"
                @click="testConnection(provider)"
              >
                测试连接
              </button>
              <button 
                class="btn btn-primary"
                @click="configureProvider(provider)"
              >
                配置
              </button>
              <button 
                class="btn btn-danger"
                @click="removeProvider(provider)"
              >
                移除
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 文件浏览器 -->
      <div class="section">
        <div class="section-header">
          <h2>文件浏览器</h2>
          <div class="file-actions">
            <input 
              v-model="fileSearch" 
              type="text" 
              placeholder="搜索文件..." 
              class="search-input"
            />
            <button class="btn btn-secondary" @click="refreshFiles">
              <span class="btn-icon">🔄</span>
              刷新
            </button>
            <button class="btn btn-primary" @click="uploadFile">
              <span class="btn-icon">📤</span>
              上传文件
            </button>
          </div>
        </div>
        
        <div class="file-browser">
          <div class="file-toolbar">
            <div class="breadcrumb">
              <span 
                v-for="(path, index) in currentPath" 
                :key="index"
                class="breadcrumb-item"
                @click="navigateToPath(index)"
              >
                {{ path }}
              </span>
            </div>
            <div class="view-options">
              <button 
                class="view-btn"
                :class="{ active: viewMode === 'grid' }"
                @click="viewMode = 'grid'"
              >
                📊
              </button>
              <button 
                class="view-btn"
                :class="{ active: viewMode === 'list' }"
                @click="viewMode = 'list'"
              >
                📋
              </button>
            </div>
          </div>
          
          <div class="file-list" :class="viewMode">
            <div 
              v-for="file in filteredFiles" 
              :key="file.id"
              class="file-item"
              @dblclick="handleFileAction(file)"
            >
              <div class="file-icon">{{ getFileIcon(file.type) }}</div>
              <div class="file-info">
                <h4>{{ file.name }}</h4>
                <p>{{ formatBytes(file.size) }}</p>
                <span class="file-date">{{ file.modified }}</span>
              </div>
              <div class="file-actions">
                <button class="action-btn" @click="downloadFile(file)" title="下载">
                  📥
                </button>
                <button class="action-btn" @click="deleteFile(file)" title="删除">
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Storage',
  data() {
    return {
      totalSpace: 1024 * 1024 * 1024 * 100, // 100GB
      usedSpace: 1024 * 1024 * 1024 * 35, // 35GB
      fileCount: 1250,
      fileSearch: '',
      viewMode: 'grid',
      currentPath: ['根目录'],
      
      storageProviders: [
        {
          id: 1,
          name: '123网盘',
          description: '高速云存储服务',
          icon: '☁️',
          connected: true,
          space: 1024 * 1024 * 1024 * 50, // 50GB
          fileCount: 500,
          lastSync: '2024-01-15 14:30'
        },
        {
          id: 2,
          name: '115网盘',
          description: '大容量云存储',
          icon: '💾',
          connected: true,
          space: 1024 * 1024 * 1024 * 100, // 100GB
          fileCount: 750,
          lastSync: '2024-01-15 13:45'
        }
      ],
      
      files: [
        {
          id: 1,
          name: '电影',
          type: 'folder',
          size: 1024 * 1024 * 1024 * 25,
          modified: '2024-01-15 10:30'
        },
        {
          id: 2,
          name: '电视剧',
          type: 'folder',
          size: 1024 * 1024 * 1024 * 8,
          modified: '2024-01-14 16:20'
        },
        {
          id: 3,
          name: '音乐',
          type: 'folder',
          size: 1024 * 1024 * 1024 * 2,
          modified: '2024-01-13 09:15'
        },
        {
          id: 4,
          name: 'avatar.mp4',
          type: 'video',
          size: 1024 * 1024 * 2.5,
          modified: '2024-01-15 14:25'
        },
        {
          id: 5,
          name: 'document.pdf',
          type: 'document',
          size: 1024 * 512,
          modified: '2024-01-12 11:40'
        }
      ]
    }
  },
  computed: {
    freeSpace() {
      return this.totalSpace - this.usedSpace
    },
    
    filteredFiles() {
      if (!this.fileSearch) {
        return this.files
      }
      
      const query = this.fileSearch.toLowerCase()
      return this.files.filter(file => 
        file.name.toLowerCase().includes(query)
      )
    }
  },
  methods: {
    formatBytes(bytes) {
      if (bytes === 0) return '0 Bytes'
      
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    getFileIcon(type) {
      const icons = {
        folder: '📁',
        video: '🎬',
        audio: '🎵',
        image: '🖼️',
        document: '📄',
        archive: '📦',
        default: '📄'
      }
      
      return icons[type] || icons.default
    },
    
    testConnection(provider) {
      this.showNotification(`正在测试 ${provider.name} 连接...`, 'info')
      
      // 模拟连接测试
      setTimeout(() => {
        provider.connected = !provider.connected
        const status = provider.connected ? '连接成功' : '连接失败'
        this.showNotification(`${provider.name} ${status}`, provider.connected ? 'success' : 'error')
      }, 2000)
    },
    
    configureProvider(provider) {
      this.showNotification(`正在配置 ${provider.name}`, 'info')
    },
    
    removeProvider(provider) {
      if (confirm(`确定要移除 ${provider.name} 吗？`)) {
        this.storageProviders = this.storageProviders.filter(p => p.id !== provider.id)
        this.showNotification(`${provider.name} 已移除`, 'success')
      }
    },
    
    addStorageProvider() {
      this.showNotification('添加存储提供商功能开发中...', 'info')
    },
    
    refreshFiles() {
      this.showNotification('文件列表已刷新', 'success')
    },
    
    uploadFile() {
      this.showNotification('文件上传功能开发中...', 'info')
    },
    
    handleFileAction(file) {
      if (file.type === 'folder') {
        this.currentPath.push(file.name)
        this.showNotification(`进入文件夹: ${file.name}`, 'info')
      } else {
        this.downloadFile(file)
      }
    },
    
    downloadFile(file) {
      this.showNotification(`开始下载: ${file.name}`, 'info')
    },
    
    deleteFile(file) {
      if (confirm(`确定要删除 "${file.name}" 吗？`)) {
        this.files = this.files.filter(f => f.id !== file.id)
        this.showNotification(`文件 "${file.name}" 已删除`, 'success')
      }
    },
    
    navigateToPath(index) {
      this.currentPath = this.currentPath.slice(0, index + 1)
    },
    
    showNotification(message, type) {
      console.log(`[${type}] ${message}`)
    }
  }
}
</script>

<style scoped>
.storage-page {
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

.storage-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.overview-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.overview-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.overview-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #7f8c8d;
  font-weight: 500;
}

.overview-value {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
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

.file-actions {
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

.storage-providers {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.provider-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.provider-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.provider-card.connected {
  border-color: #28a745;
}

.provider-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.provider-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.provider-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.provider-info p {
  margin: 0 0 0.5rem 0;
  color: #6c757d;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.connected {
  background: #d4edda;
  color: #155724;
}

.status-badge.disconnected {
  background: #f8d7da;
  color: #721c24;
}

.provider-details {
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.detail-label {
  color: #6c757d;
}

.detail-value {
  color: #2c3e50;
  font-weight: 500;
}

.provider-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.file-browser {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  overflow: hidden;
}

.file-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e9ecef;
  background: #f8f9fa;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb-item {
  cursor: pointer;
  color: #3498db;
  font-weight: 500;
}

.breadcrumb-item:hover {
  text-decoration: underline;
}

.breadcrumb-item:not(:last-child)::after {
  content: '>';
  margin-left: 0.5rem;
  color: #6c757d;
}

.view-options {
  display: flex;
  gap: 0.5rem;
}

.view-btn {
  background: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
}

.view-btn.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.file-list {
  padding: 1rem;
}

.file-list.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.file-list.list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.file-item:hover {
  background: #f8f9fa;
}

.file-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.file-info {
  flex: 1;
}

.file-info h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.file-info p {
  margin: 0 0 0.25rem 0;
  color: #6c757d;
  font-size: 0.875rem;
}

.file-date {
  font-size: 0.75rem;
  color: #95a5a6;
}

.file-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.action-btn:hover {
  background: #e9ecef;
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

.btn-icon {
  margin-right: 0.5rem;
}

@media (max-width: 768px) {
  .storage-page {
    padding: 1rem;
  }
  
  .storage-overview {
    grid-template-columns: 1fr;
  }
  
  .storage-providers {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .file-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .file-list.grid {
    grid-template-columns: 1fr;
  }
}
</style>