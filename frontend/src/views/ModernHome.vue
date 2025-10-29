<template>
  <ModernLayout
    page-title="VabHub - 现代化媒体管理平台"
    page-description="探索、管理和分享您的媒体内容"
    :user-logged-in="userLoggedIn"
    :user-avatar="userAvatar"
    :user-name="userName"
    :user-email="userEmail"
    @search="handleSearch"
    @profile="handleProfile"
    @settings="handleSettings"
    @logout="handleLogout"
    @login="handleLogin"
  >
    <!-- 页面内容 -->
    <div class="modern-home">
      <!-- 英雄区域 -->
      <section class="modern-home__hero">
        <div class="modern-home__hero-content">
          <h1 class="modern-home__hero-title">
            现代化媒体管理体验
          </h1>
          <p class="modern-home__hero-description">
            使用最新的UI设计语言和交互技术，为您提供流畅、直观的媒体管理体验
          </p>
          
          <!-- 主题切换演示 -->
          <div class="modern-home__theme-demo">
            <ThemeToggle 
              variant="default" 
              size="large"
              class="modern-home__theme-toggle"
            />
            <span class="modern-home__theme-text">点击切换主题体验</span>
          </div>
          
          <!-- 主要操作按钮 -->
          <div class="modern-home__hero-actions">
            <ModernButton
              variant="primary"
              size="large"
              icon="Plus"
              @click="handleUpload"
            >
              上传媒体
            </ModernButton>
            
            <ModernButton
              variant="outline"
              size="large"
              icon="Compass"
              @click="handleDiscover"
            >
              探索内容
            </ModernButton>
          </div>
        </div>
        
        <!-- 背景装饰 -->
        <div class="modern-home__hero-background">
          <div class="modern-home__hero-gradient"></div>
        </div>
      </section>

      <!-- 特性展示 -->
      <section class="modern-home__features">
        <div class="modern-home__features-container">
          <h2 class="modern-home__features-title">核心特性</h2>
          
          <div class="modern-home__features-grid">
            <!-- 响应式设计 -->
            <ModernCard
              class="modern-home__feature-card"
              :hover-effect="true"
              :border-effect="true"
            >
              <template #icon>
                <el-icon class="modern-home__feature-icon">
                  <Monitor />
                </el-icon>
              </template>
              
              <template #title>
                完全响应式设计
              </template>
              
              <template #content>
                <p>适配各种屏幕尺寸，从桌面到移动设备都能完美呈现</p>
              </template>
              
              <template #actions>
                <ModernButton variant="text" size="small">
                  了解更多
                </ModernButton>
              </template>
            </ModernCard>

            <!-- 主题切换 -->
            <ModernCard
              class="modern-home__feature-card"
              :hover-effect="true"
              :border-effect="true"
            >
              <template #icon>
                <el-icon class="modern-home__feature-icon">
                  <Sunny />
                </el-icon>
              </template>
              
              <template #title>
                智能主题切换
              </template>
              
              <template #content>
                <p>支持亮色/深色主题，自动适配系统偏好设置</p>
              </template>
              
              <template #actions>
                <ModernButton variant="text" size="small">
                  体验主题
                </ModernButton>
              </template>
            </ModernCard>

            <!-- 交互反馈 -->
            <ModernCard
              class="modern-home__feature-card"
              :hover-effect="true"
              :border-effect="true"
            >
              <template #icon>
                <el-icon class="modern-home__feature-icon">
                  <Magic />
                </el-icon>
              </template>
              
              <template #title>
                丰富交互反馈
              </template>
              
              <template #content>
                <p>微动画、悬停效果、点击反馈，提升用户体验</p>
              </template>
              
              <template #actions>
                <ModernButton variant="text" size="small">
                  查看演示
                </ModernButton>
              </template>
            </ModernCard>

            <!-- 无障碍访问 -->
            <ModernCard
              class="modern-home__feature-card"
              :hover-effect="true"
              :border-effect="true"
            >
              <template #icon>
                <el-icon class="modern-home__feature-icon">
                  <Accessibility />
                </el-icon>
              </template>
              
              <template #title>
                无障碍访问支持
              </template>
              
              <template #content>
                <p>遵循WCAG标准，确保所有用户都能顺畅使用</p>
              </template>
              
              <template #actions>
                <ModernButton variant="text" size="small">
                  了解详情
                </ModernButton>
              </template>
            </ModernCard>
          </div>
        </div>
      </section>

      <!-- 交互演示区域 -->
      <section class="modern-home__demo">
        <div class="modern-home__demo-container">
          <h2 class="modern-home__demo-title">交互效果演示</h2>
          
          <div class="modern-home__demo-grid">
            <!-- 加载状态演示 -->
            <div class="modern-home__demo-item">
              <h3>加载状态</h3>
              <div class="modern-home__demo-content">
                <LoadingSpinner
                  :loading="loadingDemo"
                  type="spinner"
                  size="medium"
                  message="模拟加载中..."
                />
                <ModernButton
                  variant="outline"
                  size="small"
                  @click="toggleLoadingDemo"
                >
                  {{ loadingDemo ? '停止加载' : '开始加载' }}
                </ModernButton>
              </div>
            </div>

            <!-- 交互反馈演示 -->
            <div class="modern-home__demo-item">
              <h3>交互反馈</h3>
              <div class="modern-home__demo-content">
                <InteractiveFeedback
                  enable-hover
                  enable-click
                  hover-effect="scale"
                  click-effect="ripple"
                  @hover="handleDemoHover"
                  @click="handleDemoClick"
                >
                  <template #hover>
                    <div class="modern-home__demo-feedback">
                      <el-icon><HandPointer /></el-icon>
                      <span>悬停效果</span>
                    </div>
                  </template>
                  
                  <template #click>
                    <button class="modern-home__demo-button">
                      <el-icon><Mouse /></el-icon>
                      <span>点击效果</span>
                    </button>
                  </template>
                </InteractiveFeedback>
              </div>
            </div>

            <!-- 错误处理演示 -->
            <div class="modern-home__demo-item">
              <h3>错误边界</h3>
              <div class="modern-home__demo-content">
                <ErrorBoundary
                  :show-details="true"
                  @error="handleDemoError"
                  @retry="handleDemoRetry"
                >
                  <div class="modern-home__error-demo">
                    <p>这是一个安全的组件容器</p>
                    <ModernButton
                      variant="danger"
                      size="small"
                      @click="triggerError"
                    >
                      触发错误
                    </ModernButton>
                  </div>
                </ErrorBoundary>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 性能指标 -->
      <section class="modern-home__metrics">
        <div class="modern-home__metrics-container">
          <h2 class="modern-home__metrics-title">性能表现</h2>
          
          <div class="modern-home__metrics-grid">
            <div class="modern-home__metric">
              <div class="modern-home__metric-value">98%</div>
              <div class="modern-home__metric-label">用户满意度</div>
            </div>
            
            <div class="modern-home__metric">
              <div class="modern-home__metric-value">0.5s</div>
              <div class="modern-home__metric-label">平均加载时间</div>
            </div>
            
            <div class="modern-home__metric">
              <div class="modern-home__metric-value">99.9%</div>
              <div class="modern-home__metric-label">系统可用性</div>
            </div>
            
            <div class="modern-home__metric">
              <div class="modern-home__metric-value">A+</div>
              <div class="modern-home__metric-label">无障碍评级</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </ModernLayout>
