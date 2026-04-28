# VabHub 外部集成矩阵 (INTEGRATIONS_MATRIX)

> 外部系统/站点矩阵：用途、凭证、调用位置、失败降级、缓存策略

---

## 元数据服务

### TMDB (The Movie Database)

| 项目 | 值 |
|------|-----|
| **用途** | 影视元数据（海报、评分、演员、简介） |
| **代码入口** | `backend/app/api/media.py`, `backend/app/services/discover_service.py` |
| **凭证类型** | API Key (用户私有 / 公共展示) |
| **配置项** | `TMDB_API_KEY`, `PUBLIC_TMDB_DISCOVER_KEY` |
| **缓存策略** | Redis, 30 分钟 TTL |
| **限流** | 无（TMDB 免费层足够） |
| **失败降级** | 返回空数据，显示豆瓣/Bangumi 内容 |

### 豆瓣

| 项目 | 值 |
|------|-----|
| **用途** | 中文影视元数据、评分、热门榜单 |
| **代码入口** | `backend/app/modules/douban/client.py`, `backend/app/api/douban.py` |
| **凭证类型** | 无需 Key（公共 API） |
| **配置项** | 无 |
| **缓存策略** | Redis, 1 小时 TTL |
| **限流** | 内置请求间隔 |
| **失败降级** | 跳过豆瓣源，返回其他数据 |

### Bangumi

| 项目 | 值 |
|------|-----|
| **用途** | 动漫元数据、新番日历 |
| **代码入口** | `backend/app/api/bangumi.py` |
| **凭证类型** | 无需 Key（公共 API） |
| **配置项** | 无 |
| **缓存策略** | Redis, 1 小时 TTL |
| **限流** | 无 |
| **失败降级** | 跳过 Bangumi 源 |

### TheTVDB

| 项目 | 值 |
|------|-----|
| **用途** | 电视剧剧集信息 |
| **代码入口** | `backend/app/modules/thetvdb/` |
| **凭证类型** | API Key（可选） |
| **配置项** | `THETVDB_API_KEY` |
| **缓存策略** | Redis |
| **失败降级** | 使用 TMDB 数据 |

---

## RSS & 内容源

### RSSHub

| 项目 | 值 |
|------|-----|
| **用途** | 万物皆可 RSS（音乐榜单、新闻、社交媒体） |
| **代码入口** | `backend/app/modules/rsshub/`, `backend/app/api/rsshub.py` |
| **凭证类型** | 无需（公共实例） |
| **配置项** | `RSSHUB_BASE_URL` (默认 `https://rsshub.app`) |
| **缓存策略** | Redis, 根据 RSS TTL |
| **限流** | 公共实例有限流 |
| **失败降级** | 返回空，显示"RSSHub 不可用" |

### RSS 订阅

| 项目 | 值 |
|------|-----|
| **用途** | 用户自定义 RSS 源 |
| **代码入口** | `backend/app/modules/rss/`, `backend/app/api/rss.py` |
| **凭证类型** | 无 |
| **配置项** | 用户在 UI 配置 |
| **缓存策略** | 根据 RSS feed 自身 |
| **失败降级** | 标记源为失败，下次重试 |

---

## 下载器

### qBittorrent

| 项目 | 值 |
|------|-----|
| **用途** | BT 下载 |
| **代码入口** | `backend/app/modules/download/` |
| **凭证类型** | 用户名/密码 |
| **配置项** | UI 配置（下载器管理） |
| **缓存策略** | 无（实时查询） |
| **限流** | 无 |
| **失败降级** | 显示"下载器离线"，禁用下载功能 |

### Transmission

| 项目 | 值 |
|------|-----|
| **用途** | BT 下载 |
| **代码入口** | `backend/app/modules/download/` |
| **凭证类型** | 用户名/密码 |
| **配置项** | UI 配置 |
| **缓存策略** | 无 |
| **失败降级** | 同 qBittorrent |

---

## 云存储

### 115 网盘

| 项目 | 值 |
|------|-----|
| **用途** | 网盘存储、离线下载、STRM 播放 |
| **代码入口** | `backend/app/modules/cloud_storage/`, `backend/app/api/cloud_storage.py` |
| **凭证类型** | Cookie (通过 CookieCloud 同步) |
| **配置项** | UI 配置 |
| **缓存策略** | 文件列表缓存 |
| **限流** | 内置请求间隔 |
| **失败降级** | 显示"网盘不可用" |

### 123 网盘

| 项目 | 值 |
|------|-----|
| **用途** | 网盘存储 |
| **代码入口** | `backend/app/modules/cloud_storage/` |
| **凭证类型** | Cookie |
| **配置项** | UI 配置 |
| **失败降级** | 显示"网盘不可用" |

### RClone / OpenList

| 项目 | 值 |
|------|-----|
| **用途** | 通用云存储挂载 |
| **代码入口** | `backend/app/modules/cloud_storage/` |
| **凭证类型** | 各云服务凭证 |
| **配置项** | rclone.conf 或 UI |
| **失败降级** | 显示错误 |

