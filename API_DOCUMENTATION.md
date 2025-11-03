# VabHub API 文档 v1.6.0

## 📋 概述

VabHub 提供完整的 RESTful API 和 GraphQL API，支持媒体管理、发现推荐、下载控制等功能。

## 🔌 API 端点

### 基础信息
- **API 地址**: `http://localhost:4001`
- **文档地址**: `http://localhost:4001/docs` (Swagger UI)
- **GraphQL 地址**: `http://localhost:4001/graphql`

### 健康检查
```http
GET /health
```
**响应**:
```json
{
  "status": "healthy",
  "version": "1.5.0",
  "timestamp": "2025-11-01T10:00:00Z"
}
```

## 🎯 核心 API 功能

### 1. 自动化订阅系统 (v1.6.0 新增)

#### 创建订阅
```http
POST /api/subscription/create
```
**请求体**:
```json
{
  "name": "热门电影订阅",
  "query": "movie AND year>=2024 AND rating>=8.0",
  "enabled": true,
  "priority": 1,
  "channels": ["telegram", "email"],
  "rules": {
    "quality": "1080p",
    "language": "zh-CN",
    "size_limit": "10GB"
  }
}
```

#### 获取订阅列表
```http
GET /api/subscription/list
```
**参数**:
- `status` (可选): 订阅状态 (active, paused, completed)
- `page` (可选): 页码 (默认: 1)
- `page_size` (可选): 每页数量 (默认: 20)

#### 更新订阅
```http
PUT /api/subscription/{id}/update
```

#### 删除订阅
```http
DELETE /api/subscription/{id}
```

### 2. 文件整理系统 (v1.6.0 新增)

#### 智能重命名
```http
POST /api/file-organizer/rename
```
**请求体**:
```json
{
  "files": [
    "/path/to/movie.2024.1080p.mkv",
    "/path/to/tvshow.s01e01.mkv"
  ],
  "template": "{title} ({year}) - {quality}",
  "overwrite": false
}
```

#### 批量整理
```http
POST /api/file-organizer/organize
```
**请求体**:
```json
{
  "source_dir": "/downloads",
  "target_dir": "/media",
  "rules": {
    "movies": "Movies/{title} ({year})/{title}.{ext}",
    "tv_shows": "TV Shows/{title}/Season {season}/{title} S{season}E{episode}.{ext}"
  }
}
```

#### 获取整理状态
```http
GET /api/file-organizer/status
```

### 3. 媒体服务器集成 (v1.6.0 增强)

#### 服务器状态检查
```http
GET /api/media-server/status
```

#### 同步媒体库
```http
POST /api/media-server/sync
```

### 4. 通知系统增强 (v1.6.0 新增)

#### 发送通知
```http
POST /api/notification/send
```
**请求体**:
```json
{
  "title": "下载完成",
  "message": "电影《盗梦空间》下载完成",
  "priority": "high",
  "channels": ["telegram", "email"],
  "template": "download_complete",
  "metadata": {
    "filename": "Inception.2010.1080p.mkv",
    "size": "8.7GB",
    "duration": "2小时28分钟"
  }
}
```

#### 获取通知状态
```http
GET /api/notification/status
```

#### 使用模板发送
```http
POST /api/notification/template
```
**请求体**:
```json
{
  "template_name": "download_complete",
  "variables": {
    "title": "盗梦空间",
    "filename": "Inception.2010.1080p.mkv",
    "size": "8.7GB",
    "duration": "2小时28分钟"
  }
}
```

### 5. 发现推荐系统

#### 获取推荐内容
```http
GET /api/recommendations
```
**参数**:
- `type` (可选): 内容类型 (movie, tv, music, all)
- `limit` (可选): 返回数量 (默认: 10)
- `user_id` (可选): 用户ID (个性化推荐)

**响应**:
```json
{
  "recommendations": [
    {
      "id": "movie_123",
      "title": "盗梦空间",
      "type": "movie",
      "score": 0.95,
      "source": "tmdb",
      "metadata": {
        "year": 2010,
        "genres": ["科幻", "动作"],
        "rating": 8.8
      }
    }
  ]
}
```

#### 音乐榜单
```http
GET /api/charts/music
```
**参数**:
- `platform` (可选): 平台 (qqmusic, netease, spotify, apple)
- `chart_type` (可选): 榜单类型 (hot, new, trending)

### 2. 媒体管理

#### 搜索媒体
```http
GET /api/search
```
**参数**:
- `query`: 搜索关键词
- `type` (可选): 媒体类型
- `year` (可选): 年份过滤

#### 获取媒体详情
```http
GET /api/media/{media_id}
```

### 3. 下载管理

#### 添加下载任务
```http
POST /api/downloads
```
**请求体**:
```json
{
  "url": "magnet:?xt=urn:btih:...",
  "category": "movie",
  "priority": "high"
}
```

#### 获取下载状态
```http
GET /api/downloads/{task_id}
```

### 4. 插件系统

#### 获取插件列表
```http
GET /api/plugins
```

#### 安装插件
```http
POST /api/plugins/install
```
**请求体**:
```json
{
  "plugin_id": "music-charts",
  "version": "1.0.0"
}
```

## 🚀 GraphQL API

### 查询示例

```graphql
query GetRecommendations($type: MediaType, $limit: Int) {
  recommendations(type: $type, limit: $limit) {
    id
    title
    type
    score
    metadata {
      year
      genres
      rating
    }
  }
}
```

### 变更示例

```graphql
mutation AddDownload($input: DownloadInput!) {
  addDownload(input: $input) {
    id
    status
    progress
  }
}
```

## 🔐 认证和授权

### API 密钥认证
部分 API 需要 API 密钥认证：

```http
GET /api/protected-endpoint
Authorization: Bearer YOUR_API_KEY
```

### 用户认证
用户相关 API 需要 JWT 令牌：

```http
GET /api/user/profile
Authorization: Bearer YOUR_JWT_TOKEN
```

## 📊 错误处理

### 标准错误响应
```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "参数验证失败",
    "details": {
      "field": "year",
      "issue": "必须是数字"
    }
  }
}
```

### 常见错误码
- `400`: 请求参数错误
- `401`: 未授权访问
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器内部错误

## ⚡ 性能优化

### 缓存策略
- 推荐结果缓存: 15分钟
- 媒体详情缓存: 1小时
- 榜单数据缓存: 30分钟

### 分页支持
所有列表 API 支持分页：
```http
GET /api/media?page=1&page_size=20
```

## 🔧 开发工具

### API 测试
使用 Swagger UI 进行 API 测试：
```
http://localhost:4001/docs
```

### GraphQL Playground
使用 GraphQL Playground 进行 GraphQL 查询：
```
http://localhost:4001/graphql
```

## 📈 监控和指标

### 健康检查端点
```http
GET /health
GET /metrics
```

### 性能指标
- API 响应时间
- 请求成功率
- 并发连接数
- 缓存命中率

## 🔄 版本管理

### API 版本
当前 API 版本: `v1`

### 向后兼容性
- 所有 API 变更保持向后兼容
- 废弃的 API 会提前通知
- 新功能通过新端点添加

## 🤝 社区支持

### 问题反馈
- GitHub Issues: [项目 Issues](https://github.com/strmforge/vabhub/issues)
- 文档更新: 提交 Pull Request

### 贡献指南
参考 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

**最后更新**: 2025-11-01  
**版本**: v1.6.0  
**维护者**: VabHub 开发团队