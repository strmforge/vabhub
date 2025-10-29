<template>
  <div class="discover-grid">
    <!-- 网格布局 -->
    <div class="grid-container">
      <div 
        v-for="item in items" 
        :key="item.title + item.source"
        class="discover-item"
        @click="handleItemClick(item)"
      >
        <!-- 海报图片 -->
        <div class="item-poster">
          <img 
            v-if="item.poster_url" 
            :src="item.poster_url" 
            :alt="item.title"
            @error="handleImageError"
          />
          <div v-else class="placeholder-poster">
            <span class="placeholder-icon">{{ getCategoryIcon(item.category) }}</span>
          </div>
          
          <!-- 评分标签 -->
          <div v-if="item.rating" class="rating-badge">
            ⭐ {{ item.rating }}
          </div>
        </div>
        
        <!-- 内容信息 -->
        <div class="item-content">
          <h3 class="item-title">{{ item.title }}</h3>
          
          <div class="item-meta">
            <span class="item-category">{{ getCategoryName(item.category) }}</span>
            <span class="item-source">{{ getSourceName(item.source) }}</span>
            <span v-if="item.release_date" class="item-date">{{ formatDate(item.release_date) }}</span>
          </div>
          
          <p v-if="item.description" class="item-description">
            {{ truncateDescription(item.description) }}
          </p>
          
          <!-- 操作按钮 -->
          <div class="item-actions">
            <button 
              v-if="item.category !== 'music'"
              @click.stop="handleSearch(item)"
              class="action-btn search-btn"
            >
              搜索资源
            </button>
            <button 
              @click.stop="handleAddToLibrary(item)"
              class="action-btn library-btn"
            >
              收藏
            </button>
            <button 
              v-if="item.category === 'music'"
              @click.stop="handlePlay(item)"
              class="action-btn play-btn"
            >
              播放
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div v-if="items.length === 0 && !loading" class="empty-state">
      <div class="empty-icon">🔍</div>
      <h3>暂无发现内容</h3>
      <p>尝试切换分类或来源来发现更多内容</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'DiscoverGrid',
  props: {
    items: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  setup(props, { emit }) {
    const router = useRouter()

    // 方法
    const getCategoryIcon = (category) => {
      const icons = {
        'movie': '🎬',
        'tv': '📺',
        'anime': '🎨',
        'music': '🎵',
        'all': '📄'
      }
      return icons[category] || '📄'
    }

    const getCategoryName = (category) => {
      const names = {
        'movie': '电影',
        'tv': '电视剧',
        'anime': '动漫',
        'music': '音乐',
        'all': '全部'
      }
      return names[category] || category
    }

    const getSourceName = (source) => {
      const names = {
        'tmdb': 'TMDB',
        'douban': '豆瓣',
        'bangumi': 'Bangumi',
        'netflix_top10': 'Netflix Top 10',
        'imdb_datasets': 'IMDb Datasets',
        'spotify': 'Spotify',
        'apple_music': 'Apple Music'
      }
      return names[source] || source
    }

    const formatDate = (dateString) => {
      try {
        const date = new Date(dateString)
        return date.getFullYear() + '-' + 
               String(date.getMonth() + 1).padStart(2, '0') + '-' + 
               String(date.getDate()).padStart(2, '0')
      } catch {
        return dateString
      }
    }

    const truncateDescription = (description, maxLength = 100) => {
      if (description.length <= maxLength) {
        return description
      }
      return description.substring(0, maxLength) + '...'
    }

    const handleImageError = (event) => {
      event.target.style.display = 'none'
      event.target.parentElement.querySelector('.placeholder-poster').style.display = 'flex'
    }

    const handleItemClick = (item) => {
      emit('item-click', item)
      
      // 根据分类跳转到不同页面
      if (item.category === 'music') {
        // 跳转到音乐详情页
        router.push(`/music/detail?title=${encodeURIComponent(item.title)}`)
      } else {
        // 跳转到媒体详情页
        router.push(`/media/detail?title=${encodeURIComponent(item.title)}&category=${item.category}`)
      }
    }

    const handleSearch = (item) => {
      emit('search', item)
      
      // 跳转到搜索页面
      router.push(`/search?query=${encodeURIComponent(item.title)}&category=${item.category}`)
    }

    const handleAddToLibrary = (item) => {
      emit('add-to-library', item)
      
      // 这里应该调用添加到媒体库的API
      console.log('添加到媒体库:', item)
    }

    const handlePlay = (item) => {
      emit('play', item)
      
      // 这里应该调用音乐播放的API
      console.log('播放音乐:', item)
    }

    return {
      getCategoryIcon,
      getCategoryName,
      getSourceName,
      formatDate,
      truncateDescription,
      handleImageError,
      handleItemClick,
      handleSearch,
      handleAddToLibrary,
      handlePlay
    }
  }
}
</script>

<style scoped>
.discover-grid {
  width: 100%;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.discover-item {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: var(--shadow);
}

.discover-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: var(--primary-color);
}

.item-poster {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.item-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.discover-item:hover .item-poster img {
  transform: scale(1.05);
}

.placeholder-poster {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--bg-secondary), var(--border-color));
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 48px;
  opacity: 0.7;
}

.rating-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.item-content {
  padding: 15px;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.item-category,
.item-source,
.item-date {
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  padding: 2px 6px;
  border-radius: 4px;
}

.item-description {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
  text-align: center;
}

.action-btn:hover {
  transform: translateY(-1px);
}

.search-btn:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.library-btn:hover {
  background: #28a745;
  color: white;
  border-color: #28a745;
}

.play-btn:hover {
  background: #e74c3c;
  color: white;
  border-color: #e74c3c;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: var(--text-primary);
}

.empty-state p {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 15px;
  }
  
  .item-poster {
    height: 180px;
  }
  
  .item-content {
    padding: 12px;
  }
  
  .item-title {
    font-size: 15px;
  }
  
  .item-actions {
    flex-direction: column;
  }
  
  .action-btn {
    flex: none;
  }
}

@media (max-width: 480px) {
  .grid-container {
    grid-template-columns: 1fr;
  }
  
  .item-poster {
    height: 200px;
  }
}
</style>