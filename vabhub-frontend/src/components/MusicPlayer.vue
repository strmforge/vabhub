<template>
  <div class="music-player" :class="{ 'mini': isMini, 'expanded': isExpanded }">
    <!-- 迷你播放器 -->
    <div v-if="isMini" class="mini-player" @click="toggleExpanded">
      <div class="mini-info">
        <img :src="currentTrack?.cover || '/default-cover.png'" class="mini-cover" />
        <div class="mini-details">
          <div class="mini-title">{{ currentTrack?.title || $t('music.notPlaying') }}</div>
          <div class="mini-artist">{{ currentTrack?.artist || 'VabHub' }}</div>
        </div>
      </div>
      <div class="mini-controls">
        <button class="control-btn" @click.stop="togglePlay">
          <span v-if="isPlaying">⏸️</span>
          <span v-else>▶️</span>
        </button>
        <button class="control-btn" @click.stop="nextTrack">⏭️</button>
      </div>
    </div>

    <!-- 完整播放器 -->
    <div v-else class="full-player">
      <!-- 播放器头部 -->
      <div class="player-header">
        <h3 class="player-title">{{ $t('music.title') }}</h3>
        <div class="player-actions">
          <button class="action-btn" @click="toggleMini">
            {{ isMini ? $t('common.open') : $t('common.mini') }}
          </button>
          <button class="action-btn" @click="closePlayer">{{ $t('common.close') }}</button>
        </div>
      </div>

      <!-- 播放器内容 -->
      <div class="player-content">
        <!-- 封面和歌曲信息 -->
        <div class="track-info">
          <img :src="currentTrack?.cover || '/default-cover.png'" class="track-cover" />
          <div class="track-details">
            <h4 class="track-title">{{ currentTrack?.title || $t('music.notPlaying') }}</h4>
            <p class="track-artist">{{ currentTrack?.artist || $t('music.unknownArtist') }}</p>
            <p class="track-album">{{ currentTrack?.album || $t('music.unknownAlbum') }}</p>
          </div>
        </div>

        <!-- 进度条 -->
        <div class="progress-section">
          <div class="time-display">
            <span class="current-time">{{ formatTime(currentTime) }}</span>
            <span class="duration">{{ formatTime(duration) }}</span>
          </div>
          <div class="progress-bar" @click="seekTo">
            <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
          </div>
        </div>

        <!-- 控制按钮 -->
        <div class="controls">
          <button class="control-btn large" @click="previousTrack">⏮️</button>
          <button class="control-btn large play-btn" @click="togglePlay">
            <span v-if="isPlaying">⏸️</span>
            <span v-else>▶️</span>
          </button>
          <button class="control-btn large" @click="nextTrack">⏭️</button>
          <button class="control-btn" @click="toggleRepeat">
            <span :class="{ active: repeatMode === 'all' }">🔁</span>
          </button>
          <button class="control-btn" @click="toggleShuffle">
            <span :class="{ active: isShuffle }">🔀</span>
          </button>
        </div>

        <!-- 音量控制 -->
        <div class="volume-control">
          <button class="volume-btn" @click="toggleMute">
            <span v-if="isMuted">🔇</span>
            <span v-else-if="volume > 0.5">🔊</span>
            <span v-else>🔉</span>
          </button>
          <div class="volume-bar" @click="setVolume">
            <div class="volume-fill" :style="{ width: volume * 100 + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- 播放列表 -->
      <div class="playlist-section">
        <h4 class="playlist-title">{{ $t('music.playlist') }}</h4>
        <div class="playlist-tracks">
          <div
            v-for="(track, index) in playlist"
            :key="track.id"
            class="playlist-track"
            :class="{ active: currentTrackIndex === index }"
            @click="playTrack(index)"
          >
            <span class="track-number">{{ index + 1 }}</span>
            <img :src="track.cover" class="track-cover-small" />
            <div class="track-info-small">
              <div class="track-title-small">{{ track.title }}</div>
              <div class="track-artist-small">{{ track.artist }}</div>
            </div>
            <span class="track-duration">{{ formatTime(track.duration) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'

interface Track {
  id: string
  title: string
  artist: string
  album: string
  cover: string
  duration: number
  url: string
}

// 播放器状态
const isMini = ref(false)
const isExpanded = ref(false)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(0.7)
const isMuted = ref(false)
const repeatMode = ref<'off' | 'one' | 'all'>('off')
const isShuffle = ref(false)

// 播放列表
const playlist = ref<Track[]>([
  {
    id: '1',
    title: '示例歌曲1',
    artist: '示例艺术家',
    album: '示例专辑',
    cover: '/default-cover.png',
    duration: 240,
    url: '/music/sample1.mp3'
  },
  {
    id: '2',
    title: '示例歌曲2',
    artist: '示例艺术家',
    album: '示例专辑',
    cover: '/default-cover.png',
    duration: 180,
    url: '/music/sample2.mp3'
  }
])

const currentTrackIndex = ref(0)
const currentTrack = computed(() => playlist.value[currentTrackIndex.value])

// 音频元素
let audioElement: HTMLAudioElement | null = null

// 计算属性
const progressPercentage = computed(() => {
  return duration.value > 0 ? (currentTime.value / duration.value) * 100 : 0
})

// 格式化时间
const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 播放器控制方法
const togglePlay = () => {
  if (!audioElement) return
  
  if (isPlaying.value) {
    audioElement.pause()
  } else {
    audioElement.play()
  }
  isPlaying.value = !isPlaying.value
}

// 添加歌曲到播放列表
const addToPlaylist = (track: Track) => {
  playlist.value.push(track)
  ElMessage.success(`已添加 ${track.title} 到播放列表`)
}

// 从播放列表移除歌曲
const removeFromPlaylist = (index: number) => {
  if (playlist.value.length <= 1) {
    ElMessage.warning('播放列表至少需要保留一首歌曲')
    return
  }
  
  const removedTrack = playlist.value[index]
  playlist.value.splice(index, 1)
  
  // 如果移除的是当前播放的歌曲，播放下一首
  if (currentTrackIndex.value === index) {
    if (currentTrackIndex.value >= playlist.value.length) {
      currentTrackIndex.value = 0
    }
    playTrack(currentTrackIndex.value)
  } else if (currentTrackIndex.value > index) {
    currentTrackIndex.value--
  }
  
  ElMessage.success(`已移除 ${removedTrack.title}`)
}

// 清空播放列表
const clearPlaylist = () => {
  if (playlist.value.length <= 1) {
    ElMessage.warning('播放列表已为空')
    return
  }
  
  // 保留当前播放的歌曲
  const currentTrack = playlist.value[currentTrackIndex.value]
  playlist.value = [currentTrack]
  currentTrackIndex.value = 0
  
  ElMessage.success('播放列表已清空')
}

const playTrack = (index: number) => {
  currentTrackIndex.value = index
  if (audioElement) {
    audioElement.src = playlist.value[index].url
    audioElement.play()
    isPlaying.value = true
  }
}

const nextTrack = () => {
  if (isShuffle.value) {
    currentTrackIndex.value = Math.floor(Math.random() * playlist.value.length)
  } else {
    currentTrackIndex.value = (currentTrackIndex.value + 1) % playlist.value.length
  }
  playTrack(currentTrackIndex.value)
}

const previousTrack = () => {
  if (currentTime.value > 3) {
    // 如果播放超过3秒，回到开头
    if (audioElement) {
      audioElement.currentTime = 0
    }
  } else {
    // 否则播放上一首
    currentTrackIndex.value = currentTrackIndex.value > 0 ? currentTrackIndex.value - 1 : playlist.value.length - 1
    playTrack(currentTrackIndex.value)
  }
}

const toggleRepeat = () => {
  const modes: Array<'off' | 'one' | 'all'> = ['off', 'one', 'all']
  const currentIndex = modes.indexOf(repeatMode.value)
  repeatMode.value = modes[(currentIndex + 1) % modes.length]
}

const toggleShuffle = () => {
  isShuffle.value = !isShuffle.value
}

const toggleMute = () => {
  if (audioElement) {
    audioElement.muted = !isMuted.value
    isMuted.value = !isMuted.value
  }
}

const setVolume = (event: MouseEvent) => {
  if (!audioElement) return
  
  const volumeBar = event.currentTarget as HTMLElement
  const rect = volumeBar.getBoundingClientRect()
  const clickX = event.clientX - rect.left
  const newVolume = clickX / rect.width
  
  volume.value = Math.max(0, Math.min(1, newVolume))
  audioElement.volume = volume.value
}

const seekTo = (event: MouseEvent) => {
  if (!audioElement) return
  
  const progressBar = event.currentTarget as HTMLElement
  const rect = progressBar.getBoundingClientRect()
  const clickX = event.clientX - rect.left
  const percentage = clickX / rect.width
  
  audioElement.currentTime = percentage * duration.value
}

// 播放器界面控制
const toggleMini = () => {
  isMini.value = !isMini.value
}

const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

const closePlayer = () => {
  isExpanded.value = false
  isMini.value = true
}

// 音频事件处理
const setupAudioEvents = () => {
  if (!audioElement) return
  
  audioElement.addEventListener('timeupdate', () => {
    currentTime.value = audioElement?.currentTime || 0
  })
  
  audioElement.addEventListener('loadedmetadata', () => {
    duration.value = audioElement?.duration || 0
  })
  
  audioElement.addEventListener('ended', () => {
    if (repeatMode.value === 'one') {
      audioElement?.play()
    } else {
      nextTrack()
    }
  })
}

onMounted(() => {
  audioElement = new Audio()
  audioElement.volume = volume.value
  setupAudioEvents()
  
  // 初始化播放第一首歌曲
  if (playlist.value.length > 0) {
    audioElement.src = playlist.value[0].url
  }
})

onUnmounted(() => {
  if (audioElement) {
    audioElement.pause()
    audioElement = null
  }
})
</script>

<style scoped>
.music-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid #e0e0e0;
  z-index: 1000;
  transition: all 0.3s ease;
}

.music-player.mini {
  height: 60px;
}

.music-player.expanded {
  height: 400px;
}

/* 迷你播放器样式 */
.mini-player {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 100%;
  cursor: pointer;
}

.mini-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mini-cover {
  width: 40px;
  height: 40px;
  border-radius: 4px;
}

.mini-details {
  display: flex;
  flex-direction: column;
}

.mini-title {
  font-weight: 600;
  font-size: 14px;
}

.mini-artist {
  font-size: 12px;
  color: #666;
}

.mini-controls {
  display: flex;
  gap: 10px;
}

/* 完整播放器样式 */
.full-player {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.player-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  border-bottom: 1px solid #e0e0e0;
}

.player-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.player-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.player-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.track-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.track-cover {
  width: 100px;
  height: 100px;
  border-radius: 8px;
}

.track-details h4 {
  margin: 0 0 5px 0;
  font-size: 20px;
}

.track-artist, .track-album {
  margin: 0;
  color: #666;
}

.progress-section {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.time-display {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
}

.progress-bar {
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  cursor: pointer;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: #1976d2;
  border-radius: 2px;
  transition: width 0.1s;
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.control-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: background 0.3s;
}

.control-btn:hover {
  background: #f0f0f0;
}

.control-btn.large {
  font-size: 24px;
}

.play-btn {
  background: #1976d2;
  color: white;
}

.play-btn:hover {
  background: #1565c0;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.volume-bar {
  flex: 1;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  cursor: pointer;
}

.volume-fill {
  height: 100%;
  background: #1976d2;
  border-radius: 2px;
}

/* 播放列表样式 */
.playlist-section {
  border-top: 1px solid #e0e0e0;
  padding: 10px 20px;
  max-height: 150px;
  overflow-y: auto;
}

.playlist-title {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 600;
}

.playlist-tracks {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.playlist-track {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.playlist-track:hover {
  background: #f5f5f5;
}

.playlist-track.active {
  background: #e3f2fd;
}

.track-cover-small {
  width: 30px;
  height: 30px;
  border-radius: 4px;
}

.track-info-small {
  flex: 1;
}

.track-title-small {
  font-size: 12px;
  font-weight: 600;
}

.track-artist-small {
  font-size: 11px;
  color: #666;
}

.track-duration {
  font-size: 11px;
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .music-player.expanded {
    height: 100vh;
  }
  
  .track-info {
    flex-direction: column;
    text-align: center;
  }
  
  .controls {
    gap: 10px;
  }
  
  .control-btn {
    font-size: 18px;
    padding: 8px;
  }
}
</style>