<template>
  <div class="charts-config">
    <div class="config-header">
      <h2>排行榜配置管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="saveConfig" :loading="saving">
          <el-icon><Check /></el-icon>
          保存配置
        </el-button>
        <el-button @click="resetConfig">
          <el-icon><Refresh /></el-icon>
          重置配置
        </el-button>
        <el-button @click="testConnection" :loading="testing">
          <el-icon><Connection /></el-icon>
          测试连接
        </el-button>
      </div>
    </div>

    <!-- 配置标签页 -->
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 基本配置 -->
      <el-tab-pane label="基本配置" name="basic">
        <div class="config-section">
          <h3>数据收集配置</h3>
          <el-form :model="config" label-width="120px">
            <el-form-item label="收集间隔">
              <el-input-number 
                v-model="config.collection_interval" 
                :min="300" 
                :max="86400"
                :step="300"
              />
              <span class="unit">秒</span>
              <el-tooltip content="数据收集的时间间隔，建议设置为1小时（3600秒）以上">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </el-form-item>
            
            <el-form-item label="输出目录">
              <el-input v-model="config.output_dir" placeholder="/vol1/charts" />
            </el-form-item>
            
            <el-form-item label="启用集成">
              <el-switch v-model="config.integration.enabled" />
              <span class="switch-label">{{ config.integration.enabled ? '已启用' : '已禁用' }}</span>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>

      <!-- 数据源配置 -->
      <el-tab-pane label="数据源配置" name="providers">
        <div class="config-section">
          <h3>数据源配置</h3>
          
          <el-card 
            v-for="(providerConfig, providerName) in config.providers" 
            :key="providerName"
            class="provider-card"
          >
            <template #header>
              <div class="card-header">
                <el-switch 
                  v-model="providerConfig.enabled" 
                  @change="onProviderToggle(providerName, $event)"
                />
                <span class="provider-name">{{ getProviderName(providerName) }}</span>
                <el-tag :type="providerConfig.enabled ? 'success' : 'info'">
                  {{ providerConfig.enabled ? '已启用' : '已禁用' }}
                </el-tag>
              </div>
            </template>
            
            <div v-if="providerConfig.enabled">
              <!-- Apple Music 配置 -->
              <div v-if="providerName === 'apple_music'">
                <el-form :model="providerConfig" label-width="80px">
                  <el-form-item label="国家/地区">
                    <el-select v-model="providerConfig.country" placeholder="选择国家">
                      <el-option label="美国" value="us" />
                      <el-option label="中国" value="cn" />
                      <el-option label="日本" value="jp" />
                      <el-option label="英国" value="gb" />
                      <el-option label="全球" value="global" />
                    </el-select>
                  </el-form-item>
                  
                  <el-form-item label="数量限制">
                    <el-input-number 
                      v-model="providerConfig.limit" 
                      :min="10" 
                      :max="200"
                    />
                  </el-form-item>
                </el-form>
              </div>
              
              <!-- Spotify 配置 -->
              <div v-if="providerName === 'spotify_charts'">
                <el-form :model="providerConfig" label-width="80px">
                  <el-form-item label="地区">
                    <el-select v-model="providerConfig.region" placeholder="选择地区">
                      <el-option label="全球" value="global" />
                      <el-option label="美国" value="us" />
                      <el-option label="中国" value="cn" />
                      <el-option label="日本" value="jp" />
                    </el-select>
                  </el-form-item>
                  
                  <el-form-item label="排行榜类型">
                    <el-select v-model="providerConfig.chart_kind" placeholder="选择类型">
                      <el-option label="每日" value="daily" />
                      <el-option label="每周" value="weekly" />
                    </el-select>
                  </el-form-item>
                  
                  <el-form-item label="回溯天数">
                    <el-input-number 
                      v-model="providerConfig.lookback_days" 
                      :min="1" 
                      :max="30"
                    />
                  </el-form-item>
                </el-form>
              </div>
              
              <!-- Netflix 配置 -->
              <div v-if="providerName === 'netflix_top10'">
                <el-form :model="providerConfig" label-width="120px">
                  <el-form-item label="数据源URL">
                    <el-input 
                      v-model="providerConfig.all_weeks_url" 
                      placeholder="Netflix Top 10 数据源URL"
                    />
                  </el-form-item>
                </el-form>
              </div>
              
              <!-- IMDb 配置 -->
              <div v-if="providerName === 'imdb_datasets'">
                <el-form :model="providerConfig" label-width="100px">
                  <el-form-item label="最低投票数">
                    <el-input-number 
                      v-model="providerConfig.min_votes" 
                      :min="1000" 
                      :max="100000"
                      :step="1000"
                    />
                  </el-form-item>
                  
                  <el-form-item label="返回数量">
                    <el-input-number 
                      v-model="providerConfig.top_n" 
                      :min="10" 
                      :max="1000"
                    />
                  </el-form-item>
                  
                  <el-form-item label="合并基本信息">
                    <el-switch v-model="providerConfig.join_basics" />
                  </el-form-item>
                </el-form>
              </div>
            </div>
            
            <div v-else class="provider-disabled">
              <el-empty description="该数据源已禁用" :image-size="80" />
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <!-- 集成配置 -->
      <el-tab-pane label="集成配置" name="integration">
        <div class="config-section">
          <h3>下载器集成配置</h3>
          
          <!-- Torznab 配置 -->
          <el-card class="integration-card">
            <template #header>
              <div class="card-header">
                <h4>Torznab 配置 (Jackett/Prowlarr)</h4>
              </div>
            </template>
            
            <el-form :model="config.integration" label-width="120px">
              <el-form-item label="端点列表">
                <el-tag
                  v-for="(endpoint, index) in config.integration.torznab_endpoints"
                  :key="index"
                  closable
                  @close="removeEndpoint(index)"
                  style="margin-right: 10px; margin-bottom: 5px;"
                >
                  {{ endpoint }}
                </el-tag>
                
                <el-button @click="addEndpoint" type="primary" link>
                  <el-icon><Plus /></el-icon>
                  添加端点
                </el-button>
              </el-form-item>
              
              <el-form-item label="超时时间">
                <el-input-number 
                  v-model="config.integration.timeout" 
                  :min="10" 
                  :max="60"
                />
                <span class="unit">秒</span>
              </el-form-item>
            </el-form>
          </el-card>
          
          <!-- qBittorrent 配置 -->
          <el-card class="integration-card">
            <template #header>
              <div class="card-header">
                <h4>qBittorrent 配置</h4>
              </div>
            </template>
            
            <el-form :model="config.integration" label-width="120px">
              <el-form-item label="服务器地址">
                <el-input v-model="config.integration.qbittorrent_url" placeholder="http://127.0.0.1:8080" />
              </el-form-item>
              
              <el-form-item label="用户名">
                <el-input v-model="config.integration.qbittorrent_username" placeholder="admin" />
              </el-form-item>
              
              <el-form-item label="密码">
                <el-input 
                  v-model="config.integration.qbittorrent_password" 
                  type="password" 
                  placeholder="adminadmin"
                  show-password
                />
              </el-form-item>
            </el-form>
          </el-card>
          
          <!-- 自动化规则 -->
          <el-card class="integration-card">
            <template #header>
              <div class="card-header">
                <h4>自动化规则</h4>
              </div>
            </template>
            
            <el-form :model="config.integration" label-width="120px">
              <el-form-item label="自动下载">
                <el-switch v-model="config.integration.auto_add" />
                <span class="switch-label">{{ config.integration.auto_add ? '已启用' : '已禁用' }}</span>
                <el-alert 
                  v-if="config.integration.auto_add"
                  title="警告：启用自动下载可能会添加大量下载任务，请谨慎使用"
                  type="warning"
                  :closable="false"
                  style="margin-top: 10px;"
                />
              </el-form-item>
              
              <el-form-item label="音乐保存路径">
                <el-input v-model="config.integration.music_save_path" placeholder="/vol02/incoming/music" />
              </el-form-item>
              
              <el-form-item label="电影保存路径">
                <el-input v-model="config.integration.movie_save_path" placeholder="/vol02/incoming/movies" />
              </el-form-item>
              
              <el-form-item label="电视剧保存路径">
                <el-input v-model="config.integration.tv_save_path" placeholder="/vol02/incoming/tv" />
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 端点添加对话框 -->
    <el-dialog v-model="endpointDialogVisible" title="添加 Torznab 端点" width="500px">
      <el-form :model="newEndpoint" label-width="80px">
        <el-form-item label="端点URL">
          <el-input 
            v-model="newEndpoint.url" 
            placeholder="http://jackett:9117/api/v2.0/indexers/all/results/torznab/api?apikey=YOUR_KEY"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="endpointDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAddEndpoint">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check, Refresh, Connection, InfoFilled, Plus } from '@element-plus/icons-vue'

