# VabHub API 目录 (API_CATALOG)

> 自动扫描生成 - 基于 `backend/app/api/__init__.py`

---

## API 总览

- **总路由模块**: 130+
- **API 前缀**: `/api`
- **鉴权方式**: JWT Bearer Token
- **响应格式**: 统一 `BaseResponse` 结构

---

## 按功能域分类

### 1. 认证 (Auth)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| POST | `/api/auth/login` | `auth.login` | 无 | 用户登录 |
| POST | `/api/auth/logout` | `auth.logout` | 需要 | 用户登出 |
| GET | `/api/auth/me` | `auth.get_current_user` | 需要 | 获取当前用户 |
| POST | `/api/auth/refresh` | `auth.refresh_token` | 需要 | 刷新令牌 |

### 2. 发现页 (Discover)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/discover/home` | `discover.get_home` | 需要 | 发现页首页（多源聚合） |
| GET | `/api/discover/trending/{media_type}` | `discover.get_trending` | 需要 | 热门内容 |

### 3. 搜索 (Search)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/search` | `search.search` | 需要 | 全站搜索 |
| GET | `/api/search/sites` | `search.search_sites` | 需要 | 站点资源搜索 |
| POST | `/api/search/chain` | `search_chain.search` | 需要 | 链式搜索 |

### 4. 订阅 (Subscription)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/subscriptions` | `subscription.list` | 需要 | 订阅列表 |
| POST | `/api/subscriptions` | `subscription.create` | 需要 | 创建订阅 |
| GET | `/api/subscriptions/{id}` | `subscription.get` | 需要 | 订阅详情 |
| PUT | `/api/subscriptions/{id}` | `subscription.update` | 需要 | 更新订阅 |
| DELETE | `/api/subscriptions/{id}` | `subscription.delete` | 需要 | 删除订阅 |
| POST | `/api/subscriptions/{id}/run` | `subscription.run` | 需要 | 手动执行 |

### 5. 下载 (Download)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/downloads` | `download.list` | 需要 | 下载任务列表 |
| POST | `/api/downloads` | `download.add` | 需要 | 添加下载 |
| DELETE | `/api/downloads/{id}` | `download.remove` | 需要 | 删除任务 |
| POST | `/api/downloads/{id}/pause` | `download.pause` | 需要 | 暂停任务 |
| POST | `/api/downloads/{id}/resume` | `download.resume` | 需要 | 恢复任务 |

### 6. 媒体库 (Library)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/library/movies` | `library.list_movies` | 需要 | 电影列表 |
| GET | `/api/library/tv` | `library.list_tv` | 需要 | 剧集列表 |
| GET | `/api/media/{id}` | `media.get_detail` | 需要 | 媒体详情 |
| GET | `/api/media/search` | `media.search` | 需要 | TMDB 搜索 |

### 7. 音乐 (Music)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/music/home` | `music_home.get_home` | 需要 | 音乐首页 |
| GET | `/api/music/albums` | `music.list_albums` | 需要 | 专辑列表 |
| GET | `/api/music/artists` | `music.list_artists` | 需要 | 艺术家列表 |
| GET | `/api/music/tracks` | `music.list_tracks` | 需要 | 曲目列表 |
| GET | `/api/charts/music/platforms` | `charts.get_platforms` | 需要 | 榜单平台 |
| GET | `/api/charts/music/jsonl` | `charts.get_chart` | 需要 | 榜单数据 |

### 8. 阅读 (Reading)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/novels/center/list` | `novel_center.list` | 需要 | 小说列表 |
| GET | `/api/novel-reader/{id}` | `novel_reader.read` | 需要 | 小说阅读 |
| GET | `/api/audiobooks/center/list` | `audiobook_center.list` | 需要 | 有声书列表 |
| GET | `/api/ebooks` | `ebook.list` | 需要 | 电子书列表 |

### 9. 漫画 (Manga)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/manga/local/library` | `manga_local.library` | 需要 | 本地漫画库 |
| GET | `/api/manga/remote/search` | `manga_remote.search` | 需要 | 远程搜索 |
| GET | `/api/manga/follow/list` | `manga_follow.list` | 需要 | 追更列表 |
| POST | `/api/manga/sync/download` | `manga_sync.download` | 需要 | 下载漫画 |

