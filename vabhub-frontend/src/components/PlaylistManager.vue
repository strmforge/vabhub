<template>
  <div class="playlist-manager">
    <!-- 歌单操作栏 -->
    <div class="playlist-actions">
      <el-button type="primary" @click="createPlaylist">
        <el-icon><Plus /></el-icon>
        新建歌单
      </el-button>
      <el-button @click="importPlaylist">
        <el-icon><Upload /></el-icon>
        导入歌单
      </el-button>
    </div>

    <!-- 歌单列表 -->
    <div class="playlist-grid">
      <div
        v-for="playlist in playlists"
        :key="playlist.id"
        class="playlist-card"
        @click="openPlaylist(playlist)"
      >
        <div class="playlist-cover">
          <img v-if="playlist.cover" :src="playlist.cover" :alt="playlist.name" />
          <div v-else class="cover-placeholder">
            <el-icon><VideoPlay /></el-icon>
          </div>
          <div class="playlist-overlay">
            <div class="play-count">{{ playlist.playCount }} 次播放</div>
            <div class="track-count">{{ playlist.trackCount }} 首歌曲</div>
          </div>
        </div>
        
        <div class="playlist-info">
          <h4 class="playlist-name">{{ playlist.name }}</h4>
          <p class="playlist-desc">{{ playlist.description || '暂无描述' }}</p>
          <div class="playlist-meta">
            <span class="create-time">{{ formatTime(playlist.createTime) }}</span>
            <span class="creator">创建者: {{ playlist.creator }}</span>
          </div>
        </div>
        
        <div class="playlist-actions-menu">
          <el-dropdown @click.stop>
            <el-icon><MoreFilled /></el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="playPlaylist(playlist)">播放</el-dropdown-item>
                <el-dropdown-item @click="editPlaylist(playlist)">编辑</el-dropdown-item>
                <el-dropdown-item @click="sharePlaylist(playlist)">分享</el-dropdown-item>
                <el-dropdown-item @click="deletePlaylist(playlist)" divided>
                  删除
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- 创建/编辑歌单对话框 -->
    <el-dialog
      v-model="playlistDialogVisible"
      :title="editingPlaylist ? '编辑歌单' : '新建歌单'"
      width="400px"
    >
      <el-form :model="playlistForm" label-width="80px">
        <el-form-item label="歌单名称" required>
          <el-input v-model="playlistForm.name" placeholder="请输入歌单名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="playlistForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入歌单描述"
          />
        </el-form-item>
        <el-form-item label="封面">
          <el-upload
            class="cover-upload"
            action="#"
            :show-file-list="false"
            :before-upload="beforeCoverUpload"
          >
            <img v-if="playlistForm.cover" :src="playlistForm.cover" class="cover-preview" />
            <el-icon v-else class="cover-upload-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="标签">
          <el-select
            v-model="playlistForm.tags"
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
        <el-form-item label="隐私">
          <el-radio-group v-model="playlistForm.privacy">
            <el-radio label="public">公开</el-radio>
            <el-radio label="private">私密</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="playlistDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePlaylist">保存</el-button>
      </template>
    </el-dialog>

    <!-- 歌单详情对话框 -->
    <el-dialog
      v-model="playlistDetailVisible"
      :title="currentPlaylist?.name"
      width="800px"
      fullscreen
    >
      <PlaylistDetail 
        v-if="currentPlaylist" 
        :playlist="currentPlaylist" 
        @close="playlistDetailVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload, VideoPlay, MoreFilled } from '@element-plus/icons-vue'

interface Playlist {
  id: string
  name: string
  description: string
  cover: string
  creator: string
  createTime: number
  updateTime: number
  trackCount: number
  playCount: number
  privacy: 'public' | 'private'
  tags: string[]
}

// 歌单列表
const playlists = ref<Playlist[]>([
  {
    id: '1',
    name: '我的最爱',
    description: '收藏的经典歌曲',
    cover: '',
    creator: '用户',
    createTime: Date.now() - 86400000 * 7,
    updateTime: Date.now() - 86400000,
    trackCount: 25,
    playCount: 156,
    privacy: 'private',
    tags: ['流行', '经典']
  },
  {
    id: '2',
    name: '工作背景音乐',
    description: '专注工作的轻音乐',
    cover: '',
    creator: '用户',
    createTime: Date.now() - 86400000 * 14,
    updateTime: Date.now() - 86400000 * 2,
    trackCount: 18,
    playCount: 89,
    privacy: 'public',
    tags: ['轻音乐', '背景音乐']
  }
])

