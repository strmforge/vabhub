<template>
  <div class="music-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">音乐中心</h1>
      <div class="header-actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索音乐..."
          class="search-input"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="showUploadDialog">
          <el-icon><Upload /></el-icon>
          上传音乐
        </el-button>
      </div>
    </div>

    <!-- 音乐分类导航 -->
    <div class="music-nav">
      <el-tabs v-model="activeTab" @tab-click="handleTabChange">
        <el-tab-pane label="推荐音乐" name="recommend">
          <MusicRecommendation />
        </el-tab-pane>
        <el-tab-pane label="我的歌单" name="playlists">
          <PlaylistManager />
        </el-tab-pane>
        <el-tab-pane label="本地音乐" name="local">
          <LocalMusic />
        </el-tab-pane>
        <el-tab-pane label="在线音乐" name="online">
          <OnlineMusic />
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 音乐播放器 -->
    <MusicPlayer />

    <!-- 上传音乐对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传音乐"
      width="500px"
      :before-close="handleUploadClose"
    >
      <MusicUpload @upload-success="handleUploadSuccess" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Upload } from '@element-plus/icons-vue'
import MusicPlayer from '@/components/MusicPlayer.vue'
import MusicRecommendation from '@/components/MusicRecommendation.vue'
import PlaylistManager from '@/components/PlaylistManager.vue'
import LocalMusic from '@/components/LocalMusic.vue'
import OnlineMusic from '@/components/OnlineMusic.vue'
import MusicUpload from '@/components/MusicUpload.vue'

// 页面状态
const searchQuery = ref('')
const activeTab = ref('recommend')
const uploadDialogVisible = ref(false)

// 搜索处理
const handleSearch = () => {
  // 实现搜索逻辑
  console.log('搜索关键词:', searchQuery.value)
}

// 标签切换
const handleTabChange = (tab: any) => {
  console.log('切换到标签:', tab.props.name)
}

// 上传音乐
const showUploadDialog = () => {
  uploadDialogVisible.value = true
}

const handleUploadClose = (done: () => void) => {
  ElMessage.info('上传已取消')
  done()
}

const handleUploadSuccess = () => {
  uploadDialogVisible.value = false
  ElMessage.success('音乐上传成功')
  // 刷新音乐列表
}

// 监听搜索变化，实现防抖搜索
let searchTimer: NodeJS.Timeout
watch(searchQuery, (newQuery) => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    handleSearch()
  }, 300)
})
</script>

<style scoped>
.music-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-input {
  width: 300px;
}

.music-nav {
  margin-bottom: 30px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .music-page {
    padding: 10px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .header-actions {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
}
</style>