### 10. 日志 (Logs)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| WS | `/api/log-center/ws/logs` | `log_center.ws_logs` | 需要 | 实时日志流 |
| POST | `/api/log-center/query` | `log_center.query` | 需要 | 日志查询 |
| GET | `/api/log-center/statistics` | `log_center.stats` | 需要 | 日志统计 |
| GET | `/api/log-center/export` | `log_center.export` | 需要 | 日志导出 |

### 11. 站点 (Sites)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/sites` | `site.list` | 需要 | 站点列表 |
| POST | `/api/sites` | `site.add` | 需要 | 添加站点 |
| GET | `/api/sites/{id}` | `site.get` | 需要 | 站点详情 |
| PUT | `/api/sites/{id}` | `site.update` | 需要 | 更新站点 |
| DELETE | `/api/sites/{id}` | `site.delete` | 需要 | 删除站点 |
| POST | `/api/sites/{id}/test` | `site.test` | 需要 | 测试连接 |

### 12. 系统设置 (Settings)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/settings` | `settings.get_all` | 需要 | 获取设置 |
| PUT | `/api/settings` | `settings.update` | 需要 | 更新设置 |
| GET | `/api/system/info` | `system_settings.info` | 需要 | 系统信息 |
| POST | `/api/system/restart` | `admin_system.restart` | 管理员 | 重启服务 |

### 13. 健康检查 (Health)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/health` | `main.health` | 无 | 基础健康检查 |
| GET | `/api/health` | `health.detailed` | 无 | 详细健康检查 |
| GET | `/api/health/{item}` | `health.check_item` | 无 | 单项检查 |

### 14. 插件 (Plugins)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/plugins` | `plugins.list` | 需要 | 插件列表 |
| POST | `/api/plugins/install` | `plugins.install` | 管理员 | 安装插件 |
| DELETE | `/api/plugins/{id}` | `plugins.uninstall` | 管理员 | 卸载插件 |
| GET | `/api/plugin-hub/catalog` | `plugin_hub.catalog` | 需要 | 插件市场 |

### 15. AI 功能 (AI)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| POST | `/api/ai/orchestrator/analyze` | `ai_orchestrator.analyze` | 需要 | AI 分析 |
| POST | `/api/ai/log-doctor/diagnose` | `ai_log_doctor.diagnose` | 需要 | 故障诊断 |
| POST | `/api/ai/cleanup/suggest` | `ai_cleanup_advisor.suggest` | 需要 | 清理建议 |
| GET | `/api/recommendations` | `recommendation.get` | 需要 | 推荐内容 |

### 16. 通知 (Notifications)

| Method | Path | Handler | 鉴权 | 用途 |
|--------|------|---------|------|------|
| GET | `/api/user/notify-channels` | `user_notify_channels.list` | 需要 | 通知渠道 |
| POST | `/api/user/notify-channels` | `user_notify_channels.add` | 需要 | 添加渠道 |
| GET | `/api/notify-preferences` | `notify_preferences.get` | 需要 | 通知偏好 |

---

## 临时禁用的 API

以下 API 因各种原因临时禁用（见 `api/__init__.py` 注释）：

| API | 原因 |
|-----|------|
| `notification.router` | 调试中 |
| `notifications_user.router` | Schema 冲突 |
| `video_progress.router` | Schema 冲突 |
| `player_wall.router` | 缺少 media_file 模块 |
| `music_chart_admin.router` | 缺少 get_async_session |
| `music_subscription.router` | 缺少 get_async_session |
| `notify_test.router` | 等待修复 |

---

## 响应格式

```json
{
  "success": true,
  "message": "操作成功",
  "data": { ... },
  "timestamp": "2025-12-13T23:00:00Z"
}
```

错误响应：

```json
{
  "success": false,
  "error_code": "RESOURCE_NOT_FOUND",
  "error_message": "资源不存在",
  "timestamp": "2025-12-13T23:00:00Z"
}
```

---

## Evidence (P3-API)

### 数据来源

- `backend/app/api/__init__.py` (308 行)
- 130+ 路由模块导入
- 130+ `include_router` 调用

### 引用文件

1. `backend/app/api/__init__.py`
2. `backend/app/api/auth.py`
3. `backend/app/api/discover.py`
4. `backend/app/api/subscription.py`
5. `backend/app/api/download.py`
6. `backend/app/api/music.py`
7. `backend/app/api/log_center.py`
8. `backend/app/api/health.py`
9. `backend/app/api/plugins.py`
10. `backend/app/api/ai_orchestrator.py`

---

*生成时间: 2025-12-13 23:20 UTC+8*
