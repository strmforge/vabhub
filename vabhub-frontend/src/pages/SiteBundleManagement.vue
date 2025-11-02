<template>
  <div class="site-bundle-management">
    <div class="header">
      <h1>站点包管理</h1>
      <p>管理PT站点的HNR检测规则和配置</p>
    </div>

    <div class="toolbar">
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        创建站点包
      </el-button>
      
      <el-button @click="handleImport">
        <el-icon><Upload /></el-icon>
        导入配置
      </el-button>
      
      <el-input
        v-model="searchKeyword"
        placeholder="搜索站点包..."
        style="width: 300px; margin-left: 16px;"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <div class="content">
      <el-table :data="filteredBundles" v-loading="loading" style="width: 100%">
        <el-table-column prop="name" label="名称" min-width="150">
          <template #default="{ row }">
            <div class="bundle-name">
              <span class="name">{{ row.name }}</span>
              <el-tag v-if="row.version" size="small" type="info">
                v{{ row.version }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="selectors.length" label="选择器数量" width="120" align="center">
          <template #default="{ row }">
            <el-tag>{{ row.selectors.length }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="site_overrides" label="站点覆盖" width="120" align="center">
          <template #default="{ row }">
            <el-tag v-if="Object.keys(row.site_overrides || {}).length > 0" type="success">
              {{ Object.keys(row.site_overrides || {}).length }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editBundle(row)">编辑</el-button>
            <el-button size="small" type="primary" @click="exportBundle(row)">导出</el-button>
            <el-button size="small" type="danger" @click="deleteBundle(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingBundle ? '编辑站点包' : '创建站点包'"
      width="800px"
    >
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入站点包名称" />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="2"
            placeholder="请输入站点包描述"
          />
        </el-form-item>
        
        <el-form-item label="版本" prop="version">
          <el-input v-model="form.version" placeholder="请输入版本号" />
        </el-form-item>
        
        <el-form-item label="选择器" prop="selectors">
          <div class="selectors-editor">
            <div v-for="(selector, index) in form.selectors" :key="index" class="selector-item">
              <el-input
                v-model="form.selectors[index]"
                placeholder="请输入CSS选择器或正则表达式"
              />
              <el-button
                type="danger"
                text
                @click="removeSelector(index)"
                style="margin-left: 8px;"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
            <el-button @click="addSelector" type="primary" text>
              <el-icon><Plus /></el-icon>
              添加选择器
            </el-button>
          </div>
        </el-form-item>
        
        <el-form-item label="站点覆盖">
          <div class="site-overrides-editor">
            <div v-for="(override, siteName) in form.site_overrides" :key="siteName" class="override-item">
              <div class="override-header">
                <span class="site-name">{{ siteName }}</span>
                <el-button type="danger" text @click="removeOverride(siteName)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
              <div class="override-content">
                <el-input
                  v-model="form.site_overrides[siteName]"
                  placeholder="请输入站点特定选择器"
                />
              </div>
            </div>
            <div class="add-override">
              <el-input
                v-model="newSiteName"
                placeholder="站点名称"
                style="width: 200px; margin-right: 8px;"
              />
              <el-button @click="addOverride" type="primary" text>
                添加站点覆盖
              </el-button>
            </div>
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="saveBundle" :loading="saving">
          {{ editingBundle ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog v-model="showImportDialog" title="导入站点包" width="600px">
      <div class="import-content">
        <el-alert
          title="支持YAML或JSON格式的站点包配置"
          type="info"
          :closable="false"
          style="margin-bottom: 16px;"
        />
        
        <el-input
          v-model="importContent"
          type="textarea"
          :rows="10"
          placeholder="请粘贴YAML或JSON格式的站点包配置"
        />
      </div>
      
      <template #footer>
        <el-button @click="showImportDialog = false">取消</el-button>
        <el-button type="primary" @click="handleImportConfirm" :loading="importing">
          导入
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Upload,
  Search,
  Delete,
} from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import ApiService from '@/services/api'

interface SiteBundle {
  id: string
  name: string
  description?: string
  selectors: string[]
  site_overrides: Record<string, string[]>
  version: string
  created_at: string
  updated_at: string
}

const loading = ref(false)
const saving = ref(false)
const importing = ref(false)
const showCreateDialog = ref(false)
const showImportDialog = ref(false)
const searchKeyword = ref('')
const bundles = ref<SiteBundle[]>([])
const editingBundle = ref<SiteBundle | null>(null)
const newSiteName = ref('')
const importContent = ref('')
const formRef = ref<FormInstance>()

const form = ref({
  name: '',
  description: '',
  selectors: [''],
  site_overrides: {} as Record<string, string[]>,
  version: '1.0.0'
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入站点包名称', trigger: 'blur' }],
  version: [{ required: true, message: '请输入版本号', trigger: 'blur' }],
  selectors: [{
    validator: (rule: any, value: any, callback: any) => {
      if (!value || value.length === 0 || value.every((s: string) => !s.trim())) {
        callback(new Error('至少需要一个有效的选择器'))
      } else {
        callback()
      }
    },
    trigger: 'blur'
  }]
}

const filteredBundles = computed(() => {
  if (!searchKeyword.value) return bundles.value
  return bundles.value.filter(bundle =>
    bundle.name.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
    bundle.description?.toLowerCase().includes(searchKeyword.value.toLowerCase())
  )
})

const loadBundles = async () => {
  try {
    loading.value = true
    const response = await ApiService.siteBundle.listBundles()
    bundles.value = response.bundles
  } catch (error) {
    ElMessage.error('加载站点包失败')
  } finally {
    loading.value = false
  }
}

const editBundle = (bundle: SiteBundle) => {
  editingBundle.value = bundle
  form.value = {
    name: bundle.name,
    description: bundle.description || '',
    selectors: [...bundle.selectors],
    site_overrides: { ...bundle.site_overrides },
    version: bundle.version
  }
  showCreateDialog.value = true
}

const saveBundle = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    saving.value = true
    
    const cleanForm = {
      ...form.value,
      selectors: form.value.selectors.filter(s => s.trim()),
      site_overrides: Object.fromEntries(
        Object.entries(form.value.site_overrides)
          .filter(([_, selectors]) => selectors && selectors.length > 0)
      )
    }
    
    if (editingBundle.value) {
      await ApiService.siteBundle.updateBundle(editingBundle.value.id, cleanForm)
      ElMessage.success('站点包更新成功')
    } else {
      await ApiService.siteBundle.createBundle(cleanForm)
      ElMessage.success('站点包创建成功')
    }
    
    showCreateDialog.value = false
    resetForm()
    await loadBundles()
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    saving.value = false
  }
}

const deleteBundle = async (bundle: SiteBundle) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除站点包 "${bundle.name}" 吗？此操作不可恢复。`,
      '确认删除',
      { type: 'warning' }
    )
    
    await ApiService.siteBundle.deleteBundle(bundle.id)
    ElMessage.success('站点包删除成功')
    await loadBundles()
  } catch (error) {
    // 用户取消删除
  }
}

const exportBundle = async (bundle: SiteBundle) => {
  try {
    const response = await ApiService.siteBundle.exportBundle(bundle.id)
    const blob = new Blob([response.content], { type: 'text/yaml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${bundle.name}.yaml`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleImport = () => {
  showImportDialog.value = true
  importContent.value = ''
}

const handleImportConfirm = async () => {
  if (!importContent.value.trim()) {
    ElMessage.warning('请输入要导入的内容')
    return
  }
  
  try {
    importing.value = true
    await ApiService.siteBundle.importBundle(importContent.value)
    ElMessage.success('导入成功')
    showImportDialog.value = false
    await loadBundles()
  } catch (error) {
    ElMessage.error('导入失败')
  } finally {
    importing.value = false
  }
}

const addSelector = () => {
  form.value.selectors.push('')
}

const removeSelector = (index: number) => {
  form.value.selectors.splice(index, 1)
}

const addOverride = () => {
  if (!newSiteName.value.trim()) {
    ElMessage.warning('请输入站点名称')
    return
  }
  
  if (form.value.site_overrides[newSiteName.value]) {
    ElMessage.warning('该站点已存在')
    return
  }
  
  form.value.site_overrides[newSiteName.value] = []
  newSiteName.value = ''
}

const removeOverride = (siteName: string) => {
  delete form.value.site_overrides[siteName]
}

const resetForm = () => {
  form.value = {
    name: '',
    description: '',
    selectors: [''],
    site_overrides: {},
    version: '1.0.0'
  }
  editingBundle.value = null
  newSiteName.value = ''
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

onMounted(() => {
  loadBundles()
})
</script>

<style scoped>
.site-bundle-management {
  padding: 24px;
}

.header {
  margin-bottom: 24px;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.header p {
  margin: 8px 0 0;
  color: #666;
}

.toolbar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.bundle-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bundle-name .name {
  font-weight: 500;
}

.selectors-editor .selector-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.site-overrides-editor .override-item {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  margin-bottom: 8px;
  padding: 8px;
}

.override-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.site-name {
  font-weight: 500;
  color: #409eff;
}

.add-override {
  display: flex;
  align-items: center;
  margin-top: 8px;
}

.import-content {
  max-height: 400px;
  overflow-y: auto;
}
</style>