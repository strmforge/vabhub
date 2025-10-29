<template>
  <div class="settings-page">
    <div class="page-header">
      <h1>系统设置</h1>
    </div>
    
    <div class="settings-content">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本设置" name="basic">
          <basic-settings />
        </el-tab-pane>
        <el-tab-pane label="媒体路径" name="paths">
          <path-settings />
        </el-tab-pane>
        <el-tab-pane label="插件设置" name="plugins">
          <plugin-settings />
        </el-tab-pane>
        <el-tab-pane label="高级设置" name="advanced">
          <advanced-settings />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BasicSettings from '@/components/settings/BasicSettings.vue'
import PathSettings from '@/components/settings/PathSettings.vue'
import PluginSettings from '@/components/settings/PluginSettings.vue'
import AdvancedSettings from '@/components/settings/AdvancedSettings.vue'

const activeTab = ref('basic')
</script>

<style scoped>
.settings-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.settings-content {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}
</style>