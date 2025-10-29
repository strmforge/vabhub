<template>
  <ModernLayout
    page-title="设置 - VabHub"
    page-description="个性化您的使用体验"
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
    <div class="modern-settings">
      <!-- 设置标题 -->
      <section class="modern-settings__header">
        <div class="modern-settings__header-container">
          <h1 class="modern-settings__title">设置</h1>
          <p class="modern-settings__description">
            个性化您的 VabHub 使用体验
          </p>
        </div>
      </section>

      <!-- 设置内容 -->
      <section class="modern-settings__content">
        <div class="modern-settings__content-container">
          <!-- 设置导航 -->
          <div class="modern-settings__navigation">
            <div 
              v-for="category in settingsCategories"
              :key="category.id"
              class="modern-settings__nav-item"
              :class="{ 'modern-settings__nav-item--active': activeCategory === category.id }"
              @click="setActiveCategory(category.id)"
            >
              <el-icon class="modern-settings__nav-icon">
                <component :is="category.icon" />
              </el-icon>
              <span class="modern-settings__nav-label">{{ category.label }}</span>
            </div>
          </div>

          <!-- 设置面板 -->
          <div class="modern-settings__panels">
            <!-- 外观设置 -->
            <div 
              v-if="activeCategory === 'appearance'" 
              class="modern-settings__panel"
            >
              <h2 class="modern-settings__panel-title">外观设置</h2>
              
              <div class="modern-settings__panel-content">
                <!-- 主题设置 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">主题</h3>
                  <div class="modern-settings__theme-options">
                    <div 
                      v-for="theme in themeOptions"
                      :key="theme.value"
                      class="modern-settings__theme-option"
                      :class="{ 'modern-settings__theme-option--active': currentTheme === theme.value }"
                      @click="setTheme(theme.value)"
                    >
                      <div class="modern-settings__theme-preview">
                        <div 
                          class="modern-settings__theme-sample"
                          :data-theme="theme.value"
                        >
                          <div class="modern-settings__theme-header"></div>
                          <div class="modern-settings__theme-content">
                            <div class="modern-settings__theme-card"></div>
                            <div class="modern-settings__theme-card"></div>
                          </div>
                        </div>
                      </div>
                      <span class="modern-settings__theme-label">{{ theme.label }}</span>
                    </div>
                  </div>
                </div>

                <!-- 布局设置 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">布局</h3>
                  <div class="modern-settings__layout-options">
                    <ModernButton
                      v-for="layout in layoutOptions"
                      :key="layout.value"
                      :variant="currentLayout === layout.value ? 'primary' : 'outline'"
                      size="small"
                      @click="setLayout(layout.value)"
                    >
                      {{ layout.label }}
                    </ModernButton>
                  </div>
                </div>

                <!-- 动画设置 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">动画效果</h3>
                  <div class="modern-settings__animation-controls">
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="enableAnimations"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">启用动画效果</span>
                      </label>
                    </div>
                    
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="reduceMotion"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">减少动画（无障碍）</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 账户设置 -->
            <div 
              v-if="activeCategory === 'account'" 
              class="modern-settings__panel"
            >
              <h2 class="modern-settings__panel-title">账户设置</h2>
              
              <div class="modern-settings__panel-content">
                <!-- 个人信息 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">个人信息</h3>
                  <div class="modern-settings__profile-form">
                    <div class="modern-settings__form-row">
                      <label class="modern-settings__form-label">用户名</label>
                      <ModernInput
                        v-model="userName"
                        placeholder="请输入用户名"
                        size="medium"
                      />
                    </div>
                    
                    <div class="modern-settings__form-row">
                      <label class="modern-settings__form-label">邮箱地址</label>
                      <ModernInput
                        v-model="userEmail"
                        type="email"
                        placeholder="请输入邮箱地址"
                        size="medium"
                      />
                    </div>
                    
                    <div class="modern-settings__form-row">
                      <label class="modern-settings__form-label">头像</label>
                      <div class="modern-settings__avatar-upload">
                        <div class="modern-settings__avatar-preview">
                          <img 
                            v-if="userAvatar" 
                            :src="userAvatar" 
                            alt="用户头像"
                          />
                          <el-icon v-else class="modern-settings__avatar-placeholder">
                            <User />
                          </el-icon>
                        </div>
                        <ModernButton
                          variant="outline"
                          size="small"
                          @click="handleAvatarUpload"
                        >
                          更换头像
                        </ModernButton>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 隐私设置 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">隐私设置</h3>
                  <div class="modern-settings__privacy-controls">
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="profilePublic"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">公开个人资料</span>
                      </label>
                    </div>
                    
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="emailNotifications"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">邮件通知</span>
                      </label>
                    </div>
                    
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="pushNotifications"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">推送通知</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 播放设置 -->
            <div 
              v-if="activeCategory === 'playback'" 
              class="modern-settings__panel"
            >
              <h2 class="modern-settings__panel-title">播放设置</h2>
              
              <div class="modern-settings__panel-content">
                <!-- 视频设置 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">视频播放</h3>
                  <div class="modern-settings__playback-controls">
                    <div class="modern-settings__slider-group">
                      <label class="modern-settings__slider-label">
                        默认播放质量
                        <span class="modern-settings__slider-value">{{ videoQuality }}p</span>
                      </label>
                      <input 
                        type="range" 
                        v-model="videoQuality"
                        min="360" 
                        max="2160" 
                        step="360"
                        class="modern-settings__slider"
                      />
                      <div class="modern-settings__slider-ticks">
                        <span>360p</span>
                        <span>720p</span>
                        <span>1080p</span>
                        <span>1440p</span>
                        <span>2160p</span>
                      </div>
                    </div>
                    
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="autoPlay"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">自动播放</span>
                      </label>
                    </div>
                    
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="subtitleEnabled"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">显示字幕</span>
                      </label>
                    </div>
                  </div>
                </div>

                <!-- 音频设置 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">音频播放</h3>
                  <div class="modern-settings__audio-controls">
                    <div class="modern-settings__slider-group">
                      <label class="modern-settings__slider-label">
                        音量
                        <span class="modern-settings__slider-value">{{ volume }}%</span>
                      </label>
                      <input 
                        type="range" 
                        v-model="volume"
                        min="0" 
                        max="100" 
                        step="5"
                        class="modern-settings__slider"
                      />
                    </div>
                    
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="crossfadeEnabled"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">启用淡入淡出</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 高级设置 -->
            <div 
              v-if="activeCategory === 'advanced'" 
              class="modern-settings__panel"
            >
              <h2 class="modern-settings__panel-title">高级设置</h2>
              
              <div class="modern-settings__panel-content">
                <!-- 缓存设置 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">缓存管理</h3>
                  <div class="modern-settings__cache-controls">
                    <div class="modern-settings__cache-info">
                      <span class="modern-settings__cache-label">缓存大小</span>
                      <span class="modern-settings__cache-value">{{ cacheSize }}</span>
                    </div>
                    <ModernButton
                      variant="outline"
                      size="small"
                      @click="clearCache"
                    >
                      清除缓存
                    </ModernButton>
                  </div>
                </div>

                <!-- 开发者选项 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">开发者选项</h3>
                  <div class="modern-settings__developer-controls">
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="developerMode"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">开发者模式</span>
                      </label>
                    </div>
                    
                    <div class="modern-settings__toggle-group">
                      <label class="modern-settings__toggle-label">
                        <input 
                          type="checkbox" 
                          v-model="debugLogs"
                          class="modern-settings__toggle-input"
                        />
                        <span class="modern-settings__toggle-slider"></span>
                        <span class="modern-settings__toggle-text">调试日志</span>
                      </label>
                    </div>
                  </div>
                </div>

                <!-- 重置设置 -->
                <div class="modern-settings__setting-group">
                  <h3 class="modern-settings__setting-title">重置选项</h3>
                  <div class="modern-settings__reset-controls">
                    <ModernButton
                      variant="danger"
                      size="small"
                      @click="resetSettings"
                    >
                      重置所有设置
                    </ModernButton>
                    <p class="modern-settings__reset-warning">
                      此操作将恢复所有设置为默认值，且不可撤销。
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 设置操作 -->
      <section class="modern-settings__actions">
        <div class="modern-settings__actions-container">
          <ModernButton
            variant="outline"
            @click="handleCancel"
          >
            取消
          </ModernButton>
          
          <ModernButton
            variant="primary"
            @click="handleSave"
            :loading="saving"
          >
            保存更改
          </ModernButton>
        </div>
      </section>
    </div>
  </ModernLayout>
