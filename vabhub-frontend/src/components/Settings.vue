<template>
  <div class="settings">
    <div class="settings-header">
      <h2>系统设置</h2>
      <p>配置 VabHub 多仓库架构</p>
    </div>
    
    <div class="settings-content">
      <div class="settings-grid">
        <!-- 存储提供商配置 -->
        <div class="settings-card">
          <h3>存储提供商</h3>
          <div class="setting-item">
            <label class="setting-label">123网盘</label>
            <div class="storage-config">
              <input v-model="storageSettings.pan123.username" class="form-input" placeholder="用户名">
              <input v-model="storageSettings.pan123.password" type="password" class="form-input" placeholder="密码">
              <button class="btn btn-secondary" @click="testStorageConnection('pan123')">连接测试</button>
            </div>
          </div>
          <div class="setting-item">
            <label class="setting-label">115网盘</label>
            <div class="storage-config">
              <input v-model="storageSettings.pan115.cookie" class="form-input" placeholder="Cookie">
              <button class="btn btn-secondary" @click="testStorageConnection('pan115')">连接测试</button>
            </div>
          </div>
        </div>
        
        <!-- PT站点配置 -->
        <div class="settings-card">
          <h3>PT站点</h3>
          <div class="setting-item">
            <label class="setting-label">站点列表</label>
            <div class="pt-sites">
              <div v-for="site in ptSettings.sites" :key="site.id" class="pt-site-item">
                <input v-model="site.name" class="form-input" placeholder="站点名称">
                <input v-model="site.url" class="form-input" placeholder="站点URL">
                <input v-model="site.apiKey" type="password" class="form-input" placeholder="API密钥">
                <button class="btn btn-secondary" @click="testPTConnection(site)">测试</button>
              </div>
              <button class="btn btn-primary" @click="addPTSite">添加站点</button>
            </div>
          </div>
        </div>
        
        <!-- 刮削器配置 -->
        <div class="settings-card">
          <h3>刮削器</h3>
          <div class="setting-item">
            <label class="setting-label">TMDB API</label>
            <input v-model="scraperSettings.tmdb.apiKey" type="password" class="form-input" placeholder="API密钥">
          </div>
          <div class="setting-item">
            <label class="setting-label">刮削模式</label>
            <select v-model="scraperSettings.mode" class="form-input">
              <option value="auto">自动刮削</option>
              <option value="manual">手动刮削</option>
              <option value="hybrid">混合模式</option>
            </select>
          </div>
        </div>
        
        <!-- 核心服务配置 -->
        <div class="settings-card">
          <h3>核心服务</h3>
          <div class="setting-item">
            <label class="setting-label">API 地址</label>
            <input v-model="coreSettings.apiUrl" class="form-input" placeholder="http://localhost:8000">
          </div>
          <div class="setting-item">
            <label class="setting-label">数据库连接</label>
            <input v-model="coreSettings.databaseUrl" class="form-input" placeholder="sqlite:///vabhub.db">
          </div>
        </div>
        
        <!-- 前端配置 -->
        <div class="settings-card">
          <h3>前端配置</h3>
          <div class="setting-item">
            <label class="setting-label">主题</label>
            <select v-model="frontendSettings.theme" class="form-input">
              <option value="light">浅色</option>
              <option value="dark">深色</option>
              <option value="auto">自动</option>
            </select>
          </div>
          <div class="setting-item">
            <label class="setting-label">语言</label>
            <select v-model="frontendSettings.language" class="form-input">
              <option value="zh-CN">中文</option>
              <option value="en-US">English</option>
            </select>
          </div>
        </div>
      </div>
      
      <div class="settings-actions">
        <button class="btn btn-primary" @click="saveSettings">保存设置</button>
        <button class="btn btn-secondary" @click="resetSettings">重置</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      // 存储提供商设置
      storageSettings: {
        pan123: {
          username: '',
          password: '',
          enabled: false
        },
        pan115: {
          cookie: '',
          enabled: false
        }
      },
      // PT站点设置
      ptSettings: {
        sites: [
          {
            id: 1,
            name: '',
            url: '',
            apiKey: '',
            enabled: false
          }
        ]
      },
      // 刮削器设置
      scraperSettings: {
        tmdb: {
          apiKey: '',
          enabled: false
        },
        mode: 'auto'
      },
      // 核心服务设置
      coreSettings: {
        apiUrl: 'http://localhost:8000',
        databaseUrl: 'sqlite:///vabhub.db'
      },
      // 前端设置
      frontendSettings: {
        theme: 'light',
        language: 'zh-CN'
      }
    }
  },
  methods: {
    // 测试存储连接
    testStorageConnection(storageType) {
      const storage = this.storageSettings[storageType]
      console.log(`测试${storageType}连接:`, storage)
      // 这里应该调用后端API进行连接测试
      alert(`${storageType}连接测试中...`)
    },
    
    // 测试PT连接
    testPTConnection(site) {
      console.log('测试PT站点连接:', site)
      // 这里应该调用后端API进行PT站点连接测试
      alert(`测试${site.name}连接中...`)
    },
    
    // 添加PT站点
    addPTSite() {
      const newId = this.ptSettings.sites.length + 1
      this.ptSettings.sites.push({
        id: newId,
        name: '',
        url: '',
        apiKey: '',
        enabled: false
      })
    },
    
    // 保存设置
    saveSettings() {
      console.log('保存设置:', {
        storage: this.storageSettings,
        pt: this.ptSettings,
        scraper: this.scraperSettings,
        core: this.coreSettings,
        frontend: this.frontendSettings
      })
      
      // 这里应该调用后端API保存设置
      alert('设置已保存')
    },
    
    // 重置设置
    resetSettings() {
      this.storageSettings = {
        pan123: {
          username: '',
          password: '',
          enabled: false
        },
        pan115: {
          cookie: '',
          enabled: false
        }
      }
      
      this.ptSettings = {
        sites: [
          {
            id: 1,
            name: '',
            url: '',
            apiKey: '',
            enabled: false
          }
        ]
      }
      
      this.scraperSettings = {
        tmdb: {
          apiKey: '',
          enabled: false
        },
        mode: 'auto'
      }
      
      this.coreSettings = {
        apiUrl: 'http://localhost:8000',
        databaseUrl: 'sqlite:///vabhub.db'
      }
      
      this.frontendSettings = {
        theme: 'light',
        language: 'zh-CN'
      }
      
      alert('设置已重置')
    }
  }
}
</script>

<style scoped>
.settings-header {
  text-align: center;
  margin-bottom: 2rem;
}

.settings-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.settings-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.settings-card h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.setting-item {
  margin-bottom: 1.5rem;
}

.setting-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #34495e;
}

.storage-config {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.pt-sites {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pt-site-item {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 0.5rem;
  align-items: end;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.settings-actions {
  text-align: center;
  display: flex;
  gap: 1rem;
  justify-content: center;
}
</style>