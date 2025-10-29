<template>
  <div class="media-library">
    <!-- 顶部工具栏 -->
    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>VabHub 媒体库</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <!-- 搜索框 -->
      <v-text-field
        v-model="searchQuery"
        placeholder="搜索媒体..."
        prepend-inner-icon="mdi-magnify"
        solo
        flat
        hide-details
        class="search-field"
        @input="handleSearch"
      ></v-text-field>
      
      <!-- 操作按钮 -->
      <v-btn icon @click="refreshLibrary">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
      <v-btn icon @click="showScanDialog = true">
        <v-icon>mdi-folder-search</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- 侧边栏 -->
    <v-navigation-drawer v-model="drawer" app temporary>
      <v-list nav dense>
        <v-list-item-group v-model="selectedTab" color="primary">
          <v-list-item value="movies">
            <v-list-item-icon>
              <v-icon>mdi-movie</v-icon>
            </v-list-item-icon>
            <v-list-item-title>电影</v-list-item-title>
          </v-list-item>
          
          <v-list-item value="tv">
            <v-list-item-icon>
              <v-icon>mdi-television</v-icon>
            </v-list-item-icon>
            <v-list-item-title>电视剧</v-list-item-title>
          </v-list-item>
          
          <v-list-item value="anime">
            <v-list-item-icon>
              <v-icon>mdi-ninja</v-icon>
            </v-list-item-icon>
            <v-list-item-title>动漫</v-list-item-title>
          </v-list-item>
          
          <v-list-item value="music">
            <v-list-item-icon>
              <v-icon>mdi-music</v-icon>
            </v-list-item-icon>
            <v-list-item-title>音乐</v-list-item-title>
          </v-list-item>
          
          <v-divider></v-divider>
          
          <v-list-item value="subscriptions">
            <v-list-item-icon>
              <v-icon>mdi-rss</v-icon>
            </v-list-item-icon>
            <v-list-item-title>订阅管理</v-list-item-title>
          </v-list-item>
          
          <v-list-item value="downloads">
            <v-list-item-icon>
              <v-icon>mdi-download</v-icon>
            </v-list-item-icon>
            <v-list-item-title>下载管理</v-list-item-title>
          </v-list-item>
          
          <v-list-item value="settings">
            <v-list-item-icon>
              <v-icon>mdi-cog</v-icon>
            </v-list-item-icon>
            <v-list-item-title>系统设置</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <!-- 主内容区域 -->
    <v-main>
      <v-container fluid>
        <!-- 统计信息卡片 -->
        <v-row class="mb-4">
          <v-col cols="12" sm="6" md="3">
            <v-card class="stat-card" color="blue" dark>
              <v-card-text class="text-center">
                <v-icon large>mdi-movie</v-icon>
                <div class="stat-number">{{ stats.movies || 0 }}</div>
                <div class="stat-label">电影</div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" sm="6" md="3">
            <v-card class="stat-card" color="green" dark>
              <v-card-text class="text-center">
                <v-icon large>mdi-television</v-icon>
                <div class="stat-number">{{ stats.tv || 0 }}</div>
                <div class="stat-label">电视剧</div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" sm="6" md="3">
            <v-card class="stat-card" color="orange" dark>
              <v-card-text class="text-center">
                <v-icon large>mdi-ninja</v-icon>
                <div class="stat-number">{{ stats.anime || 0 }}</div>
                <div class="stat-label">动漫</div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" sm="6" md="3">
            <v-card class="stat-card" color="purple" dark>
              <v-card-text class="text-center">
                <v-icon large>mdi-music</v-icon>
                <div class="stat-number">{{ stats.music || 0 }}</div>
                <div class="stat-label">音乐</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- 媒体库内容 -->
        <div v-if="selectedTab === 'movies'">
          <MovieLibrary :media-items="filteredMovies" @refresh="refreshLibrary" />
        </div>
        
        <div v-if="selectedTab === 'tv'">
          <TvLibrary :media-items="filteredTv" @refresh="refreshLibrary" />
        </div>
        
        <div v-if="selectedTab === 'anime'">
          <AnimeLibrary :media-items="filteredAnime" @refresh="refreshLibrary" />
        </div>
        
        <div v-if="selectedTab === 'music'">
          <MusicLibrary :media-items="filteredMusic" @refresh="refreshLibrary" />
        </div>
        
        <div v-if="selectedTab === 'subscriptions'">
          <SubscriptionManager />
        </div>
        
        <div v-if="selectedTab === 'downloads'">
          <DownloadManager />
        </div>
        
        <div v-if="selectedTab === 'settings'">
          <SystemSettings />
        </div>
      </v-container>
    </v-main>

    <!-- 扫描对话框 -->
    <v-dialog v-model="showScanDialog" max-width="500">
      <v-card>
        <v-card-title>扫描媒体库</v-card-title>
        <v-card-text>
          <v-select
            v-model="selectedScanPaths"
            :items="scanPaths"
            label="选择扫描路径"
            multiple
            chips
          ></v-select>
          <v-checkbox v-model="recursiveScan" label="递归扫描子目录"></v-checkbox>
          <v-checkbox v-model="forceRescan" label="强制重新扫描"></v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="showScanDialog = false">取消</v-btn>
          <v-btn color="primary" @click="startScan" :loading="scanning">开始扫描</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 加载状态 -->
    <v-overlay :value="loading" z-index="999">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useMediaApi } from '../composables/useMediaApi'

