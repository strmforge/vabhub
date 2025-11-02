# 部署指南

## 部署选项

### 1. 最小骨架部署（快速验证）
**适用场景**: 快速功能验证、开发环境测试

```bash
# 使用最小骨架快速部署
git clone -b v1.6.0 https://github.com/strmforge/vabhub-deploy_min_skeleton.git
cd vabhub-deploy_min_skeleton
cp .env.example .env
# 编辑环境变量
docker-compose -f docker-compose.min.yml up -d
```

### 2. 完整部署（生产环境）
**适用场景**: 生产环境、完整功能使用

```bash
# 使用完整部署配置
git clone -b v1.6.0 https://github.com/strmforge/vabhub-deploy.git
cd vabhub-deploy
cp .env.example .env
# 编辑环境变量
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 3. Kubernetes 部署（集群环境）
**适用场景**: 高可用、集群部署

```bash
# 部署到 Kubernetes
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

## 渐进式部署策略

### 阶段1：最小验证
- 使用最小骨架验证核心功能
- 确认基础服务正常运行
- 验证 API 和前端交互

### 阶段2：功能扩展
- 添加插件系统
- 配置媒体库集成
- 设置通知和监控

### 阶段3：生产优化
- 配置高可用架构
- 设置备份和恢复
- 优化性能和安全

## 环境配置

### 开发环境
```bash
# 开发环境配置
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### 测试环境
```bash
# 测试环境配置
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d
```

### 生产环境
```bash
# 生产环境配置
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 监控和日志

### 健康检查
```bash
# 检查服务状态
curl http://localhost:8080/api/healthz
curl http://localhost:8090/health
```

### 日志查看
```bash
# 查看服务日志
docker-compose logs core
docker-compose logs web

# 查看 Kubernetes 日志
kubectl logs -f deployment/vabhub-core -n vabhub
```

## 备份和恢复

### 数据备份
```bash
# 运行备份脚本
./scripts/backup.sh

# 定时备份
0 2 * * * /path/to/vabhub-deploy/scripts/backup.sh
```

### 数据恢复
```bash
# 从备份恢复
./scripts/restore.sh /path/to/backup/file.tar.gz
```

## 故障排除

### 常见问题
1. **服务无法启动**: 检查端口冲突和资源限制
2. **数据库连接失败**: 验证数据库配置和网络连接
3. **存储空间不足**: 清理日志和临时文件

### 调试模式
```bash
# 启用调试模式
export VABHUB_DEBUG=true
docker-compose up -d
```