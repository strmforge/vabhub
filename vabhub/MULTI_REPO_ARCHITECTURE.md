# VabHub 多仓库架构实现报告

## 🏗️ 架构概述

VabHub 采用六仓分工的多仓库架构，每个仓库职责明确，协同工作：

## 📊 六仓分工明细

| 仓库 | 职能 | 主要产物 / 接口 | 彼此依赖 |
|------|------|------------------|----------|
| **vabhub（门户）** | 总入口与文档、版本编排、跨仓 Release 协调 | README/docs、versions.json、Release-propagate workflow | 读/写其它 5 仓版本号 |
| **vabhub-Core** | 后端：API/GraphQL、任务编排、WebSocket 日志、刮削与重命名集成、插件 Hook | REST /api/*、WS /ws/logs、(可选) GraphQL /graphql | 被 Frontend/Deploy/Plugins 使用 |
| **vabhub-frontend** | WebUI（Vue3/Vite）：控制台、实时日志、订阅与规则、服务器管理 | 浏览器 UI，对接 Core /api | 依赖 Core 运行 |
| **vabhub-deploy** | 部署编排：Compose/K8s、环境样例、冒烟自检 | docker-compose.*.yml、k8s/、checks/ | 同时拉起 Core/Frontend/外部服务 |
| **vabhub-plugins** | 插件生态：PDK 规范、示例插件（通知/后处理等） | plugin.json、Hook 约定、示例 | 通过 Core 的 Hook 调用 |
| **vabhub-resources** | 静态资源与模板：Logo/Icon、重命名模板、示例配置 | assets/、templates/ | 被 Frontend/Core 文档引用 |

## 🚀 各仓库详细功能

### 1) vabhub（门户）
**作用**: 项目首页与文档导航。单一事实源：用 versions.json 管理各子仓版本。触发跨仓版本推进（可选的 Release 工作流）

**核心功能**:
- 版本管理：versions.json 作为单一事实源
- 文档中心：架构文档和部署指南
- 版本协调：GitHub Actions 工作流
- 项目入口：README 和快速开始指南

### 2) vabhub-Core（后端）
**作用**: 提供 REST API（如 /api/healthz、/api/version、/api/jobs/*、/api/servers/*）。（可选）GraphQL /graphql（使用 strawberry-graphql）。WebSocket 日志中心 /ws/logs（结构化 JSON 日志）。对接下载器（qBittorrent）与媒体库（Emby/Jellyfin）。插件 Hook（download.completed、postprocess.renamed…）。

**核心接口**:
- REST API：完整的业务接口
- WebSocket：实时日志推送
- GraphQL：可选的数据查询
- 插件 Hook：事件驱动扩展

### 3) vabhub-frontend（WebUI）
**作用**: 控制台（仪表盘/任务）、LogCenter 实时日志、订阅/规则器、服务器管理（Emby/Jellyfin 并列）。

**核心功能**:
- 控制台：系统状态监控
- 实时日志：WebSocket 日志中心
- 订阅管理：规则引擎配置
- 服务器管理：媒体库集成

### 4) vabhub-deploy（部署）
**作用**: 一键拉起最小栈：qB + Emby + Core + Frontend（可选叠加 Gateway/Douban/Jellyfin-parity）。提供中国大陆可用的 .env.example、以及连通性冒烟脚本。

**部署栈**:
- 核心服务：Core + Frontend
- 下载器：qBittorrent
- 媒体库：Emby/Jellyfin
- 可选扩展：Gateway、Douban、Jellyfin-parity

### 5) vabhub-plugins（插件）
**作用**: 定义 PDK（Manifest + Hook）。提供 2 个示例插件：通知（Telegram/企业微信）、重命名后处理。

**插件系统**:
- PDK：插件开发工具包
- Hook 约定：事件触发机制
- 示例插件：通知和后处理
- 生命周期管理

### 6) vabhub-resources（资源）
**作用**: Logo/Icon、示例海报、重命名模板、文档截图。任何会被多个仓库共用的静态文件。

**资源类型**:
- 品牌资源：Logo、图标
- 模板文件：重命名模板
- 示例配置：配置文件模板
- 文档资源：截图和示意图

## 🔧 技术实现

### 版本管理机制
- **单一事实源**：versions.json 统一管理所有仓库版本
- **自动化工作流**：GitHub Actions 自动创建版本更新 PR
- **版本协调**：确保多仓库版本一致性

### 通信机制
- **API 调用**：Frontend → Core REST API
- **实时通信**：WebSocket 日志推送
- **事件驱动**：插件 Hook 机制
- **服务发现**：Deploy 编排服务间通信

### 部署架构
- **容器化**：Docker Compose / Kubernetes
- **环境隔离**：开发/测试/生产环境分离
- **健康检查**：冒烟测试和健康监控
- **配置管理**：环境变量和配置文件

## 📁 文件结构

```
vabhub/ (门户仓库)
├── .github/workflows/
│   └── versions-bump.yml      # 版本更新工作流
├── docs/
│   ├── architecture.md         # 架构设计文档
│   └── repos.md               # 仓库职责清单
├── scripts/
│   └── init_and_push.sh       # 初始化脚本
├── versions.json               # 版本配置文件
├── README.md                   # 项目说明
├── LICENSE                     # 许可证
├── .gitignore                 # Git 忽略文件
└── MULTI_REPO_ARCHITECTURE.md # 本架构文档
```

## 🚀 使用流程

### 版本更新流程
1. 修改 `versions.json` 中的版本号
2. 运行 GitHub Actions 的 "Versions Bump" 工作流
3. 工作流自动创建 Pull Request
4. 合并 PR 后版本号成为单一事实源

### 开发环境设置
```bash
# 克隆门户仓库
git clone https://github.com/strmforge/vabhub.git
cd vabhub

# 查看当前版本
cat versions.json

# 根据版本号克隆其他仓库
git clone -b v1.6.0 https://github.com/strmforge/vabhub-Core.git
git clone -b v1.6.0 https://github.com/strmforge/vabhub-frontend.git
# ... 其他仓库

# 启动开发环境
cd vabhub-deploy
docker-compose -f docker-compose.dev.yml up -d
```

## 🔗 仓库链接

- **门户**: https://github.com/strmforge/vabhub
- **Core**: https://github.com/strmforge/vabhub-Core
- **Frontend**: https://github.com/strmforge/vabhub-frontend
- **Deploy**: https://github.com/strmforge/vabhub-deploy
- **Plugins**: https://github.com/strmforge/vabhub-plugins
- **Resources**: https://github.com/strmforge/vabhub-resources

## 📊 版本信息

当前版本配置 (versions.json):
```json
{
  "schema": 1,
  "portal": "1.6.0",
  "core": "1.6.0",
  "frontend": "1.6.0",
  "deploy": "1.6.0",
  "plugins": "1.6.0",
  "resources": "1.6.0"
}
```

## ✅ 实现状态

- ✅ 门户仓库创建完成
- ✅ 版本管理机制实现
- ✅ 架构文档完善
- ✅ GitHub Actions 工作流配置
- ✅ 多仓库协调机制设计

VabHub 多仓库架构已完整实现，为后续功能开发奠定了坚实的基础架构！