<template>
  <div class="microfrontend-example">
    <h2>{{ $t('microfrontend.title') }}</h2>
    
    <!-- 微前端模块加载区域 -->
    <div class="module-container">
      <div class="module-section">
        <h3>{{ $t('microfrontend.mediaDashboard') }}</h3>
        <div class="module-content">
          <!-- 动态加载的媒体仪表板组件 -->
          <MediaDashboard ref="dashboardRef" />
        </div>
      </div>
      
      <div class="module-section">
        <h3>{{ $t('microfrontend.musicPlayer') }}</h3>
        <div class="module-content">
          <!-- 动态加载的音乐播放器组件 -->
          <MusicPlayer ref="playerRef" />
        </div>
      </div>
    </div>
    
    <!-- 微前端通信演示 -->
    <div class="communication-demo">
      <h3>{{ $t('microfrontend.communicationDemo') }}</h3>
      <div class="demo-controls">
        <el-button @click="sendTestEvent" type="primary">
          {{ $t('microfrontend.sendTestEvent') }}
        </el-button>
        <el-button @click="refreshDashboard" type="success">
          {{ $t('microfrontend.refreshDashboard') }}
        </el-button>
        <el-button @click="toggleMusicPlayer" type="warning">
          {{ $t('microfrontend.togglePlayer') }}
        </el-button>
      </div>
      
      <div class="event-log">
        <h4>{{ $t('microfrontend.eventLog') }}</h4>
        <div class="log-entries">
          <div 
            v-for="(entry, index) in eventLog" 
            :key="index"
            class="log-entry"
            :class="entry.type"
          >
            <span class="timestamp">{{ entry.timestamp }}</span>
            <span class="event-type">{{ entry.type }}</span>
            <span class="event-data">{{ entry.data }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useMicroFrontendCommunication, MicroFrontendEvents } from '@/services/microfrontend'

const { t } = useI18n()
const { useEvent, sendEvent, useSharedState } = useMicroFrontendCommunication()

// 组件引用
const dashboardRef = ref<any>(null)
const playerRef = ref<any>(null)

// 事件日志
const eventLog = ref<Array<{timestamp: string, type: string, data: any}>>([])

// 共享状态示例
const { state: sharedTheme } = useSharedState('theme', 'light')

// 添加事件到日志
const addEventToLog = (type: string, data?: any) => {
  eventLog.value.unshift({
    timestamp: new Date().toLocaleTimeString(),
    type,
    data: data ? JSON.stringify(data) : 'No data'
  })
  
  // 限制日志数量
  if (eventLog.value.length > 10) {
    eventLog.value = eventLog.value.slice(0, 10)
  }
}

// 发送测试事件
const sendTestEvent = () => {
  const testData = {
    message: 'Hello from MicroFrontend Example',
    timestamp: Date.now()
  }
  
  sendEvent('test-event', testData)
  addEventToLog('test-event-sent', testData)
}

// 刷新仪表板数据
const refreshDashboard = () => {
  if (dashboardRef.value && dashboardRef.value.refreshData) {
    dashboardRef.value.refreshData()
    addEventToLog('dashboard-refresh')
  }
}

// 切换音乐播放器状态
const toggleMusicPlayer = () => {
  if (playerRef.value) {
    // 这里可以调用音乐播放器的方法
    addEventToLog('player-toggle')
  }
}

// 监听微前端事件
const unsubscribe = useEvent('test-event', (event) => {
  addEventToLog('test-event-received', event.payload)
})

// 监听主题变化
useEvent(MicroFrontendEvents.THEME_CHANGE, (event) => {
  sharedTheme.value = event.payload
  addEventToLog('theme-changed', event.payload)
})

// 监听语言变化
useEvent(MicroFrontendEvents.LANGUAGE_CHANGE, (event) => {
  addEventToLog('language-changed', event.payload)
})

onMounted(() => {
  addEventToLog('component-mounted')
  
  // 发送模块加载完成事件
  sendEvent(MicroFrontendEvents.MODULE_LOADED, {
    module: 'MicroFrontendExample',
    timestamp: Date.now()
  })
})

onUnmounted(() => {
  unsubscribe()
})

// 暴露给微前端使用
defineExpose({
  refreshDashboard,
  sendTestEvent,
  eventLog
})
</script>

<style scoped>
.microfrontend-example {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.module-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.module-section {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background: #fafafa;
}

.module-section h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 10px;
}

.module-content {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.communication-demo {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background: #f8f9fa;
}

.demo-controls {
  margin-bottom: 20px;
}

.demo-controls .el-button {
  margin-right: 10px;
}

.event-log {
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  max-height: 300px;
  overflow-y: auto;
}

.event-log h4 {
  margin: 0;
  padding: 10px;
  background: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.log-entries {
  padding: 10px;
}

.log-entry {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.log-entry:last-child {
  border-bottom: none;
}

.timestamp {
  color: #666;
  margin-right: 10px;
  min-width: 80px;
}

.event-type {
  color: #1890ff;
  margin-right: 10px;
  font-weight: bold;
  min-width: 120px;
}

.event-data {
  color: #52c41a;
  flex: 1;
  word-break: break-all;
}

.log-entry.test-event-sent .event-type {
  color: #1890ff;
}

.log-entry.test-event-received .event-type {
  color: #52c41a;
}

.log-entry.theme-changed .event-type {
  color: #faad14;
}

.log-entry.language-changed .event-type {
  color: #722ed1;
}

@media (max-width: 768px) {
  .module-container {
    grid-template-columns: 1fr;
  }
  
  .demo-controls .el-button {
    display: block;
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>