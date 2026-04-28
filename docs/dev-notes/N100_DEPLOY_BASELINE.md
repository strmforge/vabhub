# N100 部署基线 (DEPLOY-N100-1 P0)

> 记录 N100 服务器的部署环境基线信息，用于后续部署排错参考

---

## 服务器信息

| 项目 | 值 |
|------|-----|
| 主机名 | N100 (Intel N100 迷你主机) |
| IP | 192.168.50.102 |
| 部署路径 | `/opt/vabhub` |
| VabHub 端口 | 52180 |

---

## 环境基线 (待填写)

> 首次部署时在 N100 上执行以下命令，将输出粘贴到下方

### 1. 工作目录确认

```bash
cd /opt/vabhub && pwd && ls -la
```

**输出**:
```
# 首次部署时填写
```

### 2. Git 版本

```bash
git rev-parse HEAD
```

**输出**:
```
# 首次部署时填写
```

### 3. Docker 版本

```bash
docker --version
```

**输出**:
```
# 首次部署时填写
```

### 4. Docker Compose 版本

```bash
docker compose version
```

**输出**:
```
# 首次部署时填写
```

---

## 必要文件检查

| 文件 | 用途 | 状态 |
|------|------|------|
| `docker-compose.yml` | 开发/本地构建部署 | ✅ 存在 |
| `docker-compose.prod.yml` | 生产镜像部署 | ✅ 存在 |
| `.env.docker` | 环境变量配置 | ⚠️ 需从 example 复制 |

### 主用配置

- **推荐**: `docker-compose.yml` (本地 build)
- **备选**: `docker-compose.prod.yml` (拉取 GHCR 镜像)

---

## .env.docker 必填项

```bash
# 必须设置（否则 compose 会报错）
DB_PASSWORD=<你的数据库密码>

# 可选（有默认值）
VABHUB_PORT=52180
TZ=Asia/Shanghai
SUPERUSER_NAME=admin
SUPERUSER_PASSWORD=<首次启动的管理员密码，留空则自动生成>
```

---

## 快速命令参考

```bash
# 进入目录
cd /opt/vabhub

# 拉取最新代码
git pull origin main

# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f vabhub

# 健康检查
curl http://localhost:52180/health

# 停止服务
docker compose down
```

---

## 注意事项

1. **不要在 Windows 上执行 `docker compose build/up`**
   - Windows Docker Desktop 构建的镜像无法在 Linux 上运行
   - 所有 docker 命令必须在 N100 上执行

2. **SSH 密钥配置**
   - 确保 Windows 上已配置 SSH 密钥可免密登录 N100
   - `ssh n100` 或 `ssh user@192.168.50.102`

3. **首次部署后记得保存管理员密码**
   - `docker logs vabhub | grep "初始管理员"`

---

*创建时间: 2025-12-14*
*DEPLOY-N100-1 P0 交付物*
