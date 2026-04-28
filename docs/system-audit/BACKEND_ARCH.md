# VabHub 后端架构 (BACKEND_ARCH)

> 审计 Commit: `9af3cd0e02012aeadf7c72275ac1d62159bbd56c`

---

## 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 框架 | FastAPI | 0.109+ |
| ORM | SQLAlchemy 2.0 | async |
| 数据库 | PostgreSQL / SQLite | 14+ / 3.x |
| 缓存 | Redis | 7+ |
| 任务调度 | APScheduler | 内置 |
| GraphQL | Strawberry | 可选 |

---

## 入口与启动

### 主入口

**文件**: `backend/main.py`

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. 日志初始化
    setup_logging()
    setup_realtime_logging()  # 实时日志中心
    
    # 2. 数据库初始化
    await init_db()
    
    # 3. DNS over HTTPS
    enable_doh(settings.DOH_ENABLE)
    
    # 4. 缓存系统
    cache = get_cache()
    
    # 5. 密钥管理器
    initialize_secrets()
    
    # 6. 初始管理员
    await initialize_superuser()
    
    # 7. WebSocket 任务
    await start_websocket_tasks()
    
    # 8. API 密钥管理
    api_key_manager.initialize_default_keys()
    
    # 9. 健康检查
    health_checker = get_health_checker()
    
    # 10. 定时任务调度器
    scheduler = get_scheduler()
    await scheduler.start()
    
    yield
    
    # 关闭资源
    await scheduler.shutdown()
    await close_db()
```

### API 路由注册

**文件**: `backend/app/api/__init__.py`

- 注册 **130+** 个 API 路由模块
- 使用 `api_router.include_router()` 统一管理
- 路由前缀规范化（部分模块自带前缀）

---

## 配置体系

### 配置文件

**文件**: `backend/app/core/config.py`

```python
class Settings(BaseSettings):
    # 核心配置
    APP_NAME: str = "VabHub"
    DEBUG: bool = True
    
    # 数据库
    DATABASE_URL: str = "sqlite:///./vabhub.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # /config 模式 (0.0.3)
    VABHUB_CONFIG_DIR: str = "./config"
    VABHUB_DATA_DIR: str = "./config/data"
    VABHUB_LOG_DIR: str = "./config/logs"
    
    # 媒体库路径
    MOVIE_LIBRARY_ROOT: str = "./data/library/movies"
    TV_LIBRARY_ROOT: str = "./data/library/tv"
    MUSIC_LIBRARY_ROOT: str = "./data/library/music"
    
    # 外部服务
    TMDB_API_KEY: str = ""
    RSSHUB_BASE_URL: str = "https://rsshub.app"
```

### 配置加载优先级

1. 环境变量
2. `.env` 文件
3. 默认值

---

## 数据库层

### 引擎配置

**文件**: `backend/app/core/database.py`

```python
# PostgreSQL 连接池配置 (0.0.3 优化)
engine = create_async_engine(
    db_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # 30分钟
)
```

### Session 管理

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### 迁移体系

**目录**: `backend/alembic/`

- 使用 Alembic 管理数据库迁移
- 版本文件在 `alembic/versions/`

---

## 服务层架构

### 服务目录

**路径**: `backend/app/services/`

| 服务 | 文件 | 职责 |
|------|------|------|
| 发现页 | `discover_service.py` | TMDB/豆瓣/Bangumi 聚合 |
| 音乐发现 | `music_discover_service.py` | 音乐榜单聚合 |

### 模块目录

**路径**: `backend/app/modules/`

65+ 功能模块，按业务域划分：

| 域 | 模块 | 职责 |
|-----|------|------|
| 媒体 | `video/`, `strm/`, `media_renamer/` | 视频处理 |
| 下载 | `download/`, `search/` | 下载器集成 |
| 订阅 | `subscription/`, `rss/`, `rsshub/` | 订阅管理 |
| 阅读 | `novel/`, `audiobook/`, `ebook/`, `comic/` | 阅读内容 |
| 音乐 | `music/`, `music_charts/`, `charts/` | 音乐管理 |
| 通知 | `notification/`, `alert_channels/` | 通知推送 |
| 日志 | `log_center/`, `log/` | 日志系统 |
| AI | `recommendation/`, `multimodal/` | AI 功能 |
| 站点 | `site/`, `site_manager/`, `hnr/` | 站点管理 |
| 收件箱 | `inbox/` | 统一入库 |

---

## 定时任务 (Runner/Job)

### 调度器

**文件**: `backend/app/core/scheduler.py`

```python
class VabHubScheduler:
    async def start(self):
        # 注册定时任务
        self._scheduler.add_job(...)
    
    async def shutdown(self):
        self._scheduler.shutdown()
