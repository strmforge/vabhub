<template>
  <div class="music-results-grid">
    <v-row v-if="results.length > 0">
      <v-col
        v-for="result in results"
        :key="result.id || result.title"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card 
          class="music-card"
          @click="$emit('item-click', result)"
          hover
        >
          <div class="music-cover-container">
            <v-img
              :src="result.metadata?.cover || result.metadata?.poster || '/music-placeholder.jpg'"
              :alt="result.title"
              height="200"
              class="music-cover"
            >
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-icon size="48" color="grey lighten-1">mdi-music</v-icon>
                </v-row>
              </template>
              
              <!-- 播放按钮 -->
              <div class="play-overlay">
                <v-btn 
                  icon 
                  large 
                  color="white" 
                  @click.stop="handlePlay(result)"
                  class="play-btn"
                >
                  <v-icon>mdi-play</v-icon>
                </v-btn>
              </div>
            </v-img>
          </div>
          
          <v-card-text class="music-content">
            <div class="music-title">{{ result.title }}</div>
            
            <div v-if="result.metadata?.artist" class="music-artist">
              <v-icon small left>mdi-account-music</v-icon>
              {{ result.metadata.artist }}
            </div>
            
            <div v-if="result.metadata?.album" class="music-album">
              <v-icon small left>mdi-album</v-icon>
              {{ result.metadata.album }}
            </div>
            
            <div class="music-meta">
              <v-chip 
                v-if="result.metadata?.year" 
                small 
                outlined 
                class="mr-1 mb-1"
              >
                {{ result.metadata.year }}
              </v-chip>
              
              <v-chip 
                v-if="result.metadata?.genre" 
                small 
                outlined 
                class="mr-1 mb-1"
              >
                {{ result.metadata.genre }}
              </v-chip>
              
              <v-chip 
                v-if="result.metadata?.duration" 
                small 
                outlined 
                class="mr-1 mb-1"
              >
                {{ formatDuration(result.metadata.duration) }}
              </v-chip>
            </div>
            
            <div v-if="result.metadata?.lyrics" class="music-lyrics-preview">
              {{ truncateText(result.metadata.lyrics, 80) }}
            </div>
            
            <div class="music-source">
              <v-icon small left>mdi-source-branch</v-icon>
              {{ getSourceText(result.source) }}
            </div>
          </v-card-text>
          
          <v-card-actions class="music-actions">
            <v-btn 
              small 
              color="primary" 
              @click.stop="handlePlay(result)"
            >
              <v-icon small left>mdi-play</v-icon>
              播放
            </v-btn>
            
            <v-btn 
              v-if="result.download_info" 
              small 
              outlined 
              @click.stop="handleDownload(result)"
            >
              <v-icon small left>mdi-download</v-icon>
              下载
            </v-btn>
            
            <v-spacer></v-spacer>
            
            <v-btn 
              icon 
              small 
              @click.stop="handleAddToPlaylist(result)"
            >
              <v-icon>mdi-playlist-plus</v-icon>
            </v-btn>
            
            <v-btn 
              icon 
              small 
              @click.stop="handleFavorite(result)"
            >
              <v-icon>mdi-heart-outline</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <div v-else class="no-music-results">
      <v-icon size="64" color="grey lighten-1">mdi-music-off</v-icon>
      <h3 class="mt-4">没有找到音乐</h3>
      <p class="grey--text">尝试使用不同的关键词或搜索源</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'MusicResultsGrid',
  props: {
    results: {
      type: Array,
      default: () => []
    }
  },
  emits: ['item-click'],
  setup(props, { emit }) {
    // 源文本映射
    const sourceTexts = {
      local: '本地',
      netflix_top10: 'Netflix Top 10',
      imdb_datasets: 'IMDb Datasets',
      spotify: 'Spotify',
      apple_music: 'Apple Music'
    }
    
    // 方法
    const getSourceText = (source) => {
      return sourceTexts[source] || source
    }
    
    const truncateText = (text, length) => {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    const formatDuration = (seconds) => {
      if (!seconds) return ''
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
    }
    
    const handlePlay = (result) => {
      console.log('Play music:', result)
      // 处理播放逻辑
      emit('item-click', result)
    }
    
    const handleDownload = (result) => {
      console.log('Download music:', result)
      // 处理下载逻辑
    }
    
    const handleAddToPlaylist = (result) => {
      console.log('Add to playlist:', result)
      // 处理添加到播放列表逻辑
    }
    
    const handleFavorite = (result) => {
      console.log('Favorite music:', result)
      // 处理收藏逻辑
    }
    
    return {
      getSourceText,
      truncateText,
      formatDuration,
      handlePlay,
      handleDownload,
      handleAddToPlaylist,
      handleFavorite
    }
  }
}
</script>

<style scoped>
.music-results-grid {
  width: 100%;
}

.music-card {
  height: 100%;
  transition: transform 0.2s ease-in-out;
}

.music-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.music-cover-container {
  position: relative;
}

.music-cover {
  border-radius: 4px 4px 0 0;
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
  transition: opacity 0.3s ease;
  border-radius: 4px 4px 0 0;
}

.music-card:hover .play-overlay {
  opacity: 1;
}

.play-btn {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.music-content {
  padding: 16px;
}

.music-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 8px;
  line-height: 1.2;
}

.music-artist,
.music-album {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
}

.music-meta {
  margin: 8px 0;
}

.music-lyrics-preview {
  font-size: 0.8rem;
  color: #888;
  font-style: italic;
  line-height: 1.4;
  margin: 8px 0;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
}

.music-source {
  font-size: 0.75rem;
  color: #999;
  display: flex;
  align-items: center;
  margin-top: 8px;
}

.music-actions {
  padding: 8px 16px 16px;
}

.no-music-results {
  text-align: center;
  padding: 60px 20px;
  color: #9e9e9e;
}

@media (max-width: 960px) {
  .music-card {
    margin-bottom: 16px;
  }
  
  .music-lyrics-preview {
    display: none;
  }
}
</style>