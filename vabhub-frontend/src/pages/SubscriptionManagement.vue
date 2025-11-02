<template>
  <div class="subscription-management">
    <div class="page-header">
      <h1>订阅管理</h1>
      <p>自动化订阅系统，智能监控和下载符合条件的内容</p>
    </div>

    <div class="content">
      <!-- 订阅列表 -->
      <div class="subscription-list">
        <div class="section-header">
          <h2>订阅列表</h2>
          <button class="btn btn-primary" @click="showCreateModal = true">
            <i class="icon-add"></i> 新建订阅
          </button>
        </div>

        <div class="subscription-cards">
          <div v-for="subscription in subscriptions" :key="subscription.id" class="subscription-card">
            <div class="card-header">
              <h3>{{ subscription.name }}</h3>
              <div class="status-badge" :class="subscription.status">
                {{ getStatusText(subscription.status) }}
              </div>
            </div>
            
            <div class="card-content">
              <p class="query">{{ subscription.query }}</p>
              <div class="meta-info">
                <span class="priority">优先级: {{ subscription.priority }}</span>
                <span class="last-run">最后运行: {{ formatDate(subscription.lastRun) }}</span>
              </div>
              <div class="stats">
                <span class="stat">匹配: {{ subscription.matches }}</span>
                <span class="stat">下载: {{ subscription.downloads }}</span>
                <span class="stat">错误: {{ subscription.errors }}</span>
              </div>
            </div>
            
            <div class="card-actions">
              <button class="btn btn-sm" @click="editSubscription(subscription)">编辑</button>
              <button class="btn btn-sm" @click="toggleSubscription(subscription)">
                {{ subscription.enabled ? '暂停' : '启用' }}
              </button>
              <button class="btn btn-sm btn-danger" @click="deleteSubscription(subscription)">删除</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 创建订阅模态框 -->
      <div v-if="showCreateModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>{{ editingSubscription ? '编辑订阅' : '新建订阅' }}</h3>
            <button class="close-btn" @click="closeModal">×</button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="saveSubscription">
              <div class="form-group">
                <label>订阅名称</label>
                <input v-model="formData.name" type="text" required />
              </div>
              
              <div class="form-group">
                <label>查询条件</label>
                <textarea v-model="formData.query" placeholder="例如: movie AND year>=2024 AND rating>=8.0" required></textarea>
                <div class="help-text">
                  支持自然语言和高级查询语法
                </div>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label>优先级</label>
                  <select v-model="formData.priority">
                    <option value="1">低</option>
                    <option value="2">中</option>
                    <option value="3">高</option>
                  </select>
                </div>
                
                <div class="form-group">
                  <label>通知渠道</label>
                  <div class="checkbox-group">
                    <label><input type="checkbox" v-model="formData.channels" value="telegram" /> Telegram</label>
                    <label><input type="checkbox" v-model="formData.channels" value="email" /> 邮件</label>
                    <label><input type="checkbox" v-model="formData.channels" value="console" /> 控制台</label>
                  </div>
                </div>
              </div>
              
              <div class="form-group">
                <label>规则设置</label>
                <div class="rule-settings">
                  <div class="rule-item">
                    <label>质量要求</label>
                    <select v-model="formData.rules.quality">
                      <option value="any">任意</option>
                      <option value="720p">720p</option>
                      <option value="1080p">1080p</option>
                      <option value="4k">4K</option>
                    </select>
                  </div>
                  
                  <div class="rule-item">
                    <label>语言</label>
                    <select v-model="formData.rules.language">
                      <option value="any">任意</option>
                      <option value="zh-CN">简体中文</option>
                      <option value="en">英语</option>
                      <option value="ja">日语</option>
                    </select>
                  </div>
                  
                  <div class="rule-item">
                    <label>大小限制</label>
                    <input v-model="formData.rules.sizeLimit" type="text" placeholder="例如: 10GB" />
                  </div>
                </div>
              </div>
            </form>
          </div>
          
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">取消</button>
            <button class="btn btn-primary" @click="saveSubscription">保存</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'

