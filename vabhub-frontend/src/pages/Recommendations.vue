<template>
  <div class="recommendations-page">
    <div class="page-header">
      <h1>AI 推荐</h1>
      <p>基于您的观看历史和偏好生成的个性化推荐</p>
    </div>
    
    <div class="recommendations-content">
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="热门推荐" name="hot">
          <RecommendationList :type="'hot'" />
        </el-tab-pane>
        
        <el-tab-pane label="个性化推荐" name="personalized">
          <RecommendationList :type="'personalized'" />
        </el-tab-pane>
        
        <el-tab-pane label="相似内容" name="similar">
          <RecommendationList :type="'similar'" />
        </el-tab-pane>
        
        <el-tab-pane label="新发现" name="discovery">
          <RecommendationList :type="'discovery'" />
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <!-- 推荐设置面板 -->
    <el-drawer
      v-model="showSettings"
      title="推荐设置"
      direction="rtl"
      size="300px"
    >
      <div class="settings-panel">
        <div class="setting-section">
          <h4>推荐偏好</h4>
          <el-checkbox-group v-model="preferenceSettings">
            <el-checkbox label="movie">电影</el-checkbox>
            <el-checkbox label="tv">电视剧</el-checkbox>
            <el-checkbox label="anime">动漫</el-checkbox>
            <el-checkbox label="documentary">纪录片</el-checkbox>
          </el-checkbox-group>
        </div>
        
        <div class="setting-section">
          <h4>内容类型</h4>
          <el-select v-model="contentTypes" multiple placeholder="选择内容类型">
            <el-option label="动作" value="action" />
            <el-option label="喜剧" value="comedy" />
            <el-option label="剧情" value="drama" />
            <el-option label="科幻" value="sci-fi" />
            <el-option label="悬疑" value="mystery" />
          </el-select>
        </div>
        
        <div class="setting-section">
          <h4>推荐强度</h4>
          <el-slider
            v-model="recommendationStrength"
            :min="1"
            :max="10"
            :step="1"
            show-stops
          />
        </div>
        
        <el-button type="primary" style="width: 100%; margin-top: 20px;">
          保存设置
        </el-button>
      </div>
    </el-drawer>
    
    <!-- 设置按钮 -->
    <el-button 
      class="settings-btn" 
      type="primary" 
      circle 
      @click="showSettings = true"
    >
      <el-icon><Setting /></el-icon>
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Setting } from '@element-plus/icons-vue'
import RecommendationList from '@/components/recommendation/RecommendationList.vue'

const activeTab = ref('hot')
const showSettings = ref(false)
const preferenceSettings = ref(['movie', 'tv'])
const contentTypes = ref(['action', 'drama'])
const recommendationStrength = ref(7)
</script>

<style scoped>
.recommendations-page {
  padding: 20px;
  position: relative;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-header h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

.page-header p {
  color: #666;
  font-size: 1rem;
}

.recommendations-content {
  max-width: 1200px;
  margin: 0 auto;
}

.settings-panel {
  padding: 0 20px;
}

.setting-section {
  margin-bottom: 25px;
}

.setting-section h4 {
  margin-bottom: 10px;
  color: #333;
  font-size: 1rem;
}

.settings-btn {
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: 1000;
}

:deep(.el-tabs__content) {
  padding: 20px 0;
}

:deep(.el-tabs__item) {
  font-weight: 500;
}

@media (max-width: 768px) {
  .recommendations-page {
    padding: 15px;
  }
  
  .settings-btn {
    right: 15px;
    bottom: 15px;
  }
}
</style>