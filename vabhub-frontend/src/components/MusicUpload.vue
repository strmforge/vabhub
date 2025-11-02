<template>
  <div class="music-upload">
    <!-- 上传区域 -->
    <div class="upload-area">
      <el-upload
        ref="uploadRef"
        class="upload-drag"
        drag
        multiple
        :file-list="fileList"
        :before-upload="beforeUpload"
        :on-change="handleFileChange"
        :on-remove="handleFileRemove"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :auto-upload="false"
        accept=".mp3,.flac,.wav,.aac,.m4a,.ogg"
        action="/api/music/upload"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将音乐文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 mp3, flac, wav, aac, m4a, ogg 格式，单个文件不超过 50MB
          </div>
        </template>
      </el-upload>
    </div>

    <!-- 上传文件列表 -->
    <div class="upload-list" v-if="fileList.length > 0">
      <h4>上传文件列表 ({{ fileList.length }})</h4>
      <div class="file-list">
        <div
          v-for="(file, index) in fileList"
          :key="file.uid"
          class="file-item"
          :class="{ 'uploading': file.status === 'uploading', 'success': file.status === 'success', 'error': file.status === 'error' }"
        >
          <div class="file-info">
            <div class="file-name">{{ file.name }}</div>
            <div class="file-size">{{ formatFileSize(file.size) }}</div>
            <div class="file-status">
              <span v-if="file.status === 'uploading'">上传中...</span>
              <span v-if="file.status === 'success'" class="success-text">上传成功</span>
              <span v-if="file.status === 'error'" class="error-text">上传失败</span>
            </div>
          </div>
          
          <div class="file-progress" v-if="file.status === 'uploading'">
            <el-progress :percentage="file.percentage || 0" />
          </div>
          
          <div class="file-actions">
            <el-button
              v-if="file.status === 'ready'"
              link
              @click="startUpload(file)"
            >
              开始上传
            </el-button>
            <el-button
              v-if="file.status === 'uploading'"
              link
              @click="cancelUpload(file)"
            >
              取消
            </el-button>
            <el-button
              v-if="file.status === 'error'"
              link
              @click="retryUpload(file)"
            >
              重试
            </el-button>
            <el-button link @click="removeFile(file)">
              移除
            </el-button>
          </div>
        </div>
      </div>

      <!-- 批量操作 -->
      <div class="batch-actions">
        <el-button @click="clearAll">清空列表</el-button>
        <el-button type="primary" @click="uploadAll" :disabled="!hasFilesToUpload">
          全部上传
        </el-button>
      </div>

      <!-- 上传统计 -->
      <div class="upload-stats">
        <div class="stat-item">
          <span class="stat-label">总文件数:</span>
          <span class="stat-value">{{ fileList.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">成功:</span>
          <span class="stat-value success-text">{{ successCount }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">失败:</span>
          <span class="stat-value error-text">{{ errorCount }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">总大小:</span>
          <span class="stat-value">{{ formatFileSize(totalSize) }}</span>
        </div>
      </div>
    </div>

    <!-- 音乐信息编辑 -->
    <div class="music-info" v-if="editingFile">
      <h4>编辑音乐信息</h4>
      <el-form :model="musicForm" label-width="80px">
        <el-form-item label="歌曲名称">
          <el-input v-model="musicForm.title" placeholder="请输入歌曲名称" />
        </el-form-item>
        <el-form-item label="艺术家">
          <el-input v-model="musicForm.artist" placeholder="请输入艺术家" />
        </el-form-item>
        <el-form-item label="专辑">
          <el-input v-model="musicForm.album" placeholder="请输入专辑名称" />
        </el-form-item>
        <el-form-item label="封面">
          <el-upload
            class="cover-upload"
            action="#"
            :show-file-list="false"
            :before-upload="beforeCoverUpload"
          >
            <img v-if="musicForm.cover" :src="musicForm.cover" class="cover-preview" />
            <el-icon v-else class="cover-upload-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="标签">
          <el-select
            v-model="musicForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请输入标签"
          >
            <el-option
              v-for="tag in popularTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="musicForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入歌曲描述"
          />
        </el-form-item>
      </el-form>
      
      <div class="info-actions">
        <el-button @click="cancelEdit">取消</el-button>
        <el-button type="primary" @click="saveMusicInfo">保存</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled, Plus } from '@element-plus/icons-vue'

interface UploadFile {
  uid: string
  name: string
  size: number
  type: string
  raw: File
  status: 'ready' | 'uploading' | 'success' | 'error'
  percentage?: number
  response?: any
  error?: any
}

interface MusicInfo {
  title: string
  artist: string
  album: string
  cover: string
  tags: string[]
  description: string
}

// 上传文件列表
const fileList = ref<UploadFile[]>([])
const uploadRef = ref()

// 编辑状态
const editingFile = ref<UploadFile | null>(null)
const musicForm = ref<MusicInfo>({
  title: '',
  artist: '',
  album: '',
  cover: '',
  tags: [],
  description: ''
})

// 热门标签
const popularTags = ref([
  '流行', '摇滚', '电子', '民谣', '爵士', '古典', '嘻哈', 'R&B',
  '轻音乐', '背景音乐', '游戏音乐', '电影原声', '独立音乐'
])

// 统计信息
const successCount = computed(() => 
  fileList.value.filter(file => file.status === 'success').length
)

const errorCount = computed(() => 
  fileList.value.filter(file => file.status === 'error').length
)

const totalSize = computed(() => 
  fileList.value.reduce((sum, file) => sum + file.size, 0)
)

const hasFilesToUpload = computed(() => 
  fileList.value.some(file => file.status === 'ready' || file.status === 'error')
)

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 上传前验证
const beforeUpload = (file: File) => {
  const allowedTypes = ['audio/mpeg', 'audio/flac', 'audio/wav', 'audio/aac', 'audio/mp4', 'audio/ogg']
  const isAudio = allowedTypes.includes(file.type)
  const isLt50M = file.size / 1024 / 1024 < 50

  if (!isAudio) {
    ElMessage.error('只能上传音频文件!')
    return false
  }
  if (!isLt50M) {
    ElMessage.error('音频文件大小不能超过 50MB!')
    return false
  }
  
  return true
}

// 文件变化处理
const handleFileChange = (file: UploadFile, fileList: UploadFile[]) => {
  // 自动从文件名提取基本信息
  const fileName = file.name.replace(/\.[^/.]+$/, '') // 移除扩展名
  
  // 简单的文件名解析（假设格式为 "艺术家 - 歌曲名" 或 "歌曲名"）
  const parts = fileName.split(' - ')
  if (parts.length === 2) {
    musicForm.value.artist = parts[0].trim()
    musicForm.value.title = parts[1].trim()
  } else {
    musicForm.value.title = fileName
    musicForm.value.artist = '未知艺术家'
  }
  
  musicForm.value.album = '未知专辑'
}

// 文件移除处理
const handleFileRemove = (file: UploadFile, fileList: UploadFile[]) => {
  // 文件列表会自动更新
}

// 开始上传单个文件
const startUpload = async (file: UploadFile) => {
  if (file.status === 'uploading') return
  
  file.status = 'uploading'
  file.percentage = 0
  
  try {
    // 模拟上传过程
    for (let progress = 0; progress <= 100; progress += 10) {
      await new Promise(resolve => setTimeout(resolve, 200))
      file.percentage = progress
    }
    
    file.status = 'success'
    ElMessage.success(`文件 "${file.name}" 上传成功`)
    
    // 触发上传成功事件
    emit('upload-success')
  } catch (error) {
    file.status = 'error'
    ElMessage.error(`文件 "${file.name}" 上传失败`)
  }
}

// 取消上传
const cancelUpload = (file: UploadFile) => {
  file.status = 'ready'
  file.percentage = 0
}

// 重试上传
const retryUpload = (file: UploadFile) => {
  startUpload(file)
}

// 移除文件
const removeFile = (file: UploadFile) => {
  const index = fileList.value.findIndex(f => f.uid === file.uid)
  if (index !== -1) {
    fileList.value.splice(index, 1)
  }
}

// 批量上传
const uploadAll = async () => {
  const filesToUpload = fileList.value.filter(file => 
    file.status === 'ready' || file.status === 'error'
  )
  
  if (filesToUpload.length === 0) {
    ElMessage.warning('没有可上传的文件')
    return
  }
  
  for (const file of filesToUpload) {
    await startUpload(file)
  }
}

// 清空列表
const clearAll = async () => {
  if (fileList.value.length === 0) return
  
  try {
    await ElMessageBox.confirm('确定要清空所有文件吗？', '确认清空', {
      type: 'warning'
    })
    
    fileList.value = []
    ElMessage.success('文件列表已清空')
  } catch {
    // 用户取消
  }
}

// 上传成功处理
const handleUploadSuccess = (response: any, file: UploadFile) => {
  file.status = 'success'
  file.response = response
  ElMessage.success(`文件 "${file.name}" 上传成功`)
}

// 上传错误处理
const handleUploadError = (error: any, file: UploadFile) => {
  file.status = 'error'
  file.error = error
  ElMessage.error(`文件 "${file.name}" 上传失败`)
}

// 封面上传处理
const beforeCoverUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }

  // 创建预览URL
  const reader = new FileReader()
  reader.onload = (e) => {
    musicForm.value.cover = e.target?.result as string
  }
  reader.readAsDataURL(file)
  
  return false // 阻止自动上传
}

// 编辑音乐信息
const editMusicInfo = (file: UploadFile) => {
  editingFile.value = file
  
  // 从文件名初始化表单
  const fileName = file.name.replace(/\.[^/.]+$/, '')
  const parts = fileName.split(' - ')
  
  if (parts.length === 2) {
    musicForm.value.artist = parts[0].trim()
    musicForm.value.title = parts[1].trim()
  } else {
    musicForm.value.title = fileName
    musicForm.value.artist = '未知艺术家'
  }
  
  musicForm.value.album = '未知专辑'
  musicForm.value.cover = ''
  musicForm.value.tags = []
  musicForm.value.description = ''
}

// 保存音乐信息
const saveMusicInfo = () => {
  if (!musicForm.value.title.trim()) {
    ElMessage.error('请输入歌曲名称')
    return
  }
  
  ElMessage.success('音乐信息保存成功')
  cancelEdit()
}

// 取消编辑
const cancelEdit = () => {
  editingFile.value = null
  musicForm.value = {
    title: '',
    artist: '',
    album: '',
    cover: '',
    tags: [],
    description: ''
  }
}

// 触发上传成功事件
const emit = defineEmits<{
  'upload-success': []
}>()
</script>

<style scoped>
.music-upload {
  padding: 20px;
}

.upload-area {
  margin-bottom: 30px;
}

.upload-drag {
  width: 100%;
}

.upload-list {
  border-top: 1px solid #e0e0e0;
  padding-top: 20px;
}

.upload-list h4 {
  margin: 0 0 15px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  transition: all 0.3s;
}

.file-item.uploading {
  border-color: #409eff;
  background: #f0f9ff;
}

.file-item.success {
  border-color: #67c23a;
  background: #f0f9f0;
}

.file-item.error {
  border-color: #f56c6c;
  background: #fef0f0;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 600;
  margin-bottom: 5px;
}

.file-size, .file-status {
  font-size: 0.875rem;
  color: #666;
}

.success-text {
  color: #67c23a;
}

.error-text {
  color: #f56c6c;
}

.file-progress {
  width: 200px;
  margin: 0 20px;
}

.file-actions {
  display: flex;
  gap: 10px;
}

.batch-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.upload-stats {
  display: flex;
  gap: 30px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-weight: 600;
}

.music-info {
  border-top: 1px solid #e0e0e0;
  padding-top: 20px;
  margin-top: 20px;
}

.music-info h4 {
  margin: 0 0 15px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.cover-upload {
  width: 100px;
  height: 100px;
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-preview {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
}

.cover-upload-icon {
  font-size: 20px;
  color: #8c939d;
}

.info-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .file-item {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .file-progress {
    width: 100%;
    margin: 0;
  }
  
  .file-actions {
    justify-content: flex-end;
  }
  
  .upload-stats {
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .stat-item {
    flex: 1;
    min-width: 80px;
  }
}
</style>