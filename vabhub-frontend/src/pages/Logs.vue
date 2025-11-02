<template>
  <div class="logs-page">
    <div class="page-header">
      <h1>实时日志</h1>
      <p>监控系统运行状态和调试信息</p>
    </div>
    
    <div class="logs-content">
      <!-- 日志控制面板 -->
      <div class="logs-controls">
        <div class="control-group">
          <label for="logLevel">日志级别:</label>
          <select id="logLevel" v-model="selectedLevel" class="form-select">
            <option value="all">全部</option>
            <option value="debug">调试</option>
            <option value="info">信息</option>
            <option value="warning">警告</option>
            <option value="error">错误</option>
          </select>
        </div>
        
        <div class="control-group">
          <label for="logSource">日志来源:</label>
          <select id="logSource" v-model="selectedSource" class="form-select">
            <option value="all">全部</option>
            <option value="system">系统</option>
            <option value="plugins">插件</option>
            <option value="api">API</option>
            <option value="database">数据库</option>
          </select>
        </div>
        
        <div class="control-group">
          <label for="searchLogs">搜索:</label>
          <input 
            id="searchLogs"
            v-model="searchQuery" 
            type="text" 
            placeholder="搜索日志内容..." 
            class="search-input"
          />
        </div>
        
        <div class="control-actions">
          <button 
            class="btn btn-secondary" 
            @click="clearLogs"
            :disabled="logs.length === 0"
          >
            <span class="btn-icon">🗑️</span>
            清空日志
          </button>
          <button 
            class="btn btn-primary" 
            @click="exportLogs"
            :disabled="logs.length === 0"
          >
            <span class="btn-icon">📥</span>
            导出日志
          </button>
          <button 
            class="btn" 
            :class="{ 'btn-success': autoRefresh, 'btn-secondary': !autoRefresh }"
            @click="toggleAutoRefresh"
          >
            <span class="btn-icon">{{ autoRefresh ? '⏸️' : '▶️' }}</span>
            {{ autoRefresh ? '暂停' : '开始' }}自动刷新
          </button>
        </div>
      </div>
      
      <!-- 日志统计 -->
      <div class="logs-stats">
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <h3>总日志数</h3>
            <p class="stat-value">{{ totalLogs }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">⚠️</div>
          <div class="stat-info">
            <h3>警告</h3>
            <p class="stat-value">{{ warningCount }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">❌</div>
          <div class="stat-info">
            <h3>错误</h3>
            <p class="stat-value">{{ errorCount }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🔄</div>
          <div class="stat-info">
            <h3>最后更新</h3>
            <p class="stat-value">{{ lastUpdate }}</p>
          </div>
        </div>
      </div>
      
      <!-- 日志列表 -->
      <div class="logs-container">
        <div class="logs-header">
          <div class="header-item time">时间</div>
          <div class="header-item level">级别</div>
          <div class="header-item source">来源</div>
          <div class="header-item message">消息</div>
        </div>
        
        <div class="logs-list" ref="logsList">
          <div 
            v-for="log in filteredLogs" 
            :key="log.id"
            class="log-entry"
            :class="log.level"
            @click="selectLog(log)"
            :title="log.message"
          >
            <div class="log-time">{{ formatTime(log.timestamp) }}</div>
            <div class="log-level">
              <span class="level-badge" :class="log.level">
                {{ getLevelText(log.level) }}
              </span>
            </div>
            <div class="log-source">{{ log.source }}</div>
            <div class="log-message">{{ log.message }}</div>
          </div>
          
          <div v-if="filteredLogs.length === 0" class="no-logs">
            <div class="no-logs-icon">📝</div>
            <h3>暂无日志</h3>
            <p>系统运行日志将在这里显示</p>
          </div>
        </div>
      </div>
      
      <!-- 日志详情模态框 -->
      <div v-if="selectedLog" class="modal-overlay" @click="selectedLog = null">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>日志详情</h2>
            <button @click="selectedLog = null" class="close-btn">×</button>
          </div>
          
          <div class="modal-body">
            <div class="log-detail">
              <div class="detail-row">
                <label>时间:</label>
                <span>{{ formatTime(selectedLog.timestamp, true) }}</span>
              </div>
              <div class="detail-row">
                <label>级别:</label>
                <span class="level-badge" :class="selectedLog.level">
                  {{ getLevelText(selectedLog.level) }}
                </span>
              </div>
              <div class="detail-row">
                <label>来源:</label>
                <span>{{ selectedLog.source }}</span>
              </div>
              <div class="detail-row">
                <label>消息:</label>
                <pre class="log-message-detail">{{ selectedLog.message }}</pre>
              </div>
              <div v-if="selectedLog.details" class="detail-row">
                <label>详情:</label>
                <pre class="log-details">{{ selectedLog.details }}</pre>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button @click="copyLog(selectedLog)" class="btn btn-secondary">
              复制日志
            </button>
            <button @click="selectedLog = null" class="btn btn-primary">
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Logs',
  data() {
    return {
      selectedLevel: 'all',
      selectedSource: 'all',
      searchQuery: '',
      autoRefresh: true,
      selectedLog: null,
      logs: [],
      refreshInterval: null,
      logIdCounter: 1
    }
  },
  computed: {
    filteredLogs() {
      return this.logs.filter(log => {
        // 按级别过滤
        if (this.selectedLevel !== 'all' && log.level !== this.selectedLevel) {
          return false
        }
        
        // 按来源过滤
        if (this.selectedSource !== 'all' && log.source !== this.selectedSource) {
          return false
        }
        
        // 按搜索内容过滤
        if (this.searchQuery && !log.message.toLowerCase().includes(this.searchQuery.toLowerCase())) {
          return false
        }
        
        return true
      })
    },
    
    totalLogs() {
      return this.logs.length
    },
    
    warningCount() {
      return this.logs.filter(log => log.level === 'warning').length
    },
    
    errorCount() {
      return this.logs.filter(log => log.level === 'error').length
    },
    
    lastUpdate() {
      if (this.logs.length === 0) return '暂无数据'
      const lastLog = this.logs[this.logs.length - 1]
      return this.formatTime(lastLog.timestamp)
    }
  },
  mounted() {
    this.startAutoRefresh()
    this.generateSampleLogs()
  },
  
  beforeUnmount() {
    this.stopAutoRefresh()
  },
  
  methods: {
    startAutoRefresh() {
      if (this.autoRefresh) {
        this.refreshInterval = setInterval(() => {
          this.generateSampleLogs()
        }, 3000) // 每3秒生成一条新日志
      }
    },
    
    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
      }
    },
    
    toggleAutoRefresh() {
      this.autoRefresh = !this.autoRefresh
      
      if (this.autoRefresh) {
        this.startAutoRefresh()
      } else {
        this.stopAutoRefresh()
      }
    },
    
    generateSampleLogs() {
      const levels = ['debug', 'info', 'warning', 'error']
      const sources = ['system', 'plugins', 'api', 'database']
      const messages = [
        '系统启动完成',
        '插件管理器初始化成功',
        '数据库连接已建立',
        'API服务正在监听端口 8000',
        '检测到新的媒体文件',
        '刮削器任务开始执行',
        '下载任务已完成',
        '存储空间使用率超过80%',
        '网络连接异常',
        '插件加载失败'
      ]
      
      const level = levels[Math.floor(Math.random() * levels.length)]
      const source = sources[Math.floor(Math.random() * sources.length)]
      const message = messages[Math.floor(Math.random() * messages.length)]
      
      this.addLog({
        level,
        source,
        message,
        timestamp: new Date(),
        details: level === 'error' ? '错误堆栈信息...' : null
      })
    },
    
    addLog(logData) {
      const log = {
        id: this.logIdCounter++,
        ...logData
      }
      
      this.logs.push(log)
      
      // 限制日志数量，避免内存泄漏
      if (this.logs.length > 1000) {
        this.logs = this.logs.slice(-500)
      }
      
      // 自动滚动到底部
      this.$nextTick(() => {
        const container = this.$refs.logsList
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    },
    
    clearLogs() {
      if (confirm('确定要清空所有日志吗？')) {
        this.logs = []
        this.showNotification('日志已清空', 'success')
      }
    },
    
    exportLogs() {
      const logText = this.logs.map(log => 
        `[${this.formatTime(log.timestamp, true)}] [${log.level.toUpperCase()}] [${log.source}] ${log.message}`
      ).join('\n')
      
      const blob = new Blob([logText], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `vabhub-logs-${new Date().toISOString().split('T')[0]}.txt`
      a.click()
      URL.revokeObjectURL(url)
      
      this.showNotification('日志导出成功', 'success')
    },
    
    selectLog(log) {
      this.selectedLog = log
    },
    
    copyLog(log) {
      const logText = `[${this.formatTime(log.timestamp, true)}] [${log.level.toUpperCase()}] [${log.source}] ${log.message}`
      
      navigator.clipboard.writeText(logText).then(() => {
        this.showNotification('日志已复制到剪贴板', 'success')
      }).catch(() => {
        this.showNotification('复制失败', 'error')
      })
    },
    
    formatTime(timestamp, full = false) {
      const date = new Date(timestamp)
      
      if (full) {
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        })
      }
      
      const now = new Date()
      const diff = now - date
      
      if (diff < 60000) { // 1分钟内
        return '刚刚'
      } else if (diff < 3600000) { // 1小时内
        return `${Math.floor(diff / 60000)}分钟前`
      } else if (diff < 86400000) { // 1天内
        return `${Math.floor(diff / 3600000)}小时前`
      } else {
        return date.toLocaleDateString('zh-CN')
      }
    },
    
    getLevelText(level) {
      const levelMap = {
        debug: '调试',
        info: '信息',
        warning: '警告',
        error: '错误'
      }
      
      return levelMap[level] || level
    },
    
    showNotification(message, type) {
      console.log(`[${type}] ${message}`)
    }
  }
}
</script>

<style scoped>
.logs-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.page-header p {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.logs-controls {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  align-items: end;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.control-group label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.875rem;
}

.form-select, .search-input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  width: 100%;
}

.control-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.logs-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2rem;
  opacity: 0.8;
}

