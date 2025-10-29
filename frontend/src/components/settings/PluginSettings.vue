<template>
  <div class="plugin-settings">
    <div class="settings-header">
      <h3>插件设置</h3>
    </div>
    
    <el-form :model="settings" label-width="120px">
      <el-form-item label="自动更新插件">
        <el-switch v-model="settings.autoUpdate" />
        <span class="tip">启用后系统会自动检查并更新插件</span>
      </el-form-item>
      
      <el-form-item label="插件市场源">
        <el-input v-model="settings.marketUrl" placeholder="请输入插件市场URL" />
      </el-form-item>
      
      <el-form-item label="插件安装目录">
        <el-input v-model="settings.pluginDir" placeholder="请输入插件安装目录" />
      </el-form-item>
      
      <el-form-item label="插件日志级别">
        <el-select v-model="settings.logLevel">
          <el-option label="DEBUG" value="debug" />
          <el-option label="INFO" value="info" />
          <el-option label="WARNING" value="warning" />
          <el-option label="ERROR" value="error" />
        </el-select>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
        <el-button @click="resetSettings">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

const settings = reactive({
  autoUpdate: true,
  marketUrl: 'https://plugins.vabhub.org',
  pluginDir: './plugins',
  logLevel: 'info'
})

const saveSettings = async () => {
  try {
    const response = await settingsAPI.update({
      plugin: settings
    })
    if (response.success) {
      ElMessage.success('插件设置保存成功')
    } else {
      ElMessage.error('保存失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  }
}

const resetSettings = () => {
  Object.assign(settings, {
    autoUpdate: true,
    marketUrl: 'https://plugins.vabhub.org',
    pluginDir: './plugins',
    logLevel: 'info'
  })
  ElMessage.info('设置已重置')
}
</script>

<style scoped>
.plugin-settings {
  max-width: 600px;
}

.tip {
  margin-left: 10px;
  color: #999;
  font-size: 12px;
}
</style>