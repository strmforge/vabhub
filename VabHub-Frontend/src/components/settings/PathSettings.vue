<template>
  <div class="path-settings">
    <div class="settings-header">
      <h3>媒体路径设置</h3>
      <el-button type="primary" @click="addPath">添加路径</el-button>
    </div>
    
    <el-table :data="paths" class="path-table">
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="path" label="路径" />
      <el-table-column prop="type" label="类型" width="100">
        <template #default="scope">
          <el-tag>{{ scope.row.type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="enabled" label="启用" width="80">
        <template #default="scope">
          <el-switch v-model="scope.row.enabled" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="editPath(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deletePath(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="currentPath" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="currentPath.name" />
        </el-form-item>
        <el-form-item label="路径">
          <el-input v-model="currentPath.path" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="currentPath.type">
            <el-option label="电影" value="movie" />
            <el-option label="电视剧" value="tv" />
            <el-option label="音乐" value="music" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="currentPath.enabled" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePath">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const paths = ref([
  { id: 1, name: '电影库', path: '/media/movies', type: 'movie', enabled: true },
  { id: 2, name: '电视剧库', path: '/media/tv', type: 'tv', enabled: true }
])

const dialogVisible = ref(false)
const isEditing = ref(false)

const currentPath = reactive({
  id: null,
  name: '',
  path: '',
  type: 'movie',
  enabled: true
})

const dialogTitle = ref('添加路径')

const addPath = () => {
  isEditing.value = false
  dialogTitle.value = '添加路径'
  Object.assign(currentPath, {
    id: null,
    name: '',
    path: '',
    type: 'movie',
    enabled: true
  })
  dialogVisible.value = true
}

const editPath = (path) => {
  isEditing.value = true
  dialogTitle.value = '编辑路径'
  Object.assign(currentPath, { ...path })
  dialogVisible.value = true
}

const deletePath = async (path) => {
  try {
    // 调用后端API删除路径
    const response = await settingsAPI.update({
      paths: paths.value.filter(p => p.id !== path.id)
    })
    
    if (response.success) {
      ElMessage.success(`路径删除成功: ${path.name}`)
      // 从本地列表中移除
      paths.value = paths.value.filter(p => p.id !== path.id)
    } else {
      ElMessage.error('删除失败: ' + response.message)
    }
  } catch (error) {
    ElMessage.error('删除失败: ' + error.message)
  }
}

const savePath = () => {
  if (isEditing.value) {
    // 更新现有路径
    const index = paths.value.findIndex(p => p.id === currentPath.id)
    if (index !== -1) {
      paths.value[index] = { ...currentPath }
    }
    ElMessage.success('路径更新成功')
  } else {
    // 添加新路径
    currentPath.id = Date.now()
    paths.value.push({ ...currentPath })
    ElMessage.success('路径添加成功')
  }
  dialogVisible.value = false
}
</script>

<style scoped>
.path-settings {
  padding: 20px 0;
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.path-table {
  background: #fff;
  border-radius: 8px;
}
</style>