</template>

<script>
import { ref } from 'vue'
import ModernLayout from '@/components/ui/ModernLayout.vue'
import ModernButton from '@/components/ui/ModernButton.vue'
import ModernCard from '@/components/ui/ModernCard.vue'
import ThemeToggle from '@/components/ui/ThemeToggle.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import InteractiveFeedback from '@/components/ui/InteractiveFeedback.vue'
import ErrorBoundary from '@/components/ui/ErrorBoundary.vue'
import {
  Monitor,
  Sunny,
  Magic,
  Accessibility,
  Plus,
  Compass,
  HandPointer,
  Mouse
} from '@element-plus/icons-vue'

export default {
  name: 'ModernHome',
  components: {
    ModernLayout,
    ModernButton,
    ModernCard,
    ThemeToggle,
    LoadingSpinner,
    InteractiveFeedback,
    ErrorBoundary,
    Monitor,
    Sunny,
    Magic,
    Accessibility,
    Plus,
    Compass,
    HandPointer,
    Mouse
  },
  setup() {
    // 用户状态
    const userLoggedIn = ref(true)
    const userAvatar = ref('')
    const userName = ref('现代用户')
    const userEmail = ref('user@example.com')
    
    // 演示状态
    const loadingDemo = ref(false)
    
    // 事件处理
    const handleSearch = () => {
      console.log('搜索功能触发')
    }
    
    const handleProfile = () => {
      console.log('查看个人资料')
    }
    
    const handleSettings = () => {
      console.log('打开设置')
    }
    
    const handleLogout = () => {
      userLoggedIn.value = false
      console.log('用户登出')
    }
    
    const handleLogin = () => {
      userLoggedIn.value = true
      console.log('用户登录')
    }
    
    const handleUpload = () => {
      console.log('上传媒体')
    }
    
    const handleDiscover = () => {
      console.log('探索内容')
    }
    
    const toggleLoadingDemo = () => {
      loadingDemo.value = !loadingDemo.value
      
      if (loadingDemo.value) {
        setTimeout(() => {
          loadingDemo.value = false
        }, 3000)
      }
    }
    
    const handleDemoHover = (event) => {
      console.log('悬停事件:', event)
    }
    
    const handleDemoClick = (event) => {
      console.log('点击事件:', event)
    }
    
    const handleDemoError = (error) => {
      console.log('错误捕获:', error)
    }
    
    const handleDemoRetry = () => {
      console.log('重试操作')
    }
    
    const triggerError = () => {
      throw new Error('这是演示用的错误信息')
    }
    
    return {
      userLoggedIn,
      userAvatar,
      userName,
      userEmail,
      loadingDemo,
      handleSearch,
      handleProfile,
      handleSettings,
      handleLogout,
      handleLogin,
      handleUpload,
      handleDiscover,
      toggleLoadingDemo,
      handleDemoHover,
      handleDemoClick,
      handleDemoError,
      handleDemoRetry,
      triggerError
    }
  }
}
</script>

