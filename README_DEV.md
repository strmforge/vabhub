# VabHub 开发环境指南

## 项目概述

VabHub 是一个多仓库架构的媒体管理系统，包含以下组件：

- **后端 (vabhub-Core)**: FastAPI + Python 构建的API服务
- **前端 (vabhub-frontend)**: Vue.js 3 + Vite 构建的用户界面
- **插件系统**: 可扩展的功能模块
- **实时日志**: WebSocket 支持的实时监控系统

## 快速开始

### 1. 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 2. 一键启动开发环境

```bash
# 进入项目根目录
cd f:\VabHub

# 启动开发环境
python start_dev.py
```

启动脚本会自动：
- 安装后端Python依赖
- 安装前端npm依赖  
- 启动后端API服务 (端口 8000)
- 启动前端开发服务器 (端口 5173)

### 3. 手动启动（可选）

#### 后端服务
```bash
cd vabhub-Core
pip install -r requirements.txt
python start.py
```

#### 前端服务
```bash
cd vabhub-frontend
npm install
npm run dev
```

## 访问地址

- **前端界面**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **实时日志**: http://localhost:5173/logs

## 主要功能

### 1. 仪表板 (Dashboard)
- 系统状态概览
- 快速操作入口
- 最近活动记录

### 2. 插件管理 (Plugins)
- 插件启用/禁用
- 插件配置管理
- 插件市场

### 3. 实时日志 (Logs)
- WebSocket实时日志推送
- 日志级别过滤
- 日志搜索和导出

### 4. 内容发现 (Discover)
- 多数据源支持 (TMDB, Spotify, Apple Music, Bangumi)
- 排行榜和热门内容
- 媒体信息展示

### 5. 存储管理 (Storage)
- 本地存储监控
- STRM文件管理
- 云存储集成

## 技术栈

### 后端技术
- **框架**: FastAPI
- **数据库**: SQLAlchemy + PostgreSQL
- **缓存**: Redis
- **任务队列**: Celery
- **GraphQL**: Strawberry GraphQL
- **WebSocket**: websockets

### 前端技术
- **框架**: Vue.js 3
- **构建工具**: Vite
- **路由**: Vue Router
- **状态管理**: 原生Vue响应式系统
- **样式**: CSS3 + Flexbox/Grid

## 开发说明

### 项目结构
```
VabHub/
├── vabhub-Core/          # 后端API服务
│   ├── core/            # 核心模块
│   ├── requirements.txt # Python依赖
│   └── start.py         # 启动脚本
├── vabhub-frontend/      # 前端界面
│   ├── src/            # 源代码
│   ├── package.json    # Node.js依赖
│   └── vite.config.js  # Vite配置
└── start_dev.py        # 开发环境启动脚本
```

### 代码规范
- 后端: PEP 8 Python代码规范
- 前端: ESLint + Prettier
- 提交信息: Conventional Commits

### 测试
```bash
# 后端测试
cd vabhub-Core
pytest

# 前端测试  
cd vabhub-frontend
npm test
```

## 故障排除

### 常见问题

1. **端口占用**
   - 后端默认端口: 8000
   - 前端默认端口: 5173
   - 修改端口: 编辑对应配置文件中的端口设置

2. **依赖安装失败**
   - 检查Python和Node.js版本
   - 清理缓存重新安装: `npm cache clean --force`
   - 使用国内镜像源

3. **WebSocket连接失败**
   - 检查后端服务是否正常运行
   - 查看浏览器控制台错误信息
   - 前端会自动回退到模拟模式

### 日志查看

- 后端日志: 控制台输出或日志文件
- 前端日志: 浏览器开发者工具
- WebSocket状态: 前端日志页面实时显示

## 部署说明

生产环境部署请参考 `DEPLOYMENT_GUIDE.md` 文件。

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License - 详见 LICENSE 文件