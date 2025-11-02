<template>
  <el-dropdown 
    trigger="click" 
    placement="bottom-end"
    @command="handleLanguageChange"
    class="language-switcher"
  >
    <span class="language-trigger">
      <el-icon><Globe /></el-icon>
      <span class="language-name">{{ currentLanguage.nativeName }}</span>
      <el-icon class="arrow-icon"><ArrowDown /></el-icon>
    </span>
    
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item 
          v-for="lang in supportedLanguages" 
          :key="lang.code"
          :command="lang.code"
          :class="{ 'active': lang.code === currentLanguage.code }"
        >
          <span class="language-option">
            <span class="flag">{{ lang.flag }}</span>
            <span class="name">{{ lang.nativeName }}</span>
            <span class="english-name">({{ lang.name }})</span>
          </span>
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { Globe, ArrowDown } from '@element-plus/icons-vue'
import { SUPPORTED_LANGUAGES, type SupportedLocale } from '@/types/i18n'
import { getCurrentLanguageConfig, setI18nLanguage } from '@/plugins/i18n'
import { computed } from 'vue'

const supportedLanguages = SUPPORTED_LANGUAGES

const currentLanguage = computed(() => getCurrentLanguageConfig() || SUPPORTED_LANGUAGES[0])

const handleLanguageChange = (locale: SupportedLocale) => {
  if (locale !== currentLanguage.value.code) {
    setI18nLanguage(locale)
    // 触发页面刷新以应用新语言
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
  transition: background-color 0.2s;
  color: var(--el-text-color-regular);
}

.language-trigger:hover {
  background-color: var(--el-fill-color-light);
}

.language-name {
  font-weight: 500;
  font-size: 14px;
}

.arrow-icon {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.language-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

.flag {
  font-size: 16px;
}

.name {
  font-weight: 500;
  min-width: 40px;
}

.english-name {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.el-dropdown-item.active {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.el-dropdown-item.active .english-name {
  color: var(--el-color-primary);
}
</style>