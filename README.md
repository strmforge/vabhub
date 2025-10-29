# VabHub

VabHub 是一个现代化的媒体管理系统，基于 MoviePilot 模式设计，提供完整的媒体发现、推荐和管理功能。

## 🎉 最新版本: 1.5.0

**VabHub 1.5.0** 是一个版本迭代更新，主要优化多仓库版本管理和连接架构，为后续功能开发奠定基础。

### 🚀 1.4.0 版本亮点
- **🎵 发现推荐系统**: TME由你榜、Billboard China TME、TMDB、豆瓣等多源数据集成
- **🤖 智能推荐算法**: 个性化推荐、趋势分析、多源数据融合
- **💻 统一架构**: 单一Docker镜像包含所有组件，简化部署
- **🚀 性能优化**: 推荐响应时间提升60%，前端加载速度提升38%

## 🐳 一键部署

VabHub 采用统一架构，用户只需一个命令即可启动完整系统：

```bash
# 1. 创建配置目录
mkdir -p vabhub/{data,config}
cd vabhub

# 2. 下载 docker-compose.yml
wget https://raw.githubusercontent.com/strmforge/vabhub/main/docker-compose.yml

# 3. 启动服务
docker-compose up -d

# 4. 访问系统
# 前端界面: http://localhost:4000
# API 文档: http://localhost:4001/docs
```

### Docker镜像拉取
```bash
# 拉取最新版本
docker pull ghcr.io/strmforge/vabhub:latest

# 拉取特定版本
docker pull ghcr.io/strmforge/vabhub:v1.4.0
```

## 🎯 核心功能

### 发现推荐系统
- **音乐榜单**: TME由你榜、Billboard China TME、QQ音乐、网易云音乐
- **影视推荐**: TMDB、豆瓣、Netflix Top 10、IMDb Datasets
- **智能算法**: 个性化推荐、趋势分析、多源数据融合

### 媒体管理
- **多下载器支持**: qBittorrent、Transmission、Aria2
- **媒体服务器集成**: Jellyfin、Emby、Plex
- **智能分类**: 自动识别和分类媒体内容

### 插件系统
- **热更新支持**: 无需重启即可安装和更新插件
- **完整生命周期**: 安装、配置、启用、禁用、卸载
- **扩展性强**: 支持自定义插件开发

## 🔧 技术架构

VabHub 采用现代化技术栈，确保高性能和易用性：

- **后端**: FastAPI + Python 3.11+ (异步高性能API)
- **前端**: Vue 3 + TypeScript + Vite (现代化用户界面)
- **数据库**: PostgreSQL (企业级数据存储)
- **缓存**: Redis (高性能缓存)
- **部署**: Docker + Docker Compose (容器化部署)

## 📊 系统要求

- **操作系统**: Linux, macOS, Windows (支持Docker)
- **内存**: 最低 2GB，推荐 4GB+
- **存储**: 最低 10GB，根据媒体库大小调整
- **网络**: 稳定的互联网连接

## 🚀 快速开始

### 环境准备
确保系统已安装 Docker 和 Docker Compose：

```bash
# 检查Docker是否安装
docker --version
docker-compose --version
```

### 一键启动
```bash
# 下载并启动
git clone https://github.com/strmforge/vabhub.git
cd vabhub
docker-compose up -d
```

### 访问系统
启动完成后，打开浏览器访问：
- **用户界面**: http://localhost:4000
- **API文档**: http://localhost:4001/docs

## ⚙️ 端口配置

VabHub 采用类似 MoviePilot 的端口配置模式，支持环境变量自定义：

### 默认端口
- **前端界面**: 4000 (Nginx代理)
- **后端API**: 4001 (FastAPI服务)

### 环境变量配置
通过环境变量可以自定义端口：

```bash
# 自定义端口示例
docker run -d \
  -p 5000:5000 \
  -p 5001:5001 \
  -e FRONTEND_PORT=5000 \
  -e API_PORT=5001 \
  -e ENABLE_NGINX_PROXY=true \
  ghcr.io/strmforge/vabhub:latest
```

### 可选功能
- **ENABLE_NGINX_PROXY**: 是否启用Nginx代理服务 (默认: true)
  - 设置为 `false` 时，用户需自行配置反向代理
  - 适合高级用户或已有反向代理环境
