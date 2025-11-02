# VabHub Frontend

VabHub 前端界面，基于Vue 3 + TypeScript + Vite构建的现代化Web应用。

## 功能特性

- 🎨 现代化UI设计
- 📱 响应式布局
- ⚡ 快速构建
- 🔧 TypeScript支持
- 🎯 组件化开发
- 🌐 国际化支持（中文、英文）
- 🏗️ 微前端架构（Module Federation）
- 🎵 音乐播放器组件
- 📊 媒体仪表板

## 快速开始

### 环境要求
- Node.js 18+
- npm 9+ 或 yarn 1.22+

### 本地开发
```bash
# 克隆仓库
git clone https://github.com/your-org/vabhub-frontend.git
cd vabhub-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 构建生产版本
```bash
# 构建
npm run build

# 预览生产版本
npm run preview
```

### Docker 运行
```bash
# 构建镜像
docker build -t vabhub-frontend .

# 运行容器
docker run -p 8090:8090 vabhub-frontend
```

## 项目结构

```
vabhub-frontend/
├── src/           # 源代码
│   ├── components/ # Vue组件
│   ├── views/     # 页面视图
│   ├── router/    # 路由配置
│   ├── store/     # 状态管理
│   ├── api/       # API接口
│   └── utils/     # 工具函数
├── public/        # 静态资源
├── dist/          # 构建输出
├── Dockerfile     # 容器配置
├── package.json
└── vite.config.js # Vite配置
```

## 技术栈

- **框架**: Vue 3 + Composition API
- **构建工具**: Vite + Module Federation
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **路由**: Vue Router
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **国际化**: Vue I18n
- **微前端**: Vite Federation Plugin

## 国际化功能

项目支持完整的国际化功能，包含以下特性：

### 支持的语言
- 简体中文 (zh-CN)
- 英语 (en-US)

### 使用方法

在Vue组件中使用国际化：

```vue
<template>
  <div>
    <h1>{{ $t('common.appName') }}</h1>
    <p>{{ $t('auth.loginTitle') }}</p>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>
```

### 语言切换

使用内置的 `LanguageSwitcher` 组件进行语言切换：

```vue
<LanguageSwitcher />
```

## 微前端架构

项目采用基于 Vite Module Federation 的微前端架构：

### 暴露的组件
- `MusicPlayer` - 音乐播放器组件
- `MediaDashboard` - 媒体仪表板组件

### 配置说明

在 `vite.config.ts` 中配置模块联邦：

```typescript
federation({
  name: 'vabhub-frontend',
  filename: 'remoteEntry.js',
  exposes: {
    './MusicPlayer': './src/components/MusicPlayer.vue',
    './MediaDashboard': './src/components/MediaDashboard.vue'
  },
  shared: ['vue', 'vue-router', 'pinia']
})
```

## 国际化功能

项目支持完整的国际化功能，包含以下特性：

### 支持的语言
- 简体中文 (zh-CN)
- 英语 (en-US)

### 使用方法

在Vue组件中使用国际化：

```vue
<template>
  <div>
    <h1>{{ $t('common.appName') }}</h1>
    <p>{{ $t('auth.loginTitle') }}</p>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>
```

### 语言切换

使用内置的 `LanguageSwitcher` 组件进行语言切换：

```vue
<LanguageSwitcher />
```

## 微前端架构

项目采用基于 Vite Module Federation 的微前端架构：

### 暴露的组件
- `MusicPlayer` - 音乐播放器组件
- `MediaDashboard` - 媒体仪表板组件

### 配置说明

在 `vite.config.ts` 中配置模块联邦：

```typescript
federation({
  name: 'vabhub-frontend',
  filename: 'remoteEntry.js',
  exposes: {
    './MusicPlayer': './src/components/MusicPlayer.vue',
    './MediaDashboard': './src/components/MediaDashboard.vue'
  },
  shared: ['vue', 'vue-router', 'pinia']
})
```

## 开发指南

请参考 [CONTRIBUTING.md](CONTRIBUTING.md)