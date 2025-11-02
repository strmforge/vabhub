<template>
  <div class="local-music">
    <!-- 本地音乐操作栏 -->
    <div class="local-music-actions">
      <el-button type="primary" @click="scanLocalMusic">
        <el-icon><Refresh /></el-icon>
        扫描本地音乐
      </el-button>
      <el-button @click="importLocalMusic">
        <el-icon><FolderOpened /></el-icon>
        导入文件夹
      </el-button>
      <el-button @click="exportLocalMusic">
        <el-icon><Download /></el-icon>
        导出音乐
      </el-button>
    </div>

    <!-- 音乐列表 -->
    <div class="music-list-container">
      <el-table
        :data="localMusicList"
        style="width: 100%"
        @row-click="playMusic"
        v-loading="loading"
        empty-text="暂无本地音乐，请先扫描或导入音乐文件"
      >
        <el-table-column type="index" width="50" label="#" />
        <el-table-column label="歌曲" min-width="200">
          <template #default="{ row }">
            <div class="music-info">
              <div class="music-title">{{ row.title }}</div>
              <div class="music-artist">{{ row.artist }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="专辑" min-width="150">
          <template #default="{ row }">
            <span class="music-album">{{ row.album || '未知专辑' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="时长" width="80">
          <template #default="{ row }">
            <span class="music-duration">{{ formatDuration(row.duration) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="大小" width="80">
          <template #default="{ row }">
            <span class="music-size">{{ formatFileSize(row.size) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="路径" min-width="200">
          <template #default="{ row }">
            <span class="music-path" :title="row.path">{{ truncatePath(row.path) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <div class="music-actions">
              <el-button link @click.stop="playMusic(row)">
                <el-icon><VideoPlay /></el-icon>
              </el-button>
              <el-button link @click.stop="addToPlaylist(row)">
                <el-icon><Plus /></el-icon>
              </el-button>
              <el-button link @click.stop="editMusicInfo(row)">
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-button link @click.stop="deleteMusic(row)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 统计信息 -->
    <div class="music-stats">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ localMusicList.length }}</div>
            <div class="stat-label">总歌曲数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ formatFileSize(totalSize) }}</div>
            <div class="stat-label">总大小</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ formatDuration(totalDuration) }}</div>
            <div class="stat-label">总时长</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ albumCount }}</div>
            <div class="stat-label">专辑数</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 音乐信息编辑对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑音乐信息"
      width="500px"
    >
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="歌曲名称">
          <el-input v-model="editForm.title" />
        </el-form-item>
        <el-form-item label="艺术家">
          <el-input v-model="editForm.artist" />
        </el-form-item>
        <el-form-item label="专辑">
          <el-input v-model="editForm.album" />
        </el-form-item>
        <el-form-item label="年份">
          <el-input v-model="editForm.year" type="number" />
        </el-form-item>
        <el-form-item label="流派">
          <el-input v-model="editForm.genre" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveMusicInfo">保存</el-button>
      </template>
    </el-dialog>

    <!-- 添加到歌单对话框 -->
    <el-dialog
      v-model="playlistDialogVisible"
      title="添加到歌单"
      width="400px"
    >
      <el-select v-model="selectedPlaylistId" placeholder="选择歌单" style="width: 100%">
        <el-option
          v-for="playlist in availablePlaylists"
          :key="playlist.id"
          :label="playlist.name"
          :value="playlist.id"
        />
      </el-select>
      
      <template #footer>
        <el-button @click="playlistDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAddToPlaylist">添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Refresh, FolderOpened, Download, VideoPlay, Plus, Edit, Delete 
} from '@element-plus/icons-vue'

interface LocalMusic {
  id: string
  title: string
  artist: string
  album: string
  duration: number // 秒
  size: number // 字节
  path: string
  year?: number
  genre?: string
  bitrate?: number
  sampleRate?: number
}

// 本地音乐列表
const localMusicList = ref<LocalMusic[]>([
  {
    id: '1',
    title: '夜曲',
    artist: '周杰伦',
    album: '十一月的萧邦',
    duration: 227,
    size: 5432100,
    path: 'C:/Music/周杰伦/十一月的萧邦/夜曲.mp3',
    year: 2005,
    genre: '流行',
    bitrate: 320,
    sampleRate: 44100
  },
  {
    id: '2',
    title: '青花瓷',
    artist: '周杰伦',
    album: '我很忙',
    duration: 245,
    size: 5890123,
    path: 'C:/Music/周杰伦/我很忙/青花瓷.mp3',
    year: 2007,
    genre: '中国风',
    bitrate: 320,
    sampleRate: 44100
  }
])

// 加载状态
const loading = ref(false)

