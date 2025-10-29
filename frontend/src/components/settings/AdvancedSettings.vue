<template>
  <div class="advanced-settings">
    <div class="settings-header">
      <h3>高级设置</h3>
      <el-alert
        title="警告：修改这些设置可能会影响系统稳定性"
        type="warning"
        :closable="false"
      />
    </div>
    
    <el-form :model="settings" label-width="150px">
      <el-form-item label="API端口">
        <el-input-number 
          v-model="settings.apiPort" 
          :min="1024" 
          :max="65535" 
          controls-position="right"
        />
      </el-form-item>
      
      <el-form-item label="数据库类型">
        <el-select v-model="settings.databaseType">
          <el-option label="SQLite" value="sqlite" />
          <el-option label="PostgreSQL" value="postgresql" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="数据库连接">
        <el-input v-model="settings.databaseUrl" placeholder="数据库连接字符串" />
      </el-form-item>
      
      <el-form-item label="缓存类型">
        <el-select v-model="settings.cacheType">
          <el-option label="内存缓存" value="memory" />
          <el-option label="Redis" value="redis" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="Redis连接">
        <el-input v-model="settings.redisUrl" placeholder="Redis连接字符串" />
      </el-form-item>
      
      <el-form-item label="日志文件路径">
        <el-input v-model="settings.logPath" placeholder="日志文件路径" />
      </el-form-item>
      
      <el-form-item label="最大日志文件大小">
        <el-input-number 
          v-model="settings.maxLogSize" 
          :min="1" 
          :max="1000" 
          controls-position="right"
        />
        <span class="tip">MB</span>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
        <el-button @click="resetSettings">重置</el-button>
        <el-button type="danger" @click="showRestartDialog">重启服务</el-button>
      </el-form-item>
    </el-form>
    
    <el-dialog v-model="restartDialogVisible" title="重启服务" width="400px">
      <p>确定要重启服务吗？重启期间系统将不可用。</p>
      <template #footer>
        <el-button @click="restartDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="restartService">确定重启</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const settings = reactive({
  apiPort: 8090,
  databaseType: 'sqlite',
  databaseUrl: 'sqlite:///vabhub.db',
  cacheType: 'memory',
  redisUrl: 'redis://localhost:6379',
  logPath: './logs',
  maxLogSize: 100
})

const restartDialogVisible = ref(false)

const saveSettings = async () => {
  try {
    const response = await settingsAPI.update(settings)
    if (response.success) {
      ElMessage.success('高级设置保存成功')
    } else {
      ElMessage.error('保存失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  }
}

const resetSettings = () => {
  Object.assign(settings, {
    apiPort: 8090,
    databaseType: 'sqlite',
    databaseUrl: 'sqlite:///vabhub.db',
    cacheType: 'memory',
    redisUrl: 'redis://localhost:6379',
    logPath: './logs',
    maxLogSize: 100
  })
  ElMessage.info('设置已重置')
}

const showRestartDialog = () => {
  restartDialogVisible.value = true
}

const restartService = async () => {
  try {
    const response = await settingsAPI.restart()
    if (response.success) {
      ElMessage.success('服务重启中...')
      restartDialogVisible.value = false
    } else {
      ElMessage.error('重启失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('重启失败: ' + error.message)
  }
}
</script>

<style scoped>
.advanced-settings {
  max-width: 700px;
}

.settings-header {
  margin-bottom: 20px;
}

.tip {
  margin-left: 10px;
  color: #999;
  font-size: 12px;
}
</style>