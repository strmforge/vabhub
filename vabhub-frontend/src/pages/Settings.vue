<template>
  <div class="settings">
    <!-- 页面头部 -->
    <div class="settings-header">
      <h1 class="page-title">系统设置</h1>
      <div class="header-actions">
        <el-button @click="resetSettings">重置设置</el-button>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
      </div>
    </div>

    <!-- 设置内容 -->
    <div class="settings-content">
      <!-- 侧边栏导航 -->
      <div class="settings-sidebar">
        <el-menu
          :default-active="activeTab"
          class="settings-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="general">
            <el-icon><Setting /></el-icon>
            <span>常规设置</span>
          </el-menu-item>
          <el-menu-item index="appearance">
            <el-icon><Brush /></el-icon>
            <span>外观设置</span>
          </el-menu-item>
          <el-menu-item index="notifications">
            <el-icon><Bell /></el-icon>
            <span>通知设置</span>
          </el-menu-item>
          <el-menu-item index="storage">
            <el-icon><Folder /></el-icon>
            <span>存储设置</span>
          </el-menu-item>
          <el-menu-item index="plugins">
            <el-icon><Star /></el-icon>
            <span>插件设置</span>
          </el-menu-item>
          <el-menu-item index="security">
            <el-icon><Lock /></el-icon>
            <span>安全设置</span>
          </el-menu-item>
          <el-menu-item index="about">
            <el-icon><InfoFilled /></el-icon>
            <span>关于系统</span>
          </el-menu-item>
        </el-menu>
      </div>

      <!-- 设置面板 -->
      <div class="settings-panel">
        <!-- 常规设置 -->
        <div v-if="activeTab === 'general'" class="settings-section">
          <h2 class="section-title">常规设置</h2>
          
          <el-form :model="settings.general" label-width="120px">
            <el-form-item label="语言设置">
              <el-select v-model="settings.general.language" placeholder="请选择语言">
                <el-option label="简体中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="时区设置">
              <el-select v-model="settings.general.timezone" placeholder="请选择时区">
                <el-option label="北京时间 (UTC+8)" value="Asia/Shanghai" />
                <el-option label="协调世界时 (UTC)" value="UTC" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="自动保存">
              <el-switch v-model="settings.general.autoSave" />
              <span class="setting-description">启用后系统会自动保存您的设置</span>
            </el-form-item>
            
            <el-form-item label="启动时检查更新">
              <el-switch v-model="settings.general.checkUpdates" />
              <span class="setting-description">启动时自动检查系统更新</span>
            </el-form-item>
          </el-form>
        </div>

        <!-- 外观设置 -->
        <div v-if="activeTab === 'appearance'" class="settings-section">
          <h2 class="section-title">外观设置</h2>
          
          <el-form :model="settings.appearance" label-width="120px">
            <el-form-item label="主题模式">
              <el-radio-group v-model="settings.appearance.theme">
                <el-radio label="light">浅色主题</el-radio>
                <el-radio label="dark">深色主题</el-radio>
                <el-radio label="auto">跟随系统</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="主色调">
              <el-color-picker v-model="settings.appearance.primaryColor" />
              <span class="setting-description">选择系统的主色调</span>
            </el-form-item>
            
            <el-form-item label="字体大小">
              <el-slider
                v-model="settings.appearance.fontSize"
                :min="12"
                :max="18"
                :step="1"
                show-stops
              />
              <span class="setting-description">调整系统字体大小</span>
            </el-form-item>
            
            <el-form-item label="动画效果">
              <el-switch v-model="settings.appearance.animations" />
              <span class="setting-description">启用页面切换和交互动画</span>
            </el-form-item>
          </el-form>
        </div>

        <!-- 通知设置 -->
        <div v-if="activeTab === 'notifications'" class="settings-section">
          <h2 class="section-title">通知设置</h2>
          
          <el-form :model="settings.notifications" label-width="120px">
            <el-form-item label="启用通知">
              <el-switch v-model="settings.notifications.enabled" />
              <span class="setting-description">启用系统通知功能</span>
            </el-form-item>
            
            <el-form-item label="声音提醒">
              <el-switch v-model="settings.notifications.sound" />
              <span class="setting-description">播放通知声音</span>
            </el-form-item>
            
            <el-form-item label="桌面通知">
              <el-switch v-model="settings.notifications.desktop" />
              <span class="setting-description">显示桌面通知</span>
            </el-form-item>
            
            <el-form-item label="通知类型">
              <el-checkbox-group v-model="settings.notifications.types">
                <el-checkbox label="system">系统通知</el-checkbox>
                <el-checkbox label="media">媒体更新</el-checkbox>
                <el-checkbox label="plugin">插件通知</el-checkbox>
                <el-checkbox label="security">安全提醒</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-form>
        </div>

        <!-- 存储设置 -->
        <div v-if="activeTab === 'storage'" class="settings-section">
          <h2 class="section-title">存储设置</h2>
          
          <el-form :model="settings.storage" label-width="120px">
            <el-form-item label="媒体存储路径">
              <el-input v-model="settings.storage.mediaPath" placeholder="请输入媒体文件存储路径">
                <template #append>
                  <el-button @click="browseMediaPath">浏览</el-button>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="缓存大小限制">
              <el-input-number
                v-model="settings.storage.cacheSize"
                :min="100"
                :max="5000"
                :step="100"
              />
              <span class="setting-description">MB，设置系统缓存的最大大小</span>
            </el-form-item>
            
            <el-form-item label="自动清理缓存">
              <el-switch v-model="settings.storage.autoClean" />
              <span class="setting-description">定期自动清理过期缓存</span>
            </el-form-item>
            
            <el-form-item label="备份设置">
              <el-switch v-model="settings.storage.autoBackup" />
              <span class="setting-description">自动备份系统设置和数据</span>
            </el-form-item>
          </el-form>
        </div>

        <!-- 插件设置 -->
        <div v-if="activeTab === 'plugins'" class="settings-section">
          <h2 class="section-title">插件设置</h2>
          
          <el-form :model="settings.plugins" label-width="120px">
            <el-form-item label="自动更新插件">
              <el-switch v-model="settings.plugins.autoUpdate" />
              <span class="setting-description">自动检查并更新插件</span>
            </el-form-item>
            
            <el-form-item label="插件安装路径">
              <el-input v-model="settings.plugins.installPath" placeholder="请输入插件安装路径" />
            </el-form-item>
            
            <el-form-item label="启用沙盒模式">
              <el-switch v-model="settings.plugins.sandbox" />
              <span class="setting-description">在沙盒环境中运行插件，提高安全性</span>
            </el-form-item>
            
            <el-form-item label="插件权限">
              <el-checkbox-group v-model="settings.plugins.permissions">
                <el-checkbox label="file">文件访问</el-checkbox>
                <el-checkbox label="network">网络访问</el-checkbox>
                <el-checkbox label="system">系统调用</el-checkbox>
                <el-checkbox label="storage">存储访问</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-form>
        </div>

        <!-- 安全设置 -->
        <div v-if="activeTab === 'security'" class="settings-section">
          <h2 class="section-title">安全设置</h2>
          
          <el-form :model="settings.security" label-width="120px">
            <el-form-item label="自动登出时间">
              <el-select v-model="settings.security.autoLogout" placeholder="请选择自动登出时间">
                <el-option label="15分钟" value="15" />
                <el-option label="30分钟" value="30" />
                <el-option label="1小时" value="60" />
                <el-option label="永不" value="0" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="启用双因素认证">
              <el-switch v-model="settings.security.twoFactor" />
              <span class="setting-description">启用双因素认证提高账户安全性</span>
            </el-form-item>
            
            <el-form-item label="登录尝试限制">
              <el-input-number
                v-model="settings.security.loginAttempts"
                :min="3"
                :max="10"
                :step="1"
              />
              <span class="setting-description">次，达到限制后账户将被锁定</span>
            </el-form-item>
            
            <el-form-item label="安全日志保留">
              <el-select v-model="settings.security.logRetention" placeholder="请选择日志保留时间">
                <el-option label="7天" value="7" />
                <el-option label="30天" value="30" />
                <el-option label="90天" value="90" />
                <el-option label="永久" value="0" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>

        <!-- 关于系统 -->
        <div v-if="activeTab === 'about'" class="settings-section">
          <h2 class="section-title">关于系统</h2>
          
          <el-card class="about-card">
            <div class="about-content">
              <div class="app-info">
                <h3>VabHub</h3>
                <p>版本: {{ appInfo.version }}</p>
                <p>构建时间: {{ appInfo.buildTime }}</p>
                <p>许可证: {{ appInfo.license }}</p>
              </div>
              
              <div class="system-info">
                <h4>系统信息</h4>
                <p>运行环境: {{ appInfo.environment }}</p>
                <p>Node.js 版本: {{ appInfo.nodeVersion }}</p>
                <p>Vue 版本: {{ appInfo.vueVersion }}</p>
              </div>
              
              <div class="actions">
                <el-button type="primary" @click="checkForUpdates">检查更新</el-button>
                <el-button @click="viewLicense">查看许可证</el-button>
                <el-button @click="viewDocumentation">查看文档</el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading">
        <Loading />
      </el-icon>
      <span>加载中...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Setting, Brush, Bell, Folder, Star, Lock, InfoFilled, Loading
} from '@element-plus/icons-vue'
import ApiService from '@/services/api'

