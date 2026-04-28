# VabHub 部署到 N100 指南 (DEPLOY-N100-1 P3)

> 一页搞定 VabHub 部署到 N100 服务器

---

## 🚨 重要提示

> **不要在 Windows 本机执行 `docker compose build` 或 `docker compose up`！**
>
> Windows Docker Desktop 构建的镜像无法在 Linux 服务器上运行。
> 所有 Docker 命令必须在 N100 服务器上执行。
>
> **正确做法**：使用 `scripts/deploy_n100.ps1` 脚本，它会通过 SSH 在 N100 上执行所有命令。

---

## 准备工作

### 1. SSH 密钥配置

确保 Windows 可以免密 SSH 登录 N100：

```powershell
# 测试 SSH 连接
ssh haishuai@192.168.50.102 "echo OK"

# 如果需要配置密钥
ssh-keygen -t ed25519
ssh-copy-id haishuai@192.168.50.102
```

### 2. N100 服务器要求

- Docker 已安装 (`docker --version`)
- Docker Compose v2 已安装 (`docker compose version`)
- Git 已安装 (`git --version`)
- 项目已克隆到 `/opt/vabhub`

```bash
# 在 N100 上执行
cd /opt
git clone https://github.com/strmforge/VabHub.git vabhub
```

---

## 第一次部署

### 方法 1：使用部署脚本（推荐）

```powershell
# 在 Windows 上执行
cd E:\VabHub项目\VabHub
powershell -ExecutionPolicy Bypass -File .\scripts\deploy_n100.ps1
```

脚本会自动：
1. 检查 `.env.docker` 是否存在
2. 检查 `DB_PASSWORD` 是否设置
3. 执行 `git pull`
4. 执行 `docker compose up -d --build`
5. 显示健康检查结果

### 方法 2：手动 SSH 部署

```bash
# SSH 到 N100
ssh haishuai@192.168.50.102

# 进入项目目录
cd /opt/vabhub

# 配置环境变量
cp .env.docker.example .env.docker
nano .env.docker  # 设置 DB_PASSWORD

# 构建并启动
docker compose up -d --build

# 检查状态
docker compose ps
curl http://localhost:52180/health
```

### 首次启动后

1. **获取管理员密码**：
   ```bash
   docker logs vabhub | grep "初始管理员"
   ```

2. **访问 Web 界面**：
   ```
   http://192.168.50.102:52180/
   ```

---

## 日常更新

### 完整更新（包含代码变更）

```powershell
# Windows 上执行
.\scripts\deploy_n100.ps1
```

### 快速重启（不重新构建）

```powershell
.\scripts\deploy_n100.ps1 -NoBuild
```

### 查看部署日志

```powershell
.\scripts\deploy_n100.ps1 -TailLogs
```

---

## 常见错误排查

### ❌ `.env.docker` 缺失

**错误信息**：
```
[ERROR] 缺少 .env.docker 和 .env.docker.example
```

**解决方法**：
```bash
# SSH 到 N100
cd /opt/vabhub
cp .env.docker.example .env.docker
nano .env.docker  # 设置必要配置
```

### ❌ `DB_PASSWORD` 未设置

**错误信息**：
```
Please set DB_PASSWORD in .env.docker
```

**解决方法**：
```bash
# SSH 到 N100
cd /opt/vabhub
echo "DB_PASSWORD=your_secure_password_here" >> .env.docker
```

### ❌ 端口冲突

**错误信息**：
```
Error: bind: address already in use
```

**解决方法**：
```bash
# 查看占用端口的进程
sudo lsof -i :52180

# 或修改端口
echo "VABHUB_PORT=52181" >> .env.docker
```

### ❌ `/health` 返回 404

**可能原因**：
- 服务还在启动中（等待 30 秒）
- 数据库迁移失败

**排查步骤**：
```bash
# 查看日志
docker compose logs -f vabhub

# 检查数据库连接
docker compose exec vabhub python -c "from app.core.database import engine; print('DB OK')"
```

### ❌ DB 迁移失败

**错误信息**：
```
alembic.util.exc.CommandError: Can't locate revision
```

**解决方法**：
```bash
# 重置迁移（会丢失数据！）
docker compose down -v
docker compose up -d --build
```

---

## 运维命令速查

| 操作 | 命令 |
|------|------|
| 查看状态 | `docker compose ps` |
| 查看日志 | `docker compose logs -f vabhub` |
| 重启服务 | `docker compose restart vabhub` |
| 停止服务 | `docker compose down` |
| 清理重建 | `docker compose down -v && docker compose up -d --build` |
| 进入容器 | `docker compose exec vabhub bash` |
| 健康检查 | `curl http://localhost:52180/health` |

---

## 文件结构

```
/opt/vabhub/
├── docker-compose.yml      # 主配置（本地构建）
├── docker-compose.prod.yml # 生产配置（拉取镜像）
├── .env.docker             # 环境变量（需自行创建）
├── .env.docker.example     # 环境变量模板
├── Dockerfile              # 构建配置
└── scripts/
    ├── deploy_n100.ps1     # Windows 部署脚本
    └── n100_selfcheck.sh   # N100 自检脚本
```

---

*DEPLOY-N100-1 P3 交付物*
*创建时间: 2025-12-14*
