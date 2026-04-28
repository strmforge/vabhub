# VabHub 仓库结构图 (REPO_MAP)

> 按功能域分类，标注每个目录的职责

---

## 仓库根目录

```
VabHub/
├── backend/          # 后端 FastAPI 应用
├── frontend/         # 前端 Vue 3 应用
├── docs/             # 项目文档
├── scripts/          # 开发/部署脚本
├── services/         # 微服务（Intel Center, Mesh Scheduler）
├── deploy/           # 部署配置
├── docker/           # Docker 相关
├── plugins/          # 插件目录
├── plugins-example/  # 插件示例
├── resources/        # 静态资源（站点配置）
├── templates/        # 模板（插件模板）
├── config/           # 运行时配置
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── CHANGELOG.md
```

---

## 功能域划分

### 1. 影视中心 (Media Center)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/discover.py` | 发现页 API（多源聚合） |
| `backend/app/api/media.py` | 媒体详情/搜索 |
| `backend/app/api/library.py` | 媒体库 API |
| `backend/app/api/calendar.py` | 日历/追更 |
| `backend/app/api/player_wall.py` | 电视墙 |
| `backend/app/services/discover_service.py` | 发现页聚合服务 |
| `backend/app/modules/video/` | 视频处理模块 |
| `backend/app/modules/strm/` | STRM 文件生成 |
| `backend/app/modules/media_renamer/` | 媒体重命名 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/Discover.vue` | 发现页 |
| `frontend/src/pages/HomeDashboard.vue` | 首页仪表盘 |
| `frontend/src/pages/MediaDetail.vue` | 媒体详情 |
| `frontend/src/pages/PlayerWall.vue` | 电视墙 |
| `frontend/src/pages/Calendar.vue` | 日历追更 |

---

### 2. 下载 & 订阅 (Download & Subscription)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/subscription.py` | 订阅规则 API |
| `backend/app/api/download.py` | 下载管理 API |
| `backend/app/api/search.py` | 资源搜索 API |
| `backend/app/api/rss.py` | RSS 订阅 |
| `backend/app/api/rsshub.py` | RSSHub 集成 |
| `backend/app/modules/subscription/` | 订阅服务 |
| `backend/app/modules/download/` | 下载器集成 |
| `backend/app/modules/search/` | 搜索引擎 |
| `backend/app/modules/rss/` | RSS 解析 |
| `backend/app/modules/rsshub/` | RSSHub 客户端 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/Subscriptions.vue` | 订阅管理 |
| `frontend/src/pages/Downloads.vue` | 下载管理 |
| `frontend/src/pages/Search.vue` | 资源搜索 |
| `frontend/src/pages/RSSHub.vue` | RSSHub 订阅 |
| `frontend/src/pages/RSSSubscriptions.vue` | RSS 订阅 |

---

### 3. 阅读 & 听书 & 漫画 (Reading Hub)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/novel_center.py` | 小说中心 |
| `backend/app/api/novel_reader.py` | 小说阅读器 |
| `backend/app/api/audiobook.py` | 有声书 API |
| `backend/app/api/audiobook_center.py` | 有声书中心 |
| `backend/app/api/manga_local.py` | 本地漫画 |
| `backend/app/api/manga_remote.py` | 远程漫画源 |
| `backend/app/api/manga_follow.py` | 漫画追更 |
| `backend/app/api/ebook.py` | 电子书 API |
| `backend/app/api/reading_hub.py` | 阅读中心 |
| `backend/app/modules/novel/` | 小说模块 |
| `backend/app/modules/audiobook/` | 有声书模块 |
| `backend/app/modules/comic/` | 漫画模块 |
| `backend/app/modules/ebook/` | 电子书模块 |
| `backend/app/modules/tts/` | TTS 语音合成 |
| `backend/app/modules/manga_sources/` | 漫画源适配 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/NovelCenter.vue` | 小说中心 |
| `frontend/src/pages/NovelReader.vue` | 小说阅读器 |
| `frontend/src/pages/AudiobookCenter.vue` | 有声书中心 |
| `frontend/src/pages/TTSCenter.vue` | TTS 中心 |
| `frontend/src/pages/manga/` | 漫画页面组 |
| `frontend/src/pages/reading/` | 阅读页面组 |

---

### 4. 音乐中心 (Music Center)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/music.py` | 音乐库 API |
| `backend/app/api/music_home.py` | 音乐首页 |
| `backend/app/api/music_chart_admin.py` | 榜单管理 |
| `backend/app/api/music_subscription.py` | 音乐订阅 |
| `backend/app/api/charts.py` | 榜单 API |
| `backend/app/modules/music/` | 音乐模块 |
| `backend/app/modules/music_charts/` | 榜单数据 |
| `backend/app/modules/charts/` | 榜单服务 |
| `backend/app/services/music_discover_service.py` | 音乐发现服务 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/MusicCenter.vue` | 音乐中心 |
| `frontend/src/pages/MusicSubscriptions.vue` | 音乐订阅 |

---

### 5. AI 中心 (AI Center)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/ai_orchestrator.py` | AI 编排器 |
| `backend/app/api/ai_log_doctor.py` | AI 故障诊断 |
| `backend/app/api/ai_cleanup_advisor.py` | AI 清理建议 |
| `backend/app/api/ai_reading_assistant.py` | AI 阅读助手 |
| `backend/app/api/ai_subs_workflow.py` | AI 订阅助手 |
| `backend/app/api/recommendation.py` | 推荐系统 |
| `backend/app/modules/recommendation/` | 推荐算法 |
| `backend/app/modules/multimodal/` | 多模态处理 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/AiLab.vue` | AI 实验室 |
| `frontend/src/pages/AiLogDoctor.vue` | AI 故障医生 |
| `frontend/src/pages/AiCleanupAdvisor.vue` | AI 整理顾问 |
| `frontend/src/pages/AiReadingAssistant.vue` | AI 阅读助手 |
| `frontend/src/pages/AiSubsAssistant.vue` | AI 订阅助手 |
| `frontend/src/pages/Recommendations.vue` | 推荐 |

---

### 6. 站点 & 安全 (Sites & Security)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/site.py` | 站点 API |
| `backend/app/api/site_manager.py` | 站点管理 |
| `backend/app/api/site_ai_adapter.py` | AI 站点适配 |
| `backend/app/api/cookiecloud.py` | CookieCloud |
| `backend/app/api/hnr.py` | HNR 风险检测 |
| `backend/app/api/seeding.py` | 做种管理 |
| `backend/app/modules/site/` | 站点模块 |
| `backend/app/modules/site_manager/` | 站点管理器 |
| `backend/app/modules/hnr/` | HNR 检测 |
| `backend/app/modules/safety/` | 安全策略 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/SiteManager.vue` | 站点管理 |
| `frontend/src/pages/Sites.vue` | 站点列表 |
| `frontend/src/pages/HNRMonitoring.vue` | HNR 监控 |

---

### 7. 系统 & 设置 (System & Settings)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/settings.py` | 设置 API |
| `backend/app/api/system_settings.py` | 系统设置 |
| `backend/app/api/auth.py` | 认证 API |
| `backend/app/api/health.py` | 健康检查 |
| `backend/app/api/log_center.py` | 日志中心 |
| `backend/app/api/scheduler.py` | 调度器 API |
| `backend/app/api/backup.py` | 备份 API |
| `backend/app/api/notification.py` | 通知 API |
| `backend/app/modules/log_center/` | 日志服务 |
| `backend/app/modules/notification/` | 通知模块 |
| `backend/app/modules/scheduler/` | 调度器 |
| `backend/app/modules/backup/` | 备份模块 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/Settings.vue` | 设置页 |
| `frontend/src/pages/LogCenter.vue` | 日志中心 |
| `frontend/src/pages/Notifications.vue` | 通知中心 |
| `frontend/src/pages/SchedulerMonitor.vue` | 调度监控 |
| `frontend/src/pages/StorageMonitor.vue` | 存储监控 |
| `frontend/src/pages/SystemSelfCheck.vue` | 系统自检 |

---

### 8. 插件系统 (Plugin System)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/plugins.py` | 插件 API |
| `backend/app/api/plugin_hub.py` | 插件市场 |
| `backend/app/api/plugin_config.py` | 插件配置 |
| `backend/app/plugin_sdk/` | 插件 SDK |
| `backend/plugins/` | 插件目录 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/Plugins.vue` | 插件管理 |

---

### 9. 收件箱 & 入库 (Inbox & Import)

**后端**
| 路径 | 职责 |
|------|------|
| `backend/app/api/inbox_dev.py` | 收件箱 API |
| `backend/app/api/upload.py` | 上传 API |
| `backend/app/api/transfer_history.py` | 转移历史 |
| `backend/app/modules/inbox/` | 收件箱模块 |
| `backend/app/modules/file_operation/` | 文件操作 |
| `backend/app/modules/media_renamer/` | 重命名 |

**前端**
| 路径 | 职责 |
|------|------|
| `frontend/src/pages/InboxPreview.vue` | 收件箱预览 |
| `frontend/src/pages/FileBrowser.vue` | 文件浏览器 |
| `frontend/src/pages/TransferHistory.vue` | 转移历史 |

---

## 核心入口点

### 后端入口

| 入口 | 路径 | 说明 |
|------|------|------|
| 主应用 | `backend/main.py` | FastAPI 应用入口 |
| API 路由注册 | `backend/app/api/__init__.py` | 所有路由注册 |
| 配置加载 | `backend/app/core/config.py` | Settings 类 |
| 数据库 | `backend/app/core/database.py` | SQLAlchemy 引擎 |
| 启动脚本 | `backend/main.py` (lifespan) | 初始化逻辑 |

### 前端入口

| 入口 | 路径 | 说明 |
|------|------|------|
| 主入口 | `frontend/src/main.ts` | Vue 应用创建 |
| 路由 | `frontend/src/router/index.ts` | 路由配置 |
| 布局 | `frontend/src/layouts/` | 页面布局 |
| 导航 | `frontend/src/layouts/components/AppDrawer.vue` | 侧边导航 |
| API 客户端 | `frontend/src/services/api.ts` | Axios 封装 |
| Store | `frontend/src/stores/` | Pinia 状态 |

---

## Evidence (P2)

### 执行命令

```
list_dir: backend/app
list_dir: backend/app/modules
list_dir: frontend/src
list_dir: frontend/src/pages
list_dir: backend/app/api
```

### 关键发现

1. **后端模块**: 65+ 功能模块
2. **API 文件**: 150+ 个 API 模块
3. **前端页面**: 90+ 个页面组件
4. **功能域**: 9 大功能域

### 引用文件路径 (20+)

1. `backend/main.py`
2. `backend/app/api/__init__.py`
3. `backend/app/core/config.py`
4. `backend/app/core/database.py`
5. `backend/app/api/discover.py`
6. `backend/app/api/subscription.py`
7. `backend/app/api/music.py`
8. `backend/app/api/log_center.py`
9. `backend/app/modules/subscription/`
10. `backend/app/modules/download/`
11. `backend/app/modules/music/`
12. `backend/app/services/discover_service.py`
13. `frontend/src/main.ts`
14. `frontend/src/router/index.ts`
15. `frontend/src/layouts/components/AppDrawer.vue`
16. `frontend/src/services/api.ts`
17. `frontend/src/pages/Discover.vue`
18. `frontend/src/pages/MusicCenter.vue`
19. `frontend/src/pages/LogCenter.vue`
20. `frontend/src/pages/Settings.vue`
21. `frontend/src/stores/`

---

*生成时间: 2025-12-13 23:16 UTC+8*
