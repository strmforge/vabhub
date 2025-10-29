<template>
  <div class="music-subscription">
    <!-- 头部区域 -->
    <div class="header">
      <h2>音乐订阅管理</h2>
      <div class="actions">
        <button @click="refreshSubscriptions" class="btn btn-primary">
          <i class="icon-refresh"></i> 刷新
        </button>
        <button @click="showAddSubscription" class="btn btn-success">
          <i class="icon-plus"></i> 添加订阅
        </button>
        <button @click="generateFromCharts" class="btn btn-info">
          <i class="icon-chart"></i> 从榜单生成
        </button>
      </div>
    </div>

    <!-- 订阅列表 -->
    <div class="subscription-list">
      <div v-for="subscription in subscriptions" :key="subscription.id" class="subscription-item">
        <div class="subscription-header">
          <h3>{{ subscription.name }}</h3>
          <div class="subscription-status">
            <span :class="['status-badge', subscription.status]">{{ subscription.status }}</span>
            <span class="last-run">最后运行: {{ formatTime(subscription.lastRun) }}</span>
          </div>
        </div>
        
        <div class="subscription-details">
          <div class="detail-item">
            <label>查询:</label>
            <span>{{ subscription.query }}</span>
          </div>
          <div class="detail-item">
            <label>模式:</label>
            <span>{{ subscription.mode }}</span>
          </div>
          <div class="detail-item">
            <label>结果数量:</label>
            <span>{{ subscription.resultCount }}</span>
          </div>
        </div>

        <div class="subscription-actions">
          <button @click="runSubscription(subscription.id)" class="btn btn-sm btn-primary">
            立即运行
          </button>
          <button @click="editSubscription(subscription.id)" class="btn btn-sm btn-secondary">
            编辑
          </button>
          <button @click="deleteSubscription(subscription.id)" class="btn btn-sm btn-danger">
            删除
          </button>
        </div>

        <!-- 结果预览 -->
        <div v-if="subscription.results && subscription.results.length > 0" class="results-preview">
          <h4>最新结果 ({{ subscription.results.length }})</h4>
          <div class="result-items">
            <div v-for="result in subscription.results.slice(0, 3)" :key="result.id" class="result-item">
              <div class="result-title">{{ result.title }}</div>
              <div class="result-meta">
                <span class="seeders">{{ result.seeders }} 做种</span>
                <span class="size">{{ formatSize(result.size) }}</span>
                <span class="score">评分: {{ result.score }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑订阅模态框 -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑订阅' : '添加订阅' }}</h3>
          <button @click="closeModal" class="btn-close">×</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="saveSubscription">
            <div class="form-group">
              <label>订阅名称</label>
              <input v-model="currentSubscription.name" type="text" required>
            </div>
            
            <div class="form-group">
              <label>查询关键词</label>
              <input v-model="currentSubscription.query" type="text" required>
            </div>
            
            <div class="form-group">
              <label>订阅模式</label>
              <select v-model="currentSubscription.mode">
                <option value="torznab">Torznab</option>
                <option value="rss">RSS</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>端点URL</label>
              <input v-model="currentSubscription.endpoint" type="text" required>
            </div>
            
            <div class="form-group">
              <label>规则配置</label>
              <div class="rules-config">
                <div class="rule-item">
                  <label>包含关键词:</label>
                  <input v-model="currentSubscription.rules.includeKeywords" type="text" placeholder="FLAC,WEB,ALAC">
                </div>
                <div class="rule-item">
                  <label>排除关键词:</label>
                  <input v-model="currentSubscription.rules.excludeKeywords" type="text" placeholder="Pack,合集">
                </div>
                <div class="rule-item">
                  <label>质量要求:</label>
                  <input v-model="currentSubscription.rules.requireQuality" type="text" placeholder="FLAC,ALAC">
                </div>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">保存</button>
              <button type="button" @click="closeModal" class="btn btn-secondary">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 榜单生成模态框 -->
    <div v-if="showChartsModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>从榜单生成订阅</h3>
          <button @click="closeChartsModal" class="btn-close">×</button>
        </div>
        
        <div class="modal-body">
          <div class="charts-config">
            <div class="form-group">
              <label>榜单数据文件</label>
              <input v-model="chartsConfig.dataFile" type="text" placeholder="/path/to/charts.jsonl">
            </div>
            
            <div class="form-group">
              <label>生成订阅数量</label>
              <input v-model="chartsConfig.topArtists" type="number" min="1" max="100" value="50">
            </div>
            
            <div class="form-group">
              <label>数据源</label>
              <div class="source-checkboxes">
                <label><input v-model="chartsConfig.sources" type="checkbox" value="apple_music"> Apple Music</label>
                <label><input v-model="chartsConfig.sources" type="checkbox" value="spotify"> Spotify</label>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button @click="generateSubscriptions" class="btn btn-primary">生成订阅</button>
            <button @click="closeChartsModal" class="btn btn-secondary">取消</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { musicSubscriptionApi } from '../api/musicSubscription'

export default {
  name: 'MusicSubscription',
  setup() {
    const subscriptions = ref([])
    const showModal = ref(false)
    const showChartsModal = ref(false)
    const isEditing = ref(false)
    const currentSubscription = ref({
      id: null,
      name: '',
      query: '',
      mode: 'torznab',
      endpoint: '',
      rules: {
        includeKeywords: '',
        excludeKeywords: '',
        requireQuality: ''
      }
    })
    
    const chartsConfig = ref({
      dataFile: '',
      topArtists: 50,
      sources: ['apple_music', 'spotify']
    })

    // 加载订阅列表
    const loadSubscriptions = async () => {
      try {
        const response = await musicSubscriptionApi.getSubscriptions()
        subscriptions.value = response.data
      } catch (error) {
        console.error('加载订阅失败:', error)
      }
    }

    // 刷新订阅
    const refreshSubscriptions = () => {
      loadSubscriptions()
    }

    // 显示添加订阅模态框
    const showAddSubscription = () => {
      currentSubscription.value = {
        id: null,
        name: '',
        query: '',
        mode: 'torznab',
        endpoint: '',
        rules: {
          includeKeywords: '',
          excludeKeywords: '',
          requireQuality: ''
        }
      }
      isEditing.value = false
      showModal.value = true
    }

    // 编辑订阅
    const editSubscription = (id) => {
      const subscription = subscriptions.value.find(s => s.id === id)
      if (subscription) {
        currentSubscription.value = { ...subscription }
        isEditing.value = true
        showModal.value = true
      }
    }

    // 删除订阅
    const deleteSubscription = async (id) => {
      if (confirm('确定要删除这个订阅吗？')) {
        try {
          await musicSubscriptionApi.deleteSubscription(id)
          await loadSubscriptions()
        } catch (error) {
          console.error('删除订阅失败:', error)
        }
      }
    }

    // 运行订阅
    const runSubscription = async (id) => {
      try {
        await musicSubscriptionApi.runSubscription(id)
        // 可以添加成功提示
      } catch (error) {
        console.error('运行订阅失败:', error)
      }
    }

    // 保存订阅
    const saveSubscription = async () => {
      try {
        if (isEditing.value) {
          await musicSubscriptionApi.updateSubscription(currentSubscription.value)
        } else {
          await musicSubscriptionApi.createSubscription(currentSubscription.value)
        }
        
        await loadSubscriptions()
        closeModal()
      } catch (error) {
        console.error('保存订阅失败:', error)
      }
    }

    // 关闭模态框
    const closeModal = () => {
      showModal.value = false
    }

    // 显示榜单生成模态框
    const generateFromCharts = () => {
      showChartsModal.value = true
    }

    // 关闭榜单生成模态框
    const closeChartsModal = () => {
      showChartsModal.value = false
    }

    // 生成订阅
    const generateSubscriptions = async () => {
      try {
        await musicSubscriptionApi.generateFromCharts(chartsConfig.value)
        await loadSubscriptions()
        closeChartsModal()
      } catch (error) {
        console.error('生成订阅失败:', error)
      }
    }

    // 格式化时间
    const formatTime = (timestamp) => {
      if (!timestamp) return '从未运行'
      return new Date(timestamp).toLocaleString('zh-CN')
    }

    // 格式化文件大小
    const formatSize = (bytes) => {
      if (!bytes) return '未知'
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(1024))
      return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
    }

    onMounted(() => {
      loadSubscriptions()
    })

    return {
      subscriptions,
      showModal,
      showChartsModal,
      isEditing,
      currentSubscription,
      chartsConfig,
      
      refreshSubscriptions,
      showAddSubscription,
      editSubscription,
      deleteSubscription,
      runSubscription,
      saveSubscription,
      closeModal,
      generateFromCharts,
      closeChartsModal,
      generateSubscriptions,
      formatTime,
      formatSize
    }
  }
}
</script>

<style scoped>
.music-subscription {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.actions {
  display: flex;
  gap: 10px;
}

.subscription-list {
  display: grid;
  gap: 20px;
}

.subscription-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: #fff;
}

.subscription-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.running {
  background: #d4edda;
  color: #155724;
}

.status-badge.stopped {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.subscription-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item label {
  font-weight: bold;
  color: #666;
  font-size: 12px;
}

.subscription-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.results-preview {
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.result-items {
  display: grid;
  gap: 10px;
}

.result-item {
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

.result-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.result-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #666;
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
}

.modal {
  background: #fff;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.rules-config {
  display: grid;
  gap: 10px;
}

.rule-item {
  display: flex;
  flex-direction: column;
}

.source-checkboxes {
  display: flex;
  gap: 15px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-primary {
  background: #007bff;
  color: #fff;
}

.btn-secondary {
  background: #6c757d;
  color: #fff;
}

.btn-success {
  background: #28a745;
  color: #fff;
}

.btn-danger {
  background: #dc3545;
  color: #fff;
}

.btn-info {
  background: #17a2b8;
  color: #fff;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}
</style>