```

### 任务类型

| 任务 | 触发方式 | 说明 |
|------|----------|------|
| 订阅刷新 | cron | 定时检查订阅规则 |
| 站点签到 | cron | PT 站点签到 |
| 下载状态 | interval | 轮询下载器状态 |
| 缓存清理 | cron | 清理过期缓存 |

### Runner 模块

**路径**: `backend/app/runners/`

15 个 runner 模块，处理后台任务。

---

## 通知与日志

### 通知系统

**模块**: `backend/app/modules/notification/`

- 支持 Telegram、Webhook、邮件等渠道
- 事件驱动：订阅完成、下载完成、入库完成等

### 日志中心

**API**: `backend/app/api/log_center.py`

```python
# WebSocket 实时日志
@router.websocket("/ws/logs")
async def websocket_logs(...):
    # 实时推送日志
    
# 日志查询
@router.post("/log-center/query")
async def query_logs(...):
    # 查询历史日志
```

**日志存储**: `backend/logs/` 或 `VABHUB_LOG_DIR`

---

## 外部集成入口

| 集成 | 模块 | 配置项 |
|------|------|--------|
| TMDB | `modules/video/` | `TMDB_API_KEY` |
| 豆瓣 | `modules/douban/` | 无需 key |
| Bangumi | `api/bangumi.py` | 无需 key |
| RSSHub | `modules/rsshub/` | `RSSHUB_BASE_URL` |
| 下载器 | `modules/download/` | 用户配置 |
| 115网盘 | `modules/cloud_storage/` | 用户配置 |
| Telegram | `modules/bots/` | `TELEGRAM_BOT_TOKEN` |

---

## 核心数据流

```
请求 → FastAPI 中间件 → 路由处理 → 依赖注入(DB Session) 
     → Service 层 → Module 层 → 外部 API/数据库 
     → 响应
```

---

## Evidence (P3-BACKEND)

### 执行命令

```
read_file: backend/main.py (1-100)
read_file: backend/app/api/__init__.py (1-308)
list_dir: backend/app/modules
```

### 关键发现

1. **130+ API 路由模块** 注册在 `api/__init__.py`
2. **65+ 功能模块** 在 `modules/` 目录
3. **连接池优化** 已在 0.0.3 完成
4. **实时日志** 通过 WebSocket 推送

### 引用文件路径

1. `backend/main.py` - 主入口
2. `backend/app/api/__init__.py` - API 路由注册
3. `backend/app/core/config.py` - 配置类
4. `backend/app/core/database.py` - 数据库引擎
5. `backend/app/core/scheduler.py` - 调度器
6. `backend/app/core/cache.py` - 缓存系统
7. `backend/app/core/logging.py` - 日志配置
8. `backend/app/core/log_handler.py` - 实时日志
9. `backend/app/services/discover_service.py` - 发现服务
10. `backend/app/modules/subscription/` - 订阅模块
11. `backend/app/modules/download/` - 下载模块
12. `backend/app/modules/notification/` - 通知模块
13. `backend/app/modules/log_center/` - 日志中心
14. `backend/app/api/log_center.py` - 日志 API
15. `backend/app/api/discover.py` - 发现 API

---

*生成时间: 2025-12-13 23:18 UTC+8*
