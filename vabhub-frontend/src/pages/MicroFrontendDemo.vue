<template>
  <div class="microfrontend-demo">
    <!-- 页面头部 -->
    <div class="demo-header">
      <h1>{{ $t('microfrontend.title') }}</h1>
      <p class="demo-description">
        {{ $t('microfrontend.demoDescription') }}
      </p>
    </div>

    <!-- 微前端架构说明 -->
    <div class="architecture-section">
      <h2>{{ $t('microfrontend.architecture') }}</h2>
      <div class="architecture-diagram">
        <div class="architecture-item">
          <div class="item-icon">🏠</div>
          <div class="item-content">
            <h3>{{ $t('microfrontend.hostApp') }}</h3>
            <p>{{ $t('microfrontend.hostAppDesc') }}</p>
          </div>
        </div>
        
        <div class="architecture-arrow">↓</div>
        
        <div class="architecture-item">
          <div class="item-icon">📊</div>
          <div class="item-content">
            <h3>{{ $t('microfrontend.mediaDashboard') }}</h3>
            <p>{{ $t('microfrontend.dashboardDesc') }}</p>
          </div>
        </div>
        
        <div class="architecture-arrow">↓</div>
        
        <div class="architecture-item">
          <div class="item-icon">🎵</div>
          <div class="item-content">
            <h3>{{ $t('microfrontend.musicPlayer') }}</h3>
            <p>{{ $t('microfrontend.playerDesc') }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 微前端模块演示 -->
    <div class="demo-section">
      <h2>{{ $t('microfrontend.liveDemo') }}</h2>
      <MicroFrontendExample />
    </div>

    <!-- 技术特性 -->
    <div class="features-section">
      <h2>{{ $t('microfrontend.features') }}</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🔌</div>
          <h3>{{ $t('microfrontend.feature1Title') }}</h3>
          <p>{{ $t('microfrontend.feature1Desc') }}</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">🌐</div>
          <h3>{{ $t('microfrontend.feature2Title') }}</h3>
          <p>{{ $t('microfrontend.feature2Desc') }}</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">🔄</div>
          <h3>{{ $t('microfrontend.feature3Title') }}</h3>
          <p>{{ $t('microfrontend.feature3Desc') }}</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">⚡</div>
          <h3>{{ $t('microfrontend.feature4Title') }}</h3>
          <p>{{ $t('microfrontend.feature4Desc') }}</p>
        </div>
      </div>
    </div>

    <!-- 使用说明 -->
    <div class="usage-section">
      <h2>{{ $t('microfrontend.usage') }}</h2>
      <div class="usage-steps">
        <div class="step">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3>{{ $t('microfrontend.step1Title') }}</h3>
            <p>{{ $t('microfrontend.step1Desc') }}</p>
          </div>
        </div>
        
        <div class="step">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3>{{ $t('microfrontend.step2Title') }}</h3>
            <p>{{ $t('microfrontend.step2Desc') }}</p>
          </div>
        </div>
        
        <div class="step">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3>{{ $t('microfrontend.step3Title') }}</h3>
            <p>{{ $t('microfrontend.step3Desc') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import MicroFrontendExample from '@/components/MicroFrontendExample.vue'

const { t } = useI18n()
</script>

<style scoped>
.microfrontend-demo {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.demo-header {
  text-align: center;
  margin-bottom: 40px;
}

.demo-header h1 {
  font-size: 2.5rem;
  color: #1976d2;
  margin-bottom: 10px;
}

.demo-description {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
}

.architecture-section {
  margin-bottom: 40px;
}

.architecture-section h2 {
  border-bottom: 2px solid #1976d2;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.architecture-diagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.architecture-item {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  width: 100%;
  max-width: 500px;
}

.item-icon {
  font-size: 2rem;
  margin-right: 15px;
}

.item-content h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.item-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.architecture-arrow {
  font-size: 1.5rem;
  color: #1976d2;
}

.demo-section {
  margin-bottom: 40px;
}

.demo-section h2 {
  border-bottom: 2px solid #28a745;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.features-section {
  margin-bottom: 40px;
}

.features-section h2 {
  border-bottom: 2px solid #ffc107;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.feature-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.feature-card h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.feature-card p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.usage-section {
  margin-bottom: 40px;
}

.usage-section h2 {
  border-bottom: 2px solid #dc3545;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.usage-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step {
  display: flex;
  align-items: flex-start;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
}

.step-number {
  background: #1976d2;
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  margin-right: 15px;
  flex-shrink: 0;
}

.step-content h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.step-content p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .microfrontend-demo {
    padding: 10px;
  }
  
  .demo-header h1 {
    font-size: 2rem;
  }
  
  .architecture-item {
    flex-direction: column;
    text-align: center;
  }
  
  .item-icon {
    margin-right: 0;
    margin-bottom: 10px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .step {
    flex-direction: column;
    text-align: center;
  }
  
  .step-number {
    margin-right: 0;
    margin-bottom: 10px;
  }
}
</style>