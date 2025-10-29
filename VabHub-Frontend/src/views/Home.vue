<template>
  <div class="home">
    <div class="container mx-auto px-4 py-8">
      <!-- 欢迎区域 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          欢迎使用 VabHub
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-300">
          智能媒体管理系统
        </p>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
        <div class="card">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-blue-100 dark:bg-blue-900 mr-4">
              <el-icon class="text-blue-600 dark:text-blue-400">
                <VideoCamera />
              </el-icon>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">电影</p>
              <p class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">
                {{ mediaStats.movies }}
              </p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-green-100 dark:bg-green-900 mr-4">
              <el-icon class="text-green-600 dark:text-green-400">
                <Film />
              </el-icon>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">电视剧</p>
              <p class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">
                {{ mediaStats.tvShows }}
              </p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-purple-100 dark:bg-purple-900 mr-4">
              <el-icon class="text-purple-600 dark:text-purple-400">
                <Headphone />
              </el-icon>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">音乐</p>
              <p class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">
                {{ mediaStats.music }}
              </p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-orange-100 dark:bg-orange-900 mr-4">
              <el-icon class="text-orange-600 dark:text-orange-400">
                <Collection />
              </el-icon>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">总计</p>
              <p class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">
                {{ mediaStats.total }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 快速操作 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            快速操作
          </h3>
          <div class="space-y-3">
            <el-button class="w-full" type="primary" @click="navigateToMedia">
              <el-icon class="mr-2">
                <FolderOpened />
              </el-icon>
              浏览媒体库
            </el-button>
            <el-button class="w-full" @click="scanMedia">
              <el-icon class="mr-2">
                <Refresh />
              </el-icon>
              扫描媒体库
            </el-button>
            <el-button class="w-full" @click="navigateToSettings">
              <el-icon class="mr-2">
                <Setting />
              </el-icon>
              系统设置
            </el-button>
          </div>
        </div>

        <div class="card md:col-span-2">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            最近活动
          </h3>
          <div class="text-center py-8">
            <el-icon class="text-4xl text-gray-400 mb-4">
              <Clock />
            </el-icon>
            <p class="text-gray-500 dark:text-gray-400">暂无最近活动</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import {
  VideoCamera,
  Film,
  Headphone,
  Collection,
  FolderOpened,
  Refresh,
  Setting,
  Clock
} from '@element-plus/icons-vue'

const router = useRouter()
const appStore = useAppStore()

const mediaStats = ref({
  total: 0,
  movies: 0,
  tvShows: 0,
  music: 0
})

const navigateToMedia = () => {
  router.push('/media')
}

const navigateToSettings = () => {
  router.push('/settings')
}

const scanMedia = async () => {
  // 调用扫描API
  // await api.media.scan()
  ElMessage.success('开始扫描媒体库')
}

onMounted(() => {
  // 加载媒体统计信息
  // mediaStats.value = await api.media.stats()
})
</script>

<style scoped>
.home {
  min-height: calc(100vh - 64px);
}
</style>