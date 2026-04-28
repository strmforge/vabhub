# VabHub 缺口清单与下一步建议 (GAPS_AND_NEXT)

> 按 P0/P1/P2 优先级排序，每条包含证据、影响、建议、验收标准

---

## P0：会导致"用户第一眼是空壳/404/静默失败"的问题

### P0-1：部分 API 路由临时禁用 ✅ 已全部修复

**修复记录** (2025-12-14):
- ✅ `music_chart_admin.router` - 修复 `success_response` 导入路径
- ✅ `music_subscription.router` - 修复 `success_response` 导入路径  
- ✅ `player_wall.router` - 修复 `MediaFile` 导入路径
- ✅ `notification.router` - 通知 API 已启用
- ✅ `video_progress.router` - 修复 `get_current_user` 导入路径
- ✅ `notifications_user.router` - 修复 `get_current_user` 导入路径
- ✅ `notify_test.router` - 修复依赖导入 + 添加 `get_admin_user`

**新增依赖函数**:
- `app.core.dependencies.get_admin_user` - FastAPI 管理员用户依赖

**验收标准**
- ✅ 音乐榜单管理 API 可用
- ✅ 音乐订阅 API 可用
- ✅ 电视墙 API 可用
- ✅ 通知 API 可用
- ✅ 视频播放进度 API 可用
- ✅ 用户通知 API 可用
- ✅ 通知测试 API 可用

---

### P0-2：前端 TypeScript 类型警告 ✅ 已修复

**修复记录** (2025-12-14):
- ✅ `frontend/src/services/api.ts` - 添加 axios 类型导入和拦截器类型注解
- ✅ `frontend/src/types/axios.d.ts` - 新增 axios 类型扩展声明

**修复内容**:
```typescript
import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from 'axios'

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {...},
  (error: AxiosError): Promise<never> => {...}
)
```

**验收标准**
- ✅ 拦截器类型注解完整
- ✅ 无隐式 any 泄漏到业务调用方

---

### P0-3：首次启动空库体验

**现状证据**
- 已在 0.0.3 部分解决（发现页多源聚合）
- 但音乐榜单订阅 API 被禁用

**影响面**
- 音乐中心"榜单 & 订阅"功能不完整

**建议改法**
1. 修复 `music_chart_admin.router` 和 `music_subscription.router`
2. 确保内置榜单平台（QQ音乐、网易云等）可正常调用

**验收标准**
- 空库启动，音乐中心可选择榜单
- 可创建榜单订阅

---

## P1：影响稳定性/性能/可观测性

### P1-1：数据库连接池监控 ✅ 已修复

**修复记录** (2025-12-14 - SYSTEM-AUDIT-FOLLOWUP-1 P3):
- ✅ `backend/app/api/health.py` - /health 端点已包含 DB 连接池状态
- ✅ `backend/tests/test_health.py` - 新增健康检查测试 (4/4 通过)

**端点**:
- `GET /api/health/` - 返回 `db.pool` 字段包含连接池状态
- `GET /api/health/db` - 单项 DB 检查含连接池

**响应示例**:
```json
{
  "status": "ok",
  "db": {
    "ok": true,
    "latency_ms": 2,
    "pool": "Pool size: 5  Connections in pool: 5 ..."
  }
}
```

**验收标准**
- ✅ `/api/health/` 返回连接池状态
- ✅ DB 异常时 status="degraded" 但仍返回 200

---

### P1-2：定时任务执行日志 ✅ 已修复

**修复记录** (2025-12-14 - SYSTEM-AUDIT-FOLLOWUP P4):
- ✅ `backend/app/models/task_run_history.py` - 新增任务执行历史模型
- ✅ `backend/app/core/task_context.py` - 新增任务执行上下文管理器
- ✅ `backend/app/api/task_history.py` - 新增任务历史 API
- ✅ `frontend/src/pages/TaskHistory.vue` - 新增任务历史页面

**集成的 Runners**:
- subscription_checker (订阅检查)
- music_chart_sync (音乐榜单同步)
- ops_health_check (健康检查)

**验收标准**
- ✅ 每次定时任务执行有记录
- ✅ 可在 /task-history 页面查看执行状态

---

### P1-3：缓存失效策略 ✅ 已修复

