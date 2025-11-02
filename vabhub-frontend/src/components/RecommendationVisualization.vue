<template>
  <div class="recommendation-visualization">
    <div class="visualization-header">
      <h3>推荐结果可视化</h3>
      <div class="visualization-controls">
        <button 
          @click="toggleViewMode" 
          class="view-toggle-btn"
          :class="{ active: viewMode === 'grid' }"
        >
          {{ viewMode === 'grid' ? '网格视图' : '列表视图' }}
        </button>
        <button 
          @click="toggleSortMode" 
          class="sort-btn"
        >
          排序: {{ sortOptions[sortMode] }}
        </button>
      </div>
    </div>

    <div class="visualization-content">
      <!-- 相似度分布图 -->
      <div class="similarity-chart">
        <h4>相似度分布</h4>
        <div class="chart-container">
          <div 
            v-for="(item, index) in sortedRecommendations" 
            :key="item.id || index"
            class="similarity-bar"
            :style="{ width: (item.similarity_score * 100) + '%' }"
            :class="getConfidenceClass(item.confidence)"
            :title="item.title + ' - ' + (item.similarity_score * 100).toFixed(1) + '%'"
          >
            <span class="bar-label">{{ item.title }}</span>
            <span class="bar-value">{{ (item.similarity_score * 100).toFixed(1) }}%</span>
          </div>
        </div>
      </div>

      <!-- 推荐卡片网格/列表 -->
      <div :class="['recommendation-display', viewMode]">
        <div 
          v-for="(item, index) in sortedRecommendations" 
          :key="item.id || index"
          class="recommendation-item"
          :class="item.confidence"
        >
          <div class="item-visual">
            <div class="similarity-circle" :style="{ '--similarity': item.similarity_score * 100 }">
              <span class="similarity-text">{{ (item.similarity_score * 100).toFixed(0) }}%</span>
            </div>
          </div>
          
          <div class="item-info">
            <h5 class="item-title">{{ item.title }}</h5>
            <div class="item-meta">
              <span v-if="item.type" class="meta-item">{{ item.type }}</span>
              <span v-if="item.year" class="meta-item">{{ item.year }}</span>
              <span v-if="item.rating" class="meta-item">⭐ {{ item.rating }}</span>
            </div>
            
            <div v-if="item.genres" class="genres-tags">
              <span 
                v-for="genre in item.genres.slice(0, 3)" 
                :key="genre"
                class="genre-tag"
              >
                {{ genre }}
              </span>
            </div>
            
            <div v-if="item.description" class="item-description">
              {{ truncateDescription(item.description) }}
            </div>
          </div>
          
          <div class="item-actions">
            <button @click="$emit('select-item', item)" class="action-btn primary">
              查看详情
            </button>
            <button @click="$emit('similar-to-item', item)" class="action-btn secondary">
              更多类似
            </button>
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="stats-summary">
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <span class="stat-value">{{ recommendations.length }}</span>
            <span class="stat-label">推荐总数</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🎯</div>
          <div class="stat-info">
            <span class="stat-value">{{ highConfidenceCount }}</span>
            <span class="stat-label">高相似度</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <span class="stat-value">{{ averageSimilarity }}%</span>
            <span class="stat-label">平均相似度</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🎬</div>
          <div class="stat-info">
            <span class="stat-value">{{ movieCount }}</span>
            <span class="stat-label">电影数量</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'

