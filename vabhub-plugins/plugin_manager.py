#!/usr/bin/env python3
"""
VabHub 插件管理器

提供插件动态加载、配置管理、依赖管理和生命周期管理功能
"""

import importlib
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Type, Any, Set
from dataclasses import dataclass
from plugin_base import BasePlugin

logger = logging.getLogger(__name__)


@dataclass
class PluginConfig:
    """插件配置"""
    name: str
    enabled: bool = True
    config: Dict[str, Any] = None
    dependencies: List[str] = None
    priority: int = 0
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}
        if self.dependencies is None:
            self.dependencies = []


class PluginRegistry:
    """插件注册表"""
    
    def __init__(self):
        self.plugins: Dict[str, Type[BasePlugin]] = {}
        self.configs: Dict[str, PluginConfig] = {}
    
    def register(self, plugin_class: Type[BasePlugin], config: Optional[PluginConfig] = None):
        """注册插件"""
        if not config:
            config = PluginConfig(name=plugin_class.name)
        
        self.plugins[plugin_class.name] = plugin_class
        self.configs[plugin_class.name] = config
    
    def unregister(self, plugin_name: str):
        """注销插件"""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
        if plugin_name in self.configs:
            del self.configs[plugin_name]
    
    def get_plugin_class(self, plugin_name: str) -> Optional[Type[BasePlugin]]:
        """获取插件类"""
        return self.plugins.get(plugin_name)
    
    def get_config(self, plugin_name: str) -> Optional[PluginConfig]:
        """获取插件配置"""
        return self.configs.get(plugin_name)
    
    def list_plugins(self) -> List[str]:
        """列出所有插件"""
        return list(self.plugins.keys())


