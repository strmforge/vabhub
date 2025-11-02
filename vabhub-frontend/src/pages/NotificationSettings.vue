<template>
  <div class="notification-settings">
    <div class="page-header">
      <h1>通知设置</h1>
      <p>配置多通道通知系统，实时接收系统状态和任务更新</p>
    </div>

    <div class="content">
      <!-- 通知渠道配置 -->
      <div class="channels-section">
        <h2>通知渠道</h2>
        <div class="channels-grid">
          <div v-for="channel in channels" :key="channel.id" class="channel-card">
            <div class="channel-header">
              <div class="channel-icon">{{ channel.icon }}</div>
              <div class="channel-info">
                <h3>{{ channel.name }}</h3>
                <p>{{ channel.description }}</p>
              </div>
              <div class="channel-toggle">
                <label class="toggle">
                  <input type="checkbox" v-model="channel.enabled" @change="updateChannel(channel)" />
                  <span class="slider"></span>
                </label>
              </div>
            </div>
            
            <div v-if="channel.enabled" class="channel-config">
              <div v-for="config in channel.configs" :key="config.key" class="config-item">
                <label :for="config.key">{{ config.label }}</label>
                <input 
                  :id="config.key"
                  :type="config.type" 
                  v-model="config.value"
                  :placeholder="config.placeholder"
                  @blur="saveChannelConfig(channel)"
                />
              </div>
              
              <div class="channel-actions">
                <button class="btn btn-sm" @click="testChannel(channel)">测试连接</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 通知模板 -->
      <div class="templates-section">
        <h2>通知模板</h2>
        <div class="templates-grid">
          <div v-for="template in templates" :key="template.id" class="template-card">
            <div class="template-header">
              <h3>{{ template.name }}</h3>
              <div class="template-badge" :class="template.type">{{ template.type }}</div>
            </div>
            
            <div class="template-content">
              <p class="template-preview">{{ template.preview }}</p>
              <div class="template-variables">
                <span v-for="variable in template.variables" :key="variable" class="variable-tag">
                  {{ variable }}
                </span>
              </div>
            </div>
            
            <div class="template-actions">
              <button class="btn btn-sm" @click="editTemplate(template)">编辑</button>
              <button class="btn btn-sm" @click="previewTemplate(template)">预览</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 通知规则 -->
      <div class="rules-section">
        <h2>通知规则</h2>
        <div class="rules-list">
          <div v-for="rule in rules" :key="rule.id" class="rule-item">
            <div class="rule-info">
              <h4>{{ rule.event }}</h4>
              <p>{{ rule.description }}</p>
            </div>
            
            <div class="rule-settings">
              <div class="rule-channels">
                <label v-for="channel in channels" :key="channel.id" class="channel-checkbox">
                  <input 
                    type="checkbox" 
                    :value="channel.id" 
                    v-model="rule.channels"
                    @change="saveRule(rule)"
                  />
                  {{ channel.name }}
                </label>
              </div>
              
              <div class="rule-priority">
                <label>优先级:</label>
                <select v-model="rule.priority" @change="saveRule(rule)">
                  <option value="low">低</option>
                  <option value="normal">正常</option>
                  <option value="high">高</option>
                  <option value="urgent">紧急</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 测试通知模态框 -->
      <div v-if="showTestModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>测试通知</h3>
            <button class="close-btn" @click="closeTestModal">×</button>
          </div>
          
          <div class="modal-body">
            <div class="test-form">
              <div class="form-group">
                <label>选择渠道</label>
                <div class="channel-selector">
                  <label v-for="channel in enabledChannels" :key="channel.id">
                    <input type="checkbox" :value="channel.id" v-model="testChannels" />
                    {{ channel.name }}
                  </label>
                </div>
              </div>
              
              <div class="form-group">
                <label>测试消息</label>
                <textarea v-model="testMessage" placeholder="输入测试消息内容"></textarea>
              </div>
              
              <div class="form-group">
                <label>优先级</label>
                <select v-model="testPriority">
                  <option value="low">低</option>
                  <option value="normal">正常</option>
                  <option value="high">高</option>
                </select>
              </div>
            </div>
            
            <div v-if="testResult" class="test-result" :class="testResult.success ? 'success' : 'error'">
              <h4>{{ testResult.success ? '测试成功' : '测试失败' }}</h4>
              <p>{{ testResult.message }}</p>
              <div v-if="testResult.details" class="result-details">
                <pre>{{ JSON.stringify(testResult.details, null, 2) }}</pre>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeTestModal">取消</button>
            <button class="btn btn-primary" @click="sendTestNotification">发送测试</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'

