# VabHub Deploy · 部署与运维

[![Compose](https://img.shields.io/badge/compose-ready-blue.svg)](#)
[![Kubernetes](https://img.shields.io/badge/k8s-optional-informational.svg)](#)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](#)

唯一承载 **部署模板** 的仓库：Docker Compose、Kubernetes/Helm、环境样例、备份与升级脚本等。

---

## 🚀 快速开始（Docker Compose）
```bash
cp .env.example .env
docker compose up -d
```

## 🧩 模板使用指南（本仓专属）
- PR 模板：`.github/PULL_REQUEST_TEMPLATE/compose_k8s_change.md`
- Issue 表单：`.github/ISSUE_TEMPLATE/deploy_env_issue.yml`
- 版本矩阵：`versions.json`（建议与门户对齐）
