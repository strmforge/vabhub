<template>
  <div class="music-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>音乐管理</h1>
      <p>智能音乐文件分类、重命名和整理</p>
    </div>

    <!-- 功能选项卡 -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.name }}
      </button>
    </div>

    <!-- 文件浏览器 -->
    <div v-if="activeTab === 'browser'" class="tab-content">
      <div class="file-browser">
        <div class="browser-header">
          <div class="path-navigation">
            <span 
              v-for="(part, index) in currentPathParts" 
              :key="index"
              @click="navigateToPath(part.path)"
              class="path-part"
            >
              {{ part.name }}
            </span>
          </div>
          <div class="browser-actions">
            <button @click="refreshFiles" class="btn-refresh">刷新</button>
            <button @click="showUploadDialog = true" class="btn-upload">上传</button>
          </div>
        </div>

        <div class="file-list">
          <div class="file-item" v-for="file in files" :key="file.path">
            <div class="file-icon">
              <i :class="getFileIcon(file)"></i>
            </div>
            <div class="file-info">
              <div class="file-name" @click="handleFileClick(file)">
                {{ file.name }}
              </div>
              <div class="file-details">
                <span v-if="!file.is_dir">{{ formatFileSize(file.size) }}</span>
                <span>{{ formatDate(file.modify_time) }}</span>
              </div>
            </div>
            <div class="file-actions">
              <button @click="previewFile(file)" v-if="!file.is_dir">预览</button>
              <button @click="renameFile(file)">重命名</button>
              <button @click="deleteFile(file)">删除</button>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination" v-if="totalPages > 1">
          <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">上一页</button>
          <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
          <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">下一页</button>
        </div>
      </div>
    </div>

    <!-- 音乐分类 -->
    <div v-if="activeTab === 'classification'" class="tab-content">
      <div class="classification-panel">
        <div class="panel-header">
          <h3>智能音乐分类</h3>
          <button @click="startClassification" class="btn-classify">开始分类</button>
        </div>

        <div class="classification-results">
          <div class="stats">
            <div class="stat-item">
              <span class="stat-label">总文件数</span>
              <span class="stat-value">{{ classificationStats.total_files || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">已分类</span>
              <span class="stat-value">{{ classificationStats.categorized_files || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">未分类</span>
              <span class="stat-value">{{ classificationStats.uncategorized_files || 0 }}</span>
            </div>
          </div>

          <div class="category-distribution">
            <h4>分类分布</h4>
            <div class="distribution-chart">
              <div 
                v-for="(count, category) in classificationStats.category_distribution || {}"
                :key="category"
                class="distribution-item"
              >
                <span class="category-name">{{ category }}</span>
                <span class="category-count">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="classified-files">
          <h4>分类结果</h4>
          <div class="file-classification" v-for="(classification, filePath) in classifications" :key="filePath">
            <div class="file-classification-item">
              <span class="file-name">{{ getFileName(filePath) }}</span>
              <span class="media-type">{{ classification.media_type }}</span>
              <span class="confidence" :class="getConfidenceClass(classification.confidence)">
                置信度: {{ (classification.confidence * 100).toFixed(1) }}%
              </span>
              <span class="directory-structure">
                {{ directoryStructures[filePath] }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 音乐重命名 -->
    <div v-if="activeTab === 'renaming'" class="tab-content">
      <div class="renaming-panel">
        <div class="panel-header">
          <h3>音乐文件重命名</h3>
          <div class="renaming-options">
            <select v-model="selectedTemplate">
              <option value="standard">标准格式</option>
              <option value="album">专辑格式</option>
              <option value="detailed">详细格式</option>
              <option value="simple">简单格式</option>
              <option value="classical">古典音乐格式</option>
            </select>
            <select v-model="selectedStructure">
              <option value="artist_album">艺术家/专辑</option>
              <option value="genre_artist">流派/艺术家</option>
              <option value="year_artist">年份/艺术家</option>
              <option value="simple">简单结构</option>
              <option value="flat">平铺结构</option>
            </select>
            <button @click="startRenaming" class="btn-rename">开始重命名</button>
          </div>
        </div>

        <div class="file-selection">
          <h4>选择要重命名的文件</h4>
          <div class="file-checkboxes">
            <label v-for="file in musicFiles" :key="file.path" class="file-checkbox">
              <input 
                type="checkbox" 
                :value="file.path" 
                v-model="selectedFiles"
              >
              {{ file.name }}
            </label>
          </div>
        </div>

        <div class="preview-results" v-if="renamePreview.length > 0">
          <h4>重命名预览</h4>
          <div class="preview-list">
            <div 
              v-for="preview in renamePreview" 
              :key="preview.old_path"
              class="preview-item"
            >
              <div class="old-name">{{ getFileName(preview.old_path) }}</div>
              <div class="arrow">→</div>
              <div class="new-name">{{ getFileName(preview.new_path) }}</div>
            </div>
          </div>
        </div>

        <div class="renaming-results" v-if="renamingResults.length > 0">
          <h4>重命名结果</h4>
          <div class="result-list">
            <div 
              v-for="result in renamingResults" 
              :key="result.old_path"
              :class="['result-item', { success: result.success, error: !result.success }]"
            >
              <span class="result-status">
                {{ result.success ? '✓' : '✗' }}
              </span>
              <span class="result-message">{{ result.message }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 上传对话框 -->
    <div v-if="showUploadDialog" class="modal-overlay">
      <div class="modal-content">
        <h3>上传音乐文件</h3>
        <div class="upload-area" @drop="handleFileDrop" @dragover="handleDragOver">
          <input 
            type="file" 
            ref="fileInput" 
            multiple 
            @change="handleFileSelect"
            accept=".mp3,.flac,.wav,.aac,.ogg,.m4a"
          >
          <p>拖放文件到这里或点击选择文件</p>
        </div>
        <div class="upload-progress" v-if="uploading">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
          </div>
          <span>{{ uploadProgress }}%</span>
        </div>
        <div class="modal-actions">
          <button @click="uploadFiles" :disabled="!selectedUploadFiles.length || uploading">上传</button>
          <button @click="showUploadDialog = false">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'MusicManagement',
  setup() {
    const store = useStore()
    
    // 响应式数据
    const activeTab = ref('browser')
    const currentPath = ref('/')
    const currentPage = ref(1)
    const pageSize = ref(50)
    const files = ref([])
    const totalFiles = ref(0)
    const showUploadDialog = ref(false)
    const selectedUploadFiles = ref([])
    const uploading = ref(false)
    const uploadProgress = ref(0)
    
    // 分类相关数据
    const classifications = ref({})
    const classificationStats = ref({})
    const directoryStructures = ref({})
    
    // 重命名相关数据
    const selectedFiles = ref([])
    const selectedTemplate = ref('standard')
    const selectedStructure = ref('artist_album')
    const renamePreview = ref([])
    const renamingResults = ref([])
    
    // 选项卡配置
    const tabs = [
      { id: 'browser', name: '文件浏览' },
      { id: 'classification', name: '智能分类' },
      { id: 'renaming', name: '文件重命名' }
    ]
    
    // 计算属性
    const totalPages = computed(() => Math.ceil(totalFiles.value / pageSize.value))
    const currentPathParts = computed(() => {
      const parts = currentPath.value.split('/').filter(p => p)
      const result = []
      let current = ''
      
      parts.forEach(part => {
        current += '/' + part
        result.push({
          name: part,
          path: current
        })
      })
      
      return result
    })
    
    const musicFiles = computed(() => {
      return files.value.filter(file => 
        !file.is_dir && 
        ['.mp3', '.flac', '.wav', '.aac', '.ogg', '.m4a'].some(ext => 
          file.name.toLowerCase().endsWith(ext)
        )
      )
    })
    
    // 方法
    const loadFiles = async () => {
      try {
        const response = await store.dispatch('storage/listFiles', {
          storageId: 'local',
          path: currentPath.value,
          page: currentPage.value,
          size: pageSize.value
        })
        
        files.value = response.files
        totalFiles.value = response.total
      } catch (error) {
        console.error('加载文件失败:', error)
      }
    }
    
    const navigateToPath = (path) => {
      currentPath.value = path
      currentPage.value = 1
      loadFiles()
    }
    
    const refreshFiles = () => {
      loadFiles()
    }
    
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        loadFiles()
      }
    }
    
    const getFileIcon = (file) => {
      if (file.is_dir) return 'fas fa-folder'
      
      const ext = file.name.split('.').pop().toLowerCase()
      switch (ext) {
        case 'mp3':
        case 'flac':
        case 'wav':
        case 'aac':
        case 'ogg':
        case 'm4a':
          return 'fas fa-music'
        default:
          return 'fas fa-file'
      }
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B'
      
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }
    
    const handleFileClick = (file) => {
      if (file.is_dir) {
        navigateToPath(file.path)
      }
    }
    
    const startClassification = async () => {
      try {
        const filePaths = musicFiles.value.map(file => file.path)
        
        const response = await store.dispatch('storage/classifyMedia', {
          file_paths: filePaths
        })
        
        classifications.value = response.classifications
        classificationStats.value = response.statistics
        directoryStructures.value = response.directory_structures
      } catch (error) {
        console.error('分类失败:', error)
      }
    }
    
    const startRenaming = async () => {
      try {
        const requests = selectedFiles.value.map(filePath => ({
          source_path: filePath,
          target_dir: '/Music',
          template: selectedTemplate.value,
          structure_type: selectedStructure.value,
          operation: 'move'
        }))
        
        const response = await store.dispatch('storage/batchRenameMusic', requests)
        renamingResults.value = response.results
      } catch (error) {
        console.error('重命名失败:', error)
      }
    }
    
    const getFileName = (path) => {
      return path.split('/').pop()
    }
    
    const getConfidenceClass = (confidence) => {
      if (confidence >= 0.8) return 'high'
      if (confidence >= 0.5) return 'medium'
      return 'low'
    }
    
    const handleFileDrop = (event) => {
      event.preventDefault()
      selectedUploadFiles.value = Array.from(event.dataTransfer.files)
    }
    
    const handleDragOver = (event) => {
      event.preventDefault()
    }
    
    const handleFileSelect = (event) => {
      selectedUploadFiles.value = Array.from(event.target.files)
    }
    
    const uploadFiles = async () => {
      uploading.value = true
      uploadProgress.value = 0
      
      try {
        for (let i = 0; i < selectedUploadFiles.value.length; i++) {
          const file = selectedUploadFiles.value[i]
          
          // 模拟上传进度
          const interval = setInterval(() => {
            uploadProgress.value = Math.min(uploadProgress.value + 10, 100)
          }, 100)
          
          await store.dispatch('storage/uploadFile', {
            storageId: 'local',
            file: file,
            targetPath: currentPath.value
          })
          
          clearInterval(interval)
          uploadProgress.value = ((i + 1) / selectedUploadFiles.value.length) * 100
        }
        
        showUploadDialog.value = false
        selectedUploadFiles.value = []
        loadFiles()
      } catch (error) {
        console.error('上传失败:', error)
      } finally {
        uploading.value = false
        uploadProgress.value = 0
      }
    }
    
    // 生命周期
    onMounted(() => {
      loadFiles()
    })
    
    return {
      activeTab,
      currentPath,
      currentPage,
      files,
      totalFiles,
      showUploadDialog,
      selectedUploadFiles,
      uploading,
      uploadProgress,
      classifications,
      classificationStats,
      directoryStructures,
      selectedFiles,
      selectedTemplate,
      selectedStructure,
      renamePreview,
      renamingResults,
      tabs,
      totalPages,
      currentPathParts,
      musicFiles,
      navigateToPath,
      refreshFiles,
      changePage,
      getFileIcon,
      formatFileSize,
      formatDate,
      handleFileClick,
      startClassification,
      startRenaming,
      getFileName,
      getConfidenceClass,
      handleFileDrop,
      handleDragOver,
      handleFileSelect,
      uploadFiles
    }
  }
}
</script>

<style scoped>
.music-management {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 5px;
}

.page-header p {
  color: #666;
  font-size: 1.1rem;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tabs button.active {
  border-bottom-color: #007bff;
  color: #007bff;
}

.tab-content {
  min-height: 500px;
}

.file-browser {
  border: 1px solid #ddd;
  border-radius: 5px;
  overflow: hidden;
}

.browser-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #ddd;
}

.path-navigation {
  display: flex;
  align-items: center;
}

.path-part {
  cursor: pointer;
  color: #007bff;
  margin: 0 5px;
}

.path-part:hover {
  text-decoration: underline;
}

.browser-actions button {
  margin-left: 10px;
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 3px;
  background: white;
  cursor: pointer;
}

.file-list {
  max-height: 600px;
  overflow-y: auto;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
}

.file-item:hover {
  background: #f8f9fa;
}

.file-icon {
  margin-right: 15px;
  font-size: 1.2rem;
  color: #666;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 500;
  cursor: pointer;
}

.file-name:hover {
  color: #007bff;
}

.file-details {
  font-size: 0.9rem;
  color: #666;
}

.file-details span {
  margin-right: 15px;
}

.file-actions button {
  margin-left: 5px;
  padding: 3px 8px;
  border: 1px solid #ddd;
  border-radius: 3px;
  background: white;
  cursor: pointer;
  font-size: 0.8rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
}

.pagination button {
  margin: 0 10px;
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 3px;
  background: white;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.classification-panel,
.renaming-panel {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  min-width: 100px;
}

.stat-label {
  display: block;
  font-size: 0.9rem;
  color: #666;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.distribution-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 1px solid #eee;
}

.file-classification-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 3px;
  margin-bottom: 5px;
}

.confidence.high { color: #28a745; }
.confidence.medium { color: #ffc107; }
.confidence.low { color: #dc3545; }

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
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  min-width: 400px;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 5px;
  padding: 40px;
  text-align: center;
  margin: 20px 0;
}

.upload-area:hover {
  border-color: #007bff;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  margin: 10px 0;
}

.progress-fill {
  height: 100%;
  background: #007bff;
  transition: width 0.3s;
}

.btn-classify,
.btn-rename {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 3px;
  cursor: pointer;
}

.btn-refresh,
.btn-upload {
  background: #28a745;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}

.result-item.success { color: #28a745; }
.result-item.error { color: #dc3545; }
</style>