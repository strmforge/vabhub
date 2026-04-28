# VabHub 数据模型目录 (DATA_MODEL_CATALOG)

> 自动扫描生成 - 基于 `backend/app/models/`

---

## 模型总览

- **模型文件数**: 70+
- **ORM**: SQLAlchemy 2.0 (async)
- **数据库**: PostgreSQL / SQLite

---

## 按功能域分类

### 1. 用户与认证

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| User | `user.py` | users | id, username, email, hashed_password, is_active | subscriptions, settings |
| UserSettings | `settings.py` | user_settings | id, user_id, settings_json | user |

### 2. 媒体库

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| Media | `media.py` | media | id, title, type, tmdb_id, year, poster_path | - |
| MediaServer | `media_server.py` | media_servers | id, name, type, host, api_key | - |

### 3. 订阅系统

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| Subscription | `subscription.py` | subscriptions | id, name, type, keyword, filter_rules, schedule, status | user |
| SubscriptionDefaults | `subscription_defaults.py` | subscription_defaults | id, media_type, default_rules | - |
| FilterRuleGroup | `filter_rule_group.py` | filter_rule_groups | id, name, rules_json, priority | subscriptions |
| RSSSubscription | `rss_subscription.py` | rss_subscriptions | id, name, url, interval | - |
| RSSHubSubscription | `rsshub.py` | rsshub_subscriptions | id, route, params | - |

### 4. 下载管理

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| Download | `download.py` | downloads | id, name, hash, status, progress, downloader_id | subscription |
| Downloader | `downloader.py` | downloaders | id, name, type, host, username, password | downloads |

### 5. 站点管理

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| Site | `site.py` | sites | id, name, domain, cookie, user_agent | site_domains |
| SiteDomain | `site_domain.py` | site_domains | id, site_id, domain, is_primary | site |
| SiteProfile | `site_profile.py` | site_profiles | id, site_id, profile_json | site |
| AISiteAdapter | `ai_site_adapter.py` | ai_site_adapters | id, site_id, config_json | site |
| CookieCloudConfig | `cookiecloud.py` | cookiecloud_configs | id, server_url, key, interval | - |
| HNRRecord | `hnr.py` | hnr_records | id, site_id, torrent_hash, status | site |

### 6. 音乐系统

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| MusicAlbum | `music.py` | music_albums | id, title, artist_name, year, cover_url | tracks |
| MusicArtist | `music.py` | music_artists | id, name, bio | albums |
| MusicTrack | `music.py` | music_tracks | id, title, album_id, duration, file_path | album |
| MusicChartSource | `music_chart_source.py` | music_chart_sources | id, name, platform, is_enabled | charts |
| MusicChart | `music_chart.py` | music_charts | id, source_id, name, chart_type | items |
| MusicChartItem | `music_chart_item.py` | music_chart_items | id, chart_id, rank, title, artist | chart |
| MusicDownloadJob | `music_download_job.py` | music_download_jobs | id, title, artist, status | - |

### 7. 阅读系统

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| Ebook | `ebook.py` | ebooks | id, title, author, format, file_path | - |
| Audiobook | `audiobook.py` | audiobooks | id, title, author, narrator, file_path | - |
| Novel | `novel.py` | novels | id, title, author, source, chapter_count | chapters |
| NovelChapter | `novel.py` | novel_chapters | id, novel_id, title, content | novel |
| NovelInboxImportLog | `novel_inbox_import_log.py` | novel_inbox_import_logs | id, file_path, status | - |

### 8. 漫画系统

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| MangaSource | `manga_source.py` | manga_sources | id, name, type, config_json | - |
| MangaSeriesLocal | `manga_series_local.py` | manga_series_local | id, title, path, cover_path | chapters |
| MangaChapterLocal | `manga_chapter_local.py` | manga_chapter_local | id, series_id, title, path | series |
| MangaReadingProgress | `manga_reading_progress.py` | manga_reading_progress | id, user_id, series_id, chapter_id, page | - |
| MangaDownloadJob | `manga_download_job.py` | manga_download_jobs | id, series_title, chapter_title, status | - |
| Comic | `comic.py` | comics | id, title, path | - |

