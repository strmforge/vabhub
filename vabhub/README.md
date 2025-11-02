# VabHub (Portal)

[![Versions Bump](https://img.shields.io/github/actions/workflow/status/strmforge/vabhub/versions-bump.yml?label=versions-bump)](https://github.com/strmforge/vabhub/actions/workflows/versions-bump.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

VabHub 是一个"下载器 + 重命名/刮削 + 媒体库"的自动化平台。**此仓为门户与文档中心**，并维护各子仓版本（见 `versions.json`）。

## 子仓（Repositories）
- **Core（后端）**：https://github.com/strmforge/vabhub-Core
- **Frontend（WebUI）**：https://github.com/strmforge/vabhub-frontend
- **Deploy（部署编排）**：https://github.com/strmforge/vabhub-deploy
- **Plugins（插件生态）**：https://github.com/strmforge/vabhub-plugins
- **Resources（静态资源）**：https://github.com/strmforge/vabhub-resources

---

## 快速开始（只针对本门户仓）
1. `versions.json` 按需修改子仓版本；
2. 打开 **Actions → Versions Bump** 手动运行，自动生成一个更新 PR；
3. 合并 PR 后，版本号即成为"单一事实源"，可供其他仓读取。

> 若你的 main 分支启用了保护，请在 Branch protection 里允许 **GitHub Actions** 创建 PR。

## 设计概览
见 `docs/architecture.md` 和 `docs/repos.md`。

## 最小骨架验证
使用最小骨架仓库快速验证核心功能，详见 `MINIMAL_SKELETONS.md`。

## 🔧 使用说明

### 版本更新流程
1. 修改 `versions.json` 中的版本号
2. 运行 GitHub Actions 的 "Versions Bump" 工作流
3. 工作流会自动创建 Pull Request
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

## 📁 项目结构

```
vabhub/
├── .github/workflows/          # GitHub Actions 工作流
│   └── versions-bump.yml       # 版本更新工作流
├── docs/                       # 架构文档
│   ├── architecture.md         # 架构设计
│   └── repos.md               # 仓库职责清单
├── scripts/                    # 工具脚本
│   └── init_and_push.sh       # 初始化脚本
├── versions.json               # 版本配置文件
├── README.md                   # 项目说明
├── LICENSE                     # 许可证
└── .gitignore                 # Git 忽略文件
```

## 🔗 相关链接

- **Core 仓库**: https://github.com/strmforge/vabhub-Core
- **Frontend 仓库**: https://github.com/strmforge/vabhub-frontend
- **Deploy 仓库**: https://github.com/strmforge/vabhub-deploy
- **Plugins 仓库**: https://github.com/strmforge/vabhub-plugins
- **Resources 仓库**: https://github.com/strmforge/vabhub-resources

## 🤝 贡献指南

欢迎参与 VabHub 项目的开发！请遵循以下流程：

1. Fork 相关仓库
2. 创建功能开发分支
3. 开发代码并遵循项目规范
4. 提交 Pull Request
5. 等待代码审查和合并

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。