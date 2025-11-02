# VabHub 插件开发指南

本文档详细介绍了如何为 VabHub 开发插件，包括插件架构、API 使用、事件机制和最佳实践。

## 插件架构概述

VabHub 插件系统采用模块化设计，支持热插拔和动态加载。每个插件都是一个独立的 Python 包，包含以下组件：

- **插件清单** (`plugin.json`): 定义插件元数据和配置
- **主模块** (`main.py`): 包含插件主逻辑
- **配置文件** (`config.json`): 插件配置
- **依赖文件** (`requirements.txt`): 插件依赖

## 快速开始

### 使用 Cookiecutter 模板

最快的方式是使用我们提供的 Cookiecutter 模板：

```bash
# 安装 Cookiecutter
pip install cookiecutter

# 生成新插件
cookiecutter vabhub-plugins/cookiecutter-template/

# 按照提示输入插件信息
```

### 手动创建插件

1. 在 `vabhub-Core/plugins/` 目录下创建插件文件夹
2. 创建必要的配置文件
3. 实现插件逻辑

## 插件清单 (plugin.json)

每个插件必须包含一个 `plugin.json` 文件：

```json
{
  "id": "my-plugin",
  "name": "我的插件",
  "version": "1.0.0",
  "description": "插件描述",
  "author": "作者名",
  "dependencies": ["other-plugin-id"],
  "config_schema": {
    "enabled": {
      "type": "boolean",
      "default": true,
      "description": "启用/禁用插件"
    },
    "api_key": {
      "type": "string",
      "description": "API密钥"
    }
  }
}
```

## 插件基类

所有插件必须继承自 `BasePlugin` 类：

```python
from core.plugin_manager import BasePlugin

class MyPlugin(BasePlugin):
    plugin_id = "my-plugin"
    plugin_name = "我的插件"
    plugin_version = "1.0.0"
    
    def initialize(self):
        """插件初始化"""
        # 加载配置、初始化资源
        pass
    
    def cleanup(self):
        """插件清理"""
        # 释放资源
        pass
    
    def enable(self):
        """启用插件"""
        pass
    
    def disable(self):
        """禁用插件"""
        pass
```

## 插件 API

### 配置管理

插件可以通过 `self.config` 访问配置：

```python
def initialize(self):
    api_key = self.config.get('api_key')
    enabled = self.config.get('enabled', True)
```

### 日志记录

使用标准 logging 模块：

```python
import logging
logger = logging.getLogger(__name__)

logger.info("插件消息")
logger.error("错误信息")
```

### 事件系统

插件可以监听和触发事件：

```python
from core.event_system import EventSystem

# 监听事件
EventSystem.subscribe("download_completed", self.on_download_completed)

def on_download_completed(self, data):
    """下载完成事件处理"""
    logger.info(f"下载完成: {data['title']}")

# 触发事件
EventSystem.publish("plugin_custom_event", {
    "plugin_id": self.plugin_id,
    "data": "自定义数据"
})
```

## 可用事件列表

### 系统事件

- `system_startup`: 系统启动
- `system_shutdown`: 系统关闭
- `config_updated`: 配置更新

### 下载事件

- `download_started`: 下载开始
- `download_completed`: 下载完成
- `download_failed`: 下载失败
- `download_progress`: 下载进度更新

### 媒体事件

- `media_added`: 媒体添加
- `media_updated`: 媒体更新
- `media_deleted`: 媒体删除

### 插件事件

- `plugin_loaded`: 插件加载
- `plugin_unloaded`: 插件卸载
- `plugin_enabled`: 插件启用
- `plugin_disabled`: 插件禁用

## 插件类型

### 下载器插件

实现自定义下载器：

```python
class CustomDownloaderPlugin(BasePlugin):
    def download_file(self, url, destination):
        """下载文件"""
        # 实现下载逻辑
        pass
```

### 媒体处理插件

处理媒体文件：

```python
class MediaProcessorPlugin(BasePlugin):
    def process_media(self, media_info):
        """处理媒体文件"""
        # 实现处理逻辑
        pass
```

### 通知插件

发送通知：

```python
class NotificationPlugin(BasePlugin):
    def send_notification(self, title, message):
        """发送通知"""
        # 实现通知逻辑
        pass
```

## 插件配置

### 配置架构

在 `plugin.json` 中定义配置架构：

```json
{
  "config_schema": {
    "server_url": {
      "type": "string",
      "default": "http://localhost:8080",
      "description": "服务器地址"
    },
    "timeout": {
      "type": "number",
      "default": 30,
      "description": "超时时间(秒)"
    }
  }
}
```

### 配置验证

插件可以验证配置：

```python
def validate_config(self, config):
    """验证配置"""
    if not config.get('api_key'):
        raise ValueError("API密钥不能为空")
```

## 插件测试

### 单元测试

使用 pytest 编写测试：

```python
import pytest
from main import MyPlugin

class TestMyPlugin:
    def test_plugin_initialization(self):
        plugin = MyPlugin()
        plugin.initialize()
        assert plugin.plugin_id == "my-plugin"
```

### 集成测试

测试插件与系统的集成：

```python
class TestPluginIntegration:
    def test_plugin_lifecycle(self):
        # 测试插件的完整生命周期
        pass
```

## 插件发布

### 打包插件

创建插件包：

```bash
# 创建插件包
cd my-plugin
zip -r my-plugin-1.0.0.zip .
```

### 发布到插件市场

插件可以通过 UI 界面安装，或手动复制到插件目录。

## 最佳实践

### 错误处理

```python
def process_data(self, data):
    try:
        # 处理逻辑
        pass
    except Exception as e:
        logger.error(f"处理数据失败: {e}")
        # 优雅降级
        return None
```

### 资源管理

```python
def cleanup(self):
    # 释放所有资源
    if hasattr(self, 'http_client'):
        self.http_client.close()
```

### 性能优化

- 使用异步操作
- 避免阻塞主线程
- 合理使用缓存

### 安全性

- 验证所有输入
- 使用安全的 API 调用
- 保护敏感配置

## 示例插件

### 简单示例

```python
from core.plugin_manager import BasePlugin

class HelloWorldPlugin(BasePlugin):
    plugin_id = "hello-world"
    plugin_name = "Hello World"
    
    def initialize(self):
        print("Hello World 插件已初始化")
    
    def say_hello(self, name):
        return f"Hello, {name}!"
```

### 完整示例

参考 `cookiecutter-template` 中的完整示例。

## 故障排除

### 常见问题

1. **插件无法加载**: 检查插件清单格式和依赖
2. **配置不生效**: 重启插件或检查配置验证
3. **事件不触发**: 检查事件名称和订阅逻辑

### 调试技巧

- 启用调试日志
- 使用断点调试
- 检查系统日志

## 支持与贡献

- 文档: [VabHub 文档](https://docs.vabhub.org)
- 社区: [VabHub 社区](https://community.vabhub.org)
- 问题: [GitHub Issues](https://github.com/vabhub/vabhub/issues)

---

**最后更新**: 2025-10-31  
**版本**: 1.0.0