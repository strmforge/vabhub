<template>
  <div class="plugin-market">
    <!-- 市场头部 -->
    <div class="market-header">
      <h2>插件市场</h2>
      <p>发现和安装新的VabHub插件</p>
      <div class="market-stats">
        <span class="stat-item">
          <span class="stat-value">{{ featuredPlugins.length }}</span>
          <span class="stat-label">精选插件</span>
        </span>
        <span class="stat-item">
          <span class="stat-value">{{ totalPlugins }}</span>
          <span class="stat-label">总插件数</span>
        </span>
        <span class="stat-item">
          <span class="stat-value">{{ newPluginsCount }}</span>
          <span class="stat-label">新插件</span>
        </span>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="market-controls">
      <div class="search-section">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="搜索插件..." 
          class="search-input"
        >
        <select v-model="filterCategory" class="filter-select">
          <option value="all">全部分类</option>
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
        <select v-model="sortBy" class="sort-select">
          <option value="popular">最受欢迎</option>
          <option value="newest">最新发布</option>
          <option value="rating">最高评分</option>
          <option value="downloads">最多下载</option>
        </select>
      </div>
      <div class="view-controls">
        <button 
          class="view-btn" 
          :class="{ active: viewMode === 'grid' }"
          @click="viewMode = 'grid'"
        >
          📱 网格
        </button>
        <button 
          class="view-btn" 
          :class="{ active: viewMode === 'list' }"
          @click="viewMode = 'list'"
        >
          📋 列表
        </button>
      </div>
    </div>

    <!-- 精选插件 -->
    <div class="featured-section" v-if="featuredPlugins.length > 0">
      <h3>🔥 精选插件</h3>
      <div class="featured-grid">
        <div 
          v-for="plugin in featuredPlugins" 
          :key="plugin.id" 
          class="featured-card"
        >
          <div class="featured-badge">精选</div>
          <div class="plugin-icon">{{ getPluginIcon(plugin.type) }}</div>
          <h4>{{ plugin.name }}</h4>
          <p>{{ plugin.description }}</p>
          <div class="plugin-meta">
            <span class="rating">⭐ {{ plugin.rating }}/5</span>
            <span class="downloads">📥 {{ formatDownloads(plugin.downloads) }}</span>
          </div>
          <button 
            class="btn btn-primary" 
            @click="showPluginDetails(plugin)"
          >
            查看详情
          </button>
        </div>
      </div>
    </div>

    <!-- 热门插件 -->
    <div class="popular-section" v-if="popularPlugins.length > 0">
      <h3>📈 热门插件</h3>
      <div class="popular-list">
        <div 
          v-for="(plugin, index) in popularPlugins" 
          :key="plugin.id" 
          class="popular-item"
        >
          <span class="rank">#{{ index + 1 }}</span>
          <div class="plugin-icon">{{ getPluginIcon(plugin.type) }}</div>
          <div class="plugin-info">
            <h4>{{ plugin.name }}</h4>
            <p>{{ plugin.description }}</p>
          </div>
          <div class="plugin-stats">
            <span class="downloads">{{ formatDownloads(plugin.downloads) }} 下载</span>
            <span class="rating">⭐ {{ plugin.rating }}</span>
          </div>
          <button 
            class="btn btn-primary" 
            @click="showPluginDetails(plugin)"
          >
            安装
          </button>
        </div>
      </div>
    </div>

    <!-- 插件网格/列表 -->
    <div class="plugins-section">
      <h3>所有插件 ({{ filteredPlugins.length }})</h3>
      
      <!-- 网格视图 -->
      <div v-if="viewMode === 'grid'" class="plugins-grid">
        <div 
          v-for="plugin in filteredPlugins" 
          :key="plugin.id" 
          class="plugin-card"
          :class="{ 'plugin-installed': plugin.installed }"
        >
          <div class="card-header">
            <div class="plugin-icon">{{ getPluginIcon(plugin.type) }}</div>
            <div class="plugin-badges">
              <span v-if="plugin.featured" class="badge featured">精选</span>
              <span v-if="plugin.new" class="badge new">新</span>
              <span v-if="plugin.verified" class="badge verified">✓ 认证</span>
            </div>
          </div>
          
          <div class="card-body">
            <h4>{{ plugin.name }}</h4>
            <p class="plugin-description">{{ plugin.description }}</p>
            
            <div class="plugin-meta">
              <span class="version">v{{ plugin.version }}</span>
              <span class="author">作者: {{ plugin.author }}</span>
            </div>
            
            <div class="plugin-stats">
              <div class="stat">
                <span class="stat-icon">⭐</span>
                <span class="stat-value">{{ plugin.rating }}</span>
              </div>
              <div class="stat">
                <span class="stat-icon">📥</span>
                <span class="stat-value">{{ formatDownloads(plugin.downloads) }}</span>
              </div>
              <div class="stat">
                <span class="stat-icon">👁️</span>
                <span class="stat-value">{{ formatDownloads(plugin.views) }}</span>
              </div>
            </div>
            
            <div class="plugin-tags">
              <span 
                v-for="tag in plugin.tags" 
                :key="tag" 
                class="tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>
          
          <div class="card-footer">
            <button 
              v-if="plugin.installed" 
              class="btn btn-secondary" 
              disabled
            >
              已安装
            </button>
            <button 
              v-else 
              class="btn btn-primary" 
              @click="installPlugin(plugin)"
            >
              安装
            </button>
            <button 
              class="btn btn-secondary" 
              @click="showPluginDetails(plugin)"
            >
              详情
            </button>
          </div>
        </div>
      </div>
      
      <!-- 列表视图 -->
      <div v-else class="plugins-list">
        <div 
          v-for="plugin in filteredPlugins" 
          :key="plugin.id" 
          class="list-item"
          :class="{ 'plugin-installed': plugin.installed }"
        >
          <div class="item-icon">{{ getPluginIcon(plugin.type) }}</div>
          
          <div class="item-info">
            <div class="item-header">
              <h4>{{ plugin.name }}</h4>
              <div class="item-badges">
                <span v-if="plugin.featured" class="badge featured">精选</span>
                <span v-if="plugin.new" class="badge new">新</span>
                <span v-if="plugin.verified" class="badge verified">✓</span>
              </div>
            </div>
            <p class="item-description">{{ plugin.description }}</p>
            <div class="item-meta">
              <span class="version">v{{ plugin.version }}</span>
              <span class="author">作者: {{ plugin.author }}</span>
              <span class="category">{{ plugin.category }}</span>
            </div>
          </div>
          
          <div class="item-stats">
            <div class="stat">
              <span class="stat-label">评分:</span>
              <span class="stat-value">{{ plugin.rating }}/5</span>
            </div>
            <div class="stat">
              <span class="stat-label">下载:</span>
              <span class="stat-value">{{ formatDownloads(plugin.downloads) }}</span>
            </div>
          </div>
          
          <div class="item-actions">
            <button 
              v-if="plugin.installed" 
              class="btn btn-secondary" 
              disabled
            >
              已安装
            </button>
            <button 
              v-else 
              class="btn btn-primary" 
              @click="installPlugin(plugin)"
            >
              安装
            </button>
            <button 
              class="btn btn-secondary" 
              @click="showPluginDetails(plugin)"
            >
              详情
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 插件详情模态框 -->
    <div v-if="selectedPlugin" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <div class="plugin-header">
            <div class="plugin-icon-large">{{ getPluginIcon(selectedPlugin.type) }}</div>
            <div class="plugin-title">
              <h3>{{ selectedPlugin.name }}</h3>
              <p>{{ selectedPlugin.description }}</p>
            </div>
          </div>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        
        <div class="modal-body">
          <!-- 基本信息 -->
          <div class="detail-section">
            <h4>基本信息</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <label>版本:</label>
                <span>v{{ selectedPlugin.version }}</span>
              </div>
              <div class="detail-item">
                <label>作者:</label>
                <span>{{ selectedPlugin.author }}</span>
              </div>
              <div class="detail-item">
                <label>分类:</label>
                <span>{{ selectedPlugin.category }}</span>
              </div>
              <div class="detail-item">
                <label>发布日期:</label>
                <span>{{ formatDate(selectedPlugin.releaseDate) }}</span>
              </div>
              <div class="detail-item">
                <label>最后更新:</label>
                <span>{{ formatDate(selectedPlugin.lastUpdate) }}</span>
              </div>
              <div class="detail-item">
                <label>兼容性:</label>
                <span>VabHub {{ selectedPlugin.compatibility }}</span>
              </div>
            </div>
          </div>
          
          <!-- 插件统计 -->
          <div class="detail-section">
            <h4>插件统计</h4>
            <div class="stats-grid">
              <div class="stat-card">
                <span class="stat-icon">⭐</span>
                <span class="stat-value">{{ selectedPlugin.rating }}</span>
                <span class="stat-label">评分</span>
              </div>
              <div class="stat-card">
                <span class="stat-icon">📥</span>
                <span class="stat-value">{{ formatDownloads(selectedPlugin.downloads) }}</span>
                <span class="stat-label">下载</span>
              </div>
              <div class="stat-card">
                <span class="stat-icon">👁️</span>
                <span class="stat-value">{{ formatDownloads(selectedPlugin.views) }}</span>
                <span class="stat-label">浏览</span>
              </div>
              <div class="stat-card">
                <span class="stat-icon">💬</span>
                <span class="stat-value">{{ selectedPlugin.reviews }}</span>
                <span class="stat-label">评价</span>
              </div>
            </div>
          </div>
          
          <!-- 功能特性 -->
          <div class="detail-section" v-if="selectedPlugin.features">
            <h4>功能特性</h4>
            <ul class="features-list">
              <li v-for="feature in selectedPlugin.features" :key="feature">
                ✅ {{ feature }}
              </li>
            </ul>
          </div>
          
          <!-- 系统要求 -->
          <div class="detail-section" v-if="selectedPlugin.requirements">
            <h4>系统要求</h4>
            <div class="requirements">
              <div 
                v-for="req in selectedPlugin.requirements" 
                :key="req.name"
                class="requirement-item"
              >
                <span class="req-name">{{ req.name }}:</span>
                <span class="req-value">{{ req.value }}</span>
              </div>
            </div>
          </div>
          
          <!-- 用户评价 -->
          <div class="detail-section" v-if="selectedPlugin.userReviews">
            <h4>用户评价</h4>
            <div class="reviews-list">
              <div 
                v-for="review in selectedPlugin.userReviews" 
                :key="review.id"
                class="review-item"
              >
                <div class="review-header">
                  <span class="reviewer">{{ review.user }}</span>
                  <span class="review-rating">⭐ {{ review.rating }}/5</span>
                </div>
                <p class="review-content">{{ review.content }}</p>
                <span class="review-date">{{ formatDate(review.date) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeModal">关闭</button>
          <button 
            v-if="!selectedPlugin.installed" 
            class="btn btn-primary" 
            @click="installPlugin(selectedPlugin)"
          >
            安装插件
          </button>
          <button 
            v-else 
            class="btn btn-secondary" 
            disabled
          >
            已安装
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PluginMarket',
  data() {
    return {
      searchQuery: '',
      filterCategory: 'all',
      sortBy: 'popular',
      viewMode: 'grid',
      selectedPlugin: null,
      categories: ['媒体管理', '下载工具', '通知系统', '搜索功能', '备份同步', '分析统计'],
      plugins: [
        {
          id: 'media-info-pro',
          name: '媒体信息专业版',
          description: '高级媒体文件信息识别和元数据管理',
          version: '2.1.0',
          author: 'VabHub Team',
          type: 'media',
          category: '媒体管理',
          featured: true,
          new: false,
          verified: true,
          rating: 4.8,
          downloads: 15420,
          views: 28900,
          reviews: 128,
          releaseDate: '2024-01-10',
          lastUpdate: '2024-01-25',
          compatibility: '1.5.0+',
          tags: ['媒体', '元数据', '识别'],
          features: [
            '支持100+种媒体格式',
            '自动识别影片信息',
            '批量元数据编辑',
            '智能分类整理'
          ],
          requirements: [
            { name: 'VabHub版本', value: '1.5.0+' },
            { name: '内存', value: '512MB+' },
            { name: '存储', value: '100MB' }
          ],
          userReviews: [
            {
              id: 1,
              user: '媒体爱好者',
              rating: 5,
              content: '非常强大的媒体识别功能，准确率很高！',
              date: '2024-01-20'
            }
          ]
        },
        {
          id: 'download-accelerator',
          name: '下载加速器',
          description: '多线程下载加速和断点续传功能',
          version: '1.2.3',
          author: 'Download Pro',
          type: 'download',
          category: '下载工具',
          featured: true,
          new: true,
          verified: true,
          rating: 4.6,
          downloads: 8920,
          views: 15600,
          reviews: 76,
          releaseDate: '2024-01-15',
          lastUpdate: '2024-01-28',
          compatibility: '1.4.0+',
          tags: ['下载', '加速', '多线程']
        },
        {
          id: 'smart-notifications',
          name: '智能通知系统',
          description: '多渠道智能通知和提醒管理',
          version: '1.0.5',
          author: 'Notify Inc',
          type: 'notification',
          category: '通知系统',
          featured: false,
          new: false,
          verified: true,
          rating: 4.3,
          downloads: 5430,
          views: 9800,
          reviews: 42,
          releaseDate: '2024-01-05',
          lastUpdate: '2024-01-22',
          compatibility: '1.3.0+',
          tags: ['通知', '提醒', '多渠道']
        },
        {
          id: 'advanced-search',
          name: '高级搜索',
          description: '支持多种搜索引擎的智能搜索插件',
          version: '1.1.2',
          author: 'Search Masters',
          type: 'search',
          category: '搜索功能',
          featured: false,
          new: true,
          verified: false,
          rating: 4.2,
          downloads: 3210,
          views: 6500,
          reviews: 28,
          releaseDate: '2024-01-18',
          lastUpdate: '2024-01-30',
          compatibility: '1.4.0+',
          tags: ['搜索', '智能', '多引擎']
        },
        {
          id: 'backup-manager',
          name: '备份管理器',
          description: '自动化数据备份和恢复解决方案',
          version: '1.0.8',
          author: 'Backup Pro',
          type: 'backup',
          category: '备份同步',
          featured: false,
          new: false,
          verified: true,
          rating: 4.7,
          downloads: 7650,
          views: 11200,
          reviews: 51,
          releaseDate: '2024-01-08',
          lastUpdate: '2024-01-26',
          compatibility: '1.5.0+',
          tags: ['备份', '恢复', '自动化']
        },
        {
          id: 'analytics-dashboard',
          name: '分析仪表板',
          description: '详细的使用统计和性能分析',
          version: '1.0.3',
          author: 'Analytics Team',
          type: 'analytics',
          category: '分析统计',
          featured: true,
          new: false,
          verified: true,
          rating: 4.5,
          downloads: 4320,
          views: 7800,
          reviews: 35,
          releaseDate: '2024-01-12',
          lastUpdate: '2024-01-29',
          compatibility: '1.4.0+',
          tags: ['分析', '统计', '仪表板']
        }
      ]
    }
  },
  computed: {
    featuredPlugins() {
      return this.plugins.filter(plugin => plugin.featured)
    },
    
    popularPlugins() {
      return [...this.plugins]
        .sort((a, b) => b.downloads - a.downloads)
        .slice(0, 5)
    },
    
    filteredPlugins() {
      let filtered = this.plugins
      
      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(plugin => 
          plugin.name.toLowerCase().includes(query) ||
          plugin.description.toLowerCase().includes(query) ||
          plugin.tags.some(tag => tag.toLowerCase().includes(query))
        )
      }
      
      // 分类过滤
      if (this.filterCategory !== 'all') {
        filtered = filtered.filter(plugin => plugin.category === this.filterCategory)
      }
      
      // 排序
      switch (this.sortBy) {
        case 'newest':
          filtered.sort((a, b) => new Date(b.releaseDate) - new Date(a.releaseDate))
          break
        case 'rating':
          filtered.sort((a, b) => b.rating - a.rating)
          break
        case 'downloads':
          filtered.sort((a, b) => b.downloads - a.downloads)
          break
        default: // popular
          filtered.sort((a, b) => (b.downloads + b.views) - (a.downloads + a.views))
      }
      
      return filtered
    },
    
    totalPlugins() {
      return this.plugins.length
    },
    
    newPluginsCount() {
      const oneMonthAgo = new Date()
      oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1)
      return this.plugins.filter(plugin => new Date(plugin.releaseDate) > oneMonthAgo).length
    }
  },
  methods: {
    getPluginIcon(type) {
      const icons = {
        media: '🎬',
        download: '📥',
        notification: '🔔',
        search: '🔍',
        backup: '💾',
        analytics: '📊',
        sync: '🔄'
      }
      return icons[type] || '🔌'
    },
    
    formatDownloads(count) {
      if (count >= 1000000) {
        return (count / 1000000).toFixed(1) + 'M'
      } else if (count >= 1000) {
        return (count / 1000).toFixed(1) + 'K'
      }
      return count.toString()
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('zh-CN')
    },
    
    showPluginDetails(plugin) {
      this.selectedPlugin = { ...plugin }
    },
    
    closeModal() {
      this.selectedPlugin = null
    },
    
    installPlugin(plugin) {
      console.log(`安装插件: ${plugin.name}`)
      // 这里应该调用安装API
      plugin.installed = true
      
      // 显示安装成功提示
      this.$emit('plugin-installed', plugin)
    }
  },
  mounted() {
    console.log('插件市场加载完成')
  }
}
</script>