.stat-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  color: #7f8c8d;
  font-weight: 500;
}

.stat-value {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.logs-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.logs-header {
  display: grid;
  grid-template-columns: 120px 100px 120px 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-weight: 600;
  color: #2c3e50;
}

.logs-list {
  max-height: 600px;
  overflow-y: auto;
}

.log-entry {
  display: grid;
  grid-template-columns: 120px 100px 120px 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f1f3f4;
  cursor: pointer;
  transition: background 0.3s;
}

.log-entry:hover {
  background: #f8f9fa;
}

.log-entry:last-child {
  border-bottom: none;
}

.log-entry.debug {
  border-left: 4px solid #6c757d;
}

.log-entry.info {
  border-left: 4px solid #17a2b8;
}

.log-entry.warning {
  border-left: 4px solid #ffc107;
}

.log-entry.error {
  border-left: 4px solid #dc3545;
}

.log-time {
  font-size: 0.875rem;
  color: #6c757d;
}

.level-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.level-badge.debug {
  background: #6c757d;
  color: white;
}

.level-badge.info {
  background: #17a2b8;
  color: white;
}

.level-badge.warning {
  background: #ffc107;
  color: #212529;
}

.level-badge.error {
  background: #dc3545;
  color: white;
}

.log-source {
  font-size: 0.875rem;
  color: #495057;
}

.log-message {
  font-size: 0.875rem;
  color: #2c3e50;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-logs {
  text-align: center;
  padding: 3rem 2rem;
  color: #6c757d;
}

.no-logs-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-logs h3 {
  margin: 0 0 0.5rem 0;
  color: #495057;
}

.no-logs p {
  margin: 0;
}

/* 模态框样式 */
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

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 2rem;
  max-height: 60vh;
  overflow-y: auto;
}

.log-detail {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: 1rem;
  align-items: start;
}

.detail-row label {
  font-weight: 600;
  color: #2c3e50;
}

.log-message-detail, .log-details {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background 0.3s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
}

.btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-icon {
  margin-right: 0.5rem;
}

@media (max-width: 768px) {
  .logs-page {
    padding: 1rem;
  }
  
  .logs-controls {
    grid-template-columns: 1fr;
  }
  
  .logs-stats {
    grid-template-columns: 1fr;
  }
  
  .logs-header, .log-entry {
    grid-template-columns: 80px 80px 80px 1fr;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
  }
  
  .control-actions {
    justify-content: center;
  }
  
  .detail-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}
</style>