// 组件导入
import MovieLibrary from '../components/media/MovieLibrary.vue'
import TvLibrary from '../components/media/TvLibrary.vue'
import AnimeLibrary from '../components/media/AnimeLibrary.vue'
import MusicLibrary from '../components/media/MusicLibrary.vue'
import SubscriptionManager from '../components/SubscriptionManager.vue'
import DownloadManager from '../components/DownloadManager.vue'
import SystemSettings from '../components/SystemSettings.vue'

export default {
  name: 'MediaLibrary',
  components: {
    MovieLibrary,
    TvLibrary,
    AnimeLibrary,
    MusicLibrary,
    SubscriptionManager,
    DownloadManager,
    SystemSettings
  },
  setup() {
    const {
      mediaItems,
      stats,
      loading,
      scanPaths,
      refreshMediaLibrary,
      scanMediaLibrary,
      searchMedia
    } = useMediaApi()

    // 响应式数据
    const drawer = ref(false)
    const selectedTab = ref('movies')
    const searchQuery = ref('')
    const showScanDialog = ref(false)
    const selectedScanPaths = ref([])
    const recursiveScan = ref(true)
    const forceRescan = ref(false)
    const scanning = ref(false)

    // 计算属性
    const filteredMovies = computed(() => {
      return mediaItems.value.filter(item => 
        item.type === 'movie' && 
        item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const filteredTv = computed(() => {
      return mediaItems.value.filter(item => 
        item.type === 'tv' && 
        item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const filteredAnime = computed(() => {
      return mediaItems.value.filter(item => 
        item.type === 'anime' && 
        item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const filteredMusic = computed(() => {
      return mediaItems.value.filter(item => 
        item.type === 'music' && 
        item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    // 方法
    const refreshLibrary = async () => {
      await refreshMediaLibrary()
    }

    const handleSearch = () => {
      if (searchQuery.value.length >= 2) {
        searchMedia(searchQuery.value)
      }
    }

    const startScan = async () => {
      scanning.value = true
      try {
        await scanMediaLibrary({
          paths: selectedScanPaths.value,
          recursive: recursiveScan.value,
          force_rescan: forceRescan.value
        })
        showScanDialog.value = false
        await refreshMediaLibrary()
      } catch (error) {
        console.error('扫描失败:', error)
      } finally {
        scanning.value = false
      }
    }

    // 生命周期
    onMounted(async () => {
      await refreshMediaLibrary()
    })

    return {
      drawer,
      selectedTab,
      searchQuery,
      showScanDialog,
      selectedScanPaths,
      recursiveScan,
      forceRescan,
      scanning,
      mediaItems,
      stats,
      loading,
      scanPaths,
      filteredMovies,
      filteredTv,
      filteredAnime,
      filteredMusic,
      refreshLibrary,
      handleSearch,
      startScan
    }
  }
}
</script>

<style scoped>
.media-library {
  height: 100vh;
}

.search-field {
  max-width: 300px;
  margin-right: 16px;
}

.stat-card {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin: 8px 0;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.8;
}

.v-main {
  background-color: #f5f5f5;
}

.v-card {
  transition: box-shadow 0.3s ease;
}

.v-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>