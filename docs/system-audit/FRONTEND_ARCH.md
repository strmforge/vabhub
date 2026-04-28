# VabHub 前端架构 (FRONTEND_ARCH)

> 审计 Commit: `9af3cd0e02012aeadf7c72275ac1d62159bbd56c`

---

## 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 框架 | Vue 3 | ^3.4.21 |
| UI 库 | Vuetify | ^3.5.10 |
| 状态管理 | Pinia | ^2.1.7 |
| 路由 | vue-router | ^4.3.0 |
| HTTP | Axios | ^1.6.7 |
| 构建 | Vite | ^5.1.0 |
| 语言 | TypeScript | ~5.3.3 |

---

## 目录结构

```
frontend/src/
├── main.ts              # 应用入口
├── App.vue              # 根组件
├── router/              # 路由配置
│   └── index.ts
├── stores/              # Pinia 状态管理
│   ├── app.ts           # 应用状态
│   ├── auth.ts          # 认证状态
│   ├── dashboard.ts     # 仪表盘状态
│   ├── notification.ts  # 通知状态
│   ├── search.ts        # 搜索状态
│   ├── siteManager.ts   # 站点管理状态
│   └── cookiecloud.ts   # CookieCloud 状态
├── services/            # API 服务
│   └── api.ts           # Axios 封装
├── pages/               # 页面组件 (90+)
├── components/          # 通用组件 (134+)
├── layouts/             # 布局组件
├── composables/         # 组合式函数
├── types/               # TypeScript 类型
├── utils/               # 工具函数
└── styles/              # 样式文件
```

---

## 路由与页面

### 路由配置

**文件**: `frontend/src/router/index.ts`

- 使用 `createWebHistory` (HTML5 History 模式)
- 路由守卫：检查 `requiresAuth` meta 字段
- 懒加载：使用动态 `import()` 加载页面

### 页面清单 (90+)

#### 影视中心
| 路由 | 页面 | 用途 |
|------|------|------|
| `/` | `HomeDashboard.vue` | 首页仪表盘 |
| `/discover` | `Discover.vue` | 发现页 |
| `/calendar` | `Calendar.vue` | 日历追更 |
| `/player-wall` | `PlayerWall.vue` | 电视墙 |
| `/media/:id` | `MediaDetail.vue` | 媒体详情 |

#### 下载 & 订阅
| 路由 | 页面 | 用途 |
|------|------|------|
| `/search` | `Search.vue` | 资源搜索 |
| `/downloads` | `Downloads.vue` | 下载管理 |
| `/subscriptions/*` | `Subscriptions.vue` | 订阅管理 |
| `/rss-subscriptions` | `RSSSubscriptions.vue` | RSS 订阅 |
| `/rsshub` | `RSSHub.vue` | RSSHub 订阅 |

#### 阅读中心
| 路由 | 页面 | 用途 |
|------|------|------|
| `/reading-hub` | `reading/ReadingHubPage.vue` | 阅读中心 |
| `/novel-center` | `NovelCenter.vue` | 小说中心 |
| `/novel-reader/:id` | `NovelReader.vue` | 小说阅读器 |
| `/audiobook-center` | `AudiobookCenter.vue` | 有声书中心 |
| `/tts-center` | `TTSCenter.vue` | TTS 中心 |

#### 漫画中心
| 路由 | 页面 | 用途 |
|------|------|------|
| `/manga/library` | `manga/MangaLibraryPage.vue` | 漫画库 |
| `/manga/follow` | `manga/MangaFollowCenterPage.vue` | 漫画追更 |
| `/manga/remote` | `manga/MangaRemoteExplorerPage.vue` | 远程漫画 |
| `/manga/sources` | `manga/MangaSourceBrowserPage.vue` | 漫画源 |

#### 音乐中心
| 路由 | 页面 | 用途 |
|------|------|------|
| `/music` | `MusicCenter.vue` | 音乐中心 |
| `/music/subscriptions` | `MusicSubscriptions.vue` | 音乐订阅 |