// 对话框状态
const editDialogVisible = ref(false)
const playlistDialogVisible = ref(false)

// 编辑表单
const editForm = reactive({
  title: '',
  artist: '',
  album: '',
  year: undefined as number | undefined,
  genre: ''
})

const selectedMusic = ref<LocalMusic | null>(null)
const selectedPlaylistId = ref('')

// 可用歌单列表（模拟数据）
const availablePlaylists = ref([
  { id: '1', name: '我的最爱' },
  { id: '2', name: '工作背景音乐' },
  { id: '3', name: '运动音乐' }
])

// 统计信息
const totalSize = computed(() => 
  localMusicList.value.reduce((sum, music) => sum + music.size, 0)
)

const totalDuration = computed(() => 
  localMusicList.value.reduce((sum, music) => sum + music.duration, 0)
)

const albumCount = computed(() => {
  const albums = new Set(localMusicList.value.map(music => music.album))
  return albums.size
})

// 扫描本地音乐
const scanLocalMusic = async () => {
  loading.value = true
  
  try {
    // 模拟扫描过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 这里应该是实际的扫描逻辑
    // 暂时使用模拟数据
    ElMessage.success(`扫描完成，发现 ${localMusicList.value.length} 首音乐`)
  } catch (error) {
    ElMessage.error('扫描失败，请检查文件权限')
  } finally {
    loading.value = false
  }
}

// 导入文件夹
const importLocalMusic = () => {
  ElMessage.info('导入文件夹功能开发中...')
}

// 导出音乐
const exportLocalMusic = () => {
  ElMessage.info('导出音乐功能开发中...')
}

// 播放音乐
const playMusic = (music: LocalMusic) => {
  ElMessage.success(`开始播放: ${music.title} - ${music.artist}`)
  // 这里应该触发全局播放器播放该音乐
}

// 添加到歌单
const addToPlaylist = (music: LocalMusic) => {
  selectedMusic.value = music
  selectedPlaylistId.value = ''
  playlistDialogVisible.value = true
}

// 确认添加到歌单
const confirmAddToPlaylist = () => {
  if (!selectedPlaylistId.value) {
    ElMessage.error('请选择歌单')
    return
  }

  const playlist = availablePlaylists.value.find(p => p.id === selectedPlaylistId.value)
  if (playlist && selectedMusic.value) {
    ElMessage.success(`已将"${selectedMusic.value.title}"添加到"${playlist.name}"`)
    playlistDialogVisible.value = false
  }
}

// 编辑音乐信息
const editMusicInfo = (music: LocalMusic) => {
  selectedMusic.value = music
  Object.assign(editForm, {
    title: music.title,
    artist: music.artist,
    album: music.album,
    year: music.year,
    genre: music.genre || ''
  })
  editDialogVisible.value = true
}

// 保存音乐信息
const saveMusicInfo = () => {
  if (!editForm.title.trim() || !editForm.artist.trim()) {
    ElMessage.error('歌曲名称和艺术家不能为空')
    return
  }

  if (selectedMusic.value) {
    Object.assign(selectedMusic.value, editForm)
    ElMessage.success('音乐信息保存成功')
    editDialogVisible.value = false
  }
}

// 删除音乐
const deleteMusic = async (music: LocalMusic) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除"${music.title}"吗？此操作将从本地删除文件。`,
      '确认删除',
      {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }
    )

    const index = localMusicList.value.findIndex(m => m.id === music.id)
    if (index !== -1) {
      localMusicList.value.splice(index, 1)
      ElMessage.success('音乐删除成功')
    }
  } catch {
    // 用户取消删除
  }
}

// 格式化时长
const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 截断路径显示
const truncatePath = (path: string, maxLength = 30) => {
  if (path.length <= maxLength) return path
  return '...' + path.slice(-maxLength + 3)
}
</script>

<style scoped>
.local-music {
  padding: 20px;
}

.local-music-actions {
  margin-bottom: 20px;
}

.music-list-container {
  margin-bottom: 30px;
}

.music-info {
  display: flex;
  flex-direction: column;
}

.music-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.music-artist {
  font-size: 0.875rem;
  color: #666;
}

.music-album {
  color: #666;
}

.music-duration, .music-size {
  color: #999;
  font-size: 0.875rem;
}

.music-path {
  color: #999;
  font-size: 0.875rem;
  cursor: help;
}

.music-actions {
  display: flex;
  gap: 5px;
}

.music-stats {
  margin-top: 30px;
}

.stat-card {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
}

/* 表格行悬停效果 */
:deep(.el-table__row) {
  cursor: pointer;
}

:deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .local-music-actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .music-stats .el-col {
    margin-bottom: 15px;
  }
}
</style>