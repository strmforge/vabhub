<template>
  <div class="plugin-config">
    <div class="config-header">
      <h2>{{ pluginName }} 配置</h2>
      <p>配置插件的参数和选项</p>
    </div>

    <!-- 配置表单 -->
    <div class="config-form">
      <div v-for="field in configFields" :key="field.name" class="form-field">
        <label :for="field.name" class="field-label">{{ field.label }}</label>
        
        <!-- 文本输入框 -->
        <input 
          v-if="field.type === 'text' || field.type === 'number'"
          :id="field.name"
          v-model="configData[field.name]"
          :type="field.type"
          :placeholder="field.placeholder"
          class="form-input"
          :min="field.min"
          :max="field.max"
          :step="field.step"
        >
        
        <!-- 选择框 -->
        <select 
          v-else-if="field.type === 'select'"
          :id="field.name"
          v-model="configData[field.name]"
          class="form-select"
        >
          <option 
            v-for="option in field.options" 
            :key="option.value" 
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
        
        <!-- 复选框 -->
        <div v-else-if="field.type === 'checkbox'" class="checkbox-group">
          <label class="checkbox-label">
            <input 
              type="checkbox"
              v-model="configData[field.name]"
              class="checkbox-input"
            >
            <span class="checkbox-text">{{ field.description }}</span>
          </label>
        </div>
        
        <!-- 单选按钮组 -->
        <div v-else-if="field.type === 'radio'" class="radio-group">
          <label 
            v-for="option in field.options" 
            :key="option.value"
            class="radio-label"
          >
            <input 
              type="radio"
              :value="option.value"
              v-model="configData[field.name]"
              class="radio-input"
            >
            <span class="radio-text">{{ option.label }}</span>
          </label>
        </div>
        
        <!-- 文本域 -->
        <textarea 
          v-else-if="field.type === 'textarea'"
          :id="field.name"
          v-model="configData[field.name]"
          :placeholder="field.placeholder"
          :rows="field.rows || 4"
          class="form-textarea"
        ></textarea>
        
        <!-- 文件上传 -->
        <div v-else-if="field.type === 'file'" class="file-upload">
          <input 
            type="file"
            :id="field.name"
            @change="handleFileUpload($event, field.name)"
            class="file-input"
            :accept="field.accept"
          >
          <label :for="field.name" class="file-label">
            <span class="file-icon">📁</span>
            <span class="file-text">选择文件</span>
          </label>
          <span v-if="configData[field.name]" class="file-name">
            {{ configData[field.name].name }}
          </span>
        </div>
        
        <!-- 颜色选择器 -->
        <div v-else-if="field.type === 'color'" class="color-picker">
          <input 
            type="color"
            :id="field.name"
            v-model="configData[field.name]"
            class="color-input"
          >
          <span class="color-value">{{ configData[field.name] }}</span>
        </div>
        
        <!-- 滑块 -->
        <div v-else-if="field.type === 'range'" class="range-group">
          <input 
            type="range"
            :id="field.name"
            v-model="configData[field.name]"
            :min="field.min || 0"
            :max="field.max || 100"
            :step="field.step || 1"
            class="range-input"
          >
          <span class="range-value">{{ configData[field.name] }}</span>
        </div>
        
        <div v-if="field.description" class="field-description">
          {{ field.description }}
        </div>
      </div>
    </div>

    <!-- 配置验证 -->
    <div v-if="validationErrors.length > 0" class="validation-errors">
      <h4>配置错误</h4>
      <ul>
        <li v-for="error in validationErrors" :key="error">{{ error }}</li>
      </ul>
    </div>

    <!-- 操作按钮 -->
    <div class="config-actions">
      <button 
        class="btn btn-secondary" 
        @click="resetConfig"
        :disabled="isSaving"
      >
        重置
      </button>
      <button 
        class="btn btn-secondary" 
        @click="testConfig"
        :disabled="isSaving"
      >
        测试配置
      </button>
      <button 
        class="btn btn-primary" 
        @click="saveConfig"
        :disabled="isSaving || validationErrors.length > 0"
      >
        {{ isSaving ? '保存中...' : '保存配置' }}
      </button>
    </div>

    <!-- 配置预览 -->
    <div class="config-preview">
      <h4>配置预览</h4>
      <pre class="preview-content">{{ JSON.stringify(configData, null, 2) }}</pre>
    </div>

    <!-- 测试结果 -->
    <div v-if="testResult" class="test-result" :class="{ success: testResult.success, error: !testResult.success }">
      <h4>测试结果</h4>
      <p>{{ testResult.message }}</p>
      <pre v-if="testResult.details" class="test-details">{{ testResult.details }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PluginConfig',
  props: {
    pluginId: {
      type: String,
      required: true
    },
    pluginName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isSaving: false,
      testResult: null,
      configData: {},
      originalConfig: {},
      configFields: [
        {
          name: 'autoScan',
          label: '自动扫描',
          type: 'checkbox',
          description: '启用自动扫描媒体文件',
          default: true
        },
        {
          name: 'cacheSize',
          label: '缓存大小',
          type: 'number',
          description: '设置缓存大小（MB）',
          placeholder: '输入缓存大小',
          min: 10,
          max: 10000,
          default: 1000
        },
        {
          name: 'scanInterval',
          label: '扫描间隔',
          type: 'select',
          description: '设置自动扫描的时间间隔',
          options: [
            { value: 'hourly', label: '每小时' },
            { value: 'daily', label: '每天' },
            { value: 'weekly', label: '每周' }
          ],
          default: 'daily'
        },
        {
          name: 'fileTypes',
          label: '支持的文件类型',
          type: 'text',
          description: '输入支持的文件扩展名，用逗号分隔',
          placeholder: '例如: mp4,avi,mkv',
          default: 'mp4,avi,mkv,mov'
        },
        {
          name: 'quality',
          label: '视频质量',
          type: 'radio',
          description: '选择默认视频质量',
          options: [
            { value: 'low', label: '低质量' },
            { value: 'medium', label: '中等质量' },
            { value: 'high', label: '高质量' }
          ],
          default: 'medium'
        },
        {
          name: 'themeColor',
          label: '主题颜色',
          type: 'color',
          description: '选择插件的主题颜色',
          default: '#3498db'
        },
        {
          name: 'volume',
          label: '音量',
          type: 'range',
          description: '设置默认音量',
          min: 0,
          max: 100,
          step: 1,
          default: 80
        },
        {
          name: 'description',
          label: '描述',
          type: 'textarea',
          description: '输入插件的详细描述',
          placeholder: '请输入插件描述...',
          rows: 3,
          default: ''
        }
      ]
    }
  },
  computed: {
    validationErrors() {
      const errors = []
      
      this.configFields.forEach(field => {
        const value = this.configData[field.name]
        
        // 必填字段验证
        if (field.required && !value) {
          errors.push(`${field.label} 是必填字段`)
        }
        
        // 数字范围验证
        if (field.type === 'number' && value !== undefined) {
          if (field.min !== undefined && value < field.min) {
            errors.push(`${field.label} 不能小于 ${field.min}`)
          }
          if (field.max !== undefined && value > field.max) {
            errors.push(`${field.label} 不能大于 ${field.max}`)
          }
        }
        
        // 正则表达式验证
        if (field.pattern && value) {
          const regex = new RegExp(field.pattern)
          if (!regex.test(value)) {
            errors.push(`${field.label} 格式不正确`)
          }
        }
      })
      
      return errors
    }
  },
  methods: {
    async loadConfig() {
      try {
        // 模拟从后端加载配置
        const defaultConfig = {}
        this.configFields.forEach(field => {
          defaultConfig[field.name] = field.default || ''
        })
        
        this.configData = { ...defaultConfig }
        this.originalConfig = { ...defaultConfig }
        
        console.log(`加载插件 ${this.pluginId} 的配置`)
      } catch (error) {
        console.error('加载配置失败:', error)
      }
    },
    
    async saveConfig() {
      if (this.validationErrors.length > 0) {
        return
      }
      
      this.isSaving = true
      
      try {
        // 模拟保存到后端
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        this.originalConfig = { ...this.configData }
        console.log('配置保存成功:', this.configData)
        
        this.$emit('config-saved', {
          pluginId: this.pluginId,
          config: this.configData
        })
      } catch (error) {
        console.error('保存配置失败:', error)
      } finally {
        this.isSaving = false
      }
    },
    
    resetConfig() {
      this.configData = { ...this.originalConfig }
      this.testResult = null
      console.log('配置已重置')
    },
    
    async testConfig() {
      try {
        // 模拟配置测试
        await new Promise(resolve => setTimeout(resolve, 500))
        
        const success = Math.random() > 0.3 // 70% 成功率
        
        this.testResult = {
          success,
          message: success ? '配置测试通过' : '配置测试失败',
          details: success ? '所有配置项验证通过' : '请检查配置参数'
        }
        
        console.log('配置测试完成:', this.testResult)
      } catch (error) {
        this.testResult = {
          success: false,
          message: '测试过程中发生错误',
          details: error.message
        }
      }
    },
    
    handleFileUpload(event, fieldName) {
      const file = event.target.files[0]
      if (file) {
        this.configData[fieldName] = file
        console.log('文件已选择:', file.name)
      }
    }
  },
  mounted() {
    this.loadConfig()
  },
  watch: {
    pluginId: {
      immediate: true,
      handler() {
        this.loadConfig()
      }
    }
  }
}
</script>