</template>

<script>
import { ref, onMounted } from 'vue'
import ModernLayout from '@/components/ui/ModernLayout.vue'
import ModernInput from '@/components/ui/ModernInput.vue'
import ModernButton from '@/components/ui/ModernButton.vue'
import {
  Sunny,
  User,
  VideoCamera,
  Setting
} from '@element-plus/icons-vue'

export default {
  name: 'ModernSettings',
  components: {
    ModernLayout,
    ModernInput,
    ModernButton
  },
  setup() {
    // 用户状态
    const userLoggedIn = ref(true)
    const userAvatar = ref('')
    const userName = ref('现代用户')
    const userEmail = ref('user@example.com')
    
    // 设置状态
    const activeCategory = ref('appearance')
    const saving = ref(false)
    
    // 外观设置
    const currentTheme = ref('system')
    const currentLayout = ref('default')
    const enableAnimations = ref(true)
    const reduceMotion = ref(false)
    
    // 账户设置
    const profilePublic = ref(true)
    const emailNotifications = ref(true)
    const pushNotifications = ref(false)
    
    // 播放设置
    const videoQuality = ref(1080)
    const autoPlay = ref(true)
    const subtitleEnabled = ref(false)
    const volume = ref(80)
    const crossfadeEnabled = ref(true)
    
    // 高级设置
    const cacheSize = ref('256 MB')
    const developerMode = ref(false)
    const debugLogs = ref(false)
    
    // 设置分类
    const settingsCategories = [
      { id: 'appearance', label: '外观', icon: 'Sunny' },
      { id: 'account', label: '账户', icon: 'User' },
      { id: 'playback', label: '播放', icon: 'VideoCamera' },
      { id: 'advanced', label: '高级', icon: 'Setting' }
    ]
    
    // 主题选项
    const themeOptions = [
      { value: 'light', label: '浅色' },
      { value: 'dark', label: '深色' },
      { value: 'system', label: '系统' }
    ]
    
    // 布局选项
    const layoutOptions = [
      { value: 'default', label: '默认' },
      { value: 'compact', label: '紧凑' },
      { value: 'spacious', label: '宽松' }
    ]
    
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
    
    const setActiveCategory = (category) => {
      activeCategory.value = category
    }
    
    const setTheme = (theme) => {
      currentTheme.value = theme
      // 实际应用中这里会更新主题
      document.documentElement.setAttribute('data-theme', theme)
    }
    
    const setLayout = (layout) => {
      currentLayout.value = layout
    }
    
    const handleAvatarUpload = () => {
      console.log('上传头像')
    }
    
    const clearCache = () => {
      console.log('清除缓存')
    }
    
    const resetSettings = () => {
      if (confirm('确定要重置所有设置吗？此操作不可撤销。')) {
        console.log('重置设置')
      }
    }
    
    const handleCancel = () => {
      console.log('取消更改')
    }
    
    const handleSave = async () => {
      saving.value = true
      
      // 模拟保存操作
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      console.log('保存设置')
      saving.value = false
    }
    
    // 初始化设置
    onMounted(() => {
      // 从本地存储加载设置
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) {
        currentTheme.value = savedTheme
        setTheme(savedTheme)
      }
    })
    
    return {
      userLoggedIn,
      userAvatar,
      userName,
      userEmail,
      activeCategory,
      saving,
      currentTheme,
      currentLayout,
      enableAnimations,
      reduceMotion,
      profilePublic,
      emailNotifications,
      pushNotifications,
      videoQuality,
      autoPlay,
      subtitleEnabled,
      volume,
      crossfadeEnabled,
      cacheSize,
      developerMode,
      debugLogs,
      settingsCategories,
      themeOptions,
      layoutOptions,
      handleSearch,
      handleProfile,
      handleSettings,
      handleLogout,
      handleLogin,
      setActiveCategory,
      setTheme,
      setLayout,
      handleAvatarUpload,
      clearCache,
      resetSettings,
      handleCancel,
      handleSave
    }
  }
}
</script>

