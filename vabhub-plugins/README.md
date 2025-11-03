# VabHub Plugins · 官方插件集合

[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Plugins](https://img.shields.io/badge/plugins-official-blue.svg)](#)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](#)

存放 **插件实现**：站点适配器、下载器桥接、订阅器、后处理等。由 `vabhub-Core` 的插件运行时加载。

## 约定
```
plugins/
  site.<tracker>/
  downloader.<client>/
  postproc.<name>/
```
**manifest.json** 必含：name/version/min_core_version/capabilities/config_schema
