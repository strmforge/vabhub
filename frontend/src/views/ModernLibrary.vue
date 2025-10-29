<template>
  <ModernLayout
    page-title="媒体库 - VabHub"
    page-description="管理您的媒体收藏"
    :user-logged-in="userLoggedIn"
    :user-avatar="userAvatar"
    :user-name="userName"
    :user-email="userEmail"
    @search="handleSearch"
    @profile="handleProfile"
    @settings="handleSettings"
    @logout="handleLogout"
    @login="handleLogin"
  >
    <div class="modern-library">
      <!-- 库管理工具栏 -->
      <section class="modern-library__toolbar">
        <div class="modern-library__toolbar-container">
          <div class="modern-library__toolbar-left">
            <h1 class="modern-library__title">我的媒体库</h1>
            <span class="modern-library__stats">
              {{ totalItems }} 个项目 • {{ totalSize }} • {{ lastSync }}
            </span>
          </div>
          
          <div class="modern-library__toolbar-right">
            <ModernButton
              variant="primary"
              icon="Upload"
              @click="handleUpload"
            >
              上传文件
            </ModernButton>
            
            <ModernButton
              variant="outline"
              icon="FolderAdd"
              @click="handleCreateFolder"
            >
              新建文件夹
            </ModernButton>
            
            <ModernButton
              variant="text"
              icon="Refresh"
              @click="refreshLibrary"
              :loading="refreshing"
            >
              刷新
            </ModernButton>
          </div>
        </div>
      </section>

      <!-- 库内容 -->
      <section class="modern-library__content">
        <div class="modern-library__content-container">
          <!-- 视图切换 -->
          <div class="modern-library__view-controls">
            <div class="modern-library__view-buttons">
              <ModernButton
                :variant="viewMode === 'grid' ? 'primary' : 'text'"
                icon="Grid"
                @click="setViewMode('grid')"
              >
                网格视图
              </ModernButton>
              
              <ModernButton
                :variant="viewMode === 'list' ? 'primary' : 'text'"
                icon="List"
                @click="setViewMode('list')"
              >
                列表视图
              </ModernButton>
            </div>
            
            <div class="modern-library__sort-controls">
              <ModernInput
                v-model="searchQuery"
                placeholder="搜索库内容..."
                icon="Search"
                size="small"
              />
              
              <select 
                v-model="sortBy" 
                class="modern-library__sort-select"
              >
                <option value="name">按名称</option>
                <option value="date">按日期</option>
                <option value="size">按大小</option>
                <option value="type">按类型</option>
              </select>
            </div>
          </div>

          <!-- 库项目 -->
          <div class="modern-library__items">
            <!-- 网格视图 -->
            <div 
              v-if="viewMode === 'grid'" 
              class="modern-library__grid"
            >
              <ModernCard
                v-for="item in filteredItems"
                :key="item.id"
                class="modern-library__item-card"
                :hover-effect="true"
                :border-effect="true"
                @click="openItem(item)"
                @contextmenu="handleContextMenu($event, item)"
              >
                <template #image>
                  <div class="modern-library__item-thumbnail">
                    <div 
                      class="modern-library__item-icon"
                      :class="`modern-library__item-icon--${item.type}`"
                    >
                      <el-icon>
                        <component :is="getFileIcon(item.type)" />
                      </el-icon>
                    </div>
                    
                    <!-- 文件类型标签 -->
                    <div class="modern-library__item-type">
                      {{ getFileTypeLabel(item.type) }}
                    </div>
                    
                    <!-- 操作菜单 -->
                    <div class="modern-library__item-actions">
                      <ModernButton
                        variant="primary"
                        size="small"
                        icon="More"
                        @click.stop="showItemMenu(item)"
                      />
                    </div>
                  </div>
                </template>
                
                <template #title>
                  <div class="modern-library__item-title">
                    {{ item.name }}
                  </div>
                </template>
                
                <template #subtitle>
                  <div class="modern-library__item-meta">
                    <span class="modern-library__item-size">
                      {{ $filters.formatFileSize(item.size) }}
                    </span>
                    <span class="modern-library__item-date">
                      {{ formatDate(item.modified) }}
                    </span>
                  </div>
                </template>
                
                <template #footer>
                  <div class="modern-library__item-footer">
                    <div class="modern-library__item-tags">
                      <span 
                        v-for="tag in item.tags" 
                        :key="tag"
                        class="modern-library__item-tag"
                      >
                        {{ tag }}
                      </span>
                    </div>
                    
                    <div class="modern-library__item-status">
                      <span 
                        v-if="item.isFavorite"
                        class="modern-library__item-favorite"
                      >
                        <el-icon><StarFilled /></el-icon>
                      </span>
                      
                      <span 
                        v-if="item.isShared"
                        class="modern-library__item-shared"
                      >
                        <el-icon><Share /></el-icon>
                      </span>
                    </div>
                  </div>
                </template>
              </ModernCard>
            </div>
            
            <!-- 列表视图 -->
            <div 
              v-else 
              class="modern-library__list"
            >
              <div 
                v-for="item in filteredItems"
                :key="item.id"
                class="modern-library__list-item"
                @click="openItem(item)"
                @contextmenu="handleContextMenu($event, item)"
              >
                <div class="modern-library__list-icon">
                  <el-icon>
                    <component :is="getFileIcon(item.type)" />
                  </el-icon>
                </div>
                
                <div class="modern-library__list-info">
                  <div class="modern-library__list-name">
                    {{ item.name }}
                  </div>
                  <div class="modern-library__list-details">
                    <span class="modern-library__list-type">
                      {{ getFileTypeLabel(item.type) }}
                    </span>
                    <span class="modern-library__list-size">
                      {{ $filters.formatFileSize(item.size) }}
                    </span>
                    <span class="modern-library__list-date">
                      {{ formatDate(item.modified) }}
                    </span>
                  </div>
                </div>
                
                <div class="modern-library__list-actions">
                  <ModernButton
                    variant="text"
                    size="small"
                    icon="More"
                    @click="showItemMenu(item)"
                  />
                </div>
                
                <div class="modern-library__list-status">
                  <span 
                    v-if="item.isFavorite"
                    class="modern-library__list-favorite"
                  >
                    <el-icon><StarFilled /></el-icon>
                  </span>
                  
                  <span 
                    v-if="item.isShared"
                    class="modern-library__list-shared"
                  >
                    <el-icon><Share /></el-icon>
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div 
            v-if="filteredItems.length === 0" 
            class="modern-library__empty"
          >
            <div class="modern-library__empty-content">
              <el-icon class="modern-library__empty-icon">
                <FolderOpened />
              </el-icon>
              <h3 class="modern-library__empty-title">媒体库为空</h3>
              <p class="modern-library__empty-description">
                开始上传您的第一个媒体文件
              </p>
              <ModernButton
                variant="primary"
                icon="Upload"
                @click="handleUpload"
              >
                上传文件
              </ModernButton>
            </div>
          </div>
        </div>
      </section>
    </div>
  </ModernLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import ModernLayout from '@/components/ui/ModernLayout.vue'
