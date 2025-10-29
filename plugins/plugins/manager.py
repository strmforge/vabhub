"""
VabHub 插件管理器

提供完整的插件生命周期管理，包括插件发现、安装、卸载、启用、禁用等功能。
"""

import asyncio
import importlib
import json
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Type, Any
from urllib.parse import urlparse

import aiohttp
from .base import PluginBase


class PluginInfo:
    """插件信息类"""
    
    def __init__(self, plugin_id: str, name: str, version: str, author: str, 
                 description: str, status: str = "available", enabled: bool = False,
                 homepage: str = "", dependencies: List[str] = None, 
                 install_path: str = "", settings: Dict[str, Any] = None):
        self.id = plugin_id
        self.name = name
        self.version = version
        self.author = author
        self.description = description
        self.homepage = homepage
        self.status = status  # available, installed, disabled, error
        self.enabled = enabled
        self.install_path = install_path
        self.dependencies = dependencies or []
        self.settings = settings or {}
        self.metadata: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "homepage": self.homepage,
            "status": self.status,
            "enabled": self.enabled,
            "install_path": self.install_path,
            "dependencies": self.dependencies,
            "settings": self.settings,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PluginInfo':
        """从字典创建插件信息"""
        return cls(
            plugin_id=data.get('id', ''),
            name=data.get('name', ''),
            version=data.get('version', '1.0.0'),
            author=data.get('author', ''),
            description=data.get('description', ''),
            homepage=data.get('homepage', ''),
            status=data.get('status', 'available'),
            enabled=data.get('enabled', False),
            install_path=data.get('install_path', ''),
            dependencies=data.get('dependencies', []),
            settings=data.get('settings', {})
        )


