# VabHub Resources v1.5.0

VabHub 资源配置仓库，包含系统配置、数据文件、文档和Kubernetes部署配置。

## 功能特性

- 📋 统一配置管理
- 📊 数据文件存储
- 📚 文档资源
- ☸️ Kubernetes配置
- 🔧 脚本工具

## 快速开始

### 环境要求
- 无特殊要求，所有文件可直接使用

### 使用配置
```bash
# 克隆仓库
git clone https://github.com/your-org/vabhub-resources.git
cd vabhub-resources

# 查看可用配置
ls config/

# 使用配置示例
cp config/config.example.yaml config/config.yaml
# 编辑配置文件
```

### 安装资源
```bash
# 运行安装脚本
./scripts/install_resources.sh
```

## 项目结构

```
vabhub-resources/
├── config/           # 配置文件
│   ├── categories.yaml      # 分类配置
│   ├── charts_config.yaml   # 榜单配置
│   ├── media_library.yaml   # 媒体库配置
│   ├── storage_config.yaml  # 存储配置
│   └── config.example.yaml  # 配置示例
├── data/            # 数据文件
│   ├── media_database.json  # 媒体数据库
│   └── history/            # 历史数据
├── docs/            # 文档资源
│   ├── API_KEYS_GUIDE.md   # API密钥指南
│   ├── strm_usage.md       # 流媒体使用指南
│   └── tutorials/          # 教程文档
├── kubernetes/      # K8s配置
│   ├── configmap.yaml      # 配置映射
│   ├── deployment.yaml    # 部署配置
│   ├── postgres.yaml      # 数据库配置
│   └── redis.yaml         # Redis配置
└── scripts/         # 脚本工具
    └── install_resources.sh # 资源安装脚本
```

## 配置说明

### 主要配置文件

- **categories.yaml**: 媒体分类配置
- **charts_config.yaml**: 榜单数据源配置
- **media_library.yaml**: 媒体库路径配置
- **storage_config.yaml**: 云存储服务配置

### 数据文件

- **media_database.json**: 媒体数据库文件
- **history/**: 历史数据备份

### Kubernetes配置

- **configmap.yaml**: 应用配置映射
- **deployment.yaml**: 核心服务部署
- **postgres.yaml**: PostgreSQL数据库
- **redis.yaml**: Redis缓存服务

## 部署指南

请参考 [DEPLOYMENT.md](docs/DEPLOYMENT.md)