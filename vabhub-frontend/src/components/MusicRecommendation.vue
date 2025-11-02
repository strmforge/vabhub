<template>
  <div class="music-recommendation">
    <!-- 推荐头部 -->
    <div class="recommendation-header">
      <h3 class="section-title">为你推荐</h3>
      <div class="refresh-actions">
        <el-button @click="refreshRecommendations">
          <el-icon><Refresh /></el-icon>
          刷新推荐
        </el-button>
      </div>
    </div>

    <!-- 个性化推荐 -->
    <div class="personalized-section">
      <h4 class="section-subtitle">个性化推荐</h4>
      <div class="recommendation-grid">
        <div
          v-for="item in personalizedRecommendations"
          :key="item.id"
          class="recommendation-card"
          @click="playRecommendation(item)"
        >
          <div class="recommendation-cover">
            <img :src="item.cover" :alt="item.title" />
            <div class="play-overlay">
              <el-button circle class="play-button">
                <el-icon><VideoPlay /></el-icon>
              </el-button>
            </div>
            <div class="recommendation-badge" :class="item.type">
              {{ getTypeLabel(item.type) }}
            </div>
          </div>
          <div class="recommendation-info">
            <h5 class="recommendation-title">{{ item.title }}</h5>
            <p class="recommendation-desc">{{ item.description }}</p>
            <div class="recommendation-meta">
              <span class="meta-item">{{ item.trackCount }} 首歌曲</span>
              <span class="meta-item">{{ item.playCount }} 次播放</span>
            </div>
            <div class="recommendation-tags">
              <el-tag
                v-for="tag in item.tags.slice(0, 2)"
                :key="tag"
                size="small"
                class="tag-item"
              >
                {{ tag }}
              </el-tag>
              <span v-if="item.tags.length > 2" class="more-tags">
                +{{ item.tags.length - 2 }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门推荐 -->
    <div class="popular-section">
      <h4 class="section-subtitle">热门推荐</h4>
      <div class="popular-list">
        <div
          v-for="(song, index) in popularSongs"
          :key="song.id"
          class="popular-item"
          @click="playSong(song)"
        >
          <div class="song-rank">{{ index + 1 }}</div>
          <div class="song-cover">
            <img :src="song.cover" :alt="song.title" />
          </div>
          <div class="song-info">
            <div class="song-title">{{ song.title }}</div>
            <div class="song-artist">{{ song.artist }}</div>
          </div>
          <div class="song-duration">{{ formatDuration(song.duration) }}</div>
          <div class="song-actions">
            <el-button link @click.stop="addToPlaylist(song)">
              <el-icon><Plus /></el-icon>
            </el-button>
            <el-button link @click.stop="likeSong(song)">
              <el-icon :class="{ 'liked': song.liked }">
                <StarFilled v-if="song.liked" />
                <Star v-else />
              </el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 新歌推荐 -->
    <div class="new-songs-section">
      <h4 class="section-subtitle">新歌推荐</h4>
      <div class="new-songs-grid">
        <div
          v-for="song in newSongs"
          :key="song.id"
          class="new-song-card"
          @click="playSong(song)"
        >
          <div class="song-cover">
            <img :src="song.cover" :alt="song.title" />
            <div class="new-badge">新歌</div>
          </div>
          <div class="song-details">
            <div class="song-title">{{ song.title }}</div>
            <div class="song-artist">{{ song.artist }}</div>
            <div class="song-album">{{ song.album }}</div>
            <div class="song-meta">
              <span class="meta-item">{{ formatDuration(song.duration) }}</span>
              <span class="meta-item">{{ song.releaseDate }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 相似艺术家 -->
    <div class="similar-artists-section">
      <h4 class="section-subtitle">相似艺术家</h4>
      <div class="artists-grid">
        <div
          v-for="artist in similarArtists"
          :key="artist.id"
          class="artist-card"
          @click="viewArtist(artist)"
        >
          <div class="artist-avatar">
            <img :src="artist.avatar" :alt="artist.name" />
          </div>
          <div class="artist-info">
            <div class="artist-name">{{ artist.name }}</div>
            <div class="artist-genre">{{ artist.genre }}</div>
            <div class="artist-followers">{{ artist.followers }} 粉丝</div>
          </div>
          <div class="artist-actions">
            <el-button 
              :type="artist.followed ? 'primary' : 'default'" 
              size="small"
              @click.stop="toggleFollow(artist)"
            >
              {{ artist.followed ? '已关注' : '关注' }}
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐理由 -->
    <div class="recommendation-reason">
      <h4 class="section-subtitle">推荐理由</h4>
      <div class="reason-content">
        <p>基于你的听歌历史、收藏歌曲和偏好设置，为你推荐这些内容。</p>
        <div class="reason-tags">
          <span class="reason-tag">#{{ userPreferences.primaryGenre }}</span>
          <span class="reason-tag">#{{ userPreferences.mood }}</span>
          <span class="reason-tag">#{{ userPreferences.activity }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, VideoPlay, Plus, Star, StarFilled } from '@element-plus/icons-vue'

interface RecommendationItem {
  id: string
  title: string
  description: string
  cover: string
  type: 'playlist' | 'album' | 'artist' | 'radio'
  trackCount: number
  playCount: number
  tags: string[]
  reason?: string
}

interface Song {
  id: string
  title: string
  artist: string
  album: string
  cover: string
  duration: number
  liked: boolean
  releaseDate: string
}

interface Artist {
  id: string
  name: string
  avatar: string
  genre: string
  followers: number
  followed: boolean
}

// 个性化推荐
const personalizedRecommendations = ref<RecommendationItem[]>([
  {
    id: '1',
    title: '深夜工作必备',
    description: '适合深夜工作的背景音乐',
    cover: '',
    type: 'playlist',
    trackCount: 25,
    playCount: 12345,
    tags: ['轻音乐', '背景音乐', '工作', '专注'],
    reason: '基于你最近的工作时间段推荐'
  },
  {
    id: '2',
    title: '周杰伦精选',
    description: '周杰伦经典歌曲合集',
    cover: '',
    type: 'album',
    trackCount: 15,
    playCount: 56789,
    tags: ['流行', '华语', '经典', '周杰伦']
  },
  {
    id: '3',
    title: '运动能量',
    description: '运动时的能量音乐',
    cover: '',
    type: 'playlist',
    trackCount: 20,
    playCount: 23456,
    tags: ['电子', '运动', '能量', '健身']
  }
])

// 热门歌曲
const popularSongs = ref<Song[]>([
  {
    id: '1',
    title: '夜曲',
    artist: '周杰伦',
    album: '十一月的萧邦',
    cover: '',
    duration: 227,
    liked: true,
    releaseDate: '2005-11-01'
  },
  {
    id: '2',
    title: '青花瓷',
    artist: '周杰伦',
    album: '我很忙',
    cover: '',
    duration: 245,
    liked: false,
    releaseDate: '2007-11-02'
  },
  {
    id: '3',
    title: '七里香',
    artist: '周杰伦',
    album: '七里香',
    cover: '',
    duration: 298,
    liked: true,
    releaseDate: '2004-08-03'
  }
])

// 新歌推荐
const newSongs = ref<Song[]>([
  {
    id: '4',
    title: '新歌1',
    artist: '新歌手A',
    album: '新专辑A',
    cover: '',
    duration: 210,
    liked: false,
    releaseDate: '2024-01-15'
  },
  {
    id: '5',
    title: '新歌2',
    artist: '新歌手B',
    album: '新专辑B',
    cover: '',
    duration: 195,
    liked: false,
    releaseDate: '2024-01-10'
  }
])

// 相似艺术家
const similarArtists = ref<Artist[]>([
  {
    id: '1',
    name: '林俊杰',
    avatar: '',
    genre: '流行',
    followers: 1234567,
    followed: true
  },
  {
    id: '2',
    name: '邓紫棋',
    avatar: '',
    genre: '流行',
    followers: 987654,
    followed: false
  },
  {
    id: '3',
    name: '薛之谦',
    avatar: '',
    genre: '流行',
    followers: 876543,
    followed: false
  }
])

// 用户偏好
const userPreferences = reactive({
  primaryGenre: '流行',
  mood: '放松',
  activity: '工作',
  favoriteArtists: ['周杰伦'],
  listeningHours: '20:00-23:00'
})

// 获取类型标签
const getTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    playlist: '歌单',
    album: '专辑',
    artist: '艺术家',
    radio: '电台'
  }
  return labels[type] || type
}