class PluginManager:
    """VabHub 插件管理器"""
    
    def __init__(self, plugins_dir: Path, data_dir: Path = None):
        self.plugins_dir = plugins_dir
        self.data_dir = data_dir or plugins_dir.parent / "data"
        self.logger = logging.getLogger(__name__)
        
        # 创建数据目录
        self.data_dir.mkdir(exist_ok=True)
        
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_classes: Dict[str, Type[PluginBase]] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        
        # 插件市场配置
        self.market_url = "https://api.vabhub.com/plugins"
        self.market_cache_file = self.data_dir / "market_cache.json"
        
        self._event_bus: Dict[str, List[callable]] = {}
        
        # 加载插件信息
        self._load_plugin_info()
    
    def _load_plugin_info(self):
        """加载插件信息"""
        try:
            info_file = self.data_dir / "plugin_info.json"
            if info_file.exists():
                with open(info_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for plugin_data in data:
                        plugin_info = PluginInfo.from_dict(plugin_data)
                        self.plugin_info[plugin_info.id] = plugin_info
        except Exception as e:
            self.logger.error(f"加载插件信息失败: {e}")
    
    def _save_plugin_info(self):
        """保存插件信息"""
        try:
            info_file = self.data_dir / "plugin_info.json"
            data = [plugin_info.to_dict() for plugin_info in self.plugin_info.values()]
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存插件信息失败: {e}")
    
    async def load_plugins(self) -> None:
        """Load all available plugins."""
        self.logger.info("Loading plugins...")
        
        # 扫描插件目录
        for plugin_file in self.plugins_dir.glob("*/plugin.py"):
            plugin_name = plugin_file.parent.name
            try:
                await self.load_plugin(plugin_name)
            except Exception as e:
                self.logger.error(f"Failed to load plugin {plugin_name}: {e}")
    
    async def load_plugin(self, plugin_name: str) -> PluginBase:
        """Load a specific plugin."""
        if plugin_name in self.plugins:
            self.logger.warning(f"Plugin {plugin_name} is already loaded")
            return self.plugins[plugin_name]
        
        plugin_dir = self.plugins_dir / plugin_name
        if not plugin_dir.exists():
            raise FileNotFoundError(f"Plugin directory not found: {plugin_dir}")
        
        # 动态导入插件模块
        spec = importlib.util.spec_from_file_location(
            f"plugins.{plugin_name}.plugin", 
            plugin_dir / "plugin.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 查找插件类（约定：插件类名应为 PluginNamePlugin）
        plugin_class_name = f"{plugin_name.title().replace('_', '')}Plugin"
        plugin_class = getattr(module, plugin_class_name, None)
        
        if not plugin_class or not issubclass(plugin_class, PluginBase):
            raise TypeError(f"Plugin class {plugin_class_name} not found or invalid")
        
        # 实例化插件
        plugin_instance = plugin_class()
        plugin_instance.name = plugin_name
        plugin_instance.plugin_dir = plugin_dir
        plugin_instance.logger = logging.getLogger(f"plugin.{plugin_name}")
        
        # 加载配置
        plugin_instance.config = plugin_instance.load_config()
        
        # 调用插件加载方法
        await plugin_instance.on_load()
        
        self.plugins[plugin_name] = plugin_instance
        self.plugin_classes[plugin_name] = plugin_class
        
        self.logger.info(f"Plugin {plugin_name} loaded successfully")
        return plugin_instance
    
    async def unload_plugin(self, plugin_name: str) -> None:
        """Unload a specific plugin."""
        if plugin_name not in self.plugins:
            self.logger.warning(f"Plugin {plugin_name} is not loaded")
            return
        
        plugin = self.plugins[plugin_name]
        
        try:
            # 停止所有任务
            await plugin.stop_tasks()
            
            # 调用插件卸载方法
            await plugin.on_unload()
            
            # 从管理器中移除
            del self.plugins[plugin_name]
            del self.plugin_classes[plugin_name]
            
            self.logger.info(f"Plugin {plugin_name} unloaded successfully")
        except Exception as e:
            self.logger.error(f"Error unloading plugin {plugin_name}: {e}")
    
    async def unload_all_plugins(self) -> None:
        """Unload all plugins."""
        self.logger.info("Unloading all plugins...")
        
        for plugin_name in list(self.plugins.keys()):
            await self.unload_plugin(plugin_name)
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginBase]:
        """Get a plugin instance by name."""
        return self.plugins.get(plugin_name)
    
    def get_plugins_by_type(self, plugin_type: Type) -> List[PluginBase]:
        """Get all plugins of a specific type."""
        return [
            plugin for plugin in self.plugins.values() 
            if isinstance(plugin, plugin_type)
        ]
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins with their information."""
        plugins_info = []
        
        for name, plugin in self.plugins.items():
            plugins_info.append({
                "name": name,
                "version": plugin.version,
                "description": plugin.description,
                "author": plugin.author,
                "enabled": plugin.enabled,
                "type": type(plugin).__name__
            })
        
        return plugins_info
    
    def get_plugin_info(self, plugin_id: str) -> Optional[PluginInfo]:
        """获取插件信息"""
        return self.plugin_info.get(plugin_id)
    
    def get_all_plugin_info(self, status: Optional[str] = None) -> List[PluginInfo]:
        """获取所有插件信息"""
        plugins = list(self.plugin_info.values())
        if status:
            plugins = [p for p in plugins if p.status == status]
        return plugins
    
    def install_plugin(self, plugin_id: str) -> bool:
        """安装插件"""
        try:
            if plugin_id in self.plugin_info:
                plugin_info = self.plugin_info[plugin_id]
                plugin_info.status = "installed"
                plugin_info.enabled = True
                plugin_info.install_path = str(self.plugins_dir / plugin_id)
                
                # 保存插件信息
                self._save_plugin_info()
                
                self.logger.info(f"Plugin {plugin_id} installed successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to install plugin {plugin_id}: {e}")
            return False
    
    def uninstall_plugin(self, plugin_id: str) -> bool:
        """卸载插件"""
        try:
            if plugin_id in self.plugin_info:
                plugin_info = self.plugin_info[plugin_id]
                plugin_info.status = "available"
                plugin_info.enabled = False
                plugin_info.install_path = ""
                
                # 保存插件信息
                self._save_plugin_info()
                
                self.logger.info(f"Plugin {plugin_id} uninstalled successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to uninstall plugin {plugin_id}: {e}")
            return False
    
    def enable_plugin(self, plugin_id: str) -> bool:
        """启用插件"""
        try:
            if plugin_id in self.plugin_info:
                plugin_info = self.plugin_info[plugin_id]
                plugin_info.enabled = True
                
                # 保存插件信息
                self._save_plugin_info()
                
                self.logger.info(f"Plugin {plugin_id} enabled successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to enable plugin {plugin_id}: {e}")
            return False
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """禁用插件"""
        try:
            if plugin_id in self.plugin_info:
                plugin_info = self.plugin_info[plugin_id]
                plugin_info.enabled = False
                
                # 保存插件信息
                self._save_plugin_info()
                
                self.logger.info(f"Plugin {plugin_id} disabled successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to disable plugin {plugin_id}: {e}")
            return False
    
    def scan_available_plugins(self) -> List[PluginInfo]:
        """扫描可用的插件"""
        available_plugins = []
        
        # 扫描插件目录
        for plugin_dir in self.plugins_dir.iterdir():
            if plugin_dir.is_dir():
                plugin_id = plugin_dir.name
                
                # 检查是否已存在
                if plugin_id not in self.plugin_info:
                    # 尝试读取插件元数据
                    metadata_file = plugin_dir / "metadata.json"
                    if metadata_file.exists():
                        try:
                            with open(metadata_file, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                            
                            plugin_info = PluginInfo(
                                plugin_id=plugin_id,
                                name=metadata.get('name', plugin_id.replace('_', ' ').title()),
                                version=metadata.get('version', '1.0.0'),
                                author=metadata.get('author', 'VabHub Team'),
                                description=metadata.get('description', f"{plugin_id} plugin"),
                                homepage=metadata.get('homepage', ''),
                                status="available"
                            )
                        except Exception as e:
                            self.logger.error(f"读取插件 {plugin_id} 元数据失败: {e}")
                            plugin_info = PluginInfo(
                                plugin_id=plugin_id,
                                name=plugin_id.replace('_', ' ').title(),
                                version="1.0.0",
                                author="VabHub Team",
                                description=f"{plugin_id} plugin",
                                status="available"
                            )
                    else:
                        # 创建默认插件信息
                        plugin_info = PluginInfo(
                            plugin_id=plugin_id,
                            name=plugin_id.replace('_', ' ').title(),
                            version="1.0.0",
                            author="VabHub Team",
                            description=f"{plugin_id} plugin",
                            status="available"
                        )
                    
                    self.plugin_info[plugin_id] = plugin_info
                    available_plugins.append(plugin_info)
        
        # 保存插件信息
        self._save_plugin_info()
        
        return available_plugins
    
    async def update_plugin_config(self, plugin_name: str, new_config: Dict[str, Any]) -> None:
        """Update plugin configuration."""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} not found")
        
        plugin = self.plugins[plugin_name]
        old_config = plugin.config.copy()
        
        # 更新配置
        plugin.config.update(new_config)
        plugin.save_config(plugin.config)
        
        # 通知插件配置变更
        await plugin.on_config_change(old_config, plugin.config)
    
    def register_event_handler(self, event_name: str, handler: callable) -> None:
        """Register a global event handler."""
        if event_name not in self._event_bus:
            self._event_bus[event_name] = []
        self._event_bus[event_name].append(handler)
    
    async def emit_event(self, event_name: str, *args, **kwargs) -> None:
        """Emit an event to all registered handlers."""
        # 全局事件处理器
        if event_name in self._event_bus:
            for handler in self._event_bus[event_name]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(*args, **kwargs)
                    else:
                        handler(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Error in global event handler for {event_name}: {e}")
        
        # 插件事件处理器
        for plugin in self.plugins.values():
            await plugin.emit_event(event_name, *args, **kwargs)
    
    # 插件市场功能
    async def fetch_market_plugins(self) -> List[PluginInfo]:
        """从插件市场获取可用插件"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.market_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # 缓存插件市场数据
                        with open(self.market_cache_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        
                        # 转换为插件信息
                        market_plugins = []
                        for plugin_data in data.get('plugins', []):
                            plugin_info = PluginInfo.from_dict(plugin_data)
                            plugin_info.status = "available"
                            market_plugins.append(plugin_info)
                        
                        return market_plugins
                    else:
                        self.logger.error(f"获取插件市场数据失败: {response.status}")
                        return []
        except Exception as e:
            self.logger.error(f"获取插件市场数据失败: {e}")
            # 尝试使用缓存数据
            return await self.get_cached_market_plugins()
    
    async def get_cached_market_plugins(self) -> List[PluginInfo]:
        """获取缓存的插件市场数据"""
        try:
            if self.market_cache_file.exists():
                with open(self.market_cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                market_plugins = []
                for plugin_data in data.get('plugins', []):
                    plugin_info = PluginInfo.from_dict(plugin_data)
                    plugin_info.status = "available"
                    market_plugins.append(plugin_info)
                
                return market_plugins
            return []
        except Exception as e:
            self.logger.error(f"读取缓存插件市场数据失败: {e}")
            return []
    
    async def install_from_market(self, plugin_id: str) -> bool:
        """从插件市场安装插件"""
        try:
            # 获取插件信息
            market_plugins = await self.fetch_market_plugins()
            target_plugin = None
            
            for plugin in market_plugins:
                if plugin.id == plugin_id:
                    target_plugin = plugin
                    break
            
            if not target_plugin:
                self.logger.error(f"插件 {plugin_id} 在市场中不存在")
                return False
            
            # 下载插件
            download_url = target_plugin.metadata.get('download_url')
            if not download_url:
                self.logger.error(f"插件 {plugin_id} 没有下载地址")
                return False
            
            # 创建插件目录
            plugin_dir = self.plugins_dir / plugin_id
            plugin_dir.mkdir(exist_ok=True)
            
            # 下载插件文件
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    if response.status == 200:
                        plugin_content = await response.read()
                        
                        # 保存插件文件
                        plugin_file = plugin_dir / "plugin.py"
                        with open(plugin_file, 'wb') as f:
                            f.write(plugin_content)
                        
                        # 保存插件元数据
                        metadata_file = plugin_dir / "metadata.json"
                        with open(metadata_file, 'w', encoding='utf-8') as f:
                            json.dump(target_plugin.to_dict(), f, ensure_ascii=False, indent=2)
                        
                        # 安装插件
                        return self.install_plugin(plugin_id)
                    else:
                        self.logger.error(f"下载插件失败: {response.status}")
                        return False
        except Exception as e:
            self.logger.error(f"从插件市场安装插件失败: {e}")
            return False
    
    def update_plugin_settings(self, plugin_id: str, settings: Dict[str, Any]) -> bool:
        """更新插件设置"""
        try:
            if plugin_id in self.plugin_info:
                plugin_info = self.plugin_info[plugin_id]
                plugin_info.settings.update(settings)
                
                # 保存插件信息
                self._save_plugin_info()
                
                self.logger.info(f"插件 {plugin_id} 设置更新成功")
                return True
            return False
        except Exception as e:
            self.logger.error(f"更新插件设置失败: {e}")
            return False
    
    def get_plugin_stats(self) -> Dict[str, Any]:
        """获取插件统计信息"""
        total_plugins = len(self.plugin_info)
        installed_plugins = len([p for p in self.plugin_info.values() if p.status == "installed"])
        enabled_plugins = len([p for p in self.plugin_info.values() if p.enabled])
        
        return {
            "total_plugins": total_plugins,
            "installed_plugins": installed_plugins,
            "enabled_plugins": enabled_plugins,
            "disabled_plugins": installed_plugins - enabled_plugins,
            "available_plugins": total_plugins - installed_plugins
        }