<style scoped>
.plugin-market {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.market-header {
  text-align: center;
  margin-bottom: 2rem;
}

.market-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.market-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #3498db;
}

.stat-label {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.market-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.search-section {
  display: flex;
  gap: 1rem;
  flex: 1;
  max-width: 600px;
}

.search-input, .filter-select, .sort-select {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
}

.search-input {
  flex: 1;
}

.view-controls {
  display: flex;
  gap: 0.5rem;
}

.view-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.view-btn.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.featured-section, .popular-section, .plugins-section {
  margin-bottom: 3rem;
}

.featured-section h3, .popular-section h3, .plugins-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.featured-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  position: relative;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.featured-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #ff6b6b;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.featured-card .plugin-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.featured-card h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
}

.featured-card p {
  margin: 0 0 1rem 0;
  opacity: 0.9;
}

.plugin-meta {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.popular-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.popular-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.rank {
  font-size: 1.2rem;
  font-weight: 600;
  color: #3498db;
  min-width: 40px;
}

.popular-item .plugin-icon {
  font-size: 2rem;
}

.item-info {
  flex: 1;
}

.item-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.item-header h4 {
  margin: 0;
  color: #2c3e50;
}

.plugin-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.plugins-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.plugin-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.plugin-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.plugin-card.plugin-installed {
  opacity: 0.7;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.plugin-icon {
  font-size: 2.5rem;
}

.plugin-badges {
  display: flex;
  gap: 0.5rem;
}

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.badge.featured {
  background: #ff6b6b;
  color: white;
}

.badge.new {
  background: #4ecdc4;
  color: white;
}

.badge.verified {
  background: #1dd1a1;
  color: white;
}

.card-body {
  flex: 1;
  margin-bottom: 1rem;
}

.card-body h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.plugin-description {
  color: #7f8c8d;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.plugin-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #95a5a6;
  margin-bottom: 1rem;
}

.plugin-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
}

.plugin-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #f8f9fa;
  color: #6c757d;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
}

