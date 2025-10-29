<template>
  <el-dialog
    v-model="visible"
    :title="isEdit ? '编辑媒体信息' : '媒体详情'"
    width="800px"
    @close="handleClose"
  >
    <el-form :model="form" label-width="100px" v-loading="loading">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="标题">
            <el-input v-model="form.title" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="原标题">
            <el-input v-model="form.original_title" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="类型">
            <el-select v-model="form.type" style="width: 100%">
              <el-option label="电影" value="movie" />
              <el-option label="电视剧" value="tv" />
              <el-option label="音乐" value="music" />
              <el-option label="图片" value="photo" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="年份">
            <el-input-number v-model="form.year" :min="1900" :max="2030" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="评分">
            <el-input-number v-model="form.rating" :min="0" :max="10" :step="0.1" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="海报">
        <el-input v-model="form.poster" placeholder="海报URL" />
      </el-form-item>
      
      <el-form-item label="文件路径">
        <el-input v-model="form.path" readonly />
      </el-form-item>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="文件大小">
            <el-input v-model="form.file_size" readonly>
              <template #append>MB</template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="时长">
            <el-input v-model="form.duration" readonly>
              <template #append>分钟</template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="分辨率">
            <el-input v-model="form.resolution" readonly />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="标签">
        <el-select v-model="form.tags" multiple style="width: 100%">
          <el-option v-for="tag in availableTags" :key="tag" :label="tag" :value="tag" />
        </el-select>
      </el-form-item>
      
      <el-form-item>
        <el-checkbox v-model="form.watched">已观看</el-checkbox>
        <el-checkbox v-model="form.favorite">收藏</el-checkbox>
      </el-form-item>
      
      <el-form-item label="元数据">
        <el-input
          v-model="metadataText"
          type="textarea"
          :rows="4"
          placeholder="元数据（JSON格式）"
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { mediaAPI } from '@/api'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  mediaId: {
    type: String,
    default: ''
  },
  isEdit: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'saved'])

const form = ref({
  title: '',
  original_title: '',
  type: 'movie',
  year: null,
  rating: null,
  poster: '',
  path: '',
  file_size: 0,
  duration: 0,
  resolution: '',
  tags: [],
  watched: false,
  favorite: false,
  metadata: {}
})

const loading = ref(false)
const saving = ref(false)
const availableTags = ref(['动作', '喜剧', '剧情', '科幻', '恐怖', '爱情', '动画', '纪录片'])

const metadataText = computed({
  get: () => {
    try {
      return JSON.stringify(form.value.metadata, null, 2)
    } catch {
      return '{}'
    }
  },
  set: (value) => {
    try {
      form.value.metadata = JSON.parse(value)
    } catch {
      form.value.metadata = {}
    }
  }
})

// 监听visible变化
watch(() => props.visible, (newVal) => {
  if (newVal && props.mediaId) {
    loadMediaDetail()
  } else {
    resetForm()
  }
})

// 加载媒体详情
const loadMediaDetail = async () => {
  if (!props.mediaId) return
  
  loading.value = true
  try {
    const response = await mediaAPI.get(props.mediaId)
    if (response.success) {
      form.value = { ...response.data.media }
      // 转换文件大小和时长
      if (form.value.file_size) {
        form.value.file_size = (form.value.file_size / 1024 / 1024).toFixed(2)
      }
      if (form.value.duration) {
        form.value.duration = Math.round(form.value.duration / 60)
      }
    } else {
      ElMessage.error('获取媒体详情失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('获取媒体详情失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.value = {
    title: '',
    original_title: '',
    type: 'movie',
    year: null,
    rating: null,
    poster: '',
    path: '',
    file_size: 0,
    duration: 0,
    resolution: '',
    tags: [],
    watched: false,
    favorite: false,
    metadata: {}
  }
}

// 关闭对话框
const handleClose = () => {
  emit('update:visible', false)
}

// 保存媒体信息
const handleSave = async () => {
  saving.value = true
  try {
    // 准备更新数据
    const updateData = { ...form.value }
    
    // 转换文件大小和时长
    if (updateData.file_size) {
      updateData.file_size = Math.round(parseFloat(updateData.file_size) * 1024 * 1024)
    }
    if (updateData.duration) {
      updateData.duration = parseInt(updateData.duration) * 60
    }
    
    const response = await mediaAPI.update(props.mediaId, updateData)
    if (response.success) {
      ElMessage.success('媒体信息更新成功')
      emit('saved')
      handleClose()
    } else {
      ElMessage.error('更新失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('更新失败: ' + error.message)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>