class PluginManager:
    """插件管理器"""
    
    def __init__(self, config_dir: str = "config"):
        self.plugins: Dict[str, BasePlugin] = {}
        self.registry = PluginRegistry()
        self.config_dir = Path(config_dir)
        self.logger = logging.getLogger("plugin_manager")
        
        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """加载插件配置"""
        config_file = self.config_dir / f"{plugin_name}.json"
        
        if not config_file.exists():
            return None
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load config for {plugin_name}: {e}")
            return None
    
    def save_config(self, plugin_name: str, config: Dict[str, Any]) -> bool:
        """保存插件配置"""
        config_file = self.config_dir / f"{plugin_name}.json"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save config for {plugin_name}: {e}")
            return False
    
    def resolve_dependencies(self, plugin_name: str) -> List[str]:
        """解析插件依赖"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return []
        
        dependencies = getattr(plugin, 'dependencies', [])
        resolved_deps = []
        
        for dep in dependencies:
            # 检查依赖是否已加载
            if dep not in self.plugins:
                self.logger.warning(f"Dependency {dep} not found for {plugin_name}")
                continue
            resolved_deps.append(dep)
        
        return resolved_deps
    
    def get_dependency_tree(self, plugin_name: str) -> Dict[str, Any]:
        """获取插件依赖树"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return {}
        
        tree = {
            'name': plugin_name,
            'dependencies': []
        }
        
        dependencies = getattr(plugin, 'dependencies', [])
        for dep in dependencies:
            if dep in self.plugins:
                tree['dependencies'].append(self.get_dependency_tree(dep))
        
        return tree
    
    def load_plugin_with_config(self, plugin_class: Type[BasePlugin]) -> bool:
        """加载插件并应用配置"""
        # 加载配置
        config = self.load_config(plugin_class.name)
        
        # 检查依赖
        dependencies = getattr(plugin_class, 'dependencies', [])
        for dep in dependencies:
            if dep not in self.plugins:
                self.logger.warning(f"Plugin {plugin_class.name} requires dependency {dep} which is not loaded")
                return False
        
        # 加载插件
        return self.load_plugin(plugin_class, config)
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """重新加载插件"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            self.logger.error(f"Plugin {plugin_name} not found for reload")
            return False
        
        # 保存当前配置
        config = plugin.config if hasattr(plugin, 'config') else {}
        
        # 卸载插件
        if not self.unload_plugin(plugin_name):
            return False
        
        # 重新加载插件
        plugin_class = self.registry.get_plugin_class(plugin_name)
        if not plugin_class:
            self.logger.error(f"Plugin class for {plugin_name} not found in registry")
            return False
        
        return self.load_plugin(plugin_class, config)
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            self.logger.error(f"Plugin {plugin_name} not found")
            return False
        
        plugin.enabled = True
        self.logger.info(f"Enabled plugin: {plugin_name}")
        return True
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            self.logger.error(f"Plugin {plugin_name} not found")
            return False
        
        plugin.enabled = False
        self.logger.info(f"Disabled plugin: {plugin_name}")
        return True
    
    def get_plugin_status(self, plugin_name: str) -> Dict[str, Any]:
        """获取插件状态"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return {"status": "not_found"}
        
        return {
            "name": plugin_name,
            "enabled": plugin.enabled,
            "status": "active" if plugin.enabled else "disabled",
            "dependencies": self.resolve_dependencies(plugin_name),
            "health": plugin.health_check()
        }
    
    def get_all_plugin_status(self) -> Dict[str, Dict[str, Any]]:
        """获取所有插件状态"""
        status = {}
        for plugin_name in self.list_plugins():
            status[plugin_name] = self.get_plugin_status(plugin_name)
        return status
    
    def batch_operation(self, operation: str, plugin_names: List[str]) -> Dict[str, bool]:
        """批量操作插件"""
        results = {}
        
        for plugin_name in plugin_names:
            if operation == "enable":
                results[plugin_name] = self.enable_plugin(plugin_name)
            elif operation == "disable":
                results[plugin_name] = self.disable_plugin(plugin_name)
            elif operation == "reload":
                results[plugin_name] = self.reload_plugin(plugin_name)
            else:
                results[plugin_name] = False
        
        return results
    
    def load_plugin(self, plugin_class: Type[BasePlugin], config: Optional[dict] = None) -> bool:
        """加载插件"""
        try:
            plugin = plugin_class(config or {})
            
            if not plugin.validate_config():
                self.logger.error(f"Plugin {plugin.name} config validation failed")
                return False
            
            plugin.setup()
            self.plugins[plugin.name] = plugin
            self.logger.info(f"Loaded plugin: {plugin}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_class}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            try:
                plugin.cleanup()
                del self.plugins[plugin_name]
                self.logger.info(f"Unloaded plugin: {plugin_name}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to unload plugin {plugin_name}: {e}")
        return False
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """获取插件"""
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[str]:
        """列出所有插件"""
        return list(self.plugins.keys())
    
    def execute_plugin(self, plugin_name: str, data: Any) -> Any:
        """执行插件"""
        plugin = self.get_plugin(plugin_name)
        if plugin and plugin.enabled:
            try:
                return plugin.execute(data)
            except Exception as e:
                self.logger.error(f"Plugin {plugin_name} execution failed: {e}")
        return data
    
    def health_check(self) -> Dict[str, bool]:
        """健康检查"""
        results = {}
        for name, plugin in self.plugins.items():
            try:
                results[name] = plugin.health_check()
            except Exception as e:
                self.logger.error(f"Health check failed for {name}: {e}")
                results[name] = False
        return results
    
    def cleanup(self):
        """清理所有插件"""
        for name in list(self.plugins.keys()):
            self.unload_plugin(name)
    
    async def discover_plugins(self, plugin_dir: str = "plugins"):
        """动态发现插件"""
        plugin_path = Path(plugin_dir)
        if not plugin_path.exists():
            self.logger.warning(f"插件目录不存在: {plugin_dir}")
            return []
        
        discovered_plugins = []
        
        # 支持子目录搜索
        for file_path in plugin_path.rglob("*.py"):
            if file_path.name.startswith("_") or file_path.name == "__init__.py":
                continue
            
            # 计算相对路径作为模块名
            relative_path = file_path.relative_to(plugin_path)
            module_name = str(relative_path.with_suffix('')).replace('/', '.').replace('\\', '.')
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None:
                    continue
                    
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 查找插件类
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BasePlugin) and 
                        attr != BasePlugin):
                        
                        # 检查插件是否已注册
                        if attr.name not in self.registry.plugins:
                            # 注册插件到注册表
                            self.registry.register(attr)
                            self.logger.info(f"发现插件: {attr.name}")
                        
                        # 检查插件是否已加载
                        if attr.name not in self.plugins:
                            # 加载配置
                            config = self.load_config(attr.name)
                            success = self.load_plugin(attr, config)
                            if success:
                                discovered_plugins.append(attr.name)
                                self.logger.info(f"加载插件: {attr.name}")
                        else:
                            self.logger.debug(f"插件已加载: {attr.name}")
            
            except Exception as e:
                self.logger.error(f"加载插件 {file_path} 失败: {e}")
        
        return discovered_plugins
    
    def get_plugin_dependencies(self, plugin_name: str) -> List[str]:
        """获取插件依赖"""
        plugin = self.get_plugin(plugin_name)
        if plugin and hasattr(plugin, 'dependencies'):
            return getattr(plugin, 'dependencies', [])
        return []
    
    async def load_plugin_with_dependencies(self, plugin_class: Type[BasePlugin], config: Optional[dict] = None) -> bool:
        """加载插件及其依赖"""
        # 检查依赖
        dependencies = getattr(plugin_class, 'dependencies', [])
        
        # 加载依赖插件
        for dep_name in dependencies:
            if dep_name not in self.plugins:
                # 尝试从注册表获取依赖插件类
                dep_class = self.registry.get_plugin_class(dep_name)
                if dep_class:
                    # 递归加载依赖
                    dep_success = await self.load_plugin_with_dependencies(dep_class)
                    if not dep_success:
                        self.logger.error(f"依赖插件 {dep_name} 加载失败")
                        return False
                else:
                    self.logger.error(f"依赖插件 {dep_name} 未找到")
                    return False
        
        # 加载插件
        return self.load_plugin(plugin_class, config)
    
    async def auto_discover_and_load(self, plugin_dir: str = "plugins") -> Dict[str, bool]:
        """自动发现并加载所有插件"""
        results = {}
        
        # 发现插件
        discovered_plugins = await self.discover_plugins(plugin_dir)
        
        # 按优先级排序并加载
        plugin_priority = {}
        for plugin_name in discovered_plugins:
            plugin_class = self.registry.get_plugin_class(plugin_name)
            if plugin_class:
                priority = getattr(plugin_class, 'priority', 0)
                plugin_priority[plugin_name] = priority
        
        # 按优先级从高到低排序
        sorted_plugins = sorted(plugin_priority.keys(), key=lambda x: plugin_priority[x], reverse=True)
        
        for plugin_name in sorted_plugins:
            plugin_class = self.registry.get_plugin_class(plugin_name)
            if plugin_class:
                # 加载配置
                config = self.load_config(plugin_name)
                
                # 加载插件及其依赖
                success = await self.load_plugin_with_dependencies(plugin_class, config)
                results[plugin_name] = success
                
                if success:
                    self.logger.info(f"成功加载插件: {plugin_name}")
                else:
                    self.logger.error(f"加载插件失败: {plugin_name}")
        
        return results
    
    def get_plugin_info(self, plugin_name: str) -> Dict[str, Any]:
        """获取插件详细信息"""
        plugin_class = self.registry.get_plugin_class(plugin_name)
        if not plugin_class:
            return {"error": "Plugin not found"}
        
        plugin = self.get_plugin(plugin_name)
        config = self.registry.get_config(plugin_name)
        
        info = {
            "name": plugin_name,
            "class_name": plugin_class.__name__,
            "version": getattr(plugin_class, 'version', 'unknown'),
            "description": getattr(plugin_class, 'description', ''),
            "enabled": plugin.enabled if plugin else False,
            "dependencies": getattr(plugin_class, 'dependencies', []),
            "priority": getattr(plugin_class, 'priority', 0),
            "config": config.config if config else {},
            "status": "loaded" if plugin else "discovered"
        }
        
        return info
    
    def get_all_plugin_info(self) -> Dict[str, Dict[str, Any]]:
        """获取所有插件信息"""
        info = {}
        
        # 已加载的插件
        for plugin_name in self.plugins:
            info[plugin_name] = self.get_plugin_info(plugin_name)
        
        # 已发现但未加载的插件
        for plugin_name in self.registry.list_plugins():
            if plugin_name not in info:
                info[plugin_name] = self.get_plugin_info(plugin_name)
        
        return info
    
    async def hot_reload_plugin(self, plugin_name: str) -> bool:
        """热重载插件"""
        if plugin_name not in self.plugins:
            self.logger.error(f"插件 {plugin_name} 未加载，无法热重载")
            return False
        
        try:
            # 保存当前状态
            plugin = self.plugins[plugin_name]
            was_enabled = plugin.enabled
            config = plugin.config.copy()
            
            # 卸载插件
            if not self.unload_plugin(plugin_name):
                return False
            
            # 重新加载插件
            plugin_class = self.registry.get_plugin_class(plugin_name)
            if not plugin_class:
                self.logger.error(f"插件类 {plugin_name} 未找到")
                return False
            
            success = self.load_plugin(plugin_class, config)
            if success and was_enabled:
                self.enable_plugin(plugin_name)
            
            return success
            
        except Exception as e:
            self.logger.error(f"热重载插件 {plugin_name} 失败: {e}")
            return False