const activeTab = ref('general')
const loading = ref(false)

// 默认设置
const defaultSettings = {
  general: {
    language: 'zh-CN',
    timezone: 'Asia/Shanghai',
    autoSave: true,
    checkUpdates: true
  },
  appearance: {
    theme: 'auto',
    primaryColor: '#409EFF',
    fontSize: 14,
    animations: true
  },
  notifications: {
    enabled: true,
    sound: true,
    desktop: false,
    types: ['system', 'media', 'plugin', 'security']
  },
  storage: {
    mediaPath: '',
    cacheSize: 1000,
    autoClean: true,
    autoBackup: true
  },
  plugins: {
    autoUpdate: true,
    installPath: '',
    sandbox: true,
    permissions: ['file', 'network']
  },
  security: {
    autoLogout: '30',
    twoFactor: false,
    loginAttempts: 5,
    logRetention: '30'
  }
}

const settings = ref({ ...defaultSettings })
const appInfo = ref({
  version: '1.6.0',
  buildTime: '2024-01-01',
  license: 'MIT',
  environment: 'Production',
  nodeVersion: '18.0.0',
  vueVersion: '3.3.0'
})

// 菜单选择处理
const handleMenuSelect = (index: string) => {
  activeTab.value = index
}

// 保存设置
const saveSettings = async () => {
  loading.value = true
  try {
    await ApiService.settings.saveSettings(settings.value)
    ElMessage.success('设置保存成功')
  } catch (error) {
    ElMessage.error('设置保存失败')
    console.error('保存设置失败:', error)
  } finally {
    loading.value = false
  }
}