import ModernInput from '@/components/ui/ModernInput.vue'
import ModernButton from '@/components/ui/ModernButton.vue'
import ModernCard from '@/components/ui/ModernCard.vue'
import {
  Upload,
  FolderAdd,
  Refresh,
  Grid,
  List,
  Search,
  VideoCamera,
  Headphone,
  Picture,
  Document,
  Folder,
  StarFilled,
  Share,
  More,
  FolderOpened
} from '@element-plus/icons-vue'

export default {
  name: 'ModernLibrary',
  components: {
    ModernLayout,
    ModernInput,
    ModernButton,
    ModernCard
  },
  setup() {
    // 用户状态
    const userLoggedIn = ref(true)
    const userAvatar = ref('')
    const userName = ref('现代用户')
    const userEmail = ref('user@example.com')
    
    // 库状态
    const viewMode = ref('grid')
    const searchQuery = ref('')
    const sortBy = ref('name')
    const refreshing = ref(false)
    
    // 模拟数据
    const libraryItems = ref([])
    
    // 计算属性
    const totalItems = computed(() => libraryItems.value.length)
    const totalSize = computed(() => {
      const total = libraryItems.value.reduce((sum, item) => sum + item.size, 0)
      return formatFileSize(total)
    })
    const lastSync = computed(() => {
      const latest = Math.max(...libraryItems.value.map(item => new Date(item.modified)))
      return formatDate(latest)
    })
    
    const filteredItems = computed(() => {
      let items = [...libraryItems.value]
      
      // 搜索筛选
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        items = items.filter(item => 
          item.name.toLowerCase().includes(query) ||
          item.tags.some(tag => tag.toLowerCase().includes(query))
        )
      }
      
      // 排序
      switch (sortBy.value) {
        case 'name':
          items.sort((a, b) => a.name.localeCompare(b.name))
          break
        case 'date':
          items.sort((a, b) => new Date(b.modified) - new Date(a.modified))
          break
        case 'size':
          items.sort((a, b) => b.size - a.size)
          break
        case 'type':
          items.sort((a, b) => a.type.localeCompare(b.type))
          break
      }
      
      return items
    })
    
    // 模拟数据生成
    const generateMockData = () => {
      const types = ['video', 'audio', 'image', 'document', 'folder']
      const names = [
        '项目演示视频', '会议录音', '产品图片', '设计文档',
        '旅行照片', '播客节目', '技术文档', '宣传材料',
        '培训视频', '音乐专辑', '设计素材', '项目文件'
      ]
      
      return Array.from({ length: 20 }, (_, i) => ({
        id: i + 1,
        name: names[i % names.length] + ` ${i + 1}`,
        type: types[i % types.length],
        size: Math.floor(Math.random() * 100000000) + 1000000, // 1MB - 100MB
        modified: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000),
        tags: ['工作', '个人', '重要'].slice(0, Math.floor(Math.random() * 3) + 1),
        isFavorite: Math.random() > 0.7,
        isShared: Math.random() > 0.8
      }))
    }
    
    // 工具函数
    const getFileIcon = (type) => {
      const icons = {
        video: 'VideoCamera',
        audio: 'Headphone',
        image: 'Picture',
        document: 'Document',
        folder: 'Folder'
      }
      return icons[type] || 'Document'
    }
    
    const getFileTypeLabel = (type) => {
      const labels = {
        video: '视频文件',
        audio: '音频文件',
        image: '图片文件',
        document: '文档文件',
        folder: '文件夹'
      }
      return labels[type] || '文件'
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    // 事件处理
    const handleSearch = () => {
      console.log('搜索功能触发')
    }
    
    const handleProfile = () => {
      console.log('查看个人资料')
    }
    
    const handleSettings = () => {
      console.log('打开设置')
    }
    
    const handleLogout = () => {
      userLoggedIn.value = false
      console.log('用户登出')
    }
    
    const handleLogin = () => {
      userLoggedIn.value = true
      console.log('用户登录')
    }
    
    const handleUpload = () => {
      console.log('上传文件')
    }
    
    const handleCreateFolder = () => {
      console.log('创建文件夹')
    }
    
    const refreshLibrary = async () => {
      refreshing.value = true
      
      // 模拟刷新
      await new Promise(resolve => setTimeout(resolve, 1000))
      libraryItems.value = generateMockData()
      
      refreshing.value = false
    }
    
    const setViewMode = (mode) => {
      viewMode.value = mode
    }
    
    const openItem = (item) => {
      console.log('打开项目:', item)
    }
    
    const handleContextMenu = (event, item) => {
      event.preventDefault()
      console.log('右键菜单:', item)
    }
    
    const showItemMenu = (item) => {
      console.log('显示项目菜单:', item)
    }
    
    // 初始化数据
    onMounted(() => {
      libraryItems.value = generateMockData()
    })
    
    return {
      userLoggedIn,
      userAvatar,
      userName,
      userEmail,
      viewMode,
      searchQuery,
      sortBy,
      refreshing,
      totalItems,
      totalSize,
      lastSync,
      filteredItems,
      handleSearch,
      handleProfile,
      handleSettings,
      handleLogout,
      handleLogin,
      handleUpload,
      handleCreateFolder,
      refreshLibrary,
      setViewMode,
      openItem,
      handleContextMenu,
      showItemMenu,
      getFileIcon,
      getFileTypeLabel,
      formatFileSize,
      formatDate
    }
  }
}
</script>

