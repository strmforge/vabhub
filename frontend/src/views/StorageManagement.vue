<template>
  <div class="storage-management">
    <!-- 存储管理头部 -->
    <div class="storage-header">
      <h1>存储 & 目录管理</h1>
      <p>基于MoviePilot设计，完整复刻存储管理功能</p>
    </div>

    <!-- 存储列表 -->
    <div class="storage-list">
      <h2>存储列表</h2>
      <div class="storage-cards">
        <div 
          v-for="storage in storages" 
          :key="storage.id"
          class="storage-card"
          :class="{ active: selectedStorage === storage.id }"
          @click="selectStorage(storage.id)"
        >
          <div class="storage-icon">
            <i :class="getStorageIcon(storage.type)"></i>
          </div>
          <div class="storage-info">
            <h3>{{ storage.name }}</h3>
            <p>{{ storage.description }}</p>
            <div class="storage-status">
              <span :class="['status', storage.available ? 'online' : 'offline']">
                {{ storage.available ? '在线' : '离线' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 文件浏览器 -->
    <div class="file-browser" v-if="selectedStorage">
      <div class="browser-header">
        <h2>文件浏览器</h2>
        <div class="browser-actions">
          <button @click="refreshFiles" class="btn btn-primary">
            <i class="fas fa-sync-alt"></i> 刷新
          </button>
          <button @click="createFolder" class="btn btn-secondary">
            <i class="fas fa-folder-plus"></i> 新建文件夹
          </button>
          <button @click="uploadFile" class="btn btn-success">
            <i class="fas fa-upload"></i> 上传文件
          </button>
        </div>
      </div>

      <!-- 路径导航 -->
      <div class="path-navigation">
        <breadcrumb :path="currentPath" @navigate="navigateToPath" />
      </div>

      <!-- 文件列表 -->
      <div class="file-list">
        <table class="file-table">
          <thead>
            <tr>
              <th width="40">
                <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
              </th>
              <th>名称</th>
              <th width="100">大小</th>
              <th width="150">修改时间</th>
              <th width="120">类型</th>
              <th width="200">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="file in files" :key="file.path" class="file-item">
              <td>
                <input 
                  type="checkbox" 
                  v-model="selectedFiles" 
                  :value="file.path"
                />
              </td>
              <td class="file-name">
                <i :class="getFileIcon(file)"></i>
                <span 
                  @click="file.is_dir ? navigateToPath(file.path) : previewFile(file)"
                  class="file-link"
                >
                  {{ file.name }}
                </span>
              </td>
              <td class="file-size">{{ formatFileSize(file.size) }}</td>
              <td class="file-time">{{ formatTime(file.modify_time) }}</td>
              <td class="file-type">{{ file.is_dir ? '文件夹' : '文件' }}</td>
              <td class="file-actions">
                <button 
                  v-if="!file.is_dir" 
                  @click="downloadFile(file)"
                  class="btn btn-sm btn-outline"
                >
                  <i class="fas fa-download"></i>
                </button>
                <button 
                  @click="renameFile(file)"
                  class="btn btn-sm btn-outline"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  @click="deleteFile(file)"
                  class="btn btn-sm btn-danger"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 分页 -->
        <div class="pagination" v-if="totalFiles > pageSize">
          <button 
            @click="changePage(currentPage - 1)"
            :disabled="currentPage <= 1"
            class="btn btn-outline"
          >
            上一页
          </button>
          <span class="page-info">
            第 {{ currentPage }} 页，共 {{ Math.ceil(totalFiles / pageSize) }} 页
          </span>
          <button 
            @click="changePage(currentPage + 1)"
            :disabled="currentPage >= Math.ceil(totalFiles / pageSize)"
            class="btn btn-outline"
          >
            下一页
          </button>
        </div>
      </div>
    </div>

    <!-- 文件操作面板 -->
    <div class="file-operations" v-if="selectedFiles.length > 0">
      <h3>批量操作</h3>
      <div class="operation-buttons">
        <button @click="transferFiles" class="btn btn-primary">
          <i class="fas fa-exchange-alt"></i> 转移文件
        </button>
        <button @click="deleteSelectedFiles" class="btn btn-danger">
          <i class="fas fa-trash"></i> 删除选中
        </button>
        <button @click="clearSelection" class="btn btn-outline">
          <i class="fas fa-times"></i> 取消选择
        </button>
      </div>
    </div>

    <!-- 模态框 -->
    <modal 
      v-if="showCreateFolder" 
      @close="showCreateFolder = false"
      title="新建文件夹"
    >
      <folder-creator 
        :current-path="currentPath"
        @created="handleFolderCreated"
        @cancel="showCreateFolder = false"
      />
    </modal>

    <modal 
      v-if="showTransferDialog" 
      @close="showTransferDialog = false"
      title="文件转移"
    >
      <file-transfer 
        :source-storage="selectedStorage"
        :source-paths="selectedFiles"
        :storages="storages"
        @transfer="handleFileTransfer"
        @cancel="showTransferDialog = false"
      />
    </modal>

    <!-- 加载状态 -->
    <loading-spinner v-if="loading" />
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import { useToast } from 'vue-toastification'
import Breadcrumb from '@/components/storage/Breadcrumb.vue'
import FolderCreator from '@/components/storage/FolderCreator.vue'
import FileTransfer from '@/components/storage/FileTransfer.vue'
import Modal from '@/components/common/Modal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

export default {
  name: 'StorageManagement',
  components: {
    Breadcrumb,
    FolderCreator,
    FileTransfer,
    Modal,
    LoadingSpinner
  },
  setup() {
    const toast = useToast()
    
    // 响应式数据
    const storages = ref([])
    const selectedStorage = ref('')
    const files = ref([])
    const currentPath = ref('/')
    const currentPage = ref(1)
    const pageSize = ref(50)
    const totalFiles = ref(0)
    const selectedFiles = ref([])
    const selectAll = ref(false)
    const loading = ref(false)
    const showCreateFolder = ref(false)
    const showTransferDialog = ref(false)

    // 计算属性
    const selectedStorageInfo = computed(() => {
      return storages.value.find(s => s.id === selectedStorage.value)
    })

    // 方法
    const loadStorages = async () => {
      try {
        loading.value = true
        const response = await fetch('/api/v2/storage/storages')
        if (response.ok) {
          const data = await response.json()
          storages.value = data.storages
        } else {
          toast.error('加载存储列表失败')
        }
      } catch (error) {
        toast.error('网络错误：' + error.message)
      } finally {
        loading.value = false
      }
    }

    const loadFiles = async () => {
      if (!selectedStorage.value) return
      
      try {
        loading.value = true
        const params = new URLSearchParams({
          path: currentPath.value,
          page: currentPage.value.toString(),
          size: pageSize.value.toString()
        })
        
        const response = await fetch(`/api/v2/storage/storages/${selectedStorage.value}/files?${params}`)
        if (response.ok) {
          const data = await response.json()
          files.value = data.files
          totalFiles.value = data.total
        } else {
          toast.error('加载文件列表失败')
        }
      } catch (error) {
        toast.error('网络错误：' + error.message)
      } finally {
        loading.value = false
      }
    }

    const selectStorage = (storageId) => {
      selectedStorage.value = storageId
      currentPath.value = '/'
      currentPage.value = 1
      selectedFiles.value = []
      loadFiles()
    }

    const navigateToPath = (path) => {
      currentPath.value = path
      currentPage.value = 1
      loadFiles()
    }

    const refreshFiles = () => {
      loadFiles()
    }

    const createFolder = () => {
      showCreateFolder.value = true
    }

    const uploadFile = () => {
      // 实现文件上传逻辑
      toast.info('文件上传功能开发中')
    }

    const toggleSelectAll = () => {
      if (selectAll.value) {
        selectedFiles.value = files.value.map(file => file.path)
      } else {
        selectedFiles.value = []
      }
    }

    const getStorageIcon = (storageType) => {
      const icons = {
        local: 'fas fa-hdd',
        '123cloud': 'fas fa-cloud',
        default: 'fas fa-server'
      }
      return icons[storageType] || icons.default
    }

    const getFileIcon = (file) => {
      if (file.is_dir) {
        return 'fas fa-folder'
      }
      
      const extension = file.name.split('.').pop().toLowerCase()
      const iconMap = {
        // 视频文件
        mp4: 'fas fa-file-video',
        mkv: 'fas fa-file-video',
        avi: 'fas fa-file-video',
        mov: 'fas fa-file-video',
        wmv: 'fas fa-file-video',
        // 音频文件
        mp3: 'fas fa-file-audio',
        flac: 'fas fa-file-audio',
        wav: 'fas fa-file-audio',
        // 图片文件
        jpg: 'fas fa-file-image',
        jpeg: 'fas fa-file-image',
        png: 'fas fa-file-image',
        gif: 'fas fa-file-image',
        // 默认
        default: 'fas fa-file'
      }
      
      return iconMap[extension] || iconMap.default
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const formatTime = (timestamp) => {
      return new Date(timestamp * 1000).toLocaleString()
    }

    const downloadFile = async (file) => {
      try {
        const response = await fetch(`/api/v2/storage/storages/${selectedStorage.value}/download?path=${encodeURIComponent(file.path)}`)
        if (response.ok) {
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = file.name
          a.click()
          window.URL.revokeObjectURL(url)
        } else {
          toast.error('下载文件失败')
        }
      } catch (error) {
        toast.error('下载失败：' + error.message)
      }
    }

    const renameFile = async (file) => {
      const newName = prompt('请输入新文件名：', file.name)
      if (newName && newName !== file.name) {
        try {
          const response = await fetch(`/api/v2/storage/storages/${selectedStorage.value}/rename`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              old_path: file.path,
              new_path: newName
            })
          })
          
          if (response.ok) {
            toast.success('重命名成功')
            loadFiles()
          } else {
            toast.error('重命名失败')
          }
        } catch (error) {
          toast.error('重命名失败：' + error.message)
        }
      }
    }

    const deleteFile = async (file) => {
      if (confirm(`确定要删除 ${file.name} 吗？`)) {
        try {
          const response = await fetch(`/api/v2/storage/storages/${selectedStorage.value}/files`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              paths: [file.path]
            })
          })
          
          if (response.ok) {
            toast.success('删除成功')
            loadFiles()
          } else {
            toast.error('删除失败')
          }
        } catch (error) {
          toast.error('删除失败：' + error.message)
        }
      }
    }

    const transferFiles = () => {
      if (selectedFiles.value.length === 0) {
        toast.warning('请先选择要转移的文件')
        return
      }
      showTransferDialog.value = true
    }

    const deleteSelectedFiles = async () => {
      if (selectedFiles.value.length === 0) {
        toast.warning('请先选择要删除的文件')
        return
      }
      
      if (confirm(`确定要删除选中的 ${selectedFiles.value.length} 个文件吗？`)) {
        try {
          const response = await fetch(`/api/v2/storage/storages/${selectedStorage.value}/files`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              paths: selectedFiles.value
            })
          })
          
          if (response.ok) {
            toast.success('删除成功')
            selectedFiles.value = []
            selectAll.value = false
            loadFiles()
          } else {
            toast.error('删除失败')
          }
        } catch (error) {
          toast.error('删除失败：' + error.message)
        }
      }
    }

    const clearSelection = () => {
      selectedFiles.value = []
      selectAll.value = false
    }

    const handleFolderCreated = () => {
      showCreateFolder.value = false
      loadFiles()
    }

    const handleFileTransfer = () => {
      showTransferDialog.value = false
      selectedFiles.value = []
      selectAll.value = false
      loadFiles()
    }

    const changePage = (page) => {
      currentPage.value = page
      loadFiles()
    }

    // 监听器
    watch(selectedStorage, loadFiles)
    watch(currentPage, loadFiles)

    // 生命周期
    onMounted(() => {
      loadStorages()
    })

    return {
      storages,
      selectedStorage,
      files,
      currentPath,
      currentPage,
      pageSize,
      totalFiles,
      selectedFiles,
      selectAll,
      loading,
      showCreateFolder,
      showTransferDialog,
      
      selectStorage,
      navigateToPath,
      refreshFiles,
      createFolder,
      uploadFile,
      toggleSelectAll,
      getStorageIcon,
      getFileIcon,
      formatFileSize,
      formatTime,
      downloadFile,
      renameFile,
      deleteFile,
      transferFiles,
      deleteSelectedFiles,
      clearSelection,
      handleFolderCreated,
      handleFileTransfer,
      changePage
    }
  }
}
</script>

