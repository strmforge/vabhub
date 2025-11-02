# VabHub Plugins

VabHub 插件系统，提供可扩展的插件架构，支持各种媒体服务和数据源集成。

## 功能特性

- 🔌 插件化架构
- 📊 多数据源集成
- 🔄 热插拔支持
- 📈 性能监控
- 🔧 配置管理

## 快速开始

### 环境要求
- Python 3.11+
- VabHub Core 1.0.0+

### 安装插件
```bash
# 克隆仓库
git clone https://github.com/your-org/vabhub-plugins.git
cd vabhub-plugins

# 安装依赖
pip install -r requirements.txt

# 安装到VabHub Core
python setup.py install
```

### 开发插件
```python
from plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    name = "my-plugin"
    version = "1.0.0"
    
    def setup(self):
        # 插件初始化
        pass
    
    def execute(self, data):
        # 插件执行逻辑
        return data
```

## 项目结构

```
vabhub-plugins/
├── plugins/           # 插件实现
│   ├── charts/       # 榜单插件
│   ├── cloud/        # 云存储插件
│   ├── music/        # 音乐插件
│   └── video/        # 视频插件
├── plugin_base.py    # 插件基类
├── plugin_manager.py # 插件管理器
├── plugin_system.py  # 插件系统
├── requirements.txt
└── setup.py          # 安装脚本
```

## 可用插件

### 榜单插件
- **charts_tmdb**: TMDB电影榜单
- **charts_douban**: 豆瓣电影榜单
- **charts_qq_music**: QQ音乐榜单
- **charts_netease**: 网易云音乐榜单

### 云存储插件
- **cloud_115**: 115网盘集成
- **cloud_123**: 123云盘集成
- **cloud_storage**: 通用云存储

### 音乐插件
- **music_subscription**: 音乐订阅
- **musicbrainz**: MusicBrainz数据

## 开发指南

请参考 [CONTRIBUTING.md](CONTRIBUTING.md)