// 响应式数据
const activeTab = ref('basic')
const saving = ref(false)
const testing = ref(false)
const endpointDialogVisible = ref(false)
const newEndpoint = reactive({ url: '' })

// 配置数据
const config = reactive({
  collection_interval: 3600,
  output_dir: '/vol1/charts',
  providers: {
    apple_music: {
      enabled: true,
      country: 'us',
      limit: 100
    },
    spotify_charts: {
      enabled: true,
      region: 'global',
      chart_kind: 'daily',
      lookback_days: 7
    },
    netflix_top10: {
      enabled: true,
      all_weeks_url: 'https://www.netflix.com/tudum/top10/data/all-weeks-global.xlsx'
    },
    imdb_datasets: {
      enabled: true,
      min_votes: 10000,
      top_n: 500,
      join_basics: true
    }
  },
  integration: {
    enabled: false,
    torznab_endpoints: [],
    timeout: 20,
    qbittorrent_url: 'http://127.0.0.1:8080',
    qbittorrent_username: 'admin',
    qbittorrent_password: 'adminadmin',
    auto_add: false,
    music_save_path: '/vol02/incoming/music',
    movie_save_path: '/vol02/incoming/movies',
    tv_save_path: '/vol02/incoming/tv'
  }
})

// 方法
const getProviderName = (providerName) => {
  const nameMap = {
    apple_music: 'Apple Music',
    spotify_charts: 'Spotify Charts',
    netflix_top10: 'Netflix Top 10',
    imdb_datasets: 'IMDb Datasets'
  }
  return nameMap[providerName] || providerName
}

