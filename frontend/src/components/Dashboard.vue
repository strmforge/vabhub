<template>
  <div class="dashboard">
    <!-- 顶部导航栏 -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-900">VabHub</h1>
            <nav class="ml-8 flex space-x-4">
              <router-link 
                v-for="item in navigation" 
                :key="item.name"
                :to="item.to"
                class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="[
                  $route.path === item.to 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                ]"
              >
                {{ item.name }}
              </router-link>
            </nav>
          </div>
          <div class="flex items-center space-x-4">
            <LanguageSwitcher />
            <UserAuthMenu />
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main class="flex-1 overflow-auto">
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- 统计卡片 -->
        <div class="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-2 lg:grid-cols-4">
          <div 
            v-for="stat in stats" 
            :key="stat.name"
            class="bg-white overflow-hidden shadow rounded-lg"
          >
            <div class="px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">
                {{ stat.name }}
              </dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">
                {{ stat.value }}
              </dd>
            </div>
          </div>
        </div>

        <!-- 功能模块网格 -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <!-- 媒体库概览 -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                媒体库概览
              </h3>
              <div class="grid grid-cols-2 gap-4">
                <div 
                  v-for="media in mediaStats" 
                  :key="media.type"
                  class="text-center p-4 rounded-lg bg-gray-50"
                >
                  <div class="text-2xl font-bold text-blue-600">{{ media.count }}</div>
                  <div class="text-sm text-gray-600">{{ media.label }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 下载状态 -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                下载状态
              </h3>
              <div class="space-y-3">
                <div 
                  v-for="task in downloadTasks" 
                  :key="task.id"
                  class="flex items-center justify-between"
                >
                  <div class="flex-1">
                    <div class="text-sm font-medium text-gray-900 truncate">
                      {{ task.name }}
                    </div>
                    <div class="flex items-center space-x-2">
                      <div class="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          class="bg-blue-600 h-2 rounded-full transition-all"
                          :style="{ width: task.progress + '%' }"
                        ></div>
                      </div>
                      <span class="text-xs text-gray-500">{{ task.progress }}%</span>
                    </div>
                  </div>
                  <div class="text-xs text-gray-500">{{ task.speed }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 订阅状态 -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                订阅状态
              </h3>
              <div class="space-y-3">
                <div 
                  v-for="sub in subscriptions" 
                  :key="sub.id"
                  class="flex items-center justify-between p-3 rounded-lg border"
                  :class="sub.status === 'active' ? 'border-green-200 bg-green-50' : 'border-gray-200'"
                >
                  <div>
                    <div class="font-medium text-gray-900">{{ sub.name }}</div>
                    <div class="text-sm text-gray-500">{{ sub.lastCheck }}</div>
                  </div>
                  <span 
                    class="px-2 py-1 text-xs rounded-full"
                    :class="sub.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                  >
                    {{ sub.status === 'active' ? '活跃' : '暂停' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 系统状态 -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                系统状态
              </h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">CPU使用率</span>
                  <div class="flex items-center space-x-2">
                    <div class="w-20 bg-gray-200 rounded-full h-2">
                      <div 
                        class="bg-green-600 h-2 rounded-full"
                        :style="{ width: systemStats.cpu + '%' }"
                      ></div>
                    </div>
                    <span class="text-sm font-medium">{{ systemStats.cpu }}%</span>
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">内存使用率</span>
                  <div class="flex items-center space-x-2">
                    <div class="w-20 bg-gray-200 rounded-full h-2">
                      <div 
                        class="bg-yellow-600 h-2 rounded-full"
                        :style="{ width: systemStats.memory + '%' }"
                      ></div>
                    </div>
                    <span class="text-sm font-medium">{{ systemStats.memory }}%</span>
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">磁盘使用率</span>
                  <div class="flex items-center space-x-2">
                    <div class="w-20 bg-gray-200 rounded-full h-2">
                      <div 
                        class="bg-red-600 h-2 rounded-full"
                        :style="{ width: systemStats.disk + '%' }"
                      ></div>
                    </div>
                    <span class="text-sm font-medium">{{ systemStats.disk }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 最近活动 -->
        <div class="mt-8 bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              最近活动
            </h3>
            <div class="space-y-3">
              <div 
                v-for="activity in recentActivities" 
                :key="activity.id"
                class="flex items-center space-x-3 p-3 rounded-lg border border-gray-200"
              >
                <div 
                  class="w-8 h-8 rounded-full flex items-center justify-center"
                  :class="getActivityIcon(activity.type)"
                >
                  <span class="text-white text-sm">{{ getActivityEmoji(activity.type) }}</span>
                </div>
                <div class="flex-1">
                  <div class="text-sm text-gray-900">{{ activity.message }}</div>
                  <div class="text-xs text-gray-500">{{ activity.time }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import LanguageSwitcher from './LanguageSwitcher.vue'
import UserAuthMenu from './UserAuthMenu.vue'

const router = useRouter()

// 导航菜单
const navigation = [
  { name: '仪表板', to: '/' },
  { name: '媒体库', to: '/media' },
  { name: '下载管理', to: '/downloads' },
  { name: '订阅管理', to: '/subscriptions' },
  { name: '插件市场', to: '/plugins' },
  { name: '系统设置', to: '/settings' }
]

// 统计数据
const stats = ref([
  { name: '总媒体文件', value: '1,234' },
  { name: '活跃下载', value: '12' },
  { name: '订阅源', value: '8' },
  { name: '插件数量', value: '15' }
])

// 媒体库统计
const mediaStats = ref([
  { type: 'movie', count: '856', label: '电影' },
  { type: 'tv', count: '312', label: '电视剧' },
  { type: 'anime', count: '66', label: '动漫' },
  { type: 'music', count: '0', label: '音乐' }
])

// 下载任务
const downloadTasks = ref([
  { id: 1, name: '复仇者联盟4：终局之战.1080p.BluRay', progress: 75, speed: '2.5 MB/s' },
  { id: 2, name: '权力的游戏.S08E01.720p.WEB-DL', progress: 45, speed: '1.2 MB/s' },
  { id: 3, name: '你的名字.1080p.BluRay', progress: 100, speed: '完成' }
])

// 订阅状态
const subscriptions = ref([
  { id: 1, name: '电影RSS订阅', status: 'active', lastCheck: '5分钟前' },
  { id: 2, name: '电视剧订阅', status: 'active', lastCheck: '10分钟前' },
  { id: 3, name: '动漫订阅', status: 'paused', lastCheck: '1小时前' }
])

// 系统状态
const systemStats = ref({
  cpu: 25,
  memory: 68,
  disk: 42
})

// 最近活动
const recentActivities = ref([
  { id: 1, type: 'download', message: '下载完成：你的名字.1080p.BluRay', time: '2分钟前' },
  { id: 2, type: 'subscription', message: '订阅匹配：复仇者联盟4：终局之战', time: '15分钟前' },
  { id: 3, type: 'scan', message: '媒体库扫描完成，新增3个文件', time: '1小时前' },
  { id: 4, type: 'plugin', message: '插件更新：音乐订阅插件 v2.0.0', time: '2小时前' }
])

// 获取活动图标样式
const getActivityIcon = (type) => {
  const icons = {
    download: 'bg-green-500',
    subscription: 'bg-blue-500',
    scan: 'bg-purple-500',
    plugin: 'bg-yellow-500'
  }
  return icons[type] || 'bg-gray-500'
}

// 获取活动表情
const getActivityEmoji = (type) => {
  const emojis = {
    download: '⬇️',
    subscription: '📰',
    scan: '🔍',
    plugin: '🔌'
  }
  return emojis[type] || '📝'
}

// 模拟数据加载
onMounted(async () => {
  // 这里应该调用API获取真实数据
  console.log('Dashboard mounted')
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 平滑过渡效果 */
.router-link-active {
  transition: all 0.2s ease-in-out;
}

/* 卡片悬停效果 */
.bg-white:hover {
  transform: translateY(-2px);
  transition: all 0.2s ease-in-out;
}

/* 进度条动画 */
.bg-blue-600 {
  transition: width 0.3s ease-in-out;
}
</style>