// 对话框状态
const playlistDialogVisible = ref(false)
const playlistDetailVisible = ref(false)
const editingPlaylist = ref<Playlist | null>(null)
const currentPlaylist = ref<Playlist | null>(null)

// 表单数据
const playlistForm = reactive({
  name: '',
  description: '',
  cover: '',
  tags: [] as string[],
  privacy: 'public' as 'public' | 'private'
})

// 热门标签
const popularTags = ref([
  '流行', '摇滚', '电子', '民谣', '爵士', '古典', '嘻哈', 'R&B',
  '轻音乐', '背景音乐', '游戏音乐', '电影原声', '独立音乐'
])

// 创建歌单
const createPlaylist = () => {
  editingPlaylist.value = null
  Object.assign(playlistForm, {
    name: '',
    description: '',
    cover: '',
    tags: [],
    privacy: 'public'
  })
  playlistDialogVisible.value = true
}

// 编辑歌单
const editPlaylist = (playlist: Playlist) => {
  editingPlaylist.value = playlist
  Object.assign(playlistForm, {
    name: playlist.name,
    description: playlist.description,
    cover: playlist.cover,
    tags: [...playlist.tags],
    privacy: playlist.privacy
  })
  playlistDialogVisible.value = true
}

// 保存歌单
const savePlaylist = () => {
  if (!playlistForm.name.trim()) {
    ElMessage.error('请输入歌单名称')
    return
  }

  if (editingPlaylist.value) {
    // 更新现有歌单
    Object.assign(editingPlaylist.value, {
      ...playlistForm,
      updateTime: Date.now()
    })
    ElMessage.success('歌单更新成功')
  } else {
    // 创建新歌单
    const newPlaylist: Playlist = {
      id: Date.now().toString(),
      name: playlistForm.name,
      description: playlistForm.description,
      cover: playlistForm.cover,
      creator: '用户',
      createTime: Date.now(),
      updateTime: Date.now(),
      trackCount: 0,
      playCount: 0,
      privacy: playlistForm.privacy,
      tags: playlistForm.tags
    }
    playlists.value.unshift(newPlaylist)
    ElMessage.success('歌单创建成功')
  }

  playlistDialogVisible.value = false
}

// 打开歌单详情
const openPlaylist = (playlist: Playlist) => {
  currentPlaylist.value = playlist
  playlistDetailVisible.value = true
}

// 播放歌单
const playPlaylist = (playlist: Playlist) => {
  ElMessage.success(`开始播放歌单: ${playlist.name}`)
  // 这里应该触发全局播放器播放该歌单
}

// 分享歌单
const sharePlaylist = async (playlist: Playlist) => {
  try {
    await navigator.clipboard.writeText(`分享歌单: ${playlist.name}`)
    ElMessage.success('歌单链接已复制到剪贴板')
  } catch (error) {
    ElMessage.error('分享失败，请重试')
  }
}

// 删除歌单
const deletePlaylist = async (playlist: Playlist) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除歌单"${playlist.name}"吗？此操作不可恢复。`,
      '确认删除',
      {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }
    )

    const index = playlists.value.findIndex(p => p.id === playlist.id)
    if (index !== -1) {
      playlists.value.splice(index, 1)
      ElMessage.success('歌单删除成功')
    }
  } catch {
    // 用户取消删除
  }
}

// 导入歌单
const importPlaylist = () => {
  ElMessage.info('导入歌单功能开发中...')
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
    playlistForm.cover = e.target?.result as string
  }
  reader.readAsDataURL(file)
  
  return false // 阻止自动上传
}

// 格式化时间
const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.playlist-manager {
  padding: 20px;
}

.playlist-actions {
  margin-bottom: 20px;
}

.playlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.playlist-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.playlist-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.playlist-cover {
  position: relative;
  height: 160px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.playlist-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: white;
  font-size: 48px;
}

.playlist-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  color: white;
  padding: 10px;
  font-size: 0.875rem;
}

.play-count, .track-count {
  margin: 2px 0;
}

.playlist-info {
  padding: 15px;
}

.playlist-name {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.playlist-desc {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 0.875rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.playlist-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #999;
}

.playlist-actions-menu {
  position: absolute;
  top: 10px;
  right: 10px;
  opacity: 0;
  transition: opacity 0.3s;
}

.playlist-card:hover .playlist-actions-menu {
  opacity: 1;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .playlist-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .playlist-cover {
    height: 120px;
  }
}
</style>