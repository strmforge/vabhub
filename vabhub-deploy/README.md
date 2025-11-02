# VabHub Deploy v1.5.0

VabHub 部署配置仓库，包含Docker Compose、Kubernetes配置和部署脚本。

## 功能特性

- 🐳 Docker Compose 编排
- ☸️ Kubernetes 配置
- 🔧 部署脚本
- 📊 监控配置
- 🔐 安全配置

## 快速开始

### 环境要求
- Docker & Docker Compose
- Kubernetes (可选)

### 本地部署
```bash
# 克隆仓库
git clone https://github.com/your-org/vabhub-deploy.git
cd vabhub-deploy

# 复制环境配置
cp .env.example .env
# 编辑环境变量

# 启动服务
docker-compose up -d
```

### Kubernetes 部署
```bash
# 部署到Kubernetes
kubectl apply -f kubernetes/

# 查看部署状态
kubectl get pods -n vabhub
```

## 项目结构

```
vabhub-deploy/
├── docker-compose.yml      # Docker Compose配置
├── docker-compose.prod.yml # 生产环境配置
├── docker-compose.dev.yml  # 开发环境配置
├── kubernetes/            # K8s配置
│   ├── namespace.yaml     # 命名空间
│   ├── configmap.yaml     # 配置映射
│   ├── secret.yaml        # 密钥配置
│   ├── deployment.yaml   # 部署配置
│   ├── service.yaml      # 服务配置
│   └── ingress.yaml      # 入口配置
├── scripts/              # 部署脚本
│   ├── deploy.sh         # 部署脚本
│   ├── backup.sh         # 备份脚本
│   └── health-check.sh   # 健康检查
└── monitoring/           # 监控配置
    ├── prometheus.yml    # Prometheus配置
    ├── grafana.yml       # Grafana配置
    └── alertmanager.yml  # 告警配置
```

## 部署配置

### 环境变量配置

创建 `.env` 文件并配置以下变量：

```bash
# 数据库配置
POSTGRES_DB=vabhub
POSTGRES_USER=vabhub
POSTGRES_PASSWORD=your_password

# Redis配置
REDIS_PASSWORD=your_redis_password

# 应用配置
VABHUB_SECRET_KEY=your_secret_key
VABHUB_DEBUG=false

# 服务端口
CORE_PORT=8080
WEB_PORT=8090
```

### Docker Compose 部署

```bash
# 开发环境
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# 生产环境
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Kubernetes 部署

```bash
# 创建命名空间
kubectl apply -f kubernetes/namespace.yaml

# 创建配置
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml

# 部署服务
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

## 监控和日志

### 监控配置

- **Prometheus**: 指标收集和监控
- **Grafana**: 数据可视化和仪表板
- **Alertmanager**: 告警管理

### 日志配置

- **ELK Stack**: 日志收集和分析
- **Fluentd**: 日志聚合
- **Kibana**: 日志可视化

## 备份和恢复

### 数据备份

```bash
# 运行备份脚本
./scripts/backup.sh

# 定时备份 (crontab)
0 2 * * * /path/to/vabhub-deploy/scripts/backup.sh
```

### 数据恢复

```bash
# 从备份恢复
./scripts/restore.sh /path/to/backup/file.tar.gz
```

## 安全配置

### 网络安全

- 使用TLS/SSL加密通信
- 配置防火墙规则
- 限制网络访问

### 访问控制

- RBAC权限管理
- API密钥轮换
- 审计日志记录

## 故障排除

### 常见问题

1. **服务无法启动**: 检查端口冲突和资源限制
2. **数据库连接失败**: 验证数据库配置和网络连接
3. **存储空间不足**: 清理日志和临时文件

### 日志查看

```bash
# 查看服务日志
docker-compose logs core
docker-compose logs web

# 查看Kubernetes日志
kubectl logs -f deployment/vabhub-core -n vabhub
```