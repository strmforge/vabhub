<template>
  <div class="file-organizer">
    <div class="page-header">
      <h1>文件整理</h1>
      <p>智能文件整理系统，自动重命名和组织媒体文件</p>
    </div>

    <div class="content">
      <!-- 快速操作 -->
      <div class="quick-actions">
        <div class="action-card" @click="showRenameModal = true">
          <div class="action-icon">📝</div>
          <h3>智能重命名</h3>
          <p>批量重命名文件，使用智能模板</p>
        </div>
        
        <div class="action-card" @click="showOrganizeModal = true">
          <div class="action-icon">📁</div>
          <h3>批量整理</h3>
          <p>自动整理文件到标准目录结构</p>
        </div>
        
        <div class="action-card" @click="showTemplateModal = true">
          <div class="action-icon">⚙️</div>
          <h3>模板管理</h3>
          <p>管理重命名和整理模板</p>
        </div>
      </div>

      <!-- 任务历史 -->
      <div class="task-history">
        <h2>任务历史</h2>
        <div class="task-list">
          <div v-for="task in tasks" :key="task.id" class="task-item">
            <div class="task-info">
              <h4>{{ task.name }}</h4>
              <p class="task-path">{{ task.sourcePath }} → {{ task.targetPath }}</p>
              <div class="task-meta">
                <span class="task-type">{{ getTaskTypeText(task.type) }}</span>
                <span class="task-time">{{ formatDate(task.createdAt) }}</span>
              </div>
            </div>
            
            <div class="task-status">
              <div class="status-badge" :class="task.status">
                {{ getStatusText(task.status) }}
              </div>
              <div class="progress" v-if="task.status === 'running'">
                <div class="progress-bar" :style="{ width: task.progress + '%' }"></div>
              </div>
              <div class="task-stats" v-if="task.status === 'completed'">
                <span>成功: {{ task.stats.success }}</span>
                <span>失败: {{ task.stats.failed }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 重命名模态框 -->
      <div v-if="showRenameModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>智能重命名</h3>
            <button class="close-btn" @click="closeModals">×</button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="startRename">
              <div class="form-group">
                <label>选择文件</label>
                <div class="file-selector">
                  <button type="button" class="btn btn-secondary" @click="selectFiles">选择文件</button>
                  <div class="selected-files">
                    <span v-for="file in selectedFiles" :key="file" class="file-tag">
                      {{ file }}
                      <button @click="removeFile(file)">×</button>
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="form-group">
                <label>命名模板</label>
                <select v-model="renameTemplate">
                  <option value="movie">电影模板: {title} ({year}) - {quality}</option>
                  <option value="tv">剧集模板: {title}/Season {season}/{title} S{season}E{episode}</option>
                  <option value="custom">自定义模板</option>
                </select>
                <input v-if="renameTemplate === 'custom'" v-model="customTemplate" 
                       placeholder="输入自定义模板，如: {title}_{year}_{quality}" />
              </div>
              
              <div class="form-group">
                <label>
                  <input type="checkbox" v-model="overwriteExisting" /> 
                  覆盖已存在文件
                </label>
              </div>
            </form>
          </div>
          
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModals">取消</button>
            <button class="btn btn-primary" @click="startRename" :disabled="!selectedFiles.length">
              开始重命名
            </button>
          </div>
        </div>
      </div>

      <!-- 批量整理模态框 -->
      <div v-if="showOrganizeModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>批量整理</h3>
            <button class="close-btn" @click="closeModals">×</button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="startOrganize">
              <div class="form-group">
                <label>源目录</label>
                <input v-model="organizeSource" type="text" placeholder="/path/to/source" />
              </div>
              
              <div class="form-group">
                <label>目标目录</label>
                <input v-model="organizeTarget" type="text" placeholder="/path/to/target" />
              </div>
              
              <div class="form-group">
                <label>整理规则</label>
                <div class="rule-presets">
                  <label><input type="radio" v-model="organizeRule" value="movie" /> 电影规则</label>
                  <label><input type="radio" v-model="organizeRule" value="tv" /> 剧集规则</label>
                  <label><input type="radio" v-model="organizeRule" value="music" /> 音乐规则</label>
                </div>
              </div>
              
              <div class="form-group">
                <label>
                  <input type="checkbox" v-model="createBackup" /> 
                  创建备份
                </label>
              </div>
            </form>
          </div>
          
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModals">取消</button>
            <button class="btn btn-primary" @click="startOrganize" 
                    :disabled="!organizeSource || !organizeTarget">
              开始整理
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'

export default {
  name: 'FileOrganizer',
  setup() {
    const showRenameModal = ref(false)
    const showOrganizeModal = ref(false)
    const showTemplateModal = ref(false)
    
    const selectedFiles = ref([])
    const renameTemplate = ref('movie')
    const customTemplate = ref('')
    const overwriteExisting = ref(false)
    
    const organizeSource = ref('')
    const organizeTarget = ref('')
    const organizeRule = ref('movie')
    const createBackup = ref(true)
    
    const tasks = ref([])

    // 模拟数据
    const mockTasks = [
      {
        id: '1',
        name: '电影文件重命名',
        type: 'rename',
        status: 'completed',
        progress: 100,
        sourcePath: '/downloads/movies',
        targetPath: '/media/Movies',
        createdAt: new Date(),
        stats: { success: 15, failed: 0 }
      },
      {
        id: '2',
        name: '剧集文件整理',
        type: 'organize',
        status: 'running',
        progress: 65,
        sourcePath: '/downloads/tv',
        targetPath: '/media/TV Shows',
        createdAt: new Date(Date.now() - 300000),
        stats: { success: 8, failed: 1 }
      }
    ]

    onMounted(() => {
      tasks.value = mockTasks
    })

    const selectFiles = () => {
      // 模拟文件选择
      selectedFiles.value = [
        '/downloads/movie.2024.1080p.mkv',
        '/downloads/another.movie.2023.720p.mkv'
      ]
    }

    const removeFile = (file) => {
      selectedFiles.value = selectedFiles.value.filter(f => f !== file)
    }

    const getTaskTypeText = (type) => {
      const typeMap = {
        rename: '重命名',
        organize: '整理',
        template: '模板'
      }
      return typeMap[type] || type
    }

    const getStatusText = (status) => {
      const statusMap = {
        pending: '等待中',
        running: '进行中',
        completed: '已完成',
        failed: '失败'
      }
      return statusMap[status] || status
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleString('zh-CN')
    }

    const closeModals = () => {
      showRenameModal.value = false
      showOrganizeModal.value = false
      showTemplateModal.value = false
      resetForms()
    }

    const resetForms = () => {
      selectedFiles.value = []
      renameTemplate.value = 'movie'
      customTemplate.value = ''
      overwriteExisting.value = false
      organizeSource.value = ''
      organizeTarget.value = ''
      organizeRule.value = 'movie'
      createBackup.value = true
    }

    const startRename = async () => {
      // 模拟API调用
      const newTask = {
        id: Date.now().toString(),
        name: '文件重命名任务',
        type: 'rename',
        status: 'running',
        progress: 0,
        sourcePath: selectedFiles.value.join(', '),
        targetPath: '重命名结果',
        createdAt: new Date(),
        stats: { success: 0, failed: 0 }
      }
      
      tasks.value.unshift(newTask)
      closeModals()
    }

    const startOrganize = async () => {
      // 模拟API调用
      const newTask = {
        id: Date.now().toString(),
        name: '批量整理任务',
        type: 'organize',
        status: 'running',
        progress: 0,
        sourcePath: organizeSource.value,
        targetPath: organizeTarget.value,
        createdAt: new Date(),
        stats: { success: 0, failed: 0 }
      }
      
      tasks.value.unshift(newTask)
      closeModals()
    }

    return {
      showRenameModal,
      showOrganizeModal,
      showTemplateModal,
      selectedFiles,
      renameTemplate,
      customTemplate,
      overwriteExisting,
      organizeSource,
      organizeTarget,
      organizeRule,
      createBackup,
      tasks,
      selectFiles,
      removeFile,
      getTaskTypeText,
      getStatusText,
      formatDate,
      closeModals,
      startRename,
      startOrganize
    }
  }
}
</script>

<style scoped>
.file-organizer {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.action-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.task-history {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 2rem;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
}

.task-info h4 {
  margin: 0 0 0.5rem 0;
}

.task-path {
  color: #666;
  font-size: 0.875rem;
  margin: 0 0 0.5rem 0;
}

.task-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #888;
}

.task-status {
  text-align: right;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-block;
  margin-bottom: 0.5rem;
}

.status-badge.running {
  background: #e3f2fd;
  color: #1976d2;
}

.status-badge.completed {
  background: #e8f5e8;
  color: #2e7d32;
}

.status-badge.failed {
  background: #ffebee;
  color: #c62828;
}

.progress {
  width: 100px;
  height: 4px;
  background: #f0f0f0;
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: #1976d2;
  transition: width 0.3s;
}

.task-stats {
  font-size: 0.875rem;
  color: #666;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 表单样式 */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.file-selector {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.selected-files {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.file-tag {
  background: #f0f0f0;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.file-tag button {
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
}

.rule-presets {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.rule-presets label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
}

/* 按钮样式 */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #1976d2;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #1565c0;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}
</style>