<style scoped>
.modern-settings {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 头部 */
.modern-settings__header {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  padding: var(--space-8) 0;
}

.modern-settings__header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-8);
}

.modern-settings__title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0 0 var(--space-2) 0;
}

.modern-settings__description {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin: 0;
}

/* 内容区域 */
.modern-settings__content {
  flex: 1;
  padding: var(--space-8) 0;
}

.modern-settings__content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-8);
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--space-8);
}

/* 导航 */
.modern-settings__navigation {
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
  height: fit-content;
  position: sticky;
  top: var(--space-8);
}

.modern-settings__nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-secondary);
}

.modern-settings__nav-item:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.modern-settings__nav-item--active {
  background: var(--primary-50);
  color: var(--primary-600);
  font-weight: var(--font-weight-medium);
}

.modern-settings__nav-icon {
  font-size: 1.25rem;
}

.modern-settings__nav-label {
  font-size: var(--font-size-sm);
}

/* 设置面板 */
.modern-settings__panels {
  min-height: 600px;
}

.modern-settings__panel {
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.modern-settings__panel-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0 0 var(--space-6) 0;
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-primary);
}

.modern-settings__panel-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

/* 设置组 */
.modern-settings__setting-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.modern-settings__setting-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin: 0;
}

/* 主题选项 */
.modern-settings__theme-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--space-4);
}

