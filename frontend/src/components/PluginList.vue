<template>
  <div class="plugin-list">
    <div v-if="plugins.length === 0" class="empty-state">
      <el-empty description="暂无插件" />
    </div>
    
    <div v-else class="plugin-cards">
      <el-card 
        v-for="plugin in plugins" 
        :key="plugin.id" 
        class="plugin-card"
      >
        <template #header>
          <div class="card-header">
            <h3>{{ plugin.name }}</h3>
            <el-tag :type="getStatusType(plugin.status)">
              {{ plugin.status }}
            </el-tag>
          </div>
        </template>
        
        <div class="plugin-info">
          <p>{{ plugin.description }}</p>
          <div class="plugin-meta">
            <span>版本: {{ plugin.version }}</span>
            <span>作者: {{ plugin.author }}</span>
          </div>
        </div>
        
        <template #footer>
          <div class="card-actions">
            <el-button 
              v-if="plugin.status === 'installed'" 
              type="danger" 
              size="small"
              @click="uninstallPlugin(plugin)"
            >
              卸载
            </el-button>
            <el-button 
              v-else 
              type="primary" 
              size="small"
              @click="installPlugin(plugin)"
            >
              安装
            </el-button>
            <el-button size="small" @click="viewDetails(plugin)">详情</el-button>
          </div>
        </template>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { pluginAPI } from '@/api'
import { pluginAPI } from '@/api'

const props = defineProps({
  status: {
    type: String,
    required: true
  }
})

const plugins = ref([])

// 从API获取插件列表
const fetchPlugins = async () => {
  try {
    const response = await pluginAPI.list(props.status)
    if (response.success) {
      plugins.value = response.data.plugins || []
    } else {
      ElMessage.error('获取插件列表失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('获取插件列表失败: ' + error.message)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPlugins()
})

const getStatusType = (status) => {
  const types = {
    'installed': 'success',
    'available': 'primary',
    'disabled': 'warning',
    'error': 'danger'
  }
  return types[status] || 'info'
}

const installPlugin = async (plugin) => {
  try {
    const response = await pluginAPI.install(plugin.id)
    if (response.success) {
      ElMessage.success(`安装插件成功: ${plugin.name}`)
      // 刷新插件列表
      loadPlugins()
    } else {
      ElMessage.error('安装失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('安装失败: ' + error.message)
  }
}

const uninstallPlugin = async (plugin) => {
  try {
    const response = await pluginAPI.uninstall(plugin.id)
    if (response.success) {
      ElMessage.success(`卸载插件成功: ${plugin.name}`)
      // 刷新插件列表
      loadPlugins()
    } else {
      ElMessage.error('卸载失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('卸载失败: ' + error.message)
  }
}

const viewDetails = (plugin) => {
  ElMessage.info(`查看插件详情: ${plugin.name}`)
}
</script>

<style scoped>
.plugin-list {
  padding: 20px 0;
}

.plugin-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.plugin-card {
  transition: transform 0.3s;
}

.plugin-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plugin-info p {
  margin: 0 0 10px 0;
  color: #666;
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