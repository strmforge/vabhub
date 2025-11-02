<template>
  <div class="storage-manager">
    <div class="storage-header">
      <h2>存储管理</h2>
      <p>统一管理存储提供商的文件操作</p>
    </div>
    
    <div class="storage-content">
      <!-- 存储提供商选择 -->
      <div class="storage-selector">
        <label class="selector-label">选择存储提供商：</label>
        <select v-model="selectedStorage" class="form-input">
          <option value="pan123">123网盘</option>
          <option value="pan115">115网盘</option>
        </select>
        <button class="btn btn-primary" @click="refreshFileList">刷新</button>
      </div>
      
      <!-- 文件列表 -->
      <div class="file-list-section">
        <h3>文件列表 ({{ selectedStorage }})</h3>
        <div class="file-list">
          <div v-for="file in fileList" :key="file.id" class="file-item">
            <div class="file-info">
              <span class="file-name">{{ file.name }}</span>
              <span class="file-size">{{ formatFileSize(file.size) }}</span>
              <span class="file-modified">{{ formatDate(file.modified) }}</span>
            </div>
            <div class="file-actions">
              <button class="btn btn-secondary" @click="renameFile(file)">重命名</button>
              <button class="btn btn-secondary" @click="moveFile(file)">移动</button>
              <button class="btn btn-primary" @click="downloadFile(file)">下载</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 文件操作面板 -->
      <div class="file-operations">
        <div class="operation-section">
          <h3>文件上传</h3>
          <div class="upload-section">
            <input type="file" @change="handleFileUpload" multiple>
            <button class="btn btn-primary" @click="uploadFiles">上传文件</button>
          </div>
        </div>
        
        <div class="operation-section">
          <h3>批量操作</h3>
          <div class="batch-actions">
            <button class="btn btn-secondary" @click="batchMove">批量移动</button>
            <button class="btn btn-secondary" @click="batchRename">批量重命名</button>
            <button class="btn btn-primary" @click="batchDownload">批量下载</button>
          </div>
        </div>
        
        <div class="operation-section">
          <h3>存储配额</h3>
          <div class="quota-info">
            <div class="quota-bar">
              <div class="quota-progress" :style="{ width: quota.usedPercentage + '%' }"></div>
            </div>
            <div class="quota-text">
              已使用：{{ formatFileSize(quota.used) }} / {{ formatFileSize(quota.total) }}
              ({{ quota.usedPercentage }}%)
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StorageManager',
  data() {
    return {
      selectedStorage: 'pan123',
      fileList: [
        {
          id: 1,
          name: 'movie.mp4',
          size: 1024 * 1024 * 1500, // 1.5GB
          modified: new Date('2024-01-15'),
          type: 'video'
        },
        {
          id: 2,
          name: 'document.pdf',
          size: 1024 * 1024 * 5, // 5MB
          modified: new Date('2024-01-14'),
          type: 'document'
        },
        {
          id: 3,
          name: 'image.jpg',
          size: 1024 * 1024 * 2, // 2MB
          modified: new Date('2024-01-13'),
          type: 'image'
        }
      ],
      quota: {
        used: 1024 * 1024 * 1024 * 50, // 50GB
        total: 1024 * 1024 * 1024 * 100, // 100GB
        usedPercentage: 50
      },
      selectedFiles: [],
      uploadQueue: []
    }
  },
  methods: {
    // 刷新文件列表
    refreshFileList() {
      console.log('刷新文件列表:', this.selectedStorage)
      // 这里应该调用后端API获取文件列表
    },
    
    // 重命名文件
    renameFile(file) {
      const newName = prompt('请输入新文件名:', file.name)
      if (newName && newName !== file.name) {
        console.log(`重命名文件: ${file.name} -> ${newName}`)
        // 这里应该调用后端API重命名文件
      }
    },
    
    // 移动文件
    moveFile(file) {
      const newPath = prompt('请输入目标路径:', '/')
      if (newPath) {
        console.log(`移动文件: ${file.name} -> ${newPath}`)
        // 这里应该调用后端API移动文件
      }
    },
    
    // 下载文件
    downloadFile(file) {
      console.log('下载文件:', file.name)
      // 这里应该调用后端API下载文件
    },
    
    // 处理文件上传
    handleFileUpload(event) {
      const files = Array.from(event.target.files)
      this.uploadQueue = files.map(file => ({
        file,
        name: file.name,
        size: file.size,
        progress: 0
      }))
    },
    
    // 上传文件
    uploadFiles() {
      if (this.uploadQueue.length === 0) {
        alert('请选择要上传的文件')
        return
      }
      
      console.log('开始上传文件:', this.uploadQueue)
      // 这里应该调用后端API上传文件
    },
    
    // 批量操作
    batchMove() {
      if (this.selectedFiles.length === 0) {
        alert('请先选择文件')
        return
      }
      console.log('批量移动文件:', this.selectedFiles)
    },
    
    batchRename() {
      if (this.selectedFiles.length === 0) {
        alert('请先选择文件')
        return
      }
      console.log('批量重命名文件:', this.selectedFiles)
    },
    
    batchDownload() {
      if (this.selectedFiles.length === 0) {
        alert('请先选择文件')
        return
      }
      console.log('批量下载文件:', this.selectedFiles)
    },
    
    // 工具函数
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-CN')
    }
  },
  mounted() {
    this.refreshFileList()
  }
}
</script>

<style scoped>
.storage-header {
  text-align: center;
  margin-bottom: 2rem;
}

.storage-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.storage-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.selector-label {
  font-weight: 500;
  color: #34495e;
}

.file-list-section {
  margin-bottom: 2rem;
}

.file-list-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.file-list {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
  background: white;
}

.file-item:last-child {
  border-bottom: none;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.file-name {
  font-weight: 500;
  color: #2c3e50;
}

.file-size, .file-modified {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.file-actions {
  display: flex;
  gap: 0.5rem;
}

.file-operations {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.operation-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.operation-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.upload-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.batch-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.quota-info {
  text-align: center;
}

.quota-bar {
  width: 100%;
  height: 20px;
  background: #ecf0f1;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.quota-progress {
  height: 100%;
  background: #3498db;
  transition: width 0.3s;
}

.quota-text {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
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

.form-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}
</style>