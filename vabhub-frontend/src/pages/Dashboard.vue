<template>
  <div class="dashboard">
    <!-- 页面头部 -->
    <div class="dashboard-header">
      <h1 class="page-title">{{ $t('dashboard.title') }}</h1>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          {{ $t('common.refresh') }}
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon size="24" color="#409EFF">
              <VideoCamera />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.mediaCount || 0 }}</div>
            <div class="stat-label">{{ $t('dashboard.movies') }}</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon size="24" color="#67C23A">
              <Collection />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.pluginCount || 0 }}</div>
            <div class="stat-label">{{ $t('plugins.title') }}</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon size="24" color="#E6A23C">
              <DataAnalysis />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ formatSize(stats.storageUsed || 0) }}</div>
            <div class="stat-label">{{ $t('dashboard.storageUsage') }}</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon size="24" color="#F56C6C">
              <Bell />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.unreadNotifications || 0 }}</div>
            <div class="stat-label">{{ $t('common.notifications') }}</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 主要内容区域 -->
    <div class="dashboard-content">
      <!-- 最近活动 -->
      <el-card class="recent-activities">
        <template #header>
          <div class="card-header">
            <span>{{ $t('dashboard.recentActivity') }}</span>
            <el-button text @click="viewAllActivities">{{ $t('common.viewAll') }}</el-button>
          </div>
        </template>
        <div class="activities-list">
          <div v-if="recentActivities.length === 0" class="empty-state">
            <el-empty :description="$t('common.noData')" />
          </div>
          <div v-else>
            <div 
              v-for="activity in recentActivities" 
              :key="activity.id"
              class="activity-item"
            >
              <div class="activity-icon">
                <el-icon :color="getActivityColor(activity.type)">
                  <component :is="getActivityIcon(activity.type)" />
                </el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 快速操作 -->
      <el-card class="quick-actions">
        <template #header>
          <span>{{ $t('dashboard.quickActions') }}</span>
        </template>
        <div class="actions-grid">
          <el-button class="action-btn" @click="navigateTo('discover')">
            <el-icon><Search /></el-icon>
            {{ $t('common.discover') }}
          </el-button>
          <el-button class="action-btn" @click="navigateTo('plugins')">
            <el-icon><Star /></el-icon>
            {{ $t('plugins.title') }}
          </el-button>
          <el-button class="action-btn" @click="navigateTo('storage')">
            <el-icon><Folder /></el-icon>
            {{ $t('common.storage') }}
          </el-button>
          <el-button class="action-btn" @click="navigateTo('settings')">
            <el-icon><Setting /></el-icon>
            {{ $t('settings.title') }}
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading">
        <Loading />
      </el-icon>
      <span>{{ $t('common.loading') }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { 
  Refresh, VideoCamera, Collection, DataAnalysis, Bell,
  Search, Star, Folder, Setting, Loading
} from '@element-plus/icons-vue'
import ApiService from '@/services/api'

const router = useRouter()
const { t } = useI18n()
const loading = ref(false)
const stats = ref({})
const recentActivities = ref([])

// 获取仪表板数据
const fetchDashboardData = async () => {
  loading.value = true
  try {
    const [statsData, activitiesData] = await Promise.all([
      ApiService.dashboard.getStats(),
      ApiService.dashboard.getRecentActivities(10)
    ])
    
    stats.value = statsData || {}
    recentActivities.value = (activitiesData || []).slice(0, 5) // 只显示最近5条
  } catch (error) {
    console.error('获取仪表板数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshData = () => {
  fetchDashboardData()
}

// 格式化文件大小
const formatSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化时间
const formatTime = (timestamp: string): string => {
  return new Date(timestamp).toLocaleString('zh-CN')
}

// 获取活动图标
const getActivityIcon = (type: string) => {
  const icons = {
    media: 'VideoCamera',
    plugin: 'Star',
    system: 'Setting',
    notification: 'Bell'
  }
  return icons[type] || 'Info'
}

// 获取活动颜色
const getActivityColor = (type: string) => {
  const colors = {
    media: '#409EFF',
    plugin: '#67C23A',
    system: '#E6A23C',
    notification: '#F56C6C'
  }
  return colors[type] || '#909399'
}

// 导航到页面
const navigateTo = (routeName: string) => {
  router.push({ name: routeName })
}

// 查看全部活动
const viewAllActivities = () => {
  // 这里可以跳转到活动日志页面
  console.log('查看全部活动')
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped lang="scss">
.dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  :deep(.el-card__body) {
    padding: 20px;
  }
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: var(--el-color-primary-light-9);
  border-radius: 8px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activities-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--el-border-color-light);

  &:last-child {
    border-bottom: none;
  }
}

.activity-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--el-color-primary-light-9);
  border-radius: 6px;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-btn {
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;

  .el-icon {
    font-size: 24px;
  }
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}
</style>