<style scoped>
.modern-library {
  min-height: 100vh;
}

/* 工具栏 */
.modern-library__toolbar {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  padding: var(--space-6) 0;
}

.modern-library__toolbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-8);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modern-library__toolbar-left {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.modern-library__title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0;
}

.modern-library__stats {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.modern-library__toolbar-right {
  display: flex;
  gap: var(--space-3);
}

/* 内容区域 */
.modern-library__content {
  padding: var(--space-8);
}

.modern-library__content-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 视图控制 */
.modern-library__view-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-primary);
}

.modern-library__view-buttons {
  display: flex;
  gap: var(--space-2);
}

.modern-library__sort-controls {
  display: flex;
  gap: var(--space-3);
  align-items: center;
}

.modern-library__sort-select {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

/* 网格视图 */
.modern-library__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-6);
}

.modern-library__item-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.modern-library__item-thumbnail {
  position: relative;
  height: 160px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modern-library__item-icon {
  font-size: 3rem;
  color: var(--text-tertiary);
}

.modern-library__item-icon--video {
  color: #ef4444;
}

.modern-library__item-icon--audio {
  color: #10b981;
}

.modern-library__item-icon--image {
  color: #f59e0b;
}

.modern-library__item-icon--document {
  color: #3b82f6;
}

.modern-library__item-icon--folder {
  color: #8b5cf6;
}

.modern-library__item-type {
  position: absolute;
  top: var(--space-2);
  left: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  background: var(--bg-primary);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
}

.modern-library__item-actions {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modern-library__item-card:hover .modern-library__item-actions {
  opacity: 1;
}

.modern-library__item-title {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.modern-library__item-meta {
  display: flex;
  gap: var(--space-3);
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.modern-library__item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--space-4);
}

.modern-library__item-tags {
  display: flex;
  gap: var(--space-1);
}

.modern-library__item-tag {
  font-size: var(--font-size-xs);
  color: var(--primary-600);
  background: var(--primary-50);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
}

.modern-library__item-status {
  display: flex;
  gap: var(--space-2);
}

.modern-library__item-favorite {
  color: #f59e0b;
}

.modern-library__item-shared {
  color: #10b981;
}

/* 列表视图 */
.modern-library__list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.modern-library__list-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
}

.modern-library__list-item:hover {
  background: var(--bg-secondary);
  border-color: var(--primary-300);
}

.modern-library__list-icon {
  font-size: 1.5rem;
  color: var(--text-tertiary);
  min-width: 40px;
}

.modern-library__list-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.modern-library__list-name {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.modern-library__list-details {
  display: flex;
  gap: var(--space-3);
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.modern-library__list-actions {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modern-library__list-item:hover .modern-library__list-actions {
  opacity: 1;
}

.modern-library__list-status {
  display: flex;
  gap: var(--space-2);
  min-width: 60px;
}

.modern-library__list-favorite {
  color: #f59e0b;
}

.modern-library__list-shared {
  color: #10b981;
}

/* 空状态 */
.modern-library__empty {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  text-align: center;
}

.modern-library__empty-content {
  max-width: 400px;
}

.modern-library__empty-icon {
  font-size: 4rem;
  color: var(--text-tertiary);
  margin-bottom: var(--space-4);
}

.modern-library__empty-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.modern-library__empty-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .modern-library__toolbar-container {
    flex-direction: column;
    gap: var(--space-4);
    align-items: flex-start;
  }
  
  .modern-library__view-controls {
    flex-direction: column;
    gap: var(--space-4);
    align-items: flex-start;
  }
  
  .modern-library__sort-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .modern-library__grid {
    grid-template-columns: 1fr;
  }
  
  .modern-library__list-item {
    padding: var(--space-3);
  }
  
  .modern-library__list-details {
    flex-direction: column;
    gap: var(--space-1);
  }
}

/* 深色主题适配 */
[data-theme="dark"] .modern-library__toolbar {
  background: rgba(17, 24, 39, 0.8);
  border-bottom-color: var(--border-secondary);
}

[data-theme="dark"] .modern-library__item-tag {
  background: rgba(59, 130, 246, 0.2);
  color: var(--primary-400);
}

[data-theme="dark"] .modern-library__sort-select {
  background: rgba(17, 24, 39, 0.8);
  border-color: var(--border-secondary);
  color: var(--text-primary);
}
</style>