<style scoped>
.modern-home {
  min-height: 100vh;
}

/* 英雄区域 */
.modern-home__hero {
  position: relative;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-50), var(--primary-100));
  overflow: hidden;
}

.modern-home__hero-content {
  text-align: center;
  max-width: 800px;
  padding: var(--space-8);
  z-index: 2;
  position: relative;
}

.modern-home__hero-title {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-4);
  background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.modern-home__hero-description {
  font-size: var(--font-size-xl);
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: var(--space-8);
}

.modern-home__theme-demo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  margin-bottom: var(--space-8);
  padding: var(--space-4);
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  backdrop-filter: blur(10px);
}

.modern-home__theme-text {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.modern-home__hero-actions {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
  flex-wrap: wrap;
}

.modern-home__hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.modern-home__hero-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
}

/* 特性区域 */
.modern-home__features {
  padding: var(--space-16) var(--space-8);
  background: var(--bg-primary);
}

.modern-home__features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.modern-home__features-title {
  text-align: center;
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-12);
}

.modern-home__features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-6);
}

.modern-home__feature-card {
  height: 100%;
}

.modern-home__feature-icon {
  font-size: 2.5rem;
  color: var(--primary-600);
  margin-bottom: var(--space-4);
}

/* 演示区域 */
.modern-home__demo {
  padding: var(--space-16) var(--space-8);
  background: var(--bg-secondary);
}

.modern-home__demo-container {
  max-width: 1200px;
  margin: 0 auto;
}

.modern-home__demo-title {
  text-align: center;
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-12);
}

.modern-home__demo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-8);
}

.modern-home__demo-item {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  border: 1px solid var(--border-primary);
}

.modern-home__demo-item h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

.modern-home__demo-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  align-items: center;
}

.modern-home__demo-feedback {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
}

.modern-home__demo-button {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--primary-600);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  cursor: pointer;
  font-weight: var(--font-weight-medium);
}

.modern-home__error-demo {
  text-align: center;
}

/* 性能指标区域 */
.modern-home__metrics {
  padding: var(--space-16) var(--space-8);
  background: var(--bg-primary);
}

.modern-home__metrics-container {
  max-width: 1200px;
  margin: 0 auto;
}

.modern-home__metrics-title {
  text-align: center;
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-12);
}

.modern-home__metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-8);
}

.modern-home__metric {
  text-align: center;
  padding: var(--space-6);
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-primary);
}

.modern-home__metric-value {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  color: var(--primary-600);
  margin-bottom: var(--space-2);
}

.modern-home__metric-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-home__hero-title {
    font-size: var(--font-size-3xl);
  }
  
  .modern-home__hero-description {
    font-size: var(--font-size-lg);
  }
  
  .modern-home__theme-demo {
    flex-direction: column;
    gap: var(--space-2);
  }
  
  .modern-home__hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .modern-home__features-grid,
  .modern-home__demo-grid,
  .modern-home__metrics-grid {
    grid-template-columns: 1fr;
  }
}

/* 深色主题适配 */
[data-theme="dark"] .modern-home__hero {
  background: linear-gradient(135deg, var(--primary-900), var(--primary-800));
}

[data-theme="dark"] .modern-home__theme-demo {
  background: rgba(17, 24, 39, 0.8);
}

[data-theme="dark"] .modern-home__demo-item,
[data-theme="dark"] .modern-home__metric {
  background: rgba(17, 24, 39, 0.8);
  border-color: var(--border-secondary);
}
</style>