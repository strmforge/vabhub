# VabHub (Portal) · 门户与版本协调中心

[![Docs](https://img.shields.io/badge/docs-latest-blue.svg)](#)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](#)
[![Versions Matrix](https://img.shields.io/badge/versions-matrix-success)](./versions.json)

VabHub 门户仓：**文档入口、子仓索引、版本矩阵（versions.json）、发布说明与路线图**。本仓库不包含运行代码。

---

## 仓库矩阵

| 仓库 | 作用 | 产物 |
|---|---|---|
| vabhub-Core | 后端（REST/GraphQL、识别/重命名、下载器/媒体库集成、插件运行时） | 后端 Docker 镜像 |
| vabhub-frontend | Web 前端（站点管理、规则配置、订阅与任务、纠错、日志与设置） | 前端静态产物/镜像 |
| vabhub-plugins | 官方插件集合（站点适配器、下载器桥接、后处理/订阅） | 插件源码/插件包 |
| vabhub-resources | 纯资源与规范（Schema/正则/默认规则/图标/示例） | 版本化资源文件 |
| vabhub-deploy | 部署与运维（Compose/K8s、.env.example、脚本） | 部署模板与脚本 |

> **单一事实源**：请以本仓 `versions.json` 为各子仓的推荐/对齐版本（SemVer）。

---

## 版本矩阵

- 文件：[`./versions.json`](./versions.json)  
- 流程：**先**各子仓打 tag 出包 → **再**在本仓 bump 版本矩阵 → 发布公告/变更日志。

**手动 Bump 工作流**（已内置）
- `.github/workflows/versions-bump.yml` 支持手动输入 `core/frontend/plugins/resources/deploy` 新版本，自动创建仅改 `versions.json` 的 PR。

---

## 文档导航

- `docs/overview.md`：项目概述与目标
- `docs/architecture.md`：整体架构与数据流
- `docs/roadmap.md`：路线图与迭代计划
- `docs/changelog/`：变更日志
- `docs/faq.md`：常见问题
- `docs/ops-checklist.md`：仓库初始化检查清单（Actions/保护分支/Secrets/标签保护/安全）

> **不要**在门户仓放置：后端/前端源码、compose/k8s、任何密钥。

---

# 🧩 模板使用指南（PR / Issue / Workflow）

> 适用于 GitHub 默认界面；如果你使用 CodeBuddy/Kiro 等 IDE，同样遵循本目录结构生效。

## 1) PR 模板如何选择
- 单一模板：`.github/pull_request_template.md` 会作为默认 PR 模板。
- 多模板：在 `.github/PULL_REQUEST_TEMPLATE/` 目录下选择具体模板：
  - Portal：`versions_bump.md`、`docs_update.md`
  - Core：`api_change.md`、`plugin_runtime.md`、`performance.md`
  - Frontend：`ui_change.md`、`i18n_update.md`、`accessibility.md`
  - Plugins：`new_plugin_submission.md`、`adapter_update.md`
  - Resources：`schema_change.md`、`regex_update.md`
  - Deploy：`compose_k8s_change.md`

**在 GitHub 界面选择模板：**
1. 点击 **New pull request** → **Create pull request**。  
2. 在 PR 编辑页底部找到 **Change template**（或 **Choose a template**）。  
3. 选择需要的模板，提交。

**URL 直达某模板**（示例）：
```
https://github.com/strmforge/vabhub-Core/compare/main...feat/x?expand=1&template=api_change.md
```

> _截图示意_：  
> ![选择 PR 模板（示意）](https://user-images.githubusercontent.com/placeholder/pr-template-choose.png)

## 2) Issue 模板/表单
- 每个仓都有 `ISSUE_TEMPLATE` 目录：
  - `bug_report.md`、`feature_request.md` 为常规模板
  - **表单类**（YAML）：
    - Plugins 仓：`new_plugin_intake.yml`（新插件收录）
    - Resources 仓：`resource_request.yml`（资源请求/更新）
    - Deploy 仓：`deploy_env_issue.yml`（部署问题）

在仓库 **Issues → New issue** 页面即可看到对应入口。

> _截图示意_：  
> ![Issue 表单（示意）](https://user-images.githubusercontent.com/placeholder/issue-forms.png)

## 3) 运行 Versions Bump 工作流
1. 打开 **Actions** → 选择 **Versions Bump** 工作流。  
2. 点击 **Run workflow**，按需填写版本（留空则保持不变）。  
3. 工作流会自动创建分支 `chore/bump-versions-<run_id>` 与 PR，仅修改 `versions.json`。

> _截图示意_：  
> ![Run workflow（示意）](https://user-images.githubusercontent.com/placeholder/run-workflow.png)

### 故障排除
- **看不到模板**：确认目录大小写正确：
  - `.github/pull_request_template.md`（默认）
  - `.github/PULL_REQUEST_TEMPLATE/*.md`（多模板）
  - `.github/ISSUE_TEMPLATE/{*.md,*.yml}`
- **模板没有加载**：模板文件必须在**目标分支**（通常是 `main`）上。
- **Action 没显示**：到 **Actions** 页签启用工作流；首次可能需要仓库 Owner 授权。

---

## 贡献指南 & 许可证
- PR：小步提交、描述清晰、附带文档与验证依据。
- 行为准则：见 `CODE_OF_CONDUCT.md`
- 许可证：MIT © 2025 VabHub contributors
