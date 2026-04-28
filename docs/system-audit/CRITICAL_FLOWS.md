# VabHub 关键链路时序 (CRITICAL_FLOWS)

> 端到端时序图 + 失败点与降级策略

---

## 1. 发现页多源聚合

### 时序图

```mermaid
sequenceDiagram
    participant U as 用户浏览器
    participant F as 前端 Discover.vue
    participant A as 后端 /api/discover/home
    participant S as DiscoverService
    participant T as TMDB API
    participant D as 豆瓣 API
    participant B as Bangumi API
    participant C as 缓存 (Redis)

    U->>F: 访问 /discover
    F->>A: GET /api/discover/home
    A->>S: get_home()
    
    S->>C: 检查缓存
    alt 缓存命中
        C-->>S: 返回缓存数据
    else 缓存未命中
        par 并行请求
            S->>T: fetch TMDB trending
            S->>D: fetch 豆瓣热门
            S->>B: fetch Bangumi 新番
        end
        
        T-->>S: TMDB 数据 (或失败)
        D-->>S: 豆瓣数据 (或失败)
        B-->>S: Bangumi 数据 (或失败)
        
        S->>S: 合并结果 (单源失败不影响)
        S->>C: 写入缓存 (30分钟)
    end
    
    S-->>A: DiscoverHomeResponse
    A-->>F: JSON 响应
    F->>F: 渲染卡片流
    F-->>U: 显示发现页
```

### 关键数据结构

```python
class DiscoverHomeResponse(BaseModel):
    sections: List[DiscoverSection]  # 各源区块
    has_public_keys: bool
    has_private_keys: bool
    key_source: str  # "public" / "private" / "none"
    message: Optional[str]
```

### 失败点与降级

| 失败点 | 影响 | 降级策略 |
|--------|------|----------|
| TMDB 无 Key | 无 TMDB 内容 | 显示豆瓣/Bangumi 内容 |
| TMDB API 超时 | 无 TMDB 内容 | 日志警告，返回其他源 |
| 豆瓣 API 失败 | 无豆瓣内容 | 返回其他源 |
| Bangumi API 失败 | 无 Bangumi 内容 | 返回其他源 |
| 全部失败 | 空页面 | 显示"暂无热门内容" |
| Redis 不可用 | 每次都请求源 | 降级为无缓存模式 |

---

## 2. 订阅 → 下载 → 入库

### 时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端
    participant Sub as /api/subscriptions
    participant Svc as SubscriptionService
    participant Sch as Scheduler
    participant Src as 搜索引擎
    participant DL as 下载器 (qB/TR)
    participant Inbox as 收件箱
    participant Lib as 媒体库

    U->>F: 创建订阅规则
    F->>Sub: POST /api/subscriptions
    Sub->>Svc: create_subscription()
    Svc-->>Sub: 订阅创建成功
    Sub-->>F: 返回订阅ID
    
    Note over Sch: 定时触发 (cron)
    Sch->>Svc: run_subscription(id)
    Svc->>Src: 搜索资源
    Src-->>Svc: 搜索结果列表
    
    Svc->>Svc: 过滤规则匹配
    Svc->>DL: 添加下载任务
    DL-->>Svc: 任务ID
    
    Note over DL: 下载进行中...
    DL->>DL: 下载完成
    
    Sch->>DL: 轮询下载状态
    DL-->>Sch: 完成状态
    
    Sch->>Inbox: 触发入库流程
    Inbox->>Inbox: 识别媒体类型
    Inbox->>Inbox: 重命名/整理
    Inbox->>Lib: 移动到媒体库
    
    Inbox->>Svc: 通知：入库完成
    Svc->>U: 推送通知 (Telegram/等)
```

### 关键数据结构

```python
class Subscription(BaseModel):
    id: int
    name: str
    media_type: str  # movie/tv/music/book
    keyword: str
    filter_rules: dict
    schedule: str  # cron 表达式
    status: str  # active/paused