.modern-settings__theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  border: 2px solid var(--border-primary);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
}

.modern-settings__theme-option:hover {
  border-color: var(--primary-300);
}

.modern-settings__theme-option--active {
  border-color: var(--primary-600);
  background: var(--primary-50);
}

.modern-settings__theme-preview {
  width: 100%;
  height: 80px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border-primary);
}

.modern-settings__theme-sample {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.modern-settings__theme-sample[data-theme="light"] {
  background: #ffffff;
}

.modern-settings__theme-sample[data-theme="dark"] {
  background: #1f2937;
}

.modern-settings__theme-sample[data-theme="system"] {
  background: linear-gradient(135deg, #ffffff 50%, #1f2937 50%);
}

.modern-settings__theme-header {
  height: 20px;
  background: var(--primary-500);
}

.modern-settings__theme-content {
  flex: 1;
  padding: var(--space-2);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.modern-settings__theme-card {
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
}

.modern-settings__theme-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

/* 布局选项 */
.modern-settings__layout-options {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}

/* 表单控件 */
.modern-settings__form-row {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-width: 400px;
}

.modern-settings__form-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.modern-settings__avatar-upload {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.modern-settings__avatar-preview {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.modern-settings__avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modern-settings__avatar-placeholder {
  font-size: 2rem;
  color: var(--text-tertiary);
}

/* 切换开关 */
.modern-settings__toggle-group {
  display: flex;
  align-items: center;
}

.modern-settings__toggle-label {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  padding: var(--space-2) 0;
}

.modern-settings__toggle-input {
  display: none;
}

.modern-settings__toggle-slider {
  width: 44px;
  height: 24px;
  background: var(--bg-tertiary);
  border-radius: 12px;
  position: relative;
  transition: all 0.3s ease;
}

.modern-settings__toggle-slider::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.modern-settings__toggle-input:checked + .modern-settings__toggle-slider {
  background: var(--primary-600);
}

.modern-settings__toggle-input:checked + .modern-settings__toggle-slider::before {
  transform: translateX(20px);
}

.modern-settings__toggle-text {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
}

/* 滑块控件 */
.modern-settings__slider-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-width: 400px;
}

.modern-settings__slider-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-size-sm);
  color: var(--text-primary);
}

.modern-settings__slider-value {
  font-weight: var(--font-weight-medium);
  color: var(--primary-600);
}

.modern-settings__slider {
  width: 100%;
  height: 6px;
  background: var(--bg-tertiary);
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
}

.modern-settings__slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: var(--primary-600);
  border-radius: 50%;
  cursor: pointer;
}

.modern-settings__slider-ticks {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

/* 缓存管理 */
.modern-settings__cache-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 400px;
}

.modern-settings__cache-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.modern-settings__cache-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.modern-settings__cache-value {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

/* 重置警告 */
.modern-settings__reset-warning {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin: var(--space-2) 0 0 0;
}

/* 操作区域 */
.modern-settings__actions {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-primary);
  padding: var(--space-6) 0;
  margin-top: auto;
}

.modern-settings__actions-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-8);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-settings__content-container {
    grid-template-columns: 1fr;
    gap: var(--space-6);
  }
  
  .modern-settings__navigation {
    position: static;
  }
  
  .modern-settings__theme-options {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }
  
  .modern-settings__cache-controls {
    flex-direction: column;
    gap: var(--space-4);
    align-items: flex-start;
  }
  
  .modern-settings__actions-container {
    justify-content: center;
  }
}

/* 深色主题适配 */
[data-theme="dark"] .modern-settings__header {
  background: rgba(17, 24, 39, 0.8);
  border-bottom-color: var(--border-secondary);
}

[data-theme="dark"] .modern-settings__nav-item--active {
  background: rgba(59, 130, 246, 0.2);
}

[data-theme="dark"] .modern-settings__theme-sample[data-theme="light"] {
  background: #374151;
}

[data-theme="dark"] .modern-settings__theme-sample[data-theme="dark"] {
  background: #111827;
}

[data-theme="dark"] .modern-settings__theme-sample[data-theme="system"] {
  background: linear-gradient(135deg, #374151 50%, #111827 50%);
}
</style>