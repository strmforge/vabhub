<template>
  <div class="media-list">
    <div class="list-header">
      <el-input
        v-model="searchText"
        placeholder="搜索媒体..."
        style="width: 300px"
        clearable
      />
      <el-button-group>
        <el-button @click="changeView('grid')" :type="viewMode === 'grid' ? 'primary' : ''">
          网格视图
        </el-button>
        <el-button @click="changeView('list')" :type="viewMode === 'list' ? 'primary' : ''">
          列表视图
        </el-button>
      </el-button-group>
    </div>
    
    <div class="list-content">
      <div v-if="viewMode === 'grid'" class="grid-view">
        <div 
          v-for="item in filteredMedia" 
          :key="item.id" 
          class="media-card"
        >
          <img :src="item.poster" :alt="item.title" class="poster" />
          <div class="card-content">
            <h4>{{ item.title }}</h4>
            <p class="year">{{ item.year }}</p>
            <p class="rating">评分: {{ item.rating }}</p>
          </div>
        </div>
      </div>
      
      <el-table v-else :data="filteredMedia" class="list-view">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="year" label="年份" width="100" />
        <el-table-column prop="rating" label="评分" width="100" />
        <el-table-column prop="path" label="路径" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="editMedia(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteMedia(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <div class="list-footer">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
      />
    </div>
    
    <!-- 媒体详情对话框 -->
    <MediaDetail
      v-model:visible="detailVisible"
      :media-id="currentMediaId"
      :is-edit="isEditMode"
      @saved="handleMediaSaved"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { mediaAPI } from '@/api'
import MediaDetail from './MediaDetail.vue'

const props = defineProps({
  mediaType: {
    type: String,
    required: true
  }
})

const searchText = ref('')
const viewMode = ref('grid')
const currentPage = ref(1)
const pageSize = ref(20)
const mediaList = ref([])
const total = ref(0)

// 媒体详情对话框相关
const detailVisible = ref(false)
const currentMediaId = ref('')
const isEditMode = ref(false)

// 从API获取媒体数据
const fetchMedia = async () => {
  try {
    const response = await mediaAPI.list({
      type: props.mediaType,
      search: searchText.value,
      page: currentPage.value,
      page_size: pageSize.value
    })
    
    if (response.success) {
      mediaList.value = response.data.media || []
      total.value = response.data.pagination?.total || 0
    } else {
      ElMessage.error('获取媒体列表失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('获取媒体列表失败: ' + error.message)
  }
}

// 监听搜索和分页变化
watch([searchText, currentPage], () => {
  fetchMedia()
})

// 组件挂载时获取数据
onMounted(() => {
  fetchMedia()
})

const filteredMedia = computed(() => {
  return mediaList.value.filter(item => 
    item.title.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

const changeView = (mode) => {
  viewMode.value = mode
}

const editMedia = async (item) => {
  try {
    currentMediaId.value = item.id
    isEditMode.value = true
    detailVisible.value = true
  } catch (error) {
    ElMessage.error('编辑失败: ' + error.message)
  }
}

const viewMedia = async (item) => {
  try {
    currentMediaId.value = item.id
    isEditMode.value = false
    detailVisible.value = true
  } catch (error) {
    ElMessage.error('查看详情失败: ' + error.message)
  }
}

const handleMediaSaved = () => {
  // 媒体信息保存后刷新列表
  fetchMedia()
}

const deleteMedia = async (item) => {
  try {
    const confirm = await ElMessageBox.confirm(
      `确定要删除媒体 "${item.title}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    if (confirm) {
      const response = await mediaAPI.delete(item.id)
      if (response.success) {
        ElMessage.success('媒体删除成功')
        fetchMedia() // 刷新列表
      } else {
        ElMessage.error('删除失败: ' + response.message)
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + error.message)
    }
  }
}
</script>

<style scoped>
.media-list {
  padding: 20px 0;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.media-card {
  background: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s;
}

.media-card:hover {
  transform: translateY(-2px);
}

.poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.card-content {
  padding: 10px;
}

.card-content h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
}

.year, .rating {
  margin: 0;
  font-size: 12px;
  color: #666;
}

.list-footer {
  margin-top: 20px;
  text-align: center;
}
</style>