<template>
  <div class="online-music">
    <!-- 搜索和筛选 -->
    <div class="search-filter">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索在线音乐..."
        class="search-input"
        clearable
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      
      <el-select v-model="selectedPlatform" placeholder="选择平台" @change="handlePlatformChange">
        <el-option
          v-for="platform in platforms"
          :key="platform.value"
          :label="platform.label"
          :value="platform.value"
        />
      </el-select>
      
      <el-select v-model="selectedCategory" placeholder="选择分类" @change="handleCategoryChange">
        <el-option
          v-for="category in categories"
          :key="category.value"
          :label="category.label"
          :value="category.value"
        />
      </el-select>
    </div>

    <!-- 音乐推荐 -->
    <div class="music-recommendations" v-if="!searchKeyword">
      <h3 class="section-title">热门推荐</h3>
      <div class="recommendation-grid">
        <div
          v-for="playlist in featuredPlaylists"
          :key="playlist.id"
          class="playlist-card"
          @click="openPlaylist(playlist)"
        >
          <div class="playlist-cover">
            <img :src="playlist.cover" :alt="playlist.name" />
            <div class="play-button" @click.stop="playPlaylist(playlist)">
              <el-icon><VideoPlay /></el-icon>
            </div>
          </div>
          <div class="playlist-info">
            <h4 class="playlist-name">{{ playlist.name }}</h4>
            <p class="playlist-desc">{{ playlist.description }}</p>
            <div class="playlist-stats">
              <span class="play-count">{{ playlist.playCount }} 播放</span>
              <span class="track-count">{{ playlist.trackCount }} 首</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索结果 -->
    <div class="search-results" v-if="searchKeyword">
      <h3 class="section-title">搜索结果 ({{ searchResults.length }} 条)</h3>
      <el-table
        :data="searchResults"
        style="width: 100%"
        v-loading="searchLoading"
        empty-text="暂无搜索结果"
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
            <span class="music-album">{{ row.album }}</span>
          </template>
        </el-table-column>
        <el-table-column label="时长" width="80">
          <template #default="{ row }">
            <span class="music-duration">{{ formatDuration(row.duration) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="平台" width="100">
          <template #default="{ row }">
            <el-tag :type="getPlatformTagType(row.platform)">
              {{ getPlatformName(row.platform) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <div class="music-actions">
              <el-button type="primary" link @click="playMusic(row)">
                播放
              </el-button>
              <el-button link @click="addToPlaylist(row)">
                收藏
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 音乐排行榜 -->
    <div class="music-charts" v-if="!searchKeyword">
      <h3 class="section-title">音乐排行榜</h3>
      <el-tabs v-model="activeChart" @tab-click="handleChartChange">
        <el-tab-pane label="热歌榜" name="hot">
          <div class="chart-list">
            <div v-for="(song, index) in hotSongs" :key="song.id" class="chart-item">
              <div class="chart-rank">{{ index + 1 }}</div>
              <div class="chart-info">
                <div class="song-title">{{ song.title }}</div>
                <div class="song-artist">{{ song.artist }}</div>
              </div>
              <div class="chart-actions">
                <el-button link @click="playMusic(song)">
                  <el-icon><VideoPlay /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="新歌榜" name="new">
          <div class="chart-list">
            <div v-for="(song, index) in newSongs" :key="song.id" class="chart-item">
              <div class="chart-rank">{{ index + 1 }}</div>
              <div class="chart-info">
                <div class="song-title">{{ song.title }}</div>
                <div class="song-artist">{{ song.artist }}</div>
              </div>
              <div class="chart-actions">
                <el-button link @click="playMusic(song)">
                  <el-icon><VideoPlay /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="原创榜" name="original">
          <div class="chart-list">
            <div v-for="(song, index) in originalSongs" :key="song.id" class="chart-item">
              <div class="chart-rank">{{ index + 1 }}</div>
              <div class="chart-info">
                <div class="song-title">{{ song.title }}</div>
                <div class="song-artist">{{ song.artist }}</div>
              </div>
              <div class="chart-actions">
                <el-button link @click="playMusic(song)">
                  <el-icon><VideoPlay /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 播放列表对话框 -->
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
import { ref, reactive, computed, h, defineComponent } from 'vue'
import { ElMessage, ElButton, ElIcon } from 'element-plus'
import { Search, VideoPlay } from '@element-plus/icons-vue'

interface OnlineMusic {
  id: string
  title: string
  artist: string
  album: string
  duration: number
  platform: string
  cover: string
  url: string
}

interface Playlist {
  id: string
  name: string
  description: string
  cover: string
  playCount: number
  trackCount: number
  platform: string
}

// 搜索和筛选
const searchKeyword = ref('')
const selectedPlatform = ref('all')
const selectedCategory = ref('all')
const searchLoading = ref(false)

// 平台选项
const platforms = ref([
  { label: '全部平台', value: 'all' },
  { label: '网易云音乐', value: 'netease' },
  { label: 'QQ音乐', value: 'qq' },
  { label: '酷狗音乐', value: 'kugou' },
  { label: '酷我音乐', value: 'kuwo' }
])

// 分类选项
const categories = ref([
  { label: '全部分类', value: 'all' },
  { label: '流行', value: 'pop' },
  { label: '摇滚', value: 'rock' },
  { label: '电子', value: 'electronic' },
  { label: '民谣', value: 'folk' },
  { label: '古典', value: 'classical' }
])

// 推荐歌单
const featuredPlaylists = ref<Playlist[]>([
  {
    id: '1',
    name: '热歌榜 Top 100',
    description: '全网最热门的歌曲合集',
    cover: '',
    playCount: 1250000,
    trackCount: 100,
    platform: 'netease'
  },
  {
    id: '2',
    name: '新歌首发',
    description: '最新发布的优质音乐',
    cover: '',
    playCount: 890000,
    trackCount: 50,
    platform: 'qq'
  },
  {
    id: '3',
    name: '经典老歌',
    description: '永恒的经典旋律',
    cover: '',
    playCount: 1560000,
    trackCount: 80,
    platform: 'kugou'
  }
])

// 搜索结果
const searchResults = ref<OnlineMusic[]>([])

// 排行榜数据
const activeChart = ref('hot')
const hotSongs = ref<OnlineMusic[]>([
  {
    id: '1',
    title: '夜曲',
    artist: '周杰伦',
    album: '十一月的萧邦',
    duration: 227,
    platform: 'netease',
    cover: '',
    url: ''
  },
  {
    id: '2',
    title: '青花瓷',
    artist: '周杰伦',
    album: '我很忙',
    duration: 245,
    platform: 'qq',
    cover: '',
    url: ''
  }
])

const newSongs = ref<OnlineMusic[]>([])
const originalSongs = ref<OnlineMusic[]>([])

// 对话框状态
const playlistDialogVisible = ref(false)
const selectedMusic = ref<OnlineMusic | null>(null)
const selectedPlaylistId = ref('')

// 可用歌单列表
const availablePlaylists = ref([
  { id: '1', name: '我的最爱' },
  { id: '2', name: '工作背景音乐' },
  { id: '3', name: '运动音乐' }
])

// 搜索处理
const handleSearch = () => {
  if (!searchKeyword.value.trim()) {
    searchResults.value = []
    return
  }

  searchLoading.value = true
  
  // 模拟搜索延迟
  setTimeout(() => {
    searchResults.value = [
      {
        id: 'search-1',
        title: searchKeyword.value + ' - 搜索结果1',
        artist: '艺术家1',
        album: '专辑1',
        duration: 180,
        platform: 'netease',
        cover: '',
        url: ''
      },
      {
        id: 'search-2',
        title: searchKeyword.value + ' - 搜索结果2',
        artist: '艺术家2',
        album: '专辑2',
        duration: 210,
        platform: 'qq',
        cover: '',
        url: ''
      }
    ]
    searchLoading.value = false
  }, 1000)
}

// 平台切换
const handlePlatformChange = () => {
  if (searchKeyword.value) {
    handleSearch()
  }
}

// 分类切换
const handleCategoryChange = () => {
  if (searchKeyword.value) {
    handleSearch()
  }
}

// 排行榜切换
const handleChartChange = () => {
  // 加载对应排行榜数据
  console.log('切换到排行榜:', activeChart.value)
}

// 播放音乐
const playMusic = (music: OnlineMusic) => {
  ElMessage.success(`开始播放: ${music.title} - ${music.artist}`)
  // 这里应该触发全局播放器播放该音乐
}

// 播放歌单
const playPlaylist = (playlist: Playlist) => {
  ElMessage.success(`开始播放歌单: ${playlist.name}`)
  // 这里应该触发全局播放器播放该歌单
}

// 打开歌单
const openPlaylist = (playlist: Playlist) => {
  ElMessage.info(`打开歌单: ${playlist.name}`)
  // 这里应该跳转到歌单详情页面
}

// 添加到歌单
const addToPlaylist = (music: OnlineMusic) => {
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

// 格式化时长
const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 获取平台标签类型
const getPlatformTagType = (platform: string) => {
  const types: Record<string, any> = {
    netease: 'success',
    qq: 'primary',
    kugou: 'warning',
    kuwo: 'info'
  }
  return types[platform] || 'default'
}

// 获取平台名称
const getPlatformName = (platform: string) => {
  const names: Record<string, string> = {
    netease: '网易云',
    qq: 'QQ音乐',
    kugou: '酷狗',
    kuwo: '酷我'
  }
  return names[platform] || platform
}


</script>

<style scoped>
.online-music {
  padding: 20px;
}

.search-filter {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.search-input {
  flex: 1;
}

.section-title {
  margin: 30px 0 20px 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
}

.recommendation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
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
  height: 140px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.playlist-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  cursor: pointer;
}

.playlist-card:hover .play-button {
  opacity: 1;
}

.playlist-info {
  padding: 15px;
}

.playlist-name {
  margin: 0 0 8px 0;
  font-size: 1rem;
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

.playlist-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #999;
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

.music-duration {
  color: #999;
  font-size: 0.875rem;
}

.music-actions {
  display: flex;
  gap: 10px;
}

.chart-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chart-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.chart-item:hover {
  background-color: #f5f7fa;
}

.chart-rank {
  width: 30px;
  text-align: center;
  font-weight: 600;
  color: #666;
}

.chart-info {
  flex: 1;
}

.song-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.song-artist {
  font-size: 0.875rem;
  color: #666;
}

.chart-actions {
  opacity: 0;
  transition: opacity 0.3s;
}

.chart-item:hover .chart-actions {
  opacity: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-filter {
    flex-direction: column;
  }
  
  .recommendation-grid {
    grid-template-columns: 1fr;
  }
}
</style>