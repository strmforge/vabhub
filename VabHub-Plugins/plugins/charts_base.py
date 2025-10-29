"""
排行榜数据源插件基类
基于media-oneclick和MoviePilot的最佳实践
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class DataSourcePlugin(ABC):
    """排行榜数据源插件基类"""
    
    def __init__(self):
        self.name = ""
        self.version = "1.0.0"
        self.description = ""
        self.author = "VabHub Team"
        self.enabled = True
        
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"charts.{self.name}")
        
        # 插件状态
        self.initialized = False
        self.last_update = None
        self.error_count = 0
    
    @abstractmethod
    def initialize(self) -> bool:
        """初始化插件"""
        pass
    
    @abstractmethod
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行排行榜数据获取"""
        pass
    
    @abstractmethod
    def get_supported_charts(self) -> List[Dict[str, Any]]:
        """获取支持的榜单类型"""
        pass
    
    def cleanup(self):
        """清理插件资源"""
        self.logger.info(f"清理 {self.name} 插件资源")
    
    def set_config(self, config: Dict[str, Any]):
        """设置插件配置"""
        self.config = config
        self.logger.info(f"已更新 {self.name} 插件配置")
    
    def get_status(self) -> Dict[str, Any]:
        """获取插件状态"""
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "initialized": self.initialized,
            "last_update": self.last_update,
            "error_count": self.error_count,
            "supported_charts": self.get_supported_charts()
        }
    
    def enable(self):
        """启用插件"""
        self.enabled = True
        self.logger.info(f"已启用 {self.name} 插件")
    
    def disable(self):
        """禁用插件"""
        self.enabled = False
        self.logger.info(f"已禁用 {self.name} 插件")


class MusicDataSourcePlugin(DataSourcePlugin):
    """音乐数据源插件基类"""
    
    def __init__(self):
        super().__init__()
        self.supported_chart_types = ["global_top_50", "new_releases", "top_hits"]
    
    async def get_track_info(self, track_id: str) -> Optional[Dict[str, Any]]:
        """获取歌曲详细信息"""
        raise NotImplementedError
    
    async def search_tracks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索歌曲"""
        raise NotImplementedError


class VideoDataSourcePlugin(DataSourcePlugin):
    """视频数据源插件基类"""
    
    def __init__(self):
        super().__init__()
        self.supported_chart_types = ["trending", "popular", "top_rated"]
    
    async def get_movie_info(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """获取电影详细信息"""
        raise NotImplementedError
    
    async def get_tv_show_info(self, tv_id: str) -> Optional[Dict[str, Any]]:
        """获取电视剧详细信息"""
        raise NotImplementedError


class DramaDataSourcePlugin(VideoDataSourcePlugin):
    """电视剧数据源插件基类"""
    
    def __init__(self):
        super().__init__()
        self.supported_chart_types.extend(["hot_dramas", "new_dramas", "kdrama", "jdrama"])
    
    async def get_drama_episodes(self, drama_id: str) -> List[Dict[str, Any]]:
        """获取剧集列表"""
        raise NotImplementedError


class ChartsPluginManager:
    """排行榜插件管理器"""
    
    def __init__(self):
        self.plugins: Dict[str, DataSourcePlugin] = {}
        self.logger = logging.getLogger("charts.manager")
    
    def register_plugin(self, plugin: DataSourcePlugin):
        """注册插件"""
        if plugin.name in self.plugins:
            self.logger.warning(f"插件 {plugin.name} 已存在，将被覆盖")
        
        self.plugins[plugin.name] = plugin
        self.logger.info(f"已注册插件: {plugin.name}")
    
    def unregister_plugin(self, plugin_name: str):
        """注销插件"""
        if plugin_name in self.plugins:
            plugin = self.plugins.pop(plugin_name)
            plugin.cleanup()
            self.logger.info(f"已注销插件: {plugin_name}")
    
    def get_plugin(self, plugin_name: str) -> Optional[DataSourcePlugin]:
        """获取插件"""
        return self.plugins.get(plugin_name)
    
    def get_plugins_by_type(self, plugin_type: str) -> List[DataSourcePlugin]:
        """按类型获取插件"""
        return [plugin for plugin in self.plugins.values() 
                if plugin.__class__.__name__.lower().startswith(plugin_type.lower())]
    
    async def execute_plugin(self, plugin_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行插件"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return {"success": False, "error": f"插件 {plugin_name} 未找到"}
        
        if not plugin.enabled:
            return {"success": False, "error": f"插件 {plugin_name} 已禁用"}
        
        try:
            result = await plugin.execute(data)
            plugin.last_update = datetime.now()
            plugin.error_count = 0
            return result
        except Exception as e:
            plugin.error_count += 1
            self.logger.error(f"执行插件 {plugin_name} 失败: {e}")
            return {"success": False, "error": str(e)}
    
    def get_all_plugins_status(self) -> Dict[str, Any]:
        """获取所有插件状态"""
        return {
            "total": len(self.plugins),
            "enabled": len([p for p in self.plugins.values() if p.enabled]),
            "disabled": len([p for p in self.plugins.values() if not p.enabled]),
            "plugins": {name: plugin.get_status() for name, plugin in self.plugins.items()}
        }