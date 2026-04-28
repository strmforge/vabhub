# VabHub Docker 部署 (DEPLOY_DOCKER)

> 审计 Commit: `9af3cd0e02012aeadf7c72275ac1d62159bbd56c`

---

## Docker Compose 结构

### 服务清单

| 服务 | 镜像 | 端口 | 职责 |
|------|------|------|------|
| vabhub | strmforge/vabhub:latest | 52180 | 主应用（前端+后端） |
| db | postgres:14-alpine | 5432 | PostgreSQL 数据库 |
| redis | redis:7-alpine | 6379 | 缓存 & 消息队列 |

### docker-compose.yml 分析

**文件**: `docker-compose.yml` (4638 bytes)

```yaml
version: '3.8'

services:
  vabhub:
    image: strmforge/vabhub:${VERSION:-latest}
    container_name: vabhub
    environment:
      - DATABASE_URL=postgresql://${DB_USER:-vabhub}:${DB_PASSWORD}@db:5432/${DB_NAME:-vabhub}
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - VABHUB_PORT=${VABHUB_PORT:-52180}
      - TZ=Asia/Shanghai
    volumes:
      - vabhub_data:/app/data
      - vabhub_logs:/app/logs
      - /var/run/docker.sock:/var/run/docker.sock:ro  # 可选：UI升级
    ports:
      - "${VABHUB_PORT:-52180}:${VABHUB_PORT:-52180}"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:14-alpine
    container_name: vabhub-db
    environment:
      POSTGRES_DB: ${DB_NAME:-vabhub}
      POSTGRES_USER: ${DB_USER:-vabhub}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - vabhub_postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-vabhub}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: vabhub-redis
    volumes:
      - vabhub_redis:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  vabhub_data:
  vabhub_logs:
  vabhub_postgres:
  vabhub_redis:
```

---

## 卷挂载

### 命名卷（默认）

| 卷名 | 容器路径 | 用途 |
|------|----------|------|
| vabhub_data | /app/data | 应用数据 |
| vabhub_logs | /app/logs | 日志文件 |
| vabhub_postgres | /var/lib/postgresql/data | 数据库 |
| vabhub_redis | /data | Redis 持久化 |

### /config 模式（0.0.3）

**环境变量**：
```bash
VABHUB_CONFIG_DIR=/config
VABHUB_DATA_DIR=/config/data
VABHUB_LOG_DIR=/config/logs
```

**卷挂载示例**：
```yaml
volumes:
  - ./config:/config
  - /mnt/media:/media:ro      # 媒体库（只读）
  - /mnt/downloads:/downloads  # 下载目录
```

---

## 端口配置

| 端口 | 服务 | 说明 |
|------|------|------|
| 52180 | vabhub | Web UI + API（默认） |
| 5432 | db | PostgreSQL（内部网络） |
| 6379 | redis | Redis（内部网络） |

**端口选择理由**：
- 避开常见端口：8080, 7878 (Radarr), 8989 (Sonarr), 9091 (Transmission)
- 52180 易记且无冲突

---

## 健康检查

### 应用健康

```bash
# 基础健康检查
curl http://localhost:52180/health

# 详细健康检查
curl http://localhost:52180/api/health
```

**响应示例**：
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "version": "0.0.3"
}
```

### 数据库健康

```bash
docker exec vabhub-db pg_isready -U vabhub
```

### Redis 健康

```bash
docker exec vabhub-redis redis-cli ping
```

---

## 升级流程

### 标准升级

```bash
# 1. 拉取最新镜像
docker compose pull

# 2. 重建容器
docker compose up -d

# 3. 查看日志确认启动
docker compose logs -f vabhub
```

### 指定版本升级

```bash
# 编辑 docker-compose.yml 或 .env
VERSION=0.0.3

# 拉取并重建
docker compose pull
docker compose up -d
```

### 回滚

```bash
# 指定旧版本
VERSION=0.0.2 docker compose up -d
```

---

## 备份与恢复

### 数据备份

```bash
# 备份数据库
docker exec vabhub-db pg_dump -U vabhub vabhub > backup_$(date +%Y%m%d).sql

