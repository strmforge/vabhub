# 仓库职责清单

- **strmforge/vabhub**（门户）：文档与版本中心，提供 `versions.json`；包含"Versions Bump"工作流。
- **strmforge/vabhub-Core**：后端服务（API/任务编排/WS 日志/刮削/重命名），对外公开 `/api/*` 与 `/ws/logs`。
- **strmforge/vabhub-frontend**：Vue3 前端，提供控制台、日志中心、订阅与规则、服务器管理（Emby/Jellyfin）。
- **strmforge/vabhub-deploy**：Compose/K8s 编排、环境样本与冒烟自检（qB/Emby/TMDb）。
- **strmforge/vabhub-plugins**：PDK 规范与示例插件（通知/后处理等）。
- **strmforge/vabhub-resources**：静态资源、重命名模板、文档截图等。