<template>
  <div class="search-results-grid">
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
          class="result-card"
          @click="$emit('item-click', result)"
          hover
        >
          <v-img
            :src="result.metadata?.poster || result.metadata?.cover || '/placeholder.jpg'"
            :alt="result.title"
            height="200"
            class="result-image"
          >
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-icon size="48" color="grey lighten-1">mdi-image</v-icon>
              </v-row>
            </template>
          </v-img>
          
          <v-card-text class="result-content">
            <div class="result-title">{{ result.title }}</div>
            
            <div class="result-meta">
              <v-chip 
                v-if="result.metadata?.year" 
                small 
                outlined 
                class="mr-1 mb-1"
              >
                {{ result.metadata.year }}
              </v-chip>
              
              <v-chip 
                :color="getTypeColor(result.type)" 
                small 
                class="mr-1 mb-1"
              >
                {{ getTypeText(result.type) }}
              </v-chip>
              
              <v-chip 
                v-if="result.metadata?.rating" 
                small 
                outlined 
                class="mr-1 mb-1"
              >
                <v-icon small left>mdi-star</v-icon>
                {{ result.metadata.rating }}
              </v-chip>
            </div>
            
            <div v-if="result.metadata?.overview" class="result-description">
              {{ truncateText(result.metadata.overview, 100) }}
            </div>
            
            <div class="result-source">
              <v-icon small left>mdi-source-branch</v-icon>
              {{ getSourceText(result.source) }}
            </div>
          </v-card-text>
          
          <v-card-actions class="result-actions">
            <v-btn 
              v-if="result.download_info" 
              small 
              color="primary" 
              @click.stop="handleDownload(result)"
            >
              <v-icon small left>mdi-download</v-icon>
              下载
            </v-btn>
            
            <v-btn 
              small 
              outlined 
              @click.stop="handleDetails(result)"
            >
              <v-icon small left>mdi-information</v-icon>
              详情
            </v-btn>
            
            <v-spacer></v-spacer>
            
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
    
    <div v-else class="no-results">
      <v-icon size="64" color="grey lighten-1">mdi-magnify-close</v-icon>
      <h3 class="mt-4">没有找到结果</h3>
      <p class="grey--text">尝试使用不同的关键词或搜索类型</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'SearchResultsGrid',
  props: {
    results: {
      type: Array,
      default: () => []
    }
  },
  emits: ['item-click'],
  setup(props, { emit }) {
    // 类型颜色映射
    const typeColors = {
      movie: 'blue',
      tv: 'green', 
      anime: 'orange',
      music: 'purple'
    }
    
    // 类型文本映射
    const typeTexts = {
      movie: '电影',
      tv: '电视剧',
      anime: '动漫', 
      music: '音乐'
    }
    
    // 源文本映射
    const sourceTexts = {
      local: '本地',
      tmdb: 'TMDB',
      douban: '豆瓣',
      netflix_top10: 'Netflix Top 10',
      imdb_datasets: 'IMDb Datasets',
      spotify: 'Spotify',
      apple_music: 'Apple Music'
    }
    
    // 方法
    const getTypeColor = (type) => {
      return typeColors[type] || 'grey'
    }
    
    const getTypeText = (type) => {
      return typeTexts[type] || type
    }
    
    const getSourceText = (source) => {
      return sourceTexts[source] || source
    }
    
    const truncateText = (text, length) => {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    const handleDownload = (result) => {
      console.log('Download:', result)
      // 处理下载逻辑
    }
    
    const handleDetails = (result) => {
      console.log('Details:', result)
      // 处理详情逻辑
    }
    
    const handleFavorite = (result) => {
      console.log('Favorite:', result)
      // 处理收藏逻辑
    }
    
    return {
      getTypeColor,
      getTypeText,
      getSourceText,
      truncateText,
      handleDownload,
      handleDetails,
      handleFavorite
    }
  }
}
</script>

<style scoped>
.search-results-grid {
  width: 100%;
}

.result-card {
  height: 100%;
  transition: transform 0.2s ease-in-out;
}

.result-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.result-image {
  border-radius: 4px 4px 0 0;
}

.result-content {
  padding: 16px;
}

.result-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 8px;
  line-height: 1.2;
}

.result-meta {
  margin-bottom: 8px;
}

.result-description {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.4;
  margin-bottom: 8px;
}

.result-source {
  font-size: 0.75rem;
  color: #999;
  display: flex;
  align-items: center;
}

.result-actions {
  padding: 8px 16px 16px;
}

.no-results {
  text-align: center;
  padding: 60px 20px;
  color: #9e9e9e;
}

@media (max-width: 960px) {
  .result-card {
    margin-bottom: 16px;
  }
}
</style>