export default {
  name: 'RecommendationVisualization',
  props: {
    recommendations: {
      type: Array,
      default: () => []
    }
  },
  emits: ['select-item', 'similar-to-item'],
  setup(props) {
    const viewMode = ref('grid') // 'grid' or 'list'
    const sortMode = ref('similarity') // 'similarity', 'title', 'year'
    
    const sortOptions = {
      similarity: '相似度',
      title: '标题',
      year: '年份'
    }

    const sortedRecommendations = computed(() => {
      const items = [...props.recommendations]
      
      switch (sortMode.value) {
        case 'similarity':
          return items.sort((a, b) => b.similarity_score - a.similarity_score)
        case 'title':
          return items.sort((a, b) => a.title?.localeCompare(b.title || ''))
        case 'year':
          return items.sort((a, b) => (b.year || 0) - (a.year || 0))
        default:
          return items
      }
    })

    const highConfidenceCount = computed(() => {
      return props.recommendations.filter(item => item.confidence === 'high').length
    })

    const averageSimilarity = computed(() => {
      if (props.recommendations.length === 0) return 0
      const total = props.recommendations.reduce((sum, item) => sum + item.similarity_score, 0)
      return Math.round((total / props.recommendations.length) * 100)
    })

    const movieCount = computed(() => {
      return props.recommendations.filter(item => item.type === 'movie').length
    })

    const toggleViewMode = () => {
      viewMode.value = viewMode.value === 'grid' ? 'list' : 'grid'
    }

    const toggleSortMode = () => {
      const modes = Object.keys(sortOptions)
      const currentIndex = modes.indexOf(sortMode.value)
      sortMode.value = modes[(currentIndex + 1) % modes.length]
    }

    const getConfidenceClass = (confidence) => {
      return {
        'high-confidence': confidence === 'high',
        'low-confidence': confidence === 'low'
      }
    }

    const truncateDescription = (text, maxLength = 100) => {
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }

    return {
      viewMode,
      sortMode,
      sortOptions,
      sortedRecommendations,
      highConfidenceCount,
      averageSimilarity,
      movieCount,
      toggleViewMode,
      toggleSortMode,
      getConfidenceClass,
      truncateDescription
    }
  }
}
</script>

<style scoped>
.recommendation-visualization {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.visualization-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.visualization-header h3 {
  margin: 0;
  color: #2c3e50;
}

.visualization-controls {
  display: flex;
  gap: 1rem;
}

.view-toggle-btn, .sort-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.view-toggle-btn.active, .sort-btn:hover {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.similarity-chart {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.similarity-chart h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.chart-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.similarity-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s;
  min-height: 40px;
  position: relative;
  overflow: hidden;
}

.similarity-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: currentColor;
  opacity: 0.2;
  width: 100%;
}

.similarity-bar.high-confidence {
  color: #28a745;
}

.similarity-bar.low-confidence {
  color: #ffc107;
}

.bar-label {
  font-weight: 500;
  z-index: 1;
}

.bar-value {
  font-weight: bold;
  z-index: 1;
}

.recommendation-display {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.recommendation-display.grid {
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.recommendation-display.list {
  grid-template-columns: 1fr;
}

.recommendation-item {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: transform 0.3s;
}

.recommendation-item:hover {
  transform: translateY(-2px);
}

.recommendation-item.high-confidence {
  border-left: 4px solid #28a745;
}

.recommendation-item.low-confidence {
  border-left: 4px solid #ffc107;
}

.item-visual {
  display: flex;
  justify-content: center;
}

.similarity-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
  position: relative;
}

.similarity-circle::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: conic-gradient(
    #28a745 0% calc(var(--similarity) * 1%),
    #ffc107 calc(var(--similarity) * 1%) 100%
  );
  opacity: 0.3;
}

.similarity-text {
  z-index: 1;
}

.item-info {
  flex: 1;
}

.item-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.item-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 0.8rem;
  color: #6c757d;
  background: #f8f9fa;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
}

.genres-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.genre-tag {
  font-size: 0.7rem;
  background: #e9ecef;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  color: #495057;
}

.item-description {
  font-size: 0.9rem;
  color: #6c757d;
  line-height: 1.4;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.3s;
}

.action-btn.primary {
  background: #007bff;
  color: white;
}

.action-btn.primary:hover {
  background: #0056b3;
}

.action-btn.secondary {
  background: #6c757d;
  color: white;
}

.action-btn.secondary:hover {
  background: #545b62;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-icon {
  font-size: 1.5rem;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #007bff;
}

.stat-label {
  font-size: 0.8rem;
  color: #6c757d;
}

@media (max-width: 768px) {
  .visualization-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .visualization-controls {
    justify-content: center;
  }
  
  .recommendation-display.grid {
    grid-template-columns: 1fr;
  }
  
  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .item-actions {
    flex-direction: column;
  }
}
</style>