// 重置设置
const resetSettings = async () => {
  try {
    await ElMessageBox.confirm('确定要重置所有设置吗？此操作不可撤销。', '确认重置', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    settings.value = { ...defaultSettings }
    ElMessage.success('设置已重置')
  } catch (error) {
    // 用户取消操作
  }
}

// 浏览媒体路径
const browseMediaPath = () => {
  // 这里可以集成文件选择器
  console.log('浏览媒体路径')
}

// 检查更新
const checkForUpdates = async () => {
  try {
    const updateInfo = await ApiService.settings.checkForUpdates()
    if (updateInfo.available) {
      ElMessageBox.confirm(
        `发现新版本 ${updateInfo.latestVersion}，是否立即更新？`,
        '系统更新',
        {
          confirmButtonText: '立即更新',
          cancelButtonText: '稍后再说',
          type: 'info'
        }
      ).then(() => {
        // 执行更新操作
        console.log('开始更新系统')
      })
    } else {
      ElMessage.success('当前已是最新版本')
    }
  } catch (error) {
    ElMessage.error('检查更新失败')
  }
}

// 查看许可证
const viewLicense = () => {
  window.open('/license', '_blank')
}

// 查看文档
const viewDocumentation = () => {
  window.open('/docs', '_blank')
}

// 加载设置
const loadSettings = async () => {
  loading.value = true
  try {
    const savedSettings = await ApiService.settings.getSettings()
    if (savedSettings) {
      settings.value = { ...defaultSettings, ...savedSettings }
    }
  } catch (error) {
    console.error('加载设置失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped lang="scss">
.settings {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;

  .page-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin: 0;
  }
}

.settings-content {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 24px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.settings-sidebar {
  .settings-menu {
    border-right: none;

    .el-menu-item {
      height: 48px;
      line-height: 48px;
      margin-bottom: 4px;
      border-radius: 6px;

      &.is-active {
        background-color: var(--el-color-primary-light-9);
        color: var(--el-color-primary);
      }

      .el-icon {
        margin-right: 8px;
      }
    }
  }
}

.settings-panel {
  min-height: 600px;
}

.settings-section {
  .section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 24px;
    color: var(--el-text-color-primary);
  }

  .setting-description {
    font-size: 12px;
    color: var(--el-text-color-secondary);
    margin-left: 8px;
  }
}

.about-card {
  .about-content {
    .app-info {
      margin-bottom: 24px;

      h3 {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 12px;
        color: var(--el-text-color-primary);
      }

      p {
        margin-bottom: 8px;
        color: var(--el-text-color-regular);
      }
    }

    .system-info {
      margin-bottom: 24px;

      h4 {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 12px;
        color: var(--el-text-color-primary);
      }

      p {
        margin-bottom: 8px;
        color: var(--el-text-color-regular);
      }
    }

    .actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
  }
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}
</style>