export default {
  name: 'SubscriptionManagement',
  setup() {
    const subscriptions = ref([])
    const showCreateModal = ref(false)
    const editingSubscription = ref(null)
    
    const formData = reactive({
      name: '',
      query: '',
      priority: '2',
      channels: ['console'],
      rules: {
        quality: 'any',
        language: 'any',
        sizeLimit: ''
      },
      enabled: true
    })

    // 模拟数据
    const mockSubscriptions = [
      {
        id: '1',
        name: '热门电影订阅',
        query: 'movie AND year>=2024 AND rating>=8.0',
        priority: 2,
        status: 'active',
        enabled: true,
        lastRun: new Date(),
        matches: 15,
        downloads: 12,
        errors: 0
      },
      {
        id: '2',
        name: '科幻剧集订阅',
        query: 'tv AND genre="科幻" AND season>=1',
        priority: 1,
        status: 'paused',
        enabled: false,
        lastRun: new Date(Date.now() - 86400000),
        matches: 8,
        downloads: 6,
        errors: 1
      }
    ]

    onMounted(() => {
      // 模拟API调用
      subscriptions.value = mockSubscriptions
    })

    const getStatusText = (status) => {
      const statusMap = {
        active: '运行中',
        paused: '已暂停',
        error: '错误',
        completed: '已完成'
      }
      return statusMap[status] || status
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleString('zh-CN')
    }

    const editSubscription = (subscription) => {
      editingSubscription.value = subscription
      Object.assign(formData, subscription)
      showCreateModal.value = true
    }

    const toggleSubscription = async (subscription) => {
      // 模拟API调用
      subscription.enabled = !subscription.enabled
      subscription.status = subscription.enabled ? 'active' : 'paused'
    }

    const deleteSubscription = async (subscription) => {
      if (confirm('确定要删除这个订阅吗？')) {
        // 模拟API调用
        subscriptions.value = subscriptions.value.filter(s => s.id !== subscription.id)
      }
    }

    const closeModal = () => {
      showCreateModal.value = false
      editingSubscription.value = null
      resetForm()
    }

    const resetForm = () => {
      Object.assign(formData, {
        name: '',
        query: '',
        priority: '2',
        channels: ['console'],
        rules: {
          quality: 'any',
          language: 'any',
          sizeLimit: ''
        },
        enabled: true
      })
    }

    const saveSubscription = async () => {
      // 模拟API调用
      const subscriptionData = { ...formData }
      
      if (editingSubscription.value) {
        // 更新现有订阅
        const index = subscriptions.value.findIndex(s => s.id === editingSubscription.value.id)
        if (index !== -1) {
          subscriptions.value[index] = { ...editingSubscription.value, ...subscriptionData }
        }
      } else {
        // 创建新订阅
        const newSubscription = {
          id: Date.now().toString(),
          ...subscriptionData,
          status: 'active',
          lastRun: new Date(),
          matches: 0,
          downloads: 0,
          errors: 0
        }
        subscriptions.value.push(newSubscription)
      }
      
      closeModal()
    }

    return {
      subscriptions,
      showCreateModal,
      editingSubscription,
      formData,
      getStatusText,
      formatDate,
      editSubscription,
      toggleSubscription,
      deleteSubscription,
      closeModal,
      saveSubscription
    }
  }
}
</script>

<style scoped>
.subscription-management {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.subscription-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.subscription-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.active {
  background: #e8f5e8;
  color: #2e7d32;
}

.status-badge.paused {
  background: #fff3e0;
  color: #f57c00;
}

.status-badge.error {
  background: #ffebee;
  color: #c62828;
}

.query {
  color: #666;
  margin-bottom: 1rem;
  font-family: monospace;
}

.meta-info {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #888;
}

.stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat {
  font-size: 0.875rem;
  color: #666;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 表单样式 */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.help-text {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.25rem;
}

.checkbox-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
}

.rule-settings {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.rule-item label {
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

/* 按钮样式 */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #1976d2;
  color: white;
}

.btn-primary:hover {
  background: #1565c0;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-danger {
  background: #d32f2f;
  color: white;
}

.btn-danger:hover {
  background: #c62828;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
}
</style>