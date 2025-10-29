<template>
  <div class="charts-view">
    <div class="charts-header">
      <h2>排行榜数据</h2>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
        <el-button @click="triggerCollection" :loading="collecting">
          <el-icon><Collection /></el-icon>
          手动收集
        </el-button>
      </div>
    </div>

    <!-- 数据源筛选 -->
    <div class="filters">
      <el-select v-model="selectedSource" placeholder="选择数据源" clearable>
        <el-option
          v-for="source in availableSources"
          :key="source.id"
          :label="source.name"
          :value="source.id"
        />
      </el-select>
      
      <el-input
        v-model="searchQuery"
        placeholder="搜索歌曲/影视名称"
        style="width: 200px; margin-left: 10px;"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 统计信息 -->
    <div class="stats" v-if="stats">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ stats.total_records }}</div>
              <div class="stat-label">总记录数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="18">
          <el-card class="stat-card">
            <div class="source-stats">
              <div 
                v-for="(count, source) in stats.sources" 
                :key="source"
                class="source-stat"
              >
                <span class="source-name">{{ getSourceName(source) }}</span>
                <span class="source-count">{{ count }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 数据表格 -->
    <el-table
      :data="filteredData"
      v-loading="loading"
      style="width: 100%; margin-top: 20px;"
      :default-sort="{ prop: 'rank', order: 'ascending' }"
    >
      <el-table-column prop="rank" label="排名" width="80" sortable>
        <template #default="{ row }">
          <span class="rank-badge" :class="getRankClass(row.rank)">
            {{ row.rank }}
          </span>
        </template>
      </el-table-column>
      
      <el-table-column prop="source" label="数据源" width="120">
        <template #default="{ row }">
          <el-tag :type="getSourceTagType(row.source)">
            {{ getSourceName(row.source) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="title" label="标题" min-width="200">
        <template #default="{ row }">
          <div class="title-container">
            <div class="title">{{ row.title }}</div>
            <div class="artist" v-if="row.artist_or_show">
              {{ row.artist_or_show }}
            </div>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="metrics" label="数据指标" width="150">
        <template #default="{ row }">
          <div class="metrics">
            <div v-for="(value, key) in row.metrics" :key="key" class="metric">
              <span class="metric-label">{{ getMetricLabel(key) }}:</span>
              <span class="metric-value">{{ formatMetricValue(value) }}</span>
            </div>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="search_query" label="搜索关键词" width="200">
        <template #default="{ row }">
          <el-tooltip :content="row.search_query" placement="top">
            <span class="search-query">{{ row.search_query }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      
      <el-table-column prop="date_or_week" label="日期/周期" width="120" />
      
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button 
            type="primary" 
            link 
            @click="searchContent(row)"
            v-if="row.search_query"
          >
            搜索资源
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Collection, Search } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const collecting = ref(false)
const chartsData = ref([])
const availableSources = ref([])
const stats = ref(null)
const selectedSource = ref('')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 计算属性
const filteredData = computed(() => {
  let data = chartsData.value
  
  // 按数据源过滤
  if (selectedSource.value) {
    data = data.filter(item => item.source === selectedSource.value)
  }
  
  // 按搜索关键词过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    data = data.filter(item => 
      item.title.toLowerCase().includes(query) ||
      (item.artist_or_show && item.artist_or_show.toLowerCase().includes(query)) ||
      item.search_query.toLowerCase().includes(query)
    )
  }
  
  // 分页
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  
  return data.slice(start, end)
})

// 方法
const getSourceName = (source) => {
  const sourceMap = {
    'apple_music': 'Apple Music',
    'spotify_charts': 'Spotify',
    'netflix_top10': 'Netflix',
    'imdb_datasets': 'IMDb'
  }
  return sourceMap[source] || source
}

const getSourceTagType = (source) => {
  const typeMap = {
    'apple_music': 'success',
    'spotify_charts': 'warning',
    'netflix_top10': 'danger',
    'imdb_datasets': 'info'
  }
  return typeMap[source] || ''
}

const getRankClass = (rank) => {
  if (rank <= 3) return 'rank-top-3'
  if (rank <= 10) return 'rank-top-10'
  return 'rank-normal'
}

const getMetricLabel = (key) => {
  const labelMap = {
    'plays': '播放量',
    'streams': '流媒体数',
    'weekly_hours_viewed': '周观看时长',
    'avg_rating': '评分',
    'votes': '投票数'
  }
  return labelMap[key] || key
}

const formatMetricValue = (value) => {
  if (typeof value === 'number') {
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M'
    } else if (value >= 1000) {
      return (value / 1000).toFixed(1) + 'K'
    }
  }
  return value
}

const searchContent = (row) => {
  // 这里可以集成到搜索功能
  ElMessage.info(`搜索: ${row.search_query}`)
}

// API调用
const fetchChartsData = async () => {
  loading.value = true
  try {
    const response = await fetch(`/api/charts/data?limit=1000`)
    const result = await response.json()
    
    if (result.success) {
      chartsData.value = result.data
      total.value = result.total
    } else {
      ElMessage.error('获取数据失败')
    }
  } catch (error) {
    ElMessage.error('网络错误')
  } finally {
    loading.value = false
  }
}

const fetchAvailableSources = async () => {
  try {
    const response = await fetch('/api/charts/sources')
    const result = await response.json()
    
    if (result.success) {
      availableSources.value = result.sources
    }
  } catch (error) {
    console.error('获取数据源失败:', error)
  }
}

const fetchStats = async () => {
  try {
    const response = await fetch('/api/charts/stats')
    const result = await response.json()
    
    if (result.success) {
      stats.value = result.stats
    }
  } catch (error) {
    console.error('获取统计信息失败:', error)
  }
}

const triggerCollection = async () => {
  collecting.value = true
  try {
    const response = await fetch('/api/charts/collect', {
      method: 'POST'
    })
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success('数据收集任务已触发')
      // 等待一段时间后刷新数据
      setTimeout(() => {
        refreshData()
      }, 5000)
    } else {
      ElMessage.error('触发收集失败')
    }
  } catch (error) {
    ElMessage.error('网络错误')
  } finally {
    collecting.value = false
  }
}

const refreshData = () => {
  fetchChartsData()
  fetchStats()
}

const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
}

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage
}

// 生命周期
onMounted(() => {
  refreshData()
  fetchAvailableSources()
})
</script>

<style scoped>
.charts-view {
  padding: 20px;
}

.charts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filters {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.stats {
  margin-bottom: 20px;
}

.stat-card {
  height: 100px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  color: #909399;
  margin-top: 5px;
}

.source-stats {
  display: flex;
  justify-content: space-around;
}

.source-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.source-name {
  font-size: 12px;
  color: #909399;
}

.source-count {
  font-size: 18px;
  font-weight: bold;
  color: #67C23A;
}

.rank-badge {
  display: inline-block;
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  border-radius: 50%;
  font-weight: bold;
}

.rank-top-3 {
  background: #F56C6C;
  color: white;
}

.rank-top-10 {
  background: #E6A23C;
  color: white;
}

.rank-normal {
  background: #909399;
  color: white;
}

.title-container .title {
  font-weight: bold;
}

.title-container .artist {
  color: #909399;
  font-size: 12px;
}

.metrics .metric {
  font-size: 12px;
  margin-bottom: 2px;
}

.metric-label {
  color: #909399;
}

.metric-value {
  font-weight: bold;
  margin-left: 5px;
}

.search-query {
  display: inline-block;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}
</style>