#### AI 中心
| 路由 | 页面 | 用途 |
|------|------|------|
| `/ai-lab` | `AiLab.vue` | AI 实验室 |
| `/ai-log-doctor` | `AiLogDoctor.vue` | AI 故障医生 |
| `/ai-cleanup-advisor` | `AiCleanupAdvisor.vue` | AI 整理顾问 |
| `/ai-reading-assistant` | `AiReadingAssistant.vue` | AI 阅读助手 |
| `/ai-subs-assistant` | `AiSubsAssistant.vue` | AI 订阅助手 |
| `/recommendations` | `Recommendations.vue` | 推荐 |

#### 站点 & 安全
| 路由 | 页面 | 用途 |
|------|------|------|
| `/site-manager` | `SiteManager.vue` | 站点管理 |
| `/hnr-monitoring` | `HNRMonitoring.vue` | HNR 监控 |
| `/plugins` | `Plugins.vue` | 插件管理 |

#### 系统 & 设置
| 路由 | 页面 | 用途 |
|------|------|------|
| `/settings` | `Settings.vue` | 系统设置 |
| `/logs` | `LogCenter.vue` | 日志中心 |
| `/notifications` | `Notifications.vue` | 通知中心 |
| `/scheduler` | `SchedulerMonitor.vue` | 调度监控 |
| `/storage-monitor` | `StorageMonitor.vue` | 存储监控 |

---

## 布局与导航

### 布局组件

**目录**: `frontend/src/layouts/`

```
layouts/
├── DefaultLayout.vue    # 默认布局（带侧边栏）
└── components/
    ├── AppDrawer.vue    # 侧边导航抽屉
    ├── AppBar.vue       # 顶部栏
    └── ...
```

### 导航结构 (AppDrawer.vue)

```
影视中心
├── 首页总览
├── 电视墙
├── 媒体库
├── 发现
├── 日历
└── 短剧

下载 & 订阅
├── 搜索
├── 下载管理
├── 订阅管理
├── RSS 订阅
└── RSSHub 订阅

阅读 & 听书 & 漫画
├── 阅读中心
├── 小说中心
├── 有声书中心
├── TTS 有声书
├── 本地漫画库
├── 漫画追更中心
├── 远程漫画
├── 第三方漫画源
└── 阅读历史

音乐中心
├── 音乐库
└── 榜单 & 订阅

AI 中心
├── AI 实验室
├── AI 订阅助手
├── AI 故障医生
├── AI 整理顾问
├── AI 阅读助手
└── AI 推荐

站点 & 安全
├── 站点管理
├── HNR 风险检测
└── 插件市场

系统 & 设置
├── 系统设置
├── 通知中心
├── 任务中心
├── 实时日志
├── 存储监控
├── 调度器监控
├── 系统自检
├── 云存储管理
├── 媒体服务器
└── 系统控制台
```

---

## 状态管理 (Pinia)

### Store 清单

| Store | 文件 | 职责 |
|-------|------|------|
| `useAppStore` | `app.ts` | 应用全局状态（drawer、theme） |
| `useAuthStore` | `auth.ts` | 认证状态（token、user） |
| `useDashboardStore` | `dashboard.ts` | 仪表盘数据 |
| `useNotificationStore` | `notification.ts` | 通知状态 |
| `useSearchStore` | `search.ts` | 搜索状态 |
| `useSiteManagerStore` | `siteManager.ts` | 站点管理状态 |
| `useCookieCloudStore` | `cookiecloud.ts` | CookieCloud 状态 |

### 状态模式

```typescript
// 典型 store 结构
export const useAppStore = defineStore('app', {
  state: () => ({
    drawer: true,
    theme: 'dark'
  }),
  actions: {
    setDrawer(value: boolean) {
      this.drawer = value
    }
  }
})
```

---

## API 客户端

### 配置

**文件**: `frontend/src/services/api.ts`

```typescript
const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器：添加 JWT Token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：统一错误处理
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 跳转登录
    }
    return Promise.reject(error)
  }
)
```

### API 服务分组

