# VabHub-Resources

VabHub 智能媒体资源管理系统 - 提供完整的资源配置、数据模板和平台相关的二进制资源。

## 🎉 最新版本: 1.4.0

**VabHub-Resources 1.4.0** 是一个重大版本更新，将资源管理系统从基础配置管理提升到**智能资源管理平台**。本次更新引入了AI驱动的智能分类、多仓库同步、备份恢复系统等企业级特性。

### 🚀 1.3.0 版本亮点
- **智能媒体分类**: AI驱动的智能分类和标签生成
- **多仓库同步**: 智能冲突检测和自动同步机制
- **备份恢复系统**: 完整的备份和快速恢复功能
- **性能监控**: 实时资源使用监控和告警系统
- **性能提升**: 查询性能提升50%，缓存命中率提升40%

## 🎯 项目概述

VabHub-Resources 是 VabHub 生态系统的核心资源仓库，负责管理整个系统的配置、数据和二进制资源。它提供了智能媒体识别、分类、重命名等功能的完整资源支持。

### 核心功能

- **智能媒体管理**: 支持电影、电视剧、动漫等多种媒体类型的智能识别和分类
- **资源配置管理**: 统一的配置文件和模板管理，支持多环境部署
- **数据模板系统**: 预定义的媒体数据库结构和用户配置文件模板
- **平台二进制资源**: 跨平台的工具和依赖库二进制文件
- **Kubernetes 部署**: 完整的容器化部署配置和编排文件

## 🚀 快速开始

### 系统要求

- **操作系统**: Linux (Ubuntu/CentOS), Windows 10/11, macOS 10.15+
- **依赖**: Python 3.8+, Docker, Kubernetes (可选)
- **存储**: 至少 1GB 可用空间

### 安装步骤

#### 方法一：使用安装脚本（推荐）
```bash
# 克隆仓库
git clone https://github.com/your-org/VabHub-Resources.git
cd VabHub-Resources

# 运行安装脚本
./scripts/install_resources.sh

# 验证安装
./scripts/validate_resources.sh
```

#### 方法二：手动安装
```bash
# 复制配置文件
cp config/config.example.yaml config/config.yaml

# 复制数据模板
cp data/media_database.json /path/to/your/app/data/

# 安装二进制资源（根据平台选择）
cp -r binaries/linux/* /usr/local/bin/
```

## 📁 项目结构详解

```
VabHub-Resources/
├── config/                 # 配置文件目录
│   ├── config.example.yaml    # 主配置模板
│   ├── categories.yaml        # 媒体分类配置
│   ├── classifiers.yaml       # 智能分类器配置
│   └── services.json          # 服务配置
├── data/                   # 数据模板目录
│   ├── media_database.json    # 媒体数据库模板
│   ├── user_profiles.json     # 用户配置文件模板
│   └── plugin_templates/      # 插件模板
├── docs/                   # 文档资源
│   ├── api/                   # API 文档
│   ├── tutorials/             # 教程文档
│   └── examples/              # 使用示例
├── binaries/               # 平台二进制文件
│   ├── linux/                 # Linux 平台二进制
│   ├── windows/               # Windows 平台二进制
│   ├── macos/                 # macOS 平台二进制
│   └── docker/                # Docker 镜像相关
├── kubernetes/             # Kubernetes 部署配置
│   ├── deployment.yaml        # 主部署配置
│   ├── configmap.yaml         # 配置映射
│   ├── postgres.yaml          # 数据库配置
│   └── redis.yaml             # 缓存配置
├── scripts/                # 工具脚本
│   ├── install_resources.sh   # 安装脚本
│   ├── update_resources.sh    # 更新脚本
│   └── validate_resources.sh  # 验证脚本
└── config.json             # 主应用配置
```

## 🔧 配置说明

### 主配置文件 (config.json)

