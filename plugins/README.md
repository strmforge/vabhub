# VabHub-Plugins

VabHub 插件系统，支持动态加载和管理的插件架构。

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 开发插件
```bash
# 创建插件模板
python scripts/create_plugin.py my_plugin

# 测试插件
python -m pytest tests/
```

### 安装插件
```bash
# 安装到 VabHub-Core
pip install -e .
```

## 📁 项目结构

```
VabHub-Plugins/
├── plugins/                 # 插件目录
│   ├── __init__.py
│   ├── base.py            # 插件基类
│   ├── manager.py         # 插件管理器
│   ├── example/           # 示例插件
│   │   ├── __init__.py
│   │   ├── plugin.py     # 插件实现
│   │   └── config.yaml   # 插件配置
│   └── ...
├── tests/                  # 测试代码
├── scripts/               # 工具脚本
├── requirements.txt       # Python依赖
├── setup.py              # 安装配置
└── README.md
```

## 🔧 核心功能

### 插件管理器
- 动态插件加载和卸载
- 插件生命周期管理
- 依赖关系解析
- 插件配置管理

### 插件接口
- 标准化的插件接口
- 事件系统
- API扩展机制
- 配置管理

### 插件类型
- **下载器插件** - 支持不同下载协议
- **元数据插件** - 媒体信息获取
- **通知插件** - 消息推送
- **分析插件** - 数据分析和统计

## 📊 插件开发

### 创建插件
```python
from plugins.base import PluginBase

class MyPlugin(PluginBase):
    """示例插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "my_plugin"
        self.version = "1.0.0"
        self.description = "示例插件"
    
    async def on_load(self):
        """插件加载时调用"""
        self.logger.info("插件已加载")
    
    async def on_unload(self):
        """插件卸载时调用"""
        self.logger.info("插件已卸载")
    
    async def process_media(self, media_info):
        """处理媒体信息"""
        # 插件业务逻辑
        return processed_info
```

### 插件配置
```yaml
# plugins/example/config.yaml
name: example_plugin
version: 1.0.0
description: 示例插件

dependencies:
  - requests>=2.25.0

settings:
  api_key:
    type: string
    required: true
    description: API密钥
  timeout:
    type: integer
    default: 30
    description: 请求超时时间
```

### 插件事件
```python
# 注册事件处理器
@self.register_event("media_added")
async def handle_media_added(self, media_data):
    """处理媒体添加事件"""
    self.logger.info(f"新媒体添加: {media_data['title']}")

# 触发事件
await self.emit_event("media_processed", result_data)
```

## 🔌 API接口

### 插件管理API
- `GET /api/plugins` - 获取插件列表
- `POST /api/plugins/{plugin_id}/install` - 安装插件
- `POST /api/plugins/{plugin_id}/uninstall` - 卸载插件
- `GET /api/plugins/{plugin_id}/config` - 获取插件配置
- `PUT /api/plugins/{plugin_id}/config` - 更新插件配置

### 插件服务API
- `POST /api/plugins/{plugin_id}/execute` - 执行插件功能
- `GET /api/plugins/{plugin_id}/status` - 获取插件状态
- `POST /api/plugins/{plugin_id}/reload` - 重新加载插件

## 🚀 部署

### 安装到 VabHub-Core
```bash
# 在 VabHub-Core 目录中
pip install ../VabHub-Plugins
```

### Docker 部署
```yaml
# docker-compose.yml
services:
  vabhub-core:
    build: .
    volumes:
      - ./plugins:/app/plugins
```

## 🔗 相关仓库

- [VabHub-Core](https://github.com/vabhub/vabhub-core) - 后端核心服务
- [VabHub-Frontend](https://github.com/vabhub/vabhub-frontend) - 前端界面
- [VabHub-Deploy](https://github.com/vabhub/vabhub-deploy) - 部署配置
- [VabHub-Resources](https://github.com/vabhub/vabhub-resources) - 资源文件

## 🤝 贡献指南

欢迎提交插件和功能改进！

### 开发环境设置
```bash
# 1. Fork 仓库
# 2. 克隆到本地
git clone https://github.com/your-username/vabhub-plugins.git

# 3. 创建开发分支
git checkout -b feature/your-plugin

# 4. 开发插件
# 在 plugins/ 目录下创建你的插件

# 5. 提交更改
git commit -m "feat: add your plugin"

# 6. 推送到远程
git push origin feature/your-plugin

# 7. 创建 Pull Request
```

### 插件开发规范
- 遵循插件接口规范
- 提供完整的文档
- 编写单元测试
- 支持配置管理
- 处理错误和异常

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 📞 支持

- 文档: [VabHub Wiki](https://github.com/vabhub/vabhub-wiki)
- 问题: [GitHub Issues](https://github.com/vabhub/vabhub-plugins/issues)
- 讨论: [GitHub Discussions](https://github.com/vabhub/vabhub-plugins/discussions)