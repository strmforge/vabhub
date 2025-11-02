// UI组件库统一规范

// 基础按钮组件
export const BaseButton = {
  name: 'BaseButton',
  props: {
    type: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'info'].includes(value)
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  template: `
    <button 
      :class="['btn', `btn-${type}`, `btn-${size}`]"
      :disabled="disabled || loading"
      class="base-button"
    >
      <span v-if="loading" class="btn-loading"></span>
      <slot></slot>
    </button>
  `
}

// 基础卡片组件
export const BaseCard = {
  name: 'BaseCard',
  props: {
    title: String,
    shadow: {
      type: String,
      default: 'always',
      validator: (value) => ['always', 'hover', 'never'].includes(value)
    }
  },
  template: `
    <div :class="['card', `card-shadow-${shadow}`]">
      <div v-if="title" class="card-header">
        <h3 class="card-title">{{ title }}</h3>
      </div>
      <div class="card-body">
        <slot></slot>
      </div>
    </div>
  `
}

// 基础模态框组件
export const BaseModal = {
  name: 'BaseModal',
  props: {
    show: Boolean,
    title: String,
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large', 'full'].includes(value)
    }
  },
  emits: ['update:show'],
  template: `
    <div v-if="show" class="modal-overlay" @click="$emit('update:show', false)">
      <div :class="['modal', `modal-${size}`]" @click.stop>
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="modal-close" @click="$emit('update:show', false)">×</button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  `
}

// 基础表格组件
export const BaseTable = {
  name: 'BaseTable',
  props: {
    data: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  template: `
    <div class="base-table">
      <table class="table">
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key">
              {{ column.title }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in data" :key="index">
            <td v-for="column in columns" :key="column.key">
              <slot :name="column.key" :row="row">
                {{ row[column.key] }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="loading" class="table-loading">
        <div class="loading-spinner"></div>
        <span>加载中...</span>
      </div>
      <div v-if="!loading && data.length === 0" class="table-empty">
        暂无数据
      </div>
    </div>
  `
}

// 基础表单组件
export const BaseForm = {
  name: 'BaseForm',
  props: {
    model: {
      type: Object,
      required: true
    },
    rules: {
      type: Object,
      default: () => ({})
    },
    labelWidth: {
      type: String,
      default: '100px'
    }
  },
  emits: ['submit'],
  methods: {
    validate() {
      // 表单验证逻辑
      return Promise.resolve(true)
    }
  },
  template: `
    <form @submit.prevent="$emit('submit', model)" class="base-form">
      <slot></slot>
    </form>
  `
}

// 基础输入框组件
export const BaseInput = {
  name: 'BaseInput',
  props: {
    modelValue: [String, Number],
    type: {
      type: String,
      default: 'text'
    },
    placeholder: String,
    disabled: Boolean
  },
  emits: ['update:modelValue'],
  template: `
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      @input="$emit('update:modelValue', $event.target.value)"
      class="form-input"
    />
  `
}

// 基础选择器组件
export const BaseSelect = {
  name: 'BaseSelect',
  props: {
    modelValue: [String, Number, Array],
    options: {
      type: Array,
      default: () => []
    },
    multiple: Boolean,
    placeholder: String
  },
  emits: ['update:modelValue'],
  template: `
    <select
      :value="modelValue"
      :multiple="multiple"
      @change="$emit('update:modelValue', $event.target.value)"
      class="form-select"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <option 
        v-for="option in options" 
        :key="option.value" 
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  `
}

// 基础加载组件
export const BaseLoading = {
  name: 'BaseLoading',
  props: {
    text: {
      type: String,
      default: '加载中...'
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    }
  },
  template: `
    <div :class="['loading', `loading-${size}`]">
      <div class="loading-spinner"></div>
      <span class="loading-text">{{ text }}</span>
    </div>
  `
}

// 基础消息提示组件
export const BaseMessage = {
  name: 'BaseMessage',
  props: {
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'warning', 'error', 'info'].includes(value)
    },
    message: String,
    duration: {
      type: Number,
      default: 3000
    }
  },
  mounted() {
    if (this.duration > 0) {
      setTimeout(() => {
        this.$emit('close')
      }, this.duration)
    }
  },
  template: `
    <div :class="['message', `message-${type}`]">
      <span class="message-content">{{ message }}</span>
      <button class="message-close" @click="$emit('close')">×</button>
    </div>
  `
}

// 导出所有组件
export default {
  BaseButton,
  BaseCard,
  BaseModal,
  BaseTable,
  BaseForm,
  BaseInput,
  BaseSelect,
  BaseLoading,
  BaseMessage
}