const onProviderToggle = (providerName, enabled) => {
  ElMessage.info(`${getProviderName(providerName)} ${enabled ? '已启用' : '已禁用'}`)
}

const addEndpoint = () => {
  newEndpoint.url = ''
  endpointDialogVisible.value = true
}

const removeEndpoint = (index) => {
  config.integration.torznab_endpoints.splice(index, 1)
}

const confirmAddEndpoint = () => {
  if (newEndpoint.url.trim()) {
    config.integration.torznab_endpoints.push(newEndpoint.url.trim())
    endpointDialogVisible.value = false
    ElMessage.success('端点添加成功')
  } else {
    ElMessage.warning('请输入有效的端点URL')
  }
}

const saveConfig = async () => {
  saving.value = true
  try {
    // 这里调用API保存配置
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟API调用
    ElMessage.success('配置保存成功')
  } catch (error) {
    ElMessage.error('配置保存失败')
  } finally {
    saving.value = false
  }
}

const resetConfig = () => {
  ElMessageBox.confirm('确定要重置配置吗？这将恢复所有设置为默认值。', '确认重置', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 重置配置逻辑
    Object.assign(config, {
      collection_interval: 3600,
      output_dir: '/vol1/charts',
      integration: {
        enabled: false,
        torznab_endpoints: [],
        timeout: 20,
        qbittorrent_url: 'http://127.0.0.1:8080',
        qbittorrent_username: 'admin',
        qbittorrent_password: 'adminadmin',
        auto_add: false,
        music_save_path: '/vol02/incoming/music',
        movie_save_path: '/vol02/incoming/movies',
        tv_save_path: '/vol02/incoming/tv'
      }
    })
    ElMessage.success('配置已重置')
  }).catch(() => {
    // 用户取消
  })
}

const testConnection = async () => {
  testing.value = true
  try {
    // 这里调用API测试连接
    await new Promise(resolve => setTimeout(resolve, 2000)) // 模拟API调用
    ElMessage.success('连接测试成功')
  } catch (error) {
    ElMessage.error('连接测试失败')
  } finally {
    testing.value = false
  }
}

// 生命周期
onMounted(() => {
  // 加载配置
  loadConfig()
})

const loadConfig = async () => {
  try {
    // 这里调用API加载配置
    await new Promise(resolve => setTimeout(resolve, 500)) // 模拟API调用
    // 模拟加载的配置数据
    const loadedConfig = {
      collection_interval: 7200,
      output_dir: '/data/charts',
      integration: {
        enabled: true,
        torznab_endpoints: [
          'http://jackett:9117/api/v2.0/indexers/all/results/torznab/api?apikey=test123'
        ],
        timeout: 30
      }
    }
    Object.assign(config, loadedConfig)
  } catch (error) {
    ElMessage.error('配置加载失败')
  }
}
</script>

<style scoped>
.charts-config {
  padding: 20px;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.config-section {
  margin-bottom: 30px;
}

.config-section h3 {
  margin-bottom: 20px;
  color: #303133;
  border-left: 4px solid #409EFF;
  padding-left: 10px;
}

.provider-card, .integration-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.provider-name {
  font-weight: bold;
  font-size: 16px;
}

.provider-disabled {
  text-align: center;
  padding: 20px;
}

.unit {
  margin-left: 10px;
  color: #909399;
}

.switch-label {
  margin-left: 10px;
  color: #909399;
}

.el-form-item {
  margin-bottom: 20px;
}
</style>