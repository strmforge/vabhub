# Architecture

- **Frontend (WebUI)** 调用 **Core**：REST `/api/*`，WebSocket `/ws/logs`；（可选）GraphQL `/graphql`。
- **Deploy** 在开发 / 生产环境拉起最小栈（qBittorrent + Emby + Core + Frontend），可叠加 Stream Gateway / Douban Fallback / Jellyfin Parity。
- **Plugins** 通过 Core 的 Hook（download.completed、postprocess.renamed、scrape.done）接入扩展。
- **Resources** 存放跨仓共享的静态文件（Logo、模板、示例配置）。

> 版本编排：`versions.json` 作为单一事实源，其他仓可在构建时读取该文件决定依赖版本或生成 Release Notes。