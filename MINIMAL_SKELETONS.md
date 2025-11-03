# 最小骨架仓库

## 概述

VabHub 提供最小骨架仓库，用于快速验证和部署基础功能。

## 可用骨架

### vabhub-Core_min_skeleton
**功能**: 最小可运行后端，暴露 `/api/healthz`、`/api/version`
**包含**:
- FastAPI 基础应用
- CORS 中间件配置
- 健康检查和版本接口

### vabhub-frontend_min_skeleton  
**功能**: 最小 Vue3 + Vite 前端，包含完整的 LogCenter 组件
**包含**:
- Vue 3 + TypeScript 基础配置
- 环境变量配置
- LogCenter 组件（WebSocket 实时日志显示）
- 基础组件结构

### vabhub-deploy_min_skeleton
**功能**: Compose 最小栈：qBittorrent + Emby + Core + Frontend
**包含**:
- Docker Compose 基础配置
- 服务编排定义
- 环境变量模板

## 使用方式

### 快速验证
```bash
# 使用最小骨架快速验证功能
git clone -b v1.5.0 https://github.com/strmforge/vabhub-Core_min_skeleton.git
cd vabhub-Core_min_skeleton
pip install -r requirements.txt
python app/main.py
```

### 渐进式开发
1. 从最小骨架开始验证核心功能
2. 逐步添加业务逻辑和扩展功能
3. 最终迁移到完整实现

## 压缩包分发

每个骨架仓库都提供 `.zip` 压缩包，便于快速分发和部署。

## 验证脚本

每个骨架包含冒烟测试脚本，确保基础功能正常工作。

## 新增功能

### WebSocket 日志中心
vabhub-frontend_min_skeleton 现在包含完整的 LogCenter 组件，支持：
- 实时 WebSocket 连接
- 日志消息实时显示
- 错误处理和连接状态监控
- 可配置的 WebSocket 端点