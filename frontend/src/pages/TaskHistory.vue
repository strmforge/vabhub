<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-2">mdi-history</v-icon>
            任务执行历史
            <v-spacer />
            <v-btn
              icon="mdi-refresh"
              variant="text"
              :loading="loading"
              @click="fetchHistory"
            />
          </v-card-title>

          <v-card-text>
            <!-- 过滤器 -->
            <v-row class="mb-4">
              <v-col cols="12" md="4">
                <v-select
                  v-model="filter.taskName"
                  :items="taskNames"
                  label="任务名称"
                  clearable
                  density="compact"
                  @update:model-value="fetchHistory"
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  v-model="filter.status"
                  :items="statusOptions"
                  label="状态"
                  clearable
                  density="compact"
                  @update:model-value="fetchHistory"
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="filter.search"
                  label="搜索"
                  prepend-inner-icon="mdi-magnify"
                  clearable
                  density="compact"
                />
              </v-col>
            </v-row>

            <!-- 数据表格 -->
            <v-data-table
              :headers="headers"
              :items="filteredItems"
              :loading="loading"
              :items-per-page="20"
              class="elevation-1"
            >
              <template #item.status="{ item }">
                <v-chip
                  :color="getStatusColor(item.status)"
                  size="small"
                  variant="tonal"
                >
                  <v-icon start size="small">{{ getStatusIcon(item.status) }}</v-icon>
                  {{ getStatusText(item.status) }}
                </v-chip>
              </template>

              <template #item.started_at="{ item }">
                {{ formatTime(item.started_at) }}
              </template>

              <template #item.duration_ms="{ item }">
                <span v-if="item.duration_ms">
                  {{ formatDuration(item.duration_ms) }}
                </span>
                <span v-else class="text-grey">-</span>
              </template>

              <template #item.message="{ item }">
                <span class="text-truncate d-inline-block" style="max-width: 300px">
                  {{ item.message || '-' }}
                </span>
              </template>

              <template #item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="showDetail(item)"
                />
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 详情对话框 -->
    <v-dialog v-model="detailDialog" max-width="700">
      <v-card v-if="selectedItem">
        <v-card-title>
          <v-icon class="mr-2">mdi-information</v-icon>
          任务详情 #{{ selectedItem.id }}
        </v-card-title>
        <v-card-text>
          <v-list density="compact">
            <v-list-item>
              <template #prepend>
                <v-icon>mdi-tag</v-icon>
              </template>
              <v-list-item-title>任务名称</v-list-item-title>
              <v-list-item-subtitle>{{ selectedItem.task_name }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-checkbox-marked-circle</v-icon>
              </template>
              <v-list-item-title>状态</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip :color="getStatusColor(selectedItem.status)" size="small">
                  {{ getStatusText(selectedItem.status) }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-clock-start</v-icon>
              </template>
              <v-list-item-title>开始时间</v-list-item-title>
              <v-list-item-subtitle>{{ formatTime(selectedItem.started_at) }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="selectedItem.finished_at">
              <template #prepend>
                <v-icon>mdi-clock-end</v-icon>
              </template>
              <v-list-item-title>结束时间</v-list-item-title>
              <v-list-item-subtitle>{{ formatTime(selectedItem.finished_at) }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="selectedItem.duration_ms">
              <template #prepend>
                <v-icon>mdi-timer</v-icon>
              </template>
              <v-list-item-title>耗时</v-list-item-title>
              <v-list-item-subtitle>{{ formatDuration(selectedItem.duration_ms) }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="selectedItem.message">
              <template #prepend>
                <v-icon>mdi-message-text</v-icon>
              </template>
              <v-list-item-title>消息</v-list-item-title>
              <v-list-item-subtitle>{{ selectedItem.message }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="selectedItem.host">
              <template #prepend>
                <v-icon>mdi-server</v-icon>
              </template>
              <v-list-item-title>主机 / PID</v-list-item-title>
              <v-list-item-subtitle>{{ selectedItem.host }} / {{ selectedItem.pid }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <!-- 元数据 -->
          <v-expansion-panels v-if="selectedItem.meta_json && Object.keys(selectedItem.meta_json).length > 0" class="mt-4">
            <v-expansion-panel title="元数据 (meta_json)">
              <v-expansion-panel-text>
                <pre class="text-body-2 bg-grey-lighten-4 pa-2 rounded">{{ JSON.stringify(selectedItem.meta_json, null, 2) }}</pre>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <!-- 错误信息 -->
          <v-alert
            v-if="selectedItem.error_type"
            type="error"
            variant="tonal"
            class="mt-4"
          >
            <div class="font-weight-bold">{{ selectedItem.error_type }}</div>
            <pre v-if="selectedItem.error_traceback" class="text-body-2 mt-2" style="white-space: pre-wrap;">{{ selectedItem.error_traceback }}</pre>
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="detailDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

interface TaskRunHistory {
  id: number
  task_name: string
  task_type: string | null
  status: string
  started_at: string
  finished_at: string | null
  duration_ms: number | null
  message: string | null
  error_type: string | null
  error_traceback: string | null
  meta_json: Record<string, unknown> | null
  host: string | null
  pid: number | null
  created_at: string
}

const loading = ref(false)
const items = ref<TaskRunHistory[]>([])
const taskNames = ref<string[]>([])
const detailDialog = ref(false)
const selectedItem = ref<TaskRunHistory | null>(null)

const filter = ref({
  taskName: null as string | null,
  status: null as string | null,
  search: ''
})

const statusOptions = [
  { title: '运行中', value: 'running' },
  { title: '成功', value: 'success' },
  { title: '失败', value: 'failed' }
]

const headers = [
  { title: 'ID', key: 'id', width: 80 },
  { title: '任务名称', key: 'task_name' },
  { title: '状态', key: 'status', width: 120 },
  { title: '开始时间', key: 'started_at', width: 180 },
  { title: '耗时', key: 'duration_ms', width: 100 },
  { title: '消息', key: 'message' },
  { title: '操作', key: 'actions', width: 80, sortable: false }
]

const filteredItems = computed(() => {
  if (!filter.value.search) return items.value
  const search = filter.value.search.toLowerCase()
  return items.value.filter(item =>
    item.task_name.toLowerCase().includes(search) ||
    (item.message?.toLowerCase().includes(search))
  )
})

async function fetchHistory() {
  loading.value = true
  try {
    const params: Record<string, string | number> = { page: 1, page_size: 100 }
    if (filter.value.taskName) params.task_name = filter.value.taskName
    if (filter.value.status) params.status = filter.value.status

    const response = await api.get('/api/tasks/history', { params })
    items.value = response.data.items || response.data
  } catch (error) {
    console.error('获取任务历史失败:', error)
  } finally {
    loading.value = false
  }
}

async function fetchTaskNames() {
  try {
    const response = await api.get('/api/tasks/names')
    taskNames.value = response.data.names || []
  } catch (error) {
    console.error('获取任务名称列表失败:', error)
  }
}

function showDetail(item: TaskRunHistory) {
  selectedItem.value = item
  detailDialog.value = true
}

function getStatusColor(status: string): string {
  switch (status) {
    case 'success': return 'success'
    case 'failed': return 'error'
    case 'running': return 'info'
    default: return 'grey'
  }
}

function getStatusIcon(status: string): string {
  switch (status) {
    case 'success': return 'mdi-check-circle'
    case 'failed': return 'mdi-alert-circle'
    case 'running': return 'mdi-loading mdi-spin'
    default: return 'mdi-help-circle'
  }
}

function getStatusText(status: string): string {
  switch (status) {
    case 'success': return '成功'
    case 'failed': return '失败'
    case 'running': return '运行中'
    default: return status
  }
}

function formatTime(timeStr: string): string {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
  return `${(ms / 60000).toFixed(1)}m`
}

onMounted(() => {
  fetchHistory()
  fetchTaskNames()
})
</script>
