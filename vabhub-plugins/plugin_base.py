#!/usr/bin/env python3
"""
VabHub 插件基类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    """插件基类"""
    
    name: str = "base_plugin"
    version: str = "1.0.0"
    description: str = "Base plugin class"
    enabled: bool = True
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"plugin.{self.name}")
    
    @abstractmethod
    def setup(self) -> None:
        """插件初始化"""
        pass
    
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """插件执行逻辑"""
        pass
    
    def validate_config(self) -> bool:
        """验证配置"""
        return True
    
    def health_check(self) -> bool:
        """健康检查"""
        return True
    
    def cleanup(self) -> None:
        """清理资源"""
        pass
    
    def __str__(self) -> str:
        return f"{self.name} v{self.version}"
    
    def __repr__(self) -> str:
        return f"<Plugin {self.name} v{self.version}>"


class ChartPlugin(BasePlugin):
    """榜单插件基类"""
    
    chart_type: str = "general"
    data_source: str = "unknown"
    
    def get_chart_data(self, limit: int = 50) -> Dict[str, Any]:
        """获取榜单数据"""
        return {"items": [], "total": 0, "source": self.data_source}


class CloudStoragePlugin(BasePlugin):
    """云存储插件基类"""
    
    storage_type: str = "general"
    
    def upload_file(self, file_path: str, remote_path: str) -> bool:
        """上传文件"""
        return False
    
    def download_file(self, remote_path: str, local_path: str) -> bool:
        """下载文件"""
        return False
    
    def list_files(self, path: str = "/") -> list:
        """列出文件"""
        return []