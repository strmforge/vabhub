<template>
  <div class="plugins-page">
    <div class="page-header">
      <h1>插件管理</h1>
      <el-button type="primary" @click="refreshPlugins">刷新插件</el-button>
    </div>
    
    <div class="plugins-content">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="已安装" name="installed">
          <plugin-list :status="'installed'" />
        </el-tab-pane>
        <el-tab-pane label="可用插件" name="available">
          <plugin-list :status="'available'" />
        </el-tab-pane>
        <el-tab-pane label="插件市场" name="market">
          <plugin-market />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import PluginList from '@/components/PluginList.vue'
import PluginMarket from '@/components/PluginMarket.vue'
import { pluginAPI } from '@/api'

const activeTab = ref('installed')

const refreshPlugins = async () => {
  try {
    const response = await pluginAPI.list()
    if (response.success) {
      ElMessage.success('插件列表刷新成功')
      // 刷新子组件的插件列表
      if (activeTab.value === 'installed') {
        // 触发已安装插件列表刷新
      } else if (activeTab.value === 'market') {
        // 触发插件市场刷新
      }
    } else {
      ElMessage.error('刷新失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('刷新失败: ' + error.message)
  }
}
</script>

<style scoped>
.plugins-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.plugins-content {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}
</style>