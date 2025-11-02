<template>
  <div class="vab-table-container">
    <!-- 表格工具栏 -->
    <div v-if="showToolbar" class="vab-table-toolbar">
      <div class="toolbar-left">
        <slot name="toolbar-left">
          <el-input
            v-if="showSearch"
            v-model="searchText"
            :placeholder="searchPlaceholder"
            :style="{ width: searchWidth }"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </slot>
      </div>
      
      <div class="toolbar-right">
        <slot name="toolbar-right">
          <el-button
            v-if="showRefresh"
            :icon="Refresh"
            @click="handleRefresh"
            :loading="loading"
          >
            刷新
          </el-button>
          
          <el-button
            v-if="showExport"
            :icon="Download"
            @click="handleExport"
          >
            导出
          </el-button>
        </slot>
      </div>
    </div>
    
    <!-- 数据表格 -->
    <el-table
      ref="tableRef"
      :data="tableData"
      :border="border"
      :stripe="stripe"
      :size="size"
      :fit="fit"
      :show-header="showHeader"
      :highlight-current-row="highlightCurrentRow"
      :row-class-name="rowClassName"
      :row-style="rowStyle"
      :cell-class-name="cellClassName"
      :cell-style="cellStyle"
      :header-row-class-name="headerRowClassName"
      :header-row-style="headerRowStyle"
      :header-cell-class-name="headerCellClassName"
      :header-cell-style="headerCellStyle"
      :empty-text="emptyText"
      :default-expand-all="defaultExpandAll"
      :default-sort="defaultSort"
      :tooltip-effect="tooltipEffect"
      :show-summary="showSummary"
      :sum-text="sumText"
      :summary-method="summaryMethod"
      v-bind="$attrs"
      v-on="$attrs"
      @selection-change="handleSelectionChange"
      @sort-change="handleSortChange"
      @filter-change="handleFilterChange"
      @row-click="handleRowClick"
      @row-dblclick="handleRowDblClick"
    >
      <!-- 选择列 -->
      <el-table-column
        v-if="showSelection"
        type="selection"
        :width="selectionWidth"
        :reserve-selection="reserveSelection"
      />
      
      <!-- 索引列 -->
      <el-table-column
        v-if="showIndex"
        type="index"
        :label="indexLabel"
        :width="indexWidth"
        :align="indexAlign"
      />
      
      <!-- 自定义列 -->
      <slot></slot>
      
      <!-- 操作列 -->
      <el-table-column
        v-if="showAction"
        :label="actionLabel"
        :width="actionWidth"
        :align="actionAlign"
        :fixed="actionFixed"
      >
        <template #default="scope">
          <slot name="action" :row="scope.row" :$index="scope.$index">
            <el-button
              v-if="showEdit"
              link
              type="primary"
              size="small"
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            
            <el-button
              v-if="showDelete"
              link
              type="danger"
              size="small"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </slot>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页器 -->
    <div v-if="showPagination" class="vab-table-pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="pageSizes"
        :layout="paginationLayout"
        :total="total"
        :background="paginationBackground"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { ElTable, ElTableColumn, ElPagination, ElInput, ElButton, ElIcon } from 'element-plus'
import { Search, Refresh, Download } from '@element-plus/icons-vue'