| 服务 | 对应 API | 用途 |
|------|----------|------|
| `authApi` | `/auth/*` | 认证 |
| `searchApi` | `/search/*` | 搜索 |
| `subscriptionApi` | `/subscriptions/*` | 订阅 |
| `downloadApi` | `/downloads/*` | 下载 |
| `mediaApi` | `/media/*` | 媒体 |
| `musicApi` | `/music/*` | 音乐 |
| `discoverApi` | `/discover/*` | 发现页 |
| `chartsApi` | `/charts/*` | 榜单 |
| `logCenterApi` | `/log-center/*` | 日志 |
| `siteApi` | `/sites/*` | 站点 |
| `pluginApi` | `/plugins/*` | 插件 |

---

## 关键页面组件树

### Discover.vue (发现页)

```
Discover.vue
├── PageHeader
├── v-alert (数据源状态)
├── v-tabs (分类切换)
└── v-row
    └── v-col * N
        └── MediaCard (媒体卡片)
            ├── v-img (海报)
            ├── 标题
            ├── 评分
            └── 操作按钮
```

### MusicCenter.vue (音乐中心)

```
MusicCenter.vue
├── PageHeader
├── 统计卡片 (艺术家/专辑/曲目/大小)
├── v-tabs
│   ├── 我的音乐
│   │   ├── v-tabs (专辑/艺术家/曲目)
│   │   └── 内容列表
│   ├── 榜单 & 订阅
│   │   ├── 榜单选择器
│   │   ├── 我的订阅列表
│   │   └── 榜单曲目表
│   └── 音乐任务
│       └── 任务列表
└── 播放器组件
```

### LogCenter.vue (日志中心)

```
LogCenter.vue
├── PageHeader
├── 统计卡片 (总日志/错误/警告/连接状态)
├── 过滤工具栏
│   ├── 日志级别选择
│   ├── 日志来源选择
│   └── 关键词搜索
└── 日志显示区
    ├── 控制按钮 (暂停/导出/清空)
    └── 日志条目列表
        └── LogEntry * N
            ├── 时间戳
            ├── 级别标签
            ├── 来源
            └── 消息内容
```

---

## 错误处理与空态

### 空态处理模式

```vue
<!-- 典型空态处理 -->
<template>
  <v-progress-linear v-if="loading" indeterminate />
  
  <v-alert v-else-if="error" type="error">
    {{ error.message }}
    <v-btn @click="retry">重试</v-btn>
  </v-alert>
  
  <div v-else-if="items.length === 0" class="text-center py-8">
    <v-icon size="64">mdi-inbox-outline</v-icon>
    <p>暂无数据</p>
  </div>
  
  <div v-else>
    <!-- 正常内容 -->
  </div>
</template>
```

### Toast 通知

使用 `vue-toastification` 处理操作反馈：

```typescript
import { useToast } from 'vue-toastification'
const toast = useToast()

toast.success('操作成功')
toast.error('操作失败')
toast.warning('警告信息')
```

---

## Evidence (P4)

### 执行命令

```
read_file: frontend/src/router/index.ts (1-150)
list_dir: frontend/src/stores
list_dir: frontend/src/pages
```

### 关键发现

1. **90+ 页面组件** 覆盖全功能
2. **7 个 Pinia Store** 管理状态
3. **统一 API 客户端** 带拦截器
4. **空态处理** 基本覆盖

### 引用文件路径

1. `frontend/src/main.ts`
2. `frontend/src/App.vue`
3. `frontend/src/router/index.ts`
4. `frontend/src/services/api.ts`
5. `frontend/src/stores/app.ts`
6. `frontend/src/stores/auth.ts`
7. `frontend/src/layouts/components/AppDrawer.vue`
8. `frontend/src/pages/Discover.vue`
9. `frontend/src/pages/MusicCenter.vue`
10. `frontend/src/pages/LogCenter.vue`
11. `frontend/src/pages/Settings.vue`
12. `frontend/src/pages/HomeDashboard.vue`
13. `frontend/src/components/`
14. `frontend/src/types/`
15. `frontend/src/utils/`

---

*生成时间: 2025-12-13 23:22 UTC+8*