export default {
  name: 'NotificationSettings',
  setup() {
    const showTestModal = ref(false)
    const testChannels = ref([])
    const testMessage = ref('这是一条测试通知消息')
    const testPriority = ref('normal')
    const testResult = ref(null)

    // 通知渠道数据
    const channels = reactive([
      {
        id: 'telegram',
        name: 'Telegram',
        icon: '📱',
        description: 'Telegram机器人通知',
        enabled: true,
        configs: [
          { key: 'botToken', label: 'Bot Token', type: 'text', value: '', placeholder: '输入Telegram Bot Token' },
          { key: 'chatId', label: 'Chat ID', type: 'text', value: '', placeholder: '输入聊天ID' }
        ]
      },
      {
        id: 'email',
        name: '电子邮件',
        icon: '📧',
        description: '邮件通知',
        enabled: false,
        configs: [
          { key: 'smtpServer', label: 'SMTP服务器', type: 'text', value: '', placeholder: 'smtp.gmail.com' },
          { key: 'smtpPort', label: '端口', type: 'number', value: '587', placeholder: '587' },
          { key: 'username', label: '用户名', type: 'text', value: '', placeholder: 'your-email@gmail.com' },
          { key: 'password', label: '密码', type: 'password', value: '', placeholder: '输入密码' }
        ]
      },
      {
        id: 'serverchan',
        name: 'Server酱',
        icon: '🔔',
        description: '微信通知服务',
        enabled: false,
        configs: [
          { key: 'sendKey', label: 'SendKey', type: 'text', value: '', placeholder: '输入Server酱SendKey' }
        ]
      },
      {
        id: 'console',
        name: '控制台',
        icon: '💻',
        description: '控制台输出（调试用）',
        enabled: true,
        configs: []
      }
    ])

    // 通知模板数据
    const templates = reactive([
      {
        id: 'download_complete',
        name: '下载完成',
        type: 'success',
        preview: '🎉 下载完成！\n📺 标题：{title}\n📁 文件：{filename}\n💾 大小：{size}',
        variables: ['title', 'filename', 'size', 'duration']
      },
      {
        id: 'subscription_update',
        name: '订阅更新',
        type: 'info',
        preview: '📢 订阅更新\n🎬 剧集：{title}\n📅 季数：{season}\n🎯 集数：{episode}',
        variables: ['title', 'season', 'episode', 'link']
      },
      {
        id: 'system_error',
        name: '系统错误',
        type: 'error',
        preview: '❌ 系统错误\n💥 模块：{module}\n📝 错误：{error}\n⏰ 时间：{time}',
        variables: ['module', 'error', 'time']
      }
    ])

    // 通知规则数据
    const rules = reactive([
      {
        id: 'download_complete',
        event: '下载完成',
        description: '当下载任务完成时发送通知',
        channels: ['telegram', 'console'],
        priority: 'normal'
      },
      {
        id: 'subscription_match',
        event: '订阅匹配',
        description: '当订阅规则匹配到新内容时发送通知',
        channels: ['telegram'],
        priority: 'normal'
      },
      {
        id: 'system_error',
        event: '系统错误',
        description: '当系统发生错误时发送通知',
        channels: ['telegram', 'email'],
        priority: 'high'
      },
      {
        id: 'storage_warning',
        event: '存储警告',
        description: '当存储空间不足时发送通知',
        channels: ['telegram'],
        priority: 'high'
      }
    ])

    const enabledChannels = computed(() => {
      return channels.filter(channel => channel.enabled)
    })

    onMounted(() => {
      // 模拟加载配置数据
      loadConfigurations()
    })

    const loadConfigurations = () => {
      // 模拟从API加载配置
      console.log('加载通知配置')
    }

    const updateChannel = async (channel) => {
      // 模拟API调用
      console.log(`更新渠道 ${channel.name} 状态: ${channel.enabled}`)
    }

    const saveChannelConfig = async (channel) => {
      // 模拟API调用
      console.log(`保存渠道 ${channel.name} 配置`)
    }

    const testChannel = async (channel) => {
      // 模拟测试连接
      console.log(`测试渠道 ${channel.name}`)
      
      // 显示测试结果
      testResult.value = {
        success: true,
        message: `渠道 ${channel.name} 连接测试成功`,
        details: { channel: channel.name, timestamp: new Date() }
      }
    }

    const editTemplate = (template) => {
      console.log('编辑模板:', template.name)
    }

    const previewTemplate = (template) => {
      console.log('预览模板:', template.name)
    }

    const saveRule = async (rule) => {
      // 模拟API调用
      console.log('保存规则:', rule.event)
    }

    const sendTestNotification = async () => {
      // 模拟发送测试通知
      console.log('发送测试通知', {
        channels: testChannels.value,
        message: testMessage.value,
        priority: testPriority.value
      })

      // 模拟测试结果
      testResult.value = {
        success: true,
        message: '测试通知发送成功',
        details: {
          channels: testChannels.value,
          sent: testChannels.value.length,
          failed: 0,
          timestamp: new Date()
        }
      }
    }

    const closeTestModal = () => {
      showTestModal.value = false
      testResult.value = null
      testChannels.value = []
      testMessage.value = '这是一条测试通知消息'
      testPriority.value = 'normal'
    }

    return {
      showTestModal,
      testChannels,
      testMessage,
      testPriority,
      testResult,
      channels,
      templates,
      rules,
      enabledChannels,
      updateChannel,
      saveChannelConfig,
      testChannel,
      editTemplate,
      previewTemplate,
      saveRule,
      sendTestNotification,
      closeTestModal
    }
  }
}
</script>