### 9. 通知系统

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| Notification | `notification.py` | notifications | id, user_id, type, title, message, is_read | user |
| AlertChannel | `alert_channel.py` | alert_channels | id, name, type, config_json | - |
| UserNotifyChannel | `user_notify_channel.py` | user_notify_channels | id, user_id, type, config_json | user |

### 10. 收件箱 & 入库

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| InboxItem | `inbox.py` | inbox_items | id, path, detected_type, status | - |
| InboxRunLog | `inbox.py` | inbox_run_logs | id, run_time, items_processed, errors | - |
| TransferHistory | `transfer_history.py` | transfer_history | id, source_path, dest_path, media_type | - |
| IdentificationHistory | `identification_history.py` | identification_history | id, file_path, result_json | - |

### 11. 云存储

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| CloudStorage | `cloud_storage.py` | cloud_storages | id, name, type, config_json | - |
| STRMFile | `strm.py` | strm_files | id, name, target_url, library_path | - |

### 12. 插件系统

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| Plugin | `plugin.py` | plugins | id, name, version, is_enabled, config_json | - |
| PluginConfig | `plugin_config.py` | plugin_configs | id, plugin_id, key, value | plugin |
| PluginAudit | `plugin_audit.py` | plugin_audits | id, plugin_id, action, timestamp | plugin |

### 13. 系统配置

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| Directory | `directory.py` | directories | id, name, path, type | - |
| Backup | `backup.py` | backups | id, name, path, created_at, size | - |
| GlobalRules | `global_rules.py` | global_rules | id, rule_type, rules_json | - |
| Cache | `cache.py` | cache | id, key, value, expires_at | - |

### 14. AI & 监控

| 模型 | 文件 | 表名 | 主要字段 | 关联 |
|------|------|------|----------|------|
| MultimodalMetrics | `multimodal_metrics.py` | multimodal_metrics | id, timestamp, metrics_json | - |
| OCRTask | `ocr.py` | ocr_tasks | id, image_path, result_text, status | - |
| OCRStatistics | `ocr_statistics.py` | ocr_statistics | id, date, total_tasks, success_rate | - |
| Dashboard | `dashboard.py` | dashboard_configs | id, user_id, layout_json | user |

---

## 枚举类型

| 枚举 | 文件 | 值 |
|------|------|-----|
| MediaType | `enums/media_type.py` | movie, tv, anime, music, book |
| NotificationType | `enums/notification_type.py` | info, success, warning, error |
| AlertSeverity | `enums/alert_severity.py` | low, medium, high, critical |
| AlertChannelType | `enums/alert_channel_type.py` | telegram, webhook, email |
| MangaSourceType | `enums/manga_source_type.py` | local, remote, third_party |
| ReadingMediaType | `enums/reading_media_type.py` | novel, ebook, audiobook, manga |

---

## 关系图（简化）

```
User
├── Subscription (1:N)
├── Notification (1:N)
├── UserNotifyChannel (1:N)
└── UserSettings (1:1)

Subscription
├── FilterRuleGroup (N:1)
└── Download (1:N)

Site
├── SiteDomain (1:N)
├── SiteProfile (1:1)
├── HNRRecord (1:N)
└── AISiteAdapter (1:1)

MusicChartSource
└── MusicChart (1:N)
    └── MusicChartItem (1:N)

MangaSeriesLocal
└── MangaChapterLocal (1:N)

Novel
└── NovelChapter (1:N)
```

---

## Evidence (PZ-DATA)

### 扫描结果

- 70+ 模型文件
- 覆盖全部功能域

### 引用文件

1. `backend/app/models/__init__.py`
2. `backend/app/models/user.py`
3. `backend/app/models/subscription.py`
4. `backend/app/models/download.py`
5. `backend/app/models/site.py`
6. `backend/app/models/music.py`
7. `backend/app/models/ebook.py`
8. `backend/app/models/audiobook.py`
9. `backend/app/models/manga_source.py`
10. `backend/app/models/notification.py`
11. `backend/app/models/inbox.py`
12. `backend/app/models/plugin.py`

---

*生成时间: 2025-12-13 23:32 UTC+8*