// 格式化时长
const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 刷新推荐
const refreshRecommendations = async () => {
  ElMessage.info('正在更新推荐内容...')
  
  // 模拟刷新延迟
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  ElMessage.success('推荐内容已更新')
}

// 播放推荐内容
const playRecommendation = (item: RecommendationItem) => {
  ElMessage.success(`开始播放: ${item.title}`)
  // 这里应该触发全局播放器播放推荐内容
}

// 播放歌曲
const playSong = (song: Song) => {
  ElMessage.success(`开始播放: ${song.title} - ${song.artist}`)
  // 这里应该触发全局播放器播放歌曲
}

// 添加到歌单
const addToPlaylist = (song: Song) => {
  ElMessage.info(`将"${song.title}"添加到歌单`)
  // 这里应该打开歌单选择对话框
}

// 喜欢/取消喜欢歌曲
const likeSong = (song: Song) => {
  song.liked = !song.liked
  ElMessage.success(song.liked ? '已添加到喜欢列表' : '已从喜欢列表移除')
}

// 查看艺术家
const viewArtist = (artist: Artist) => {
  ElMessage.info(`查看艺术家: ${artist.name}`)
  // 这里应该跳转到艺术家详情页面
}

// 关注/取消关注艺术家
const toggleFollow = (artist: Artist) => {
  artist.followed = !artist.followed
  ElMessage.success(artist.followed ? '关注成功' : '已取消关注')
}
</script>

