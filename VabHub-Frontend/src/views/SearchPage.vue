<template>
  <div class="search-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1>智能搜索</h1>
      <p class="page-description">搜索电影、电视剧、动漫、音乐等媒体资源</p>
    </div>

    <!-- 搜索组件 -->
    <SearchComponent />

    <!-- 功能说明 -->
    <div class="features-section">
      <h2>搜索功能特性</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🔍</div>
          <h3>多源搜索</h3>
          <p>支持TMDB、豆瓣、Netflix Top 10、IMDb Datasets等多个数据源</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">⚡</div>
          <h3>智能优化</h3>
          <p>针对老电视剧等特殊内容进行智能搜索优化</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>高级过滤</h3>
          <p>支持按类型、来源、质量等多维度筛选结果</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📱</div>
          <h3>响应式设计</h3>
          <p>完美适配桌面端和移动端设备</p>
        </div>
      </div>
    </div>

    <!-- 使用指南 -->
    <div class="guide-section">
      <h2>使用指南</h2>
      <div class="guide-steps">
        <div class="guide-step">
          <span class="step-number">1</span>
          <div class="step-content">
            <h4>输入搜索关键词</h4>
            <p>在搜索框中输入电影名称、电视剧名、音乐标题等</p>
          </div>
        </div>
        <div class="guide-step">
          <span class="step-number">2</span>
          <div class="step-content">
            <h4>选择搜索类型</h4>
            <p>根据需要选择电影、电视剧、动漫或音乐类型</p>
          </div>
        </div>
        <div class="guide-step">
          <span class="step-number">3</span>
          <div class="step-content">
            <h4>查看搜索结果</h4>
            <p>浏览搜索结果，使用过滤器精确定位所需内容</p>
          </div>
        </div>
        <div class="guide-step">
          <span class="step-number">4</span>
          <div class="step-content">
            <h4>执行操作</h4>
            <p>下载资源、添加到媒体库或查看详细信息</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchComponent from '../components/SearchComponent.vue'

export default {
  name: 'SearchPage',
  components: {
    SearchComponent
  },
  setup() {
    return {
      // 页面逻辑可以在这里添加
    }
  }
}
</script>

<style scoped>
.search-page {
  min-height: 100vh;
  background: var(--bg-secondary);
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 0;
}

.page-header h1 {
  font-size: 3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 10px;
}

.page-description {
  font-size: 1.2rem;
  color: #7f8c8d;
  max-width: 600px;
  margin: 0 auto;
}

.features-section {
  margin: 60px 0;
  padding: 40px 0;
}

.features-section h2 {
  text-align: center;
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 40px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 15px;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

.guide-section {
  margin: 60px 0;
  padding: 40px 0;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
}

.guide-section h2 {
  text-align: center;
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 40px;
}

.guide-steps {
  max-width: 800px;
  margin: 0 auto;
}

.guide-step {
  display: flex;
  align-items: flex-start;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #3498db;
  color: white;
  border-radius: 50%;
  font-weight: bold;
  margin-right: 20px;
  flex-shrink: 0;
}

.step-content h4 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.step-content p {
  color: #7f8c8d;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .search-page {
    padding: 10px;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .feature-card {
    padding: 20px;
  }
  
  .guide-step {
    flex-direction: column;
    text-align: center;
  }
  
  .step-number {
    margin-right: 0;
    margin-bottom: 15px;
  }
}
</style>