.card-footer {
  display: flex;
  gap: 0.5rem;
}

.plugins-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.list-item.plugin-installed {
  opacity: 0.7;
}

.item-icon {
  font-size: 2rem;
}

.item-info {
  flex: 1;
}

.item-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #95a5a6;
  margin-top: 0.5rem;
}

.item-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.stat-label {
  color: #7f8c8d;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 2rem;
  border-bottom: 1px solid #eee;
}

.plugin-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.plugin-icon-large {
  font-size: 4rem;
}

.plugin-title h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.plugin-title p {
  margin: 0;
  color: #7f8c8d;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
}

.modal-body {
  padding: 2rem;
  flex: 1;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 2rem;
}

.detail-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f3f4;
}

.detail-item label {
  font-weight: 500;
  color: #34495e;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.stat-icon {
  font-size: 1.5rem;
  display: block;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  display: block;
}

.stat-label {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.features-list {
  list-style: none;
  padding: 0;
}

.features-list li {
  padding: 0.5rem 0;
  color: #27ae60;
}

.requirements {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.requirement-item {
  display: flex;
  justify-content: space-between;
  padding: 0.25rem 0;
}

.req-name {
  font-weight: 500;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.reviewer {
  font-weight: 600;
}

.review-content {
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.review-date {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .plugin-market {
    padding: 1rem;
  }
  
  .market-controls {
    flex-direction: column;
  }
  
  .search-section {
    max-width: none;
  }
  
  .featured-grid {
    grid-template-columns: 1fr;
  }
  
  .popular-item {
    flex-direction: column;
    text-align: center;
  }
  
  .list-item {
    flex-direction: column;
    text-align: center;
  }
  
  .modal-content {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>