<style scoped>
.plugin-config {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.config-header {
  text-align: center;
  margin-bottom: 2rem;
}

.config-header h2 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.config-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-field {
  margin-bottom: 1.5rem;
}

.field-label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.3s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #3498db;
}

.checkbox-group, .radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-label, .radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-input, .radio-input {
  margin: 0;
}

.file-upload {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.file-input {
  display: none;
}

.file-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.file-label:hover {
  background: #e9ecef;
}

.file-name {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.color-picker {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.color-input {
  width: 60px;
  height: 40px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.range-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.range-input {
  flex: 1;
}

.range-value {
  min-width: 40px;
  text-align: center;
  font-weight: 600;
  color: #3498db;
}

.field-description {
  font-size: 0.8rem;
  color: #7f8c8d;
  margin-top: 0.25rem;
}

.validation-errors {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.validation-errors h4 {
  margin: 0 0 0.5rem 0;
}

.validation-errors ul {
  margin: 0;
  padding-left: 1.5rem;
}

.config-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-bottom: 2rem;
}

.config-preview {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 6px;
  margin-bottom: 2rem;
}

.config-preview h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.preview-content {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  max-height: 200px;
  overflow: auto;
}

.test-result {
  padding: 1.5rem;
  border-radius: 6px;
  margin-bottom: 2rem;
}

.test-result.success {
  background: #d4edda;
  color: #155724;
}

.test-result.error {
  background: #f8d7da;
  color: #721c24;
}

.test-result h4 {
  margin: 0 0 0.5rem 0;
}

.test-details {
  background: rgba(255, 255, 255, 0.5);
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  max-height: 150px;
  overflow: auto;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .plugin-config {
    padding: 1rem;
  }
  
  .config-form {
    padding: 1rem;
  }
  
  .config-actions {
    flex-direction: column;
  }
  
  .file-upload, .color-picker, .range-group {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>