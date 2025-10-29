<template>
  <div class="plugin-market">
    <div class="market-header">
      <el-input
        v-model="searchText"
        placeholder="搜索插件..."
        style="width: 300px"
        clearable
      />
      <el-button type="primary" @click="refreshMarket">刷新市场</el-button>
    </div>
    
    <div class="market-content">
      <div v-if="marketPlugins.length === 0" class="empty-state">
        <el-empty description="暂无可用插件" />
      </div>
      
      <div v-else class="market-grid">
        <el-card 
          v-for="plugin in filteredPlugins" 
          :key="plugin.id" 
          class="market-card"
        >
          <template #header>
            <div class="card-header">
              <h3>{{ plugin.name }}</h3>
              <el-tag type="primary">官方</el-tag>
            </div>
          </template>
          
          <div class="plugin-details">
            <p class="description">{{ plugin.description }}</p>
            <div class="plugin-stats">
              <span>下载量: {{ plugin.downloads }}</span>
              <span>评分: {{ plugin.rating }}</span>
            </div>
            <div class="plugin-meta">
              <span>版本: {{ plugin.version }}</span>
              <span>作者: {{ plugin.author }}</span>
            </div>
          </div>
          
          <template #footer>
            <div class="card-actions">
              <el-button type="primary" @click="installPlugin(plugin)">安装</el-button>
              <el-button @click="viewDetails(plugin)">详情</el-button>
            </div>
          </template>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const searchText = ref('')

const marketPlugins = ref([
  {
    id: 1,
    name: '豆瓣插件',
    description: '从豆瓣获取电影和电视剧信息',
    version: '1.0.0',
    author: 'VabHub Team',
    downloads: 1000,
    rating: '4.8'
  },
  {
    id: 2,
    name: '下载器插件',
    description: '支持多种下载器的集成',
    version: '1.0.0',
    author: 'VabHub Team',
    downloads: 800,
    rating: '4.5'
  }
])

const filteredPlugins = computed(() => {
  return marketPlugins.value.filter(plugin => 
    plugin.name.toLowerCase().includes(searchText.value.toLowerCase()) ||
    plugin.description.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

const refreshMarket = async () => {
  try {
    const response = await pluginAPI.list('available')
    if (response.success) {
      ElMessage.success('插件市场刷新成功')
      // 更新插件市场数据
      plugins.value = response.data.plugins || []
    } else {
      ElMessage.error('刷新失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('刷新失败: ' + error.message)
  }
}

const installPlugin = async (plugin) => {
  try {
    const response = await pluginAPI.install(plugin.id)
    if (response.success) {
      ElMessage.success(`安装插件成功: ${plugin.name}`)
      // 刷新插件市场列表
      refreshMarket()
    } else {
      ElMessage.error('安装失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('安装失败: ' + error.message)
  }
}

const viewDetails = (plugin) => {
  ElMessage.info(`查看插件详情: ${plugin.name}`)
}
</script>

<style scoped>
.plugin-market {
  padding: 20px 0;
}

.market-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.market-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.market-card {
  transition: transform 0.3s;
}

.market-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.description {
  margin: 0 0 15px 0;
  color: #666;
  line-height: 1.5;
}

.plugin-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: #333;
}

.plugin-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>