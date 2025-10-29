<template>
  <div class="basic-settings">
    <el-form :model="form" label-width="120px">
      <el-form-item label="系统名称">
        <el-input v-model="form.systemName" placeholder="请输入系统名称" />
      </el-form-item>
      
      <el-form-item label="语言设置">
        <el-select v-model="form.language" placeholder="请选择语言">
          <el-option label="简体中文" value="zh-CN" />
          <el-option label="English" value="en-US" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="主题设置">
        <el-radio-group v-model="form.theme">
          <el-radio label="light">浅色主题</el-radio>
          <el-radio label="dark">深色主题</el-radio>
          <el-radio label="auto">自动切换</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="自动扫描">
        <el-switch v-model="form.autoScan" />
        <span class="tip">启用后系统会自动扫描媒体文件</span>
      </el-form-item>
      
      <el-form-item label="扫描间隔">
        <el-input-number 
          v-model="form.scanInterval" 
          :min="1" 
          :max="24" 
          controls-position="right"
        />
        <span class="tip">小时</span>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
        <el-button @click="resetSettings">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { settingsAPI } from '@/api'

const form = reactive({
  systemName: 'VabHub',
  language: 'zh-CN',
  theme: 'auto',
  autoScan: true,
  scanInterval: 6,
  apiPort: 8090,
  databaseType: 'sqlite',
  cacheType: 'memory'
})

// 加载设置
const loadSettings = async () => {
  try {
    const response = await settingsAPI.get()
    if (response.success) {
      Object.assign(form, response.data.settings)
    }
  } catch (error) {
    ElMessage.error('加载设置失败: ' + error.message)
  }
}

const saveSettings = async () => {
  try {
    const response = await settingsAPI.update(form)
    if (response.success) {
      ElMessage.success('设置保存成功')
    } else {
      ElMessage.error('保存失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  }
}

const resetSettings = async () => {
  try {
    const defaultSettings = {
      systemName: 'VabHub',
      language: 'zh-CN',
      theme: 'auto',
      autoScan: true,
      scanInterval: 6,
      apiPort: 8090,
      databaseType: 'sqlite',
      cacheType: 'memory'
    }
    
    const response = await settingsAPI.update(defaultSettings)
    if (response.success) {
      Object.assign(form, defaultSettings)
      ElMessage.success('设置已重置')
    } else {
      ElMessage.error('重置失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('重置失败: ' + error.message)
  }
}

// 组件挂载时加载设置
onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.basic-settings {
  max-width: 600px;
}

.tip {
  margin-left: 10px;
  color: #999;
  font-size: 12px;
}
</style>