export default {
  name: 'VabTable',
  components: {
    ElTable,
    ElTableColumn,
    ElPagination,
    ElInput,
    ElButton,
    ElIcon,
    Search,
    Refresh,
    Download
  },
  props: {
    // 表格数据
    data: {
      type: Array,
      default: () => []
    },
    
    // 表格配置
    border: {
      type: Boolean,
      default: true
    },
    stripe: {
      type: Boolean,
      default: true
    },
    size: {
      type: String,
      default: 'default'
    },
    fit: {
      type: Boolean,
      default: true
    },
    showHeader: {
      type: Boolean,
      default: true
    },
    highlightCurrentRow: {
      type: Boolean,
      default: false
    },
    
    // 工具栏配置
    showToolbar: {
      type: Boolean,
      default: true
    },
    showSearch: {
      type: Boolean,
      default: true
    },
    searchPlaceholder: {
      type: String,
      default: '请输入搜索内容'
    },
    searchWidth: {
      type: String,
      default: '200px'
    },
    showRefresh: {
      type: Boolean,
      default: true
    },
    showExport: {
      type: Boolean,
      default: false
    },
    
    // 选择列配置
    showSelection: {
      type: Boolean,
      default: false
    },
    selectionWidth: {
      type: Number,
      default: 55
    },
    reserveSelection: {
      type: Boolean,
      default: false
    },
    
    // 索引列配置
    showIndex: {
      type: Boolean,
      default: false
    },
    indexLabel: {
      type: String,
      default: '序号'
    },
    indexWidth: {
      type: Number,
      default: 80
    },
    indexAlign: {
      type: String,
      default: 'center'
    },
    
    // 操作列配置
    showAction: {
      type: Boolean,
      default: false
    },
    actionLabel: {
      type: String,
      default: '操作'
    },
    actionWidth: {
      type: [Number, String],
      default: 'auto'
    },
    actionAlign: {
      type: String,
      default: 'center'
    },
    actionFixed: {
      type: [Boolean, String],
      default: false
    },
    showEdit: {
      type: Boolean,
      default: true
    },
    showDelete: {
      type: Boolean,
      default: true
    },
    
    // 分页配置
    showPagination: {
      type: Boolean,
      default: true
    },
    currentPage: {
      type: Number,
      default: 1
    },
    pageSize: {
      type: Number,
      default: 10
    },
    pageSizes: {
      type: Array,
      default: () => [10, 20, 50, 100]
    },
    paginationLayout: {
      type: String,
      default: 'total, sizes, prev, pager, next, jumper'
    },
    total: {
      type: Number,
      default: 0
    },
    paginationBackground: {
      type: Boolean,
      default: true
    },
    
    // 其他配置
    emptyText: {
      type: String,
      default: '暂无数据'
    },
    defaultExpandAll: {
      type: Boolean,
      default: false
    },
    defaultSort: {
      type: Object,
      default: null
    },
    tooltipEffect: {
      type: String,
      default: 'dark'
    },
    showSummary: {
      type: Boolean,
      default: false
    },
    sumText: {
      type: String,
      default: '合计'
    },
    summaryMethod: {
      type: Function,
      default: null
    },
    
    // 样式回调
    rowClassName: {
      type: Function,
      default: null
    },
    rowStyle: {
      type: Function,
      default: null
    },
    cellClassName: {
      type: Function,
      default: null
    },
    cellStyle: {
      type: Function,
      default: null
    },
    headerRowClassName: {
      type: Function,
      default: null
    },
    headerRowStyle: {
      type: Function,
      default: null
    },
    headerCellClassName: {
      type: Function,
      default: null
    },
    headerCellStyle: {
      type: Function,
      default: null
    }
  },
  emits: [
    'search',
    'refresh',
    'export',
    'selection-change',
    'sort-change',
    'filter-change',
    'row-click',
    'row-dblclick',
    'edit',
    'delete',
    'size-change',
    'current-change'
  ],
  data() {
    return {
      searchText: '',
      loading: false,
      tableData: this.data
    }
  },
  watch: {
    data: {
      handler(newVal) {
        this.tableData = newVal
      },
      deep: true
    }
  },
  methods: {
    // 搜索处理
    handleSearch() {
      this.$emit('search', this.searchText)
    },
    
    // 刷新处理
    async handleRefresh() {
      this.loading = true
      try {
        await this.$emit('refresh')
      } finally {
        this.loading = false
      }
    },
    
    // 导出处理
    handleExport() {
      this.$emit('export')
    },
    
    // 表格事件处理
    handleSelectionChange(selection) {
      this.$emit('selection-change', selection)
    },
    
    handleSortChange(sort) {
      this.$emit('sort-change', sort)
    },
    
    handleFilterChange(filters) {
      this.$emit('filter-change', filters)
    },
    
    handleRowClick(row, column, event) {
      this.$emit('row-click', row, column, event)
    },
    
    handleRowDblClick(row, column, event) {
      this.$emit('row-dblclick', row, column, event)
    },
    
    // 操作处理
    handleEdit(row) {
      this.$emit('edit', row)
    },
    
    handleDelete(row) {
      this.$emit('delete', row)
    },
    
    // 分页处理
    handleSizeChange(size) {
      this.$emit('size-change', size)
    },
    
    handleCurrentChange(page) {
      this.$emit('current-change', page)
    },
    
    // 公共方法
    clearSelection() {
      this.$refs.tableRef?.clearSelection()
    },
    
    toggleRowSelection(row, selected) {
      this.$refs.tableRef?.toggleRowSelection(row, selected)
    },
    
    toggleAllSelection() {
      this.$refs.tableRef?.toggleAllSelection()
    },
    
    sort(prop, order) {
      this.$refs.tableRef?.sort(prop, order)
    }
  }
}
</script>

<style scoped>
.vab-table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.vab-table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
  background-color: var(--el-fill-color-light);
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.vab-table-pagination {
  padding: 16px 20px;
  border-top: 1px solid var(--el-border-color-light);
  background-color: var(--el-fill-color-light);
  display: flex;
  justify-content: center;
}

/* 暗色主题适配 */
[data-theme="dark"] .vab-table-container {
  background-color: var(--el-bg-color);
}

[data-theme="dark"] .vab-table-toolbar,
[data-theme="dark"] .vab-table-pagination {
  background-color: var(--el-fill-color-dark);
  border-color: var(--el-border-color);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .vab-table-toolbar {
    flex-direction: column;
    gap: 12px;
    padding: 12px 16px;
  }
  
  .toolbar-left,
  .toolbar-right {
    width: 100%;
    justify-content: space-between;
  }
  
  .vab-table-pagination {
    padding: 12px 16px;
  }
  
  .el-pagination {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>