```

### 失败点与降级

| 失败点 | 影响 | 降级策略 |
|--------|------|----------|
| 搜索无结果 | 无下载 | 记录日志，下次重试 |
| 下载器离线 | 无法下载 | 返回错误，UI 显示状态 |
| 下载失败 | 任务中断 | 标记失败，支持手动重试 |
| 入库识别失败 | 文件未整理 | 保留在收件箱，等待手动处理 |
| 通知发送失败 | 用户无感知 | 日志记录，不影响主流程 |

---

## 3. 音乐榜单 → 订阅 → 自动循环

### 时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as MusicCenter.vue
    participant API as /api/charts
    participant CS as ChartsService
    participant MS as MusicSubscriptionService
    participant Sch as Scheduler
    participant DL as 下载器
    participant Lib as 音乐库

    U->>F: 访问榜单 & 订阅
    F->>API: GET /api/charts/music/platforms
    API->>CS: get_supported_platforms()
    CS-->>API: 平台列表 (QQ/网易/Spotify)
    API-->>F: 返回平台
    
    U->>F: 选择榜单
    F->>API: GET /api/charts/music/jsonl?platform=netease
    API->>CS: get_charts(netease, hot)
    CS-->>API: 榜单曲目
    API-->>F: 曲目列表
    
    U->>F: 订阅此榜单
    F->>API: POST /api/music/subscriptions
    API->>MS: create_subscription()
    MS-->>API: 订阅创建成功
    
    Note over Sch: 每日自动执行
    Sch->>MS: run_music_subscriptions()
    MS->>CS: get_charts() (获取最新榜单)
    CS-->>MS: 最新曲目
    
    MS->>MS: 对比已有曲目
    MS->>DL: 下载新曲目
    DL-->>MS: 下载完成
    
    MS->>Lib: 入库音乐文件
    MS->>U: 通知：新曲目已入库
```

### 失败点与降级

| 失败点 | 影响 | 降级策略 |
|--------|------|----------|
| 榜单 API 失败 | 无榜单数据 | 返回缓存数据 |
| 订阅执行失败 | 无新内容 | 记录日志，下次重试 |
| 音乐下载失败 | 曲目缺失 | 标记失败，支持重试 |

---

## 4. 日志中心

### 时序图

```mermaid
sequenceDiagram
    participant App as 应用代码
    participant LH as LogHandler
    participant WS as WebSocket Manager
    participant F as LogCenter.vue
    participant U as 用户

    App->>LH: logger.info("消息")
    LH->>LH: 格式化日志
    LH->>LH: 写入文件
    LH->>WS: 广播日志事件
    
    U->>F: 访问 /logs
    F->>WS: WebSocket 连接
    WS-->>F: 连接成功
    
    WS->>F: 推送历史日志
    F->>F: 渲染日志列表
    
    Note over App,F: 实时日志流
    App->>LH: logger.error("错误")
    LH->>WS: 广播
    WS->>F: 推送新日志
    F->>F: 追加显示
    F-->>U: 实时更新
    
    U->>F: 设置过滤条件
    F->>WS: 发送过滤参数
    WS->>WS: 应用过滤
    WS->>F: 推送过滤后日志
```

### 关键数据结构

```python
class LogEntry(BaseModel):
    timestamp: datetime
    level: str  # DEBUG/INFO/WARNING/ERROR
    source: str  # 模块名
    message: str
    extra: Optional[dict]
```

### 失败点与降级

| 失败点 | 影响 | 降级策略 |
|--------|------|----------|
| WebSocket 断连 | 无实时更新 | 前端自动重连 |
| 日志文件写入失败 | 日志丢失 | 降级为 stdout |
| Redis 不可用 | 广播失败 | 降级为文件读取 |

---

## 5. 用户认证流程

### 时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as Login.vue
    participant A as /api/auth
    participant DB as 数据库
    participant JWT as JWT Service

    U->>F: 输入用户名/密码
    F->>A: POST /api/auth/login
    A->>DB: 查询用户
    DB-->>A: 用户记录
    
    A->>A: 验证密码 (bcrypt)
    alt 验证成功
        A->>JWT: 生成 Token
        JWT-->>A: access_token + refresh_token
        A-->>F: 返回 Token
        F->>F: 存储 Token (localStorage)
        F->>F: 跳转首页
    else 验证失败
        A-->>F: 401 错误
        F-->>U: 显示错误提示
    end
    
    Note over F,A: 后续请求
    F->>A: GET /api/xxx (带 Bearer Token)
    A->>JWT: 验证 Token
    JWT-->>A: Token 有效
    A-->>F: 正常响应
```

---

## Evidence (P5)

### 关键文件引用

1. `backend/app/services/discover_service.py` - 发现页聚合
2. `backend/app/modules/subscription/` - 订阅服务
3. `backend/app/modules/download/` - 下载模块
4. `backend/app/modules/inbox/` - 收件箱入库
5. `backend/app/modules/charts/service.py` - 榜单服务
6. `backend/app/api/log_center.py` - 日志 API
7. `backend/app/core/log_handler.py` - 日志处理
8. `backend/app/api/auth.py` - 认证 API
9. `frontend/src/pages/Discover.vue`
10. `frontend/src/pages/MusicCenter.vue`
11. `frontend/src/pages/LogCenter.vue`
12. `frontend/src/pages/Login.vue`

### 关键发现

1. **并行请求** - 发现页多源并行，单源失败不阻塞
2. **定时调度** - 订阅通过 Scheduler 定时执行
3. **WebSocket** - 日志实时推送
4. **JWT 认证** - 无状态 Token 认证

---

*生成时间: 2025-12-13 23:25 UTC+8*