# 备份数据卷
docker run --rm -v vabhub_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/vabhub_data_$(date +%Y%m%d).tar.gz -C /data .
```

### 数据恢复

```bash
# 恢复数据库
cat backup_20251213.sql | docker exec -i vabhub-db psql -U vabhub vabhub

# 恢复数据卷
docker run --rm -v vabhub_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/vabhub_data_20251213.tar.gz -C /data
```

---

## 常见故障

### 1. 数据库连接失败

**症状**：启动时报错 `connection refused`

**排查**：
```bash
# 检查 db 容器状态
docker compose ps db
docker compose logs db
```

**解决**：
- 确保 `DB_PASSWORD` 已设置
- 等待数据库健康检查通过

### 2. Redis 连接失败

**症状**：缓存不可用

**排查**：
```bash
docker compose ps redis
docker exec vabhub-redis redis-cli ping
```

**解决**：
- 检查 Redis 容器是否运行
- 确认 `REDIS_URL` 配置正确

### 3. 端口冲突

**症状**：`bind: address already in use`

**排查**：
```bash
netstat -tlnp | grep 52180
```

**解决**：
- 修改 `VABHUB_PORT` 环境变量
- 或停止占用端口的服务

### 4. 权限问题

**症状**：无法写入 `/app/data`

**解决**：
```bash
# 使用命名卷（推荐）
# 或设置目录权限
sudo chown -R 1000:1000 ./config
```

---

## 生产环境配置

### 推荐配置

```yaml
# docker-compose.prod.yml
services:
  vabhub:
    image: strmforge/vabhub:0.0.3  # 固定版本
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 512M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 环境变量文件

```bash
# .env.docker
DB_PASSWORD=your_secure_password
SECRET_KEY=your_random_secret
JWT_SECRET_KEY=your_jwt_secret
VABHUB_PORT=52180
TZ=Asia/Shanghai
```

---

## Evidence (PZ-DEPLOY)

### 分析文件

1. `docker-compose.yml`
2. `docker-compose.prod.yml`
3. `Dockerfile`
4. `.env.docker.example`
5. `docs/user/DEPLOY_WITH_DOCKER.md`

### 关键发现

1. **All-in-One 架构** - 前端后端合一
2. **健康检查完备** - 三个服务都有 healthcheck
3. **/config 模式** - 0.0.3 支持统一配置目录
4. **版本策略** - 支持固定版本部署

---

## /health 端点说明 (SYSTEM-AUDIT-FOLLOWUP-1)

### 端点用途

`/api/health/` 端点用于监控系统健康状态，适合作为：
- Docker healthcheck 目标
- 负载均衡器健康探测
- 监控系统告警源

### 端点列表

| 端点 | 返回码 | 说明 |
|------|--------|------|
| `GET /api/health/` | 200 (始终) | 基础检查 + DB 连接池状态 |
| `GET /api/health/full` | 200 (始终) | 完整检查 (DB + Cache + Disk) |
| `GET /api/health/db` | 200 (始终) | 单项 DB 检查 |

### 响应格式

```json
{
  "status": "ok",           // "ok" 或 "degraded"
  "version": "0.0.3",
  "time": "2025-12-14T02:10:00+00:00",
  "uptime_seconds": 3600,
  "db": {
    "ok": true,
    "latency_ms": 2,
    "pool": "Pool size: 5  Connections in pool: 5 ...",
    "error": null
  }
}
```

### Docker Compose 配置示例

```yaml
services:
  vabhub:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/api/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 故障排查

| status | db.ok | 含义 | 处理建议 |
|--------|-------|------|----------|
| ok | true | 正常 | - |
| degraded | false | DB 异常 | 检查数据库连接、连接池状态 |
| degraded | true | 其他组件异常 | 检查 /health/full 详情 |

---

*更新时间: 2025-12-14 02:16 UTC+8*
