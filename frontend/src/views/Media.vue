<template>
  <div class="media-page">
    <div class="page-header">
      <h1>媒体库管理</h1>
      <el-button type="primary" @click="scanMedia">扫描媒体</el-button>
    </div>
    
    <div class="media-content">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="电影" name="movies">
          <media-list :type="'movie'" />
        </el-tab-pane>
        <el-tab-pane label="电视剧" name="tv">
          <media-list :type="'tv'" />
        </el-tab-pane>
        <el-tab-pane label="音乐" name="music">
          <media-list :type="'music'" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import MediaList from '@/components/MediaList.vue'

const activeTab = ref('movies')

const scanMedia = async () => {
  try {
    const response = await mediaAPI.scan({
      paths: ['/media/movies', '/media/tv'],
      scan_type: 'full',
      force_rescan: false
    })
    
    if (response.success) {
      ElMessage.success('媒体扫描任务已启动')
      // 可以在这里添加任务状态监控
    } else {
      ElMessage.error('扫描失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('扫描失败: ' + error.message)
  }
}
</script>

<style scoped>
.media-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.media-content {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}
</style>