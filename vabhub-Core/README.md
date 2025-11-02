# VabHub Core v1.5.0

VabHub 核心后端服务，提供媒体管理、推荐算法、API接口等核心功能。

## 功能特性

- 🚀 高性能API服务
- 🤖 智能推荐算法
- 🔐 安全认证系统
- 📊 数据聚合与分析
- 🔌 插件系统支持

## 快速开始

### 环境要求
- Python 3.11+
- Docker & Docker Compose

### 本地开发
```bash
# 克隆仓库
git clone https://github.com/your-org/vabhub-Core.git
cd vabhub-Core

# 安装依赖
pip install -r requirements.txt

# 启动服务
python start.py
```

### Docker 运行
```bash
# 构建镜像
docker build -t vabhub-core .

# 运行容器
docker run -p 8080:8000 vabhub-core
```

## 项目结构

```
vabhub-Core/
├── api/           # API接口层
├── app/           # 应用层
├── core/          # 核心模块
├── utils/         # 工具类
├── config/        # 配置管理
├── tests/         # 测试代码
├── Dockerfile     # 容器配置
├── requirements.txt
└── start.py       # 启动脚本
```

## API 文档

启动服务后访问：http://localhost:8080/docs

## 贡献指南

请参考 [CONTRIBUTING.md](CONTRIBUTING.md)