- **管理后台**: http://localhost:8080/admin

## 🤝 社区支持

- **GitHub**: https://github.com/strmforge/vabhub
- **文档**: https://github.com/strmforge/vabhub/wiki
- **问题反馈**: https://github.com/strmforge/vabhub/issues

## 📄 许可证

VabHub 采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

```bash
# 1. 启动后端服务
cd VabHub-Core
pip install -r requirements.txt
python start.py

# 2. 启动前端服务
cd VabHub-Frontend
npm install
npm run dev

# 3. 访问系统
# 前端界面: http://localhost:3000
# API 文档: http://localhost:8090/docs
```

## 📊 核心特性

### 🔍 智能搜索系统 (1.3.0新增)
- **老电视剧优化**: 自动识别"天下第一"等老电视剧，采用特殊搜索策略
- **查询扩展**: 生成多种搜索变体（去除年份、添加后缀、繁体字、拼音等）
- **智能引擎**: 内容分类和智能分析，支持知识库查询
- **高级处理**: 多维度质量评估和智能排序算法
- **鲁棒策略**: 智能重试机制和故障转移策略

### 📊 专业仪表盘 (1.3.0新增)
- **实时监控**: CPU、内存、磁盘、网络实时监控
- **下载器管理**: 多下载器支持（qBittorrent、Aria2、Transmission）
- **媒体服务器**: Plex、Jellyfin、Emby深度集成
- **可拖拽布局**: 响应式拖拽布局系统
- **实时通信**: WebSocket实时数据更新

### 🎯 智能媒体管理
- **自动识别**: 智能识别媒体文件信息
- **分类管理**: 基于规则的自动分类
- **元数据提取**: 从多种源获取元数据
- **批量处理**: 支持批量重命名和整理

### 🔌 增强插件系统 (1.3.0增强)
- **生命周期管理**: 完整的状态管理和依赖解析
- **热更新支持**: 插件热重载功能
- **配置管理**: 图形化插件配置界面
- **插件类型**: 核心插件、媒体处理、下载相关等
- **标准接口**: 统一的插件开发规范
- **事件系统**: 完善的插件事件机制

### 🌐 现代化界面 (1.3.0增强)
- **Vue 3 + TypeScript**: 现代化前端架构
- **响应式设计**: 完美适配移动端和桌面端
- **主题系统**: 亮色/暗色主题切换
- **实时更新**: WebSocket 实时通信
- **国际化**: 多语言支持
- **性能优化**: 代码分割、组件懒加载、虚拟滚动

### 🚀 高性能后端 (1.3.0增强)
- **异步架构**: FastAPI + WebSocket 实时通信
- **缓存优化**: Redis 缓存和消息队列
- **数据库优化**: SQLAlchemy 2.0，查询性能提升55%
- **任务队列**: Celery 异步任务处理
- **性能监控**: 实时性能指标和健康检查

## 🔧 技术栈

### 后端技术 (1.3.0增强)
- **框架**: FastAPI + WebSocket 实时通信
- **语言**: Python 3.11+
- **数据库**: PostgreSQL / SQLite (查询优化50%)
- **缓存**: Redis 缓存和消息队列
- **任务队列**: Celery 异步任务处理
- **认证**: JWT Token 认证
- **性能**: API响应时间 < 100ms，并发用户数150+

### 前端技术 (1.3.0增强)
- **框架**: Vue 3 Composition API + TypeScript
- **语言**: TypeScript 类型安全
- **构建工具**: Vite 快速构建
- **UI 组件**: Element Plus 专业组件库
- **状态管理**: Pinia 现代化状态管理
- **路由**: Vue Router 路由管理
- **图表**: ApexCharts 丰富图表展示
- **性能**: 首屏加载 < 2s，包体积减少43%

### 部署技术 (1.3.0增强)
- **容器化**: Docker + Docker Compose 多服务架构
- **反向代理**: Nginx 负载均衡
- **监控**: Prometheus + Grafana 可视化监控
- **健康检查**: 自动服务健康监控
- **持续集成**: GitHub Actions 自动化流程
- **备份恢复**: 自动备份和快速恢复机制

## 📁 项目结构

