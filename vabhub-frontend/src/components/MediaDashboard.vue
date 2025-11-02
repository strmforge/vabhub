<template>
  <div class="media-dashboard">
    <!-- 仪表板头部 -->
    <div class="dashboard-header">
      <h2>{{ $t('dashboard.title') }}</h2>
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
          <div class="stat-icon">🎬</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.movies }}</div>
            <div class="stat-label">{{ $t('dashboard.movies') }}</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon">📺</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.tvShows }}</div>
            <div class="stat-label">{{ $t('dashboard.tvShows') }}</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon">🎵</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.music }}</div>
            <div class="stat-label">{{ $t('dashboard.music') }}</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon">📚</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.books }}</div>
            <div class="stat-label">{{ $t('dashboard.books') }}</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <span>{{ $t('dashboard.mediaDistribution') }}</span>
            </template>
            <div class="chart-container">
              <apexchart
                type="pie"
                height="300"
                :options="pieChartOptions"
                :series="pieChartSeries"
              />
            </div>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <span>{{ $t('dashboard.storageUsage') }}</span>
            </template>
            <div class="chart-container">
              <apexchart
                type="bar"
                height="300"
                :options="barChartOptions"
                :series="barChartSeries"
              />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 最近活动 -->
    <div class="recent-activity">
      <el-card>
        <template #header>
          <span>{{ $t('dashboard.recentActivity') }}</span>
        </template>
        <el-timeline>
          <el-timeline-item
            v-for="activity in recentActivities"
            :key="activity.id"
            :timestamp="activity.timestamp"
            :type="activity.type"
          >
            <div class="activity-item">
              <div class="activity-icon">{{ activity.icon }}</div>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-description">{{ activity.description }}</div>
              </div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Refresh } from '@element-plus/icons-vue'

const { t } = useI18n()

// 统计数据
const stats = ref({
  movies: 0,
  tvShows: 0,
  music: 0,
  books: 0
})

// 饼图数据
const pieChartSeries = ref([44, 55, 13, 43])
const pieChartOptions = computed(() => ({
  chart: {
    type: 'pie',
    height: 300
  },
  labels: [
    t('dashboard.movies'),
    t('dashboard.tvShows'),
    t('dashboard.music'),
    t('dashboard.books')
  ],
  colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560'],
  legend: {
    position: 'bottom'
  }
}))

// 柱状图数据
const barChartSeries = ref([{
  name: t('dashboard.storageUsage'),
  data: [30, 40, 35, 50]
}])
const barChartOptions = computed(() => ({
  chart: {
    type: 'bar',
    height: 300
  },
  plotOptions: {
    bar: {
      borderRadius: 4,
      horizontal: false
    }
  },
  dataLabels: {
    enabled: false
  },
  xaxis: {
    categories: [
      t('dashboard.movies'),
      t('dashboard.tvShows'),
      t('dashboard.music'),
      t('dashboard.books')
    ]
  }
}))

// 最近活动
const recentActivities = ref([
  {
    id: 1,
    icon: '🎬',
    title: t('dashboard.activity.movieAdded'),
    description: 'The Matrix (1999)',
    timestamp: '2 小时前',
    type: 'primary'
  },
  {
    id: 2,
    icon: '📺',
    title: t('dashboard.activity.tvShowUpdated'),
    description: 'Breaking Bad S03E05',
    timestamp: '4 小时前',
    type: 'success'
  },
  {
    id: 3,
    icon: '🎵',
    title: t('dashboard.activity.musicDownloaded'),
    description: 'Album: Random Access Memories',
    timestamp: '1 天前',
    type: 'warning'
  }
])

// 刷新数据
const refreshData = async () => {
  // 模拟数据加载
  stats.value = {
    movies: Math.floor(Math.random() * 1000) + 500,
    tvShows: Math.floor(Math.random() * 500) + 200,
    music: Math.floor(Math.random() * 2000) + 1000,
    books: Math.floor(Math.random() * 300) + 100
  }
}

onMounted(() => {
  refreshData()
})

// 暴露给微前端使用
defineExpose({
  refreshData,
  stats
})
</script>

<style scoped>
.media-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h2 {
  margin: 0;
  color: var(--el-text-color-primary);
  font-size: 24px;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  font-size: 48px;
  margin-right: 20px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: var(--el-color-primary);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.charts-section {
  margin-bottom: 30px;
}

.chart-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chart-container {
  padding: 10px;
}

.recent-activity {
  margin-bottom: 30px;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.activity-icon {
  font-size: 24px;
  margin-right: 15px;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  margin-bottom: 5px;
  color: var(--el-text-color-primary);
}

.activity-description {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

@media (max-width: 768px) {
  .media-dashboard {
    padding: 10px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-section .el-col {
    margin-bottom: 20px;
  }
}
</style>