<style scoped>
.storage-management {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.storage-header {
  text-align: center;
  margin-bottom: 30px;
}

.storage-header h1 {
  color: #333;
  margin-bottom: 10px;
}

.storage-list {
  margin-bottom: 30px;
}

.storage-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 15px;
}

.storage-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.storage-card:hover {
  border-color: #007bff;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.1);
}

.storage-card.active {
  border-color: #007bff;
  background-color: #f8f9fa;
}

.storage-icon {
  font-size: 24px;
  margin-right: 15px;
  color: #007bff;
}

.storage-info h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.storage-info p {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.status {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.status.online {
  background-color: #d4edda;
  color: #155724;
}

.status.offline {
  background-color: #f8d7da;
  color: #721c24;
}

.file-browser {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background-color: #fff;
}

.browser-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.browser-actions {
  display: flex;
  gap: 10px;
}

.file-table {
  width: 100%;
  border-collapse: collapse;
}

.file-table th,
.file-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.file-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.file-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-link {
  cursor: pointer;
  color: #007bff;
}

.file-link:hover {
  text-decoration: underline;
}

.file-actions {
  display: flex;
  gap: 5px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.file-operations {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.operation-buttons {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn {
  padding: 8px 16px;
  border: 1px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #1e7e34;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-outline {
  background-color: transparent;
  border-color: #007bff;
  color: #007bff;
}

.btn-outline:hover {
  background-color: #007bff;
  color: white;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>