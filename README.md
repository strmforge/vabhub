# VabHub — Personal Media Automation Hub

[![Portal](https://img.shields.io/badge/Portal-vabhub-blue)](https://github.com/strmforge/vabhub)
[![Core CI](https://img.shields.io/github/actions/workflow/status/strmforge/vabhub-Core/ci.yml?branch=main&label=Core%20CI)](https://github.com/strmforge/vabhub-Core/actions)
[![Frontend CI](https://img.shields.io/github/actions/workflow/status/strmforge/vabhub-frontend/ci.yml?branch=main&label=Frontend%20CI)](https://github.com/strmforge/vabhub-frontend/actions)
[![Deploy](https://img.shields.io/github/v/release/strmforge/vabhub-deploy?label=Deploy%20Release)](https://github.com/strmforge/vabhub-deploy/releases)
[![License](https://img.shields.io/badge/License-MIT-green)](#license)

> 门户/文档入口。**对外只宣传一个仓：本仓。** 安装与使用请移步 `vabhub-deploy`。

## 一键安装
- 👉 前往 **[vabhub-deploy](https://github.com/strmforge/vabhub-deploy)**，按 `README` 的 `docker-compose` 或 `Helm` 操作即可。
- 国内用户推荐：前端 Cloudflare，后端阿里云香港/本地 NAS。

## 仓库矩阵
- **Core（后端主仓）**：https://github.com/strmforge/vabhub-Core
- **Frontend（WebUI）**：https://github.com/strmforge/vabhub-frontend
- **Deploy（分发主仓）**：https://github.com/strmforge/vabhub-deploy
- Plugins / Resources：见组织内其他仓。

## 功能概览（对标 MoviePilot）
- 存储适配：**123 云盘**（OpenAPI）、**115 网盘**（OpenAPI）
- 订阅→下载→重命名→刮削→入库流水线
- 插件市场（registry.json）与一键安装
- 多云与免备案部署模板（Cloudflare/Aliyun/Tencent/local）

## 反馈 & 贡献
- Issues/Discussions 统一开在本仓；子模块开发问题再转到对应仓。
- 贡献指南与路线图见 `/docs` 与 Projects。

## License
MIT