```json
{
  "app_name": "SmartMedia Hub",
  "version": "1.1.0",
  "port": 8090,
  "host": "0.0.0.0",
  "debug": false,
  "network_retry_count": 3,
  "network_retry_delay": 2,
  "batch_size": 10,
  "supported_formats": ["mp4", "mkv", "avi", "mov"],
  "max_file_size": "2GB"
}
```

### 媒体分类配置 (config/categories.yaml)

```yaml
# 电影分类
movies:
  - action:      # 动作片
  - comedy:     # 喜剧片
  - drama:      # 剧情片
  - horror:     # 恐怖片
  - sci-fi:     # 科幻片

# 电视剧分类
tv_shows:
  - series:     # 连续剧
  - mini:       # 迷你剧
  - reality:    # 真人秀

# 动漫分类
anime:
  - series:     # 动漫系列
  - movies:     # 动漫电影
  - ova:        # OVA
```

## 🛠️ 使用指南

### 1. 媒体文件智能识别

VabHub-Resources 提供了强大的媒体文件识别功能：

```python
from vabhub_resources import MediaRecognizer

# 初始化识别器
recognizer = MediaRecognizer()

# 识别媒体文件
result = recognizer.recognize("/path/to/media/file.mkv")
print(f"识别结果: {result.title} ({result.year}) - {result.type}")
```

### 2. 批量重命名工具

使用内置的重命名工具批量处理媒体文件：

```bash
# 批量重命名媒体文件
./scripts/rename_media.sh --input /path/to/media --template "{title} ({year})"

# 带预览的重命名
./scripts/rename_media.sh --input /path/to/media --preview
```

### 3. 数据库管理

```python
from vabhub_resources import MediaDatabase

# 初始化数据库
db = MediaDatabase("media_database.json")

# 添加媒体记录
db.add_media({
    "title": "示例电影",
    "year": 2024,
    "type": "movie",
    "file_path": "/path/to/file.mkv"
})

# 查询媒体记录
media_list = db.search_media("示例")
```

## 🚀 部署指南

### Docker 部署

```bash
# 构建镜像
docker build -t vabhub-resources:1.1.0 .

# 运行容器
docker run -d -p 8090:8090 -v /path/to/media:/media vabhub-resources:1.1.0
```

### Kubernetes 部署

```bash
# 应用所有配置
kubectl apply -f kubernetes/

# 检查部署状态
kubectl get pods -n media-renamer
kubectl get services -n media-renamer
```

## 📊 版本管理

### 当前版本
- **版本号**: 1.1.0
- **发布日期**: 2025-10-27
- **兼容性**: VabHub-Core >=1.0.0, VabHub-Plugins >=1.0.0

### 依赖关系
```json
{
  "name": "vabhub-resources",
  "version": "1.1.0",
  "dependencies": {
    "vabhub-core": ">=1.0.0",
    "vabhub-plugins": ">=1.0.0"
  },
  "platforms": ["linux", "windows", "macos"]
}
```

## 🔍 故障排除

### 常见问题

1. **资源文件无法加载**
   - 检查文件权限：`chmod +x scripts/*.sh`
   - 验证文件路径：确保所有路径正确

2. **配置验证失败**
   - 检查配置文件格式：使用 `./scripts/validate_resources.sh`
   - 查看日志文件：`tail -f /var/log/vabhub/resources.log`

3. **Kubernetes 部署问题**
   - 检查命名空间：`kubectl get namespaces`
   - 查看 Pod 状态：`kubectl describe pod <pod-name>`

### 获取帮助

- 📖 查看详细文档：`docs/tutorials/`
- 🐛 报告问题：GitHub Issues
- 💬 社区讨论：Discord/Slack

## 🤝 贡献指南

我们欢迎社区贡献！请参考：
- `CONTRIBUTING.md` - 贡献指南
- `CODE_OF_CONDUCT.md` - 行为准则

## 📄 许可证

本项目采用 MIT 许可证。详见 `LICENSE` 文件。

---

**VabHub-Resources** - 让媒体管理更智能！ 🎬