**修复记录** (2025-12-14 - SYSTEM-AUDIT-FOLLOWUP P5):
- ✅ `backend/app/core/config.py` - 新增统一 TTL 常量
- ✅ `backend/app/api/discover.py` - 使用配置 TTL + ?refresh=1 参数
- ✅ `backend/app/api/music_home.py` - 使用配置 TTL + ?refresh=1 参数

**配置常量**:
```python
DISCOVER_CACHE_TTL_SECONDS = 1800  # 30 分钟
MUSIC_HOME_CACHE_TTL_SECONDS = 900  # 15 分钟
CACHE_MIN_REFRESH_INTERVAL_SECONDS = 60  # 1 分钟
```

**验收标准**
- ✅ TTL 统一配置，支持环境变量覆盖
- ✅ API 支持 ?refresh=1 强制刷新

---

### P1-4：日志文件轮转 ✅ 已修复

**修复记录** (2025-12-14 - SYSTEM-AUDIT-FOLLOWUP P6):
- ✅ `backend/app/core/config.py` - 新增日志轮转配置常量
- ✅ `backend/app/core/logging.py` - 使用配置的轮转设置

**配置常量**:
```python
LOG_ROTATION = "50 MB"   # 支持 env: LOG_ROTATION
LOG_RETENTION = "14 days"  # 支持 env: LOG_RETENTION
LOG_COMPRESSION = "zip"   # 支持 env: LOG_COMPRESSION
```

**验收标准**
- ✅ 日志轮转已配置，支持环境变量覆盖
- ✅ 默认 50MB 轮转，14 天保留，zip 压缩

---

## P2：体验增强

### P2-1：发现页分类筛选

**现状证据**
- 文件: `frontend/src/pages/Discover.vue`
- 当前只有"全部"视图

**影响面**
- 用户无法按类型筛选

**建议改法**
1. 添加 Tabs：电影 / 剧集 / 动漫
2. 后端支持 `media_type` 参数

**验收标准**
- 可按类型筛选发现内容

---

### P2-2：搜索结果排序

**现状证据**
- 文件: `frontend/src/pages/Search.vue`
- 缺少排序选项

**影响面**
- 用户难以找到最佳资源

**建议改法**
1. 添加排序下拉：做种数 / 大小 / 时间
2. 后端返回排序字段

**验收标准**
- 搜索结果可按多维度排序

---

### P2-3：批量操作

**现状证据**
- 订阅列表、下载列表无批量操作

**影响面**
- 管理大量项目效率低

**建议改法**
1. 添加多选功能
2. 支持批量删除/暂停/恢复

**验收标准**
- 可勾选多个项目批量操作

---

### P2-4：快捷键支持

**现状证据**
- 前端无全局快捷键

**影响面**
- 高效用户无法快速操作

**建议改法**
1. `Ctrl+K` 全局搜索
2. `Ctrl+/` 显示快捷键帮助

**验收标准**
- 快捷键可用且有帮助提示

---

## 下一步建议路线图

```
Week 1: P0 修复
├── 修复被禁用的 API 路由
├── 解决 TypeScript 类型问题
└── 确保音乐订阅可用

Week 2: P1 稳定性
├── 添加连接池监控
├── 任务执行日志
└── 日志轮转配置

Week 3-4: P2 体验
├── 发现页分类
├── 搜索排序
└── 批量操作
```

---

## Evidence (P7)

### 分析方法

1. 扫描 `api/__init__.py` 中被注释的路由
2. 检查前端 TypeScript 错误
3. 对比功能完整性

### 引用文件

1. `backend/app/api/__init__.py` - 路由注册
2. `backend/app/core/database.py` - 连接池
3. `backend/app/core/logging.py` - 日志配置
4. `backend/app/core/scheduler.py` - 调度器
5. `backend/app/core/cache.py` - 缓存
6. `frontend/src/services/api.ts` - API 客户端
7. `frontend/src/pages/Discover.vue` - 发现页
8. `frontend/src/pages/Search.vue` - 搜索页
9. `frontend/src/pages/MusicCenter.vue` - 音乐中心
10. `frontend/package.json` - 前端配置

---

*生成时间: 2025-12-13 23:30 UTC+8*
