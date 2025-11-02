<template>
  <div class="plugins">
    <div class="plugins-header">
      <h2>插件管理</h2>
      <p>管理 VabHub 多仓库架构中的插件</p>
    </div>
    
    <div class="plugins-content">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">已安装插件</h3>
          <button class="btn btn-primary">安装新插件</button>
        </div>
        
        <div class="plugins-list">
          <div class="plugin-item" v-for="plugin in plugins" :key="plugin.id">
            <div class="plugin-info">
              <h4>{{ plugin.name }}</h4>
              <p>{{ plugin.description }}</p>
              <span class="plugin-version">版本: {{ plugin.version }}</span>
            </div>
            <div class="plugin-actions">
              <button class="btn btn-secondary" @click="togglePlugin(plugin)">
                {{ plugin.enabled ? '禁用' : '启用' }}
              </button>
              <button class="btn btn-primary" @click="configurePlugin(plugin)">配置</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Plugins',
  data() {
    return {
      plugins: [
        {
          id: 'core-plugin',
          name: '核心插件',
          description: '提供基础功能支持',
          version: '1.5.0',
          enabled: true
        },
        {
          id: 'auth-plugin',
          name: '认证插件',
          description: '用户认证和授权管理',
          version: '1.2.0',
          enabled: true
        },
        {
          id: 'storage-plugin',
          name: '存储插件',
          description: '文件存储和资源管理',
          version: '1.1.0',
          enabled: true
        }
      ]
    }
  },
  methods: {
    togglePlugin(plugin) {
      plugin.enabled = !plugin.enabled
      console.log(`${plugin.name} ${plugin.enabled ? '已启用' : '已禁用'}`)
    },
    configurePlugin(plugin) {
      console.log(`配置插件: ${plugin.name}`)
    }
  }
}
</script>

<style scoped>
.plugins-header {
  text-align: center;
  margin-bottom: 2rem;
}

.plugins-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.plugins-content {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plugins-list {
  margin-top: 1rem;
}

.plugin-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 1rem;
  background: #fafafa;
}

.plugin-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.plugin-info p {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
}

.plugin-version {
  font-size: 0.8rem;
  color: #95a5a6;
}

.plugin-actions {
  display: flex;
  gap: 0.5rem;
}
</style>