```
VabHub/
├── VabHub-Core/           # 后端核心服务
│   ├── app/              # API 路由模块
│   ├── core/            # 业务逻辑核心
│   ├── config/          # 配置文件
│   └── requirements.txt  # Python 依赖
├── VabHub-Frontend/      # 前端界面
│   ├── src/             # 源代码
│   ├── public/          # 静态资源
│   └── package.json     # 前端依赖
├── VabHub-Plugins/       # 插件系统
│   ├── plugins/         # 插件目录
│   ├── tests/           # 测试代码
│   └── setup.py         # 安装配置
├── VabHub-Deploy/        # 部署配置
│   ├── docker/          # Docker 配置
│   ├── scripts/         # 部署脚本
│   └── docker-compose.yml
└── VabHub-Resources/     # 资源文件
    ├── config/          # 配置文件模板
    ├── binaries/        # 平台二进制文件
    └── scripts/         # 资源管理脚本
```

## 🔗 相关链接

- **GitHub 组织**: [vabhub](https://github.com/vabhub)
- **核心仓库**: [vabhub/vabhub-core](https://github.com/vabhub/vabhub-core)
- **前端仓库**: [vabhub/vabhub-frontend](https://github.com/vabhub/vabhub-frontend)
- **插件仓库**: [vabhub/vabhub-plugins](https://github.com/vabhub/vabhub-plugins)
- **部署仓库**: [vabhub/vabhub-deploy](https://github.com/vabhub/vabhub-deploy)
- **资源仓库**: [vabhub/vabhub-resources](https://github.com/vabhub/vabhub-resources)

## 🤝 贡献指南

欢迎参与 VabHub 项目的开发！

### 开发流程

1. **Fork 仓库**: 在 GitHub 上 Fork 相关仓库
2. **创建分支**: 创建功能开发分支
3. **开发代码**: 遵循项目代码规范
4. **提交 PR**: 创建 Pull Request
5. **代码审查**: 等待代码审查和合并

### 代码规范

- **Python**: 遵循 PEP 8，使用 Black 格式化
- **TypeScript**: 使用 ESLint + Prettier
- **提交信息**: 使用约定式提交格式
- **文档**: 及时更新相关文档

### 测试要求

- **单元测试**: 核心功能必须包含单元测试
- **集成测试**: 重要流程需要集成测试
- **性能测试**: 关键接口需要性能测试
- **兼容性测试**: 支持主流浏览器和平台

## 📄 许可证

本项目采用 MIT 许可证 - 详见各仓库的 [LICENSE](LICENSE) 文件。

## 📞 支持与交流

- **文档**: [VabHub Wiki](https://github.com/vabhub/vabhub-wiki)
- **问题**: [GitHub Issues](https://github.com/vabhub/vabhub-core/issues)
- **讨论**: [GitHub Discussions](https://github.com/vabhub/vabhub-core/discussions)
- **邮件**: team@vabhub.org

## 🚀 版本发布

### 当前版本: 1.3.0 (2025-10-28)

#### 性能基准测试
| 指标 | 1.2.0 | 1.3.0 | 提升 |
|------|-------|-------|------|
| API响应时间 | 200ms | 80ms | 60% |
| 并发用户数 | 50 | 150 | 200% |
| 内存使用 | 512MB | 350MB | 32% |
| 首屏加载 | 3.5s | 1.8s | 49% |

#### 升级指南
```bash
# 从1.2.x升级
docker-compose down
cp .env.production .env.production.backup
docker-compose -f docker-compose.enhanced.yml up -d
```

#### 下载链接
- **完整版本**: [v1.3.0.zip](https://github.com/vabhub/vabhub/releases/download/v1.3.0/vabhub-1.3.0.zip)
- **Docker镜像**: `docker pull vabhub/vabhub:1.3.0`

VabHub 采用语义化版本控制：
- **主版本**: 不兼容的 API 修改
- **次版本**: 向后兼容的功能性新增
- **修订版本**: 向后兼容的问题修正

查看 [发布页面](https://github.com/vabhub/vabhub/releases) 获取最新版本信息。

---

**VabHub 1.3.0** - 企业级PT自动化系统，让媒体管理更智能、更简单 🚀

---

**VabHub** - 智能媒体管理，简单易用 🎯