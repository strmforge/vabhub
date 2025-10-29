"""
Example Plugin Implementation

This module provides an example plugin implementation for VabHub.
"""

import asyncio
from typing import Dict, Any
from ..base import PluginBase


class ExamplePlugin(PluginBase):
    """Example plugin for VabHub."""
    
    def __init__(self):
        super().__init__()
        self.name = "example"
        self.version = "1.0.0"
        self.description = "示例插件"
        self.author = "VabHub Team"
    
    async def on_load(self) -> None:
        """Called when the plugin is loaded."""
        self.logger.info("示例插件已加载")
        
        # 启动后台任务
        self.create_task(self._background_task())
    
    async def on_unload(self) -> None:
        """Called when the plugin is unloaded."""
        self.logger.info("示例插件已卸载")
        
        # 停止所有任务
        await self.stop_tasks()
    
    async def on_config_change(self, old_config: Dict[str, Any], new_config: Dict[str, Any]) -> None:
        """Called when plugin configuration changes."""
        self.logger.info(f"配置已变更: {old_config} -> {new_config}")
    
    async def process_message(self, message: str) -> str:
        """Process a message and return a response."""
        self.logger.info(f"处理消息: {message}")
        return f"插件响应: {message}"
    
    async def _background_task(self) -> None:
        """Background task that runs periodically."""
        while True:
            try:
                self.logger.debug("示例插件后台任务运行中...")
                await asyncio.sleep(60)  # 每分钟运行一次
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"后台任务错误: {e}")
                await asyncio.sleep(10)