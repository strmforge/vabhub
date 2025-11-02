<template>
  <div class="log-center">
    <div class="log-header">
      <h2>实时日志中心</h2>
      <p>监控系统、插件和下载器的实时日志</p>
    </div>

    <!-- 日志控制面板 -->
    <div class="log-controls">
      <div class="control-group">
        <label class="form-label">日志级别:</label>
        <select v-model="logLevel" class="form-select" @change="updateLogFilter">
          <option value="all">全部</option>
          <option value="info">信息</option>
          <option value="warning">警告</option>
          <option value="error">错误</option>
          <option value="debug">调试</option>
        </select>
      </div>
      
      <div class="control-group">
        <label class="form-label">日志来源:</label>
        <select v-model="logSource" class="form-select" @change="updateLogFilter">
          <option value="all">全部来源</option>
          <option value="system">系统</option>
          <option value="plugins">插件</option>
          <option value="downloaders">下载器</option>
          <option value="api">API</option>
        </select>
      </div>
      
      <div class="control-group">
        <label class="form-label">自动滚动:</label>
        <label class="switch">
          <input type="checkbox" v-model="autoScroll">
          <span class="slider"></span>
        </label>
      </div>
      
      <div class="control-group">
        <button class="btn btn-secondary" @click="clearLogs">
          🗑️ 清空日志
        </button>
        <button class="btn btn-primary" @click="toggleWebSocket">
          {{ isConnected ? '🔴 断开连接' : '🟢 连接' }}
        </button>
      </div>
    </div>

    <!-- 日志统计 -->
    <div class="log-stats">
      <div class="stat-item">
        <span class="stat-label">总日志数:</span>
        <span class="stat-value">{{ totalLogs }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">错误:</span>
        <span class="stat-value error">{{ errorCount }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">警告:</span>
        <span class="stat-value warning">{{ warningCount }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">信息:</span>
        <span class="stat-value info">{{ infoCount }}</span>
      </div>
    </div>

    <!-- 日志显示区域 -->
    <div class="log-container" ref="logContainer">
      <div 
        v-for="log in filteredLogs" 
        :key="log.id" 
        class="log-entry"
        :class="getLogLevelClass(log.level)"
      >
        <div class="log-timestamp">
          {{ formatTimestamp(log.timestamp) }}
        </div>
        <div class="log-source">
          <span class="source-badge">{{ log.source }}</span>
        </div>
        <div class="log-message">
          {{ log.message }}
        </div>
        <div class="log-level">
          <span class="level-badge" :class="getLevelBadgeClass(log.level)">
            {{ log.level.toUpperCase() }}
          </span>
        </div>
      </div>
      
      <!-- 连接状态指示器 -->
      <div v-if="!isConnected" class="connection-status">
        <div class="status-indicator disconnected"></div>
        <span>WebSocket 未连接</span>
      </div>
      <div v-else class="connection-status">
        <div class="status-indicator connected"></div>
        <span>WebSocket 已连接</span>
      </div>
    </div>

    <!-- 日志搜索 -->
    <div class="log-search">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="搜索日志内容..." 
        class="search-input"
        @input="updateLogFilter"
      >
      <button class="btn btn-secondary" @click="exportLogs">
        📥 导出日志
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LogCenter',
  data() {
    return {
      logs: [],
      logLevel: 'all',
      logSource: 'all',
      searchQuery: '',
      autoScroll: true,
      isConnected: false,
      websocket: null,
      totalLogs: 0,
      errorCount: 0,
      warningCount: 0,
      infoCount: 0,
      debugCount: 0
    }
  },
  computed: {
    filteredLogs() {
      return this.logs.filter(log => {
        const matchesLevel = this.logLevel === 'all' || log.level === this.logLevel
        const matchesSource = this.logSource === 'all' || log.source === this.logSource
        const matchesSearch = this.searchQuery === '' || 
                            log.message.toLowerCase().includes(this.searchQuery.toLowerCase())
        
        return matchesLevel && matchesSource && matchesSearch
      })
    }
  },
  watch: {
    filteredLogs() {
      if (this.autoScroll) {
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    }
  },
  mounted() {
    // 初始化一些示例日志
    this.initializeSampleLogs()
    // 连接WebSocket
    this.connectWebSocket()
  },
  beforeUnmount() {
    if (this.websocket) {
      this.websocket.close()
    }
  },
  methods: {
    initializeSampleLogs() {
      const sampleLogs = [
        {
          id: 1,
          timestamp: new Date(),
          level: 'info',
          source: 'system',
          message: 'VabHub 系统启动成功'
        },
        {
          id: 2,
          timestamp: new Date(Date.now() - 1000),
          level: 'info',
          source: 'plugins',
          message: '插件管理器初始化完成'
        },
        {
          id: 3,
          timestamp: new Date(Date.now() - 2000),
          level: 'warning',
          source: 'downloaders',
          message: '下载器连接超时，正在重试...'
        },
        {
          id: 4,
          timestamp: new Date(Date.now() - 3000),
          level: 'error',
          source: 'api',
          message: 'API 请求失败: 连接被拒绝'
        }
      ]
      
      this.logs = sampleLogs
      this.updateStats()
    },
    
    connectWebSocket() {
      try {
        // 连接到实际的WebSocket端点
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const host = window.location.hostname || 'localhost'
        const port = window.location.port || '8000'
        const wsUrl = `${protocol}//${host}:${port}/ws/logs`
        
        this.websocket = new WebSocket(wsUrl)
        
        this.websocket.onopen = () => {
          this.isConnected = true
          this.addLog('info', 'system', 'WebSocket 连接成功')
          console.log('WebSocket connected to', wsUrl)
        }
        
        this.websocket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            if (data.type === 'log') {
              this.addLog(data.level, data.source, data.message, {
                id: data.id,
                timestamp: new Date(data.timestamp)
              })
            }
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error)
          }
        }
        
        this.websocket.onclose = () => {
          this.isConnected = false
          this.addLog('warning', 'system', 'WebSocket 连接已断开')
          console.log('WebSocket disconnected')
        }
        
        this.websocket.onerror = (error) => {
          console.error('WebSocket error:', error)
          this.addLog('error', 'system', `WebSocket 连接错误: ${error.message || '未知错误'}`)
        }
        
      } catch (error) {
        console.error('WebSocket连接失败:', error)
        this.addLog('error', 'system', `WebSocket连接失败: ${error.message}`)
        
        // 如果WebSocket连接失败，回退到模拟模式
        setTimeout(() => {
          this.isConnected = true
          this.addLog('info', 'system', 'WebSocket 连接失败，使用模拟模式')
          this.startLogSimulation()
        }, 1000)
      }
    },
    
    startLogSimulation() {
      // 模拟实时日志推送
      setInterval(() => {
        const sources = ['system', 'plugins', 'downloaders', 'api']
        const levels = ['info', 'warning', 'error', 'debug']
        const messages = [
          '插件执行完成',
          '下载任务开始',
          '媒体文件处理中',
          'API请求处理',
          '缓存更新完成',
          '数据库查询执行'
        ]
        
        const randomSource = sources[Math.floor(Math.random() * sources.length)]
        const randomLevel = levels[Math.floor(Math.random() * levels.length)]
        const randomMessage = messages[Math.floor(Math.random() * messages.length)]
        
        this.addLog(randomLevel, randomSource, randomMessage)
      }, 3000)
    },
    
    addLog(level, source, message, options = {}) {
      const log = {
        id: options.id || Date.now(),
        timestamp: options.timestamp || new Date(),
        level,
        source,
        message
      }
      
      this.logs.unshift(log) // 新日志添加到顶部
      this.updateStats()
      
      // 限制日志数量，避免内存问题
      if (this.logs.length > 1000) {
        this.logs = this.logs.slice(0, 1000)
      }
    },
    
    updateStats() {
      this.totalLogs = this.logs.length
      this.errorCount = this.logs.filter(log => log.level === 'error').length
      this.warningCount = this.logs.filter(log => log.level === 'warning').length
      this.infoCount = this.logs.filter(log => log.level === 'info').length
      this.debugCount = this.logs.filter(log => log.level === 'debug').length
    },
    
    updateLogFilter() {
      // 过滤逻辑已经在computed属性中处理
    },
    
    clearLogs() {
      this.logs = []
      this.updateStats()
      this.addLog('info', 'system', '日志已清空')
    },
    
    toggleWebSocket() {
      if (this.isConnected) {
        this.disconnectWebSocket()
      } else {
        this.connectWebSocket()
      }
    },
    
    disconnectWebSocket() {
      if (this.websocket) {
        this.websocket.close()
      }
      this.isConnected = false
      this.addLog('info', 'system', 'WebSocket 连接已断开')
    },
    
    scrollToBottom() {
      const container = this.$refs.logContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    
    getLogLevelClass(level) {
      return `log-level-${level}`
    },
    
    getLevelBadgeClass(level) {
      return `badge-${level}`
    },
    
    formatTimestamp(timestamp) {
      return new Date(timestamp).toLocaleTimeString('zh-CN', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    },
    
    exportLogs() {
      const logText = this.logs.map(log => 
        `[${this.formatTimestamp(log.timestamp)}] [${log.source}] [${log.level.toUpperCase()}] ${log.message}`
      ).join('\n')
      
      const blob = new Blob([logText], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `vabhub-logs-${new Date().toISOString().split('T')[0]}.txt`
      a.click()
      URL.revokeObjectURL(url)
      
      this.addLog('info', 'system', '日志导出完成')
    }
  }
}
</script>

<style scoped>
.log-center {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  height: calc(100vh - 140px);
  display: flex;
  flex-direction: column;
}

.log-header {
  text-align: center;
  margin-bottom: 2rem;
}

.log-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.log-header p {
  color: #7f8c8d;
}

.log-controls {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: #2c3e50;
  white-space: nowrap;
}

.form-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.log-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  font-weight: 500;
  color: #7f8c8d;
}

.stat-value {
  font-weight: 600;
  color: #2c3e50;
}

.stat-value.error {
  color: #e74c3c;
}

.stat-value.warning {
  color: #f39c12;
}

.stat-value.info {
  color: #3498db;
}

.log-container {
  flex: 1;
  background: #1e1e1e;
  border-radius: 8px;
  padding: 1rem;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.log-entry {
  display: grid;
  grid-template-columns: 120px 100px 1fr 80px;
  gap: 1rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #333;
  align-items: center;
}

.log-entry:last-child {
  border-bottom: none;
}

.log-timestamp {
  color: #888;
  font-size: 0.8rem;
}

.log-source .source-badge {
  background: #555;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.log-message {
  color: #ddd;
  word-break: break-all;
}

.level-badge {
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge-error {
  background: #e74c3c;
  color: white;
}

.badge-warning {
  background: #f39c12;
  color: white;
}

.badge-info {
  background: #3498db;
  color: white;
}

.badge-debug {
  background: #9b59b6;
  color: white;
}

.log-level-error .log-message {
  color: #e74c3c;
}

.log-level-warning .log-message {
  color: #f39c12;
}

.log-level-info .log-message {
  color: #3498db;
}

.log-level-debug .log-message {
  color: #9b59b6;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #333;
  border-radius: 4px;
  margin-top: 1rem;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-indicator.connected {
  background: #27ae60;
  animation: pulse 2s infinite;
}

.status-indicator.disconnected {
  background: #e74c3c;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.log-search {
  display: flex;
  gap: 1rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .log-center {
    padding: 1rem;
    height: auto;
  }
  
  .log-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .log-stats {
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .log-entry {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .log-search {
    flex-direction: column;
  }
}
</style>