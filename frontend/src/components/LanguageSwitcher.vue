<template>
  <el-dropdown 
    trigger="click" 
    placement="bottom-end"
    @command="handleLanguageChange"
    class="language-switcher"
  >
    <span class="language-trigger">
      <el-icon><Global /></el-icon>
      <span class="language-name">{{ currentLanguageName }}</span>
      <el-icon><ArrowDown /></el-icon>
    </span>
    
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item 
          v-for="locale in availableLocales" 
          :key="locale.code"
          :command="locale.code"
          :class="{ active: currentLocale === locale.code }"
        >
          <span class="locale-item">
            <span class="flag">{{ getFlagEmoji(locale.code) }}</span>
            <span class="name">{{ locale.name }}</span>
            <el-icon v-if="currentLocale === locale.code" class="check-icon">
              <Check />
            </el-icon>
          </span>
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Global, ArrowDown, Check } from '@element-plus/icons-vue'
import { availableLocales, changeLocale, getCurrentLocale } from '../locales'

const { t } = useI18n()

// 计算属性
const currentLocale = computed(() => getCurrentLocale())

const currentLanguageName = computed(() => {
  const locale = availableLocales.find(locale => locale.code === currentLocale.value)
  return locale ? locale.name : 'Language'
})

// 获取国旗emoji
const getFlagEmoji = (localeCode) => {
  const flagMap = {
    'zh-CN': '🇨🇳',
    'en-US': '🇺🇸'
  }
  return flagMap[localeCode] || '🌐'
}

// 处理语言切换
const handleLanguageChange = (localeCode) => {
  if (localeCode !== currentLocale.value) {
    changeLocale(localeCode)
    // 重新加载页面以应用语言更改
    window.location.reload()
  }
}
</script>

<style scoped>
.language-switcher {
  cursor: pointer;
}

.language-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.language-trigger:hover {
  background-color: var(--el-fill-color-light);
}

.language-name {
  font-size: 14px;
  font-weight: 500;
}

.locale-item {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 120px;
}

.flag {
  font-size: 16px;
}

.name {
  flex: 1;
  font-size: 14px;
}

.check-icon {
  color: var(--el-color-primary);
}

.el-dropdown-item.active {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .language-name {
    display: none;
  }
  
  .language-trigger {
    padding: 8px;
  }
}
</style>