<style scoped>
.notification-settings {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.channels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.channel-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
}

.channel-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.channel-icon {
  font-size: 2rem;
}

.channel-info {
  flex: 1;
}

.channel-info h3 {
  margin: 0 0 0.5rem 0;
}

.channel-info p {
  margin: 0;
  color: #666;
  font-size: 0.875rem;
}

.channel-config {
  border-top: 1px solid #f0f0f0;
  padding-top: 1rem;
}

.config-item {
  margin-bottom: 1rem;
}

.config-item label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
}

.config-item input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
}

.channel-actions {
  margin-top: 1rem;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.template-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.template-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.template-badge.success {
  background: #e8f5e8;
  color: #2e7d32;
}

.template-badge.info {
  background: #e3f2fd;
  color: #1976d2;
}

.template-badge.error {
  background: #ffebee;
  color: #c62828;
}

.template-preview {
  white-space: pre-line;
  font-family: monospace;
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 1rem;
}

.template-variables {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.variable-tag {
  background: #f0f0f0;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #666;
}

.template-actions {
  display: flex;
  gap: 0.5rem;
}

.rules-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.rule-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.rule-info {
  flex: 1;
}

.rule-info h4 {
  margin: 0 0 0.5rem 0;
}

.rule-info p {
  margin: 0;
  color: #666;
  font-size: 0.875rem;
}

.rule-settings {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 200px;
}

.rule-channels {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.channel-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.rule-priority {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rule-priority label {
  font-size: 0.875rem;
  font-weight: 500;
}

.rule-priority select {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
}

/* 切换开关样式 */
.toggle {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle input {
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
  background-color: #1976d2;
}

input:checked + .slider:before {
  transform: translateX(26px);
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
  max-width: 500px;
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

.test-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.channel-selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.channel-selector label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
}

.test-result {
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.test-result.success {
  background: #e8f5e8;
  border: 1px solid #c8e6c9;
}

.test-result.error {
  background: #ffebee;
  border: 1px solid #ffcdd2;
}

.result-details pre {
  background: rgba(0,0,0,0.05);
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  overflow-x: auto;
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

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
}
</style>