---

## 站点 & PT

### PT 站点适配

| 项目 | 值 |
|------|-----|
| **用途** | 资源搜索、签到、数据统计 |
| **代码入口** | `backend/app/modules/site/`, `backend/app/modules/site_manager/` |
| **凭证类型** | Cookie (通过 CookieCloud 或手动) |
| **配置项** | 站点配置文件 (`resources/site-profiles/`) |
| **缓存策略** | 搜索结果缓存 |
| **限流** | 每站点独立限流 |
| **失败降级** | 标记站点离线，跳过搜索 |

### CookieCloud

| 项目 | 值 |
|------|-----|
| **用途** | 浏览器 Cookie 同步 |
| **代码入口** | `backend/app/modules/cookiecloud/`, `backend/app/api/cookiecloud.py` |
| **凭证类型** | CookieCloud 服务器地址 + 密钥 |
| **配置项** | UI 配置 |
| **缓存策略** | 无 |
| **失败降级** | 提示手动更新 Cookie |

---

## 通知 & Bot

### Telegram Bot

| 项目 | 值 |
|------|-----|
| **用途** | 通知推送、远程控制 |
| **代码入口** | `backend/app/modules/bots/`, `backend/app/api/user_telegram.py` |
| **凭证类型** | Bot Token + Chat ID |
| **配置项** | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| **缓存策略** | 无 |
| **限流** | Telegram API 限流 |
| **失败降级** | 日志记录，不影响主流程 |

### Webhook

| 项目 | 值 |
|------|-----|
| **用途** | 通用通知推送 |
| **代码入口** | `backend/app/modules/notification/` |
| **凭证类型** | Webhook URL |
| **配置项** | UI 配置 |
| **失败降级** | 日志记录 |

---

## 媒体服务器

### Jellyfin / Emby / Plex

| 项目 | 值 |
|------|-----|
| **用途** | 媒体库刷新、播放统计 |
| **代码入口** | `backend/app/modules/media_server/` |
| **凭证类型** | API Key / Token |
| **配置项** | UI 配置 |
| **缓存策略** | 无 |
| **失败降级** | 显示"媒体服务器离线" |

---

## AI & 插件

### AI Orchestrator

| 项目 | 值 |
|------|-----|
| **用途** | AI 功能总控（推荐、诊断、整理） |
| **代码入口** | `backend/app/api/ai_orchestrator.py` |
| **凭证类型** | 取决于后端 AI 服务 |
| **配置项** | AI 相关环境变量 |
| **失败降级** | AI 功能不可用，回退传统逻辑 |

### Plugin Hub

| 项目 | 值 |
|------|-----|
| **用途** | 插件市场、插件安装 |
| **代码入口** | `backend/app/api/plugin_hub.py` |
| **凭证类型** | 无 |
| **配置项** | `PLUGIN_HUB_SOURCES` |
| **缓存策略** | 插件列表缓存 |
| **失败降级** | 显示"插件市场不可用" |

---

## 矩阵总表

| 集成 | 类型 | 需要 Key | 代码入口 | 降级策略 |
|------|------|----------|----------|----------|
| TMDB | 元数据 | 是 | `api/media.py` | 显示其他源 |
| 豆瓣 | 元数据 | 否 | `modules/douban/` | 跳过 |
| Bangumi | 元数据 | 否 | `api/bangumi.py` | 跳过 |
| RSSHub | 内容源 | 否 | `modules/rsshub/` | 显示不可用 |
| qBittorrent | 下载器 | 凭证 | `modules/download/` | 禁用下载 |
| 115 网盘 | 云存储 | Cookie | `modules/cloud_storage/` | 显示不可用 |
| PT 站点 | 资源搜索 | Cookie | `modules/site/` | 标记离线 |
| CookieCloud | 凭证同步 | 密钥 | `modules/cookiecloud/` | 手动更新 |
| Telegram | 通知 | Token | `modules/bots/` | 日志记录 |
| Jellyfin/Emby | 媒体服务器 | Token | `modules/media_server/` | 显示离线 |
| Plugin Hub | 插件 | 否 | `api/plugin_hub.py` | 显示不可用 |

---

## Evidence (P6)

### 关键文件引用

1. `backend/app/api/media.py`
2. `backend/app/services/discover_service.py`
3. `backend/app/modules/douban/client.py`
4. `backend/app/api/bangumi.py`
5. `backend/app/modules/rsshub/`
6. `backend/app/modules/download/`
7. `backend/app/modules/cloud_storage/`
8. `backend/app/modules/site/`
9. `backend/app/modules/cookiecloud/`
10. `backend/app/modules/bots/`
11. `backend/app/modules/media_server/`
12. `backend/app/api/plugin_hub.py`
13. `backend/app/core/public_metadata_config.py`

---

*生成时间: 2025-12-13 23:28 UTC+8*