<style scoped>
.music-recommendation {
  padding: 20px;
}

.recommendation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.section-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.section-subtitle {
  margin: 30px 0 20px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.recommendation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.recommendation-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.recommendation-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.recommendation-cover {
  position: relative;
  height: 160px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.recommendation-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.recommendation-card:hover .play-overlay {
  opacity: 1;
}

.play-button {
  background: rgba(255, 255, 255, 0.9);
  color: #2c3e50;
  border: none;
}

.recommendation-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.recommendation-badge.playlist {
  background: #e74c3c;
}

.recommendation-badge.album {
  background: #3498db;
}

.recommendation-badge.artist {
  background: #9b59b6;
}

.recommendation-badge.radio {
  background: #f39c12;
}

.recommendation-info {
  padding: 15px;
}

.recommendation-title {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.recommendation-desc {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 0.875rem;
  line-height: 1.4;
}

.recommendation-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 0.75rem;
  color: #999;
}

.recommendation-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tag-item {
  margin-right: 5px;
}

.more-tags {
  font-size: 0.75rem;
  color: #999;
}

.popular-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 30px;
}

.popular-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.popular-item:hover {
  background-color: #f8f9fa;
}

.song-rank {
  width: 30px;
  text-align: center;
  font-weight: 600;
  color: #666;
  font-size: 1.1rem;
}

.song-cover {
  width: 40px;
  height: 40px;
  margin: 0 15px;
}

.song-cover img {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  object-fit: cover;
}

.song-info {
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

.song-duration {
  color: #999;
  font-size: 0.875rem;
  margin-right: 15px;
}

.song-actions {
  display: flex;
  gap: 10px;
}

.song-actions .el-icon.liked {
  color: #f56c6c;
}

.new-songs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.new-song-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s;
}

.new-song-card:hover {
  transform: translateY(-2px);
}

.new-song-card .song-cover {
  position: relative;
  width: 100%;
  height: 120px;
  margin: 0;
}

.new-song-card .song-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.new-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #e74c3c;
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 600;
}

.song-details {
  padding: 10px;
}

.song-details .song-title {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 0.875rem;
}

.song-details .song-artist,
.song-details .song-album {
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 2px;
}

.song-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #999;
  margin-top: 5px;
}

.artists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.artist-card {
  display: flex;
  align-items: center;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.artist-card:hover {
  background-color: #f8f9fa;
}

.artist-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
}

.artist-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.artist-info {
  flex: 1;
}

.artist-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.artist-genre,
.artist-followers {
  font-size: 0.75rem;
  color: #666;
}

.recommendation-reason {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 30px;
}

.reason-content p {
  margin: 0 0 15px 0;
  color: #666;
}

.reason-tags {
  display: flex;
  gap: 10px;
}

.reason-tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .recommendation-grid {
    grid-template-columns: 1fr;
  }
  
  .new-songs-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  
  .artists-grid {
    grid-template-columns: 1fr;
  }
  
  .popular-item {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .song-actions {
    margin-left: auto;
  }
}
</style>