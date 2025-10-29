"""
Plugin Base Classes for VabHub

This module provides the base classes and interfaces for VabHub plugins.
Compatible with the new event-driven plugin system.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from pathlib import Path
import yaml

# Import new plugin system components
try:
    from vabhub_core.core.plugin import BasePlugin, PluginLifecycle
    from vabhub_core.core.event import EventManager, EventType
    from vabhub_core.core.scheduler import SchedulerManager
except ImportError:
    # Fallback for standalone plugin usage
    BasePlugin = ABC
    PluginLifecycle = object
    EventManager = object
    EventType = object
    SchedulerManager = object


class PluginBase(BasePlugin):
    """Base class for all VabHub plugins. Compatible with new plugin system."""
    
    def __init__(self):
        self.name: str = ""
        self.version: str = "1.0.0"
        self.description: str = ""
        self.author: str = ""
        self.enabled: bool = True
        
        self.config: Dict[str, Any] = {}
        self.logger: logging.Logger = None
        self.plugin_dir: Path = None
        
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._tasks: List[asyncio.Task] = []
    
    @abstractmethod
    async def on_load(self) -> None:
        """Called when the plugin is loaded."""
        pass
    
    @abstractmethod
    async def on_unload(self) -> None:
        """Called when the plugin is unloaded."""
        pass
    
    async def on_config_change(self, old_config: Dict[str, Any], new_config: Dict[str, Any]) -> None:
        """Called when plugin configuration changes."""
        pass
    
    def register_event(self, event_name: str) -> Callable:
        """Decorator to register event handlers."""
        def decorator(handler: Callable) -> Callable:
            if event_name not in self._event_handlers:
                self._event_handlers[event_name] = []
            self._event_handlers[event_name].append(handler)
            return handler
        return decorator
    
    async def emit_event(self, event_name: str, *args, **kwargs) -> None:
        """Emit an event to all registered handlers."""
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(*args, **kwargs)
                    else:
                        handler(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event_name}: {e}")
    
    def create_task(self, coro) -> asyncio.Task:
        """Create and track an asyncio task."""
        task = asyncio.create_task(coro)
        self._tasks.append(task)
        return task
    
    async def stop_tasks(self) -> None:
        """Cancel all running tasks."""
        for task in self._tasks:
            if not task.done():
                task.cancel()
        
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
    
    def load_config(self) -> Dict[str, Any]:
        """Load plugin configuration from file."""
        if not self.plugin_dir:
            return {}
        
        config_file = self.plugin_dir / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save plugin configuration to file."""
        if not self.plugin_dir:
            return
        
        config_file = self.plugin_dir / "config.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)


class DownloaderPlugin(PluginBase):
    """Base class for downloader plugins."""
    
    @abstractmethod
    async def download(self, url: str, destination: Path) -> bool:
        """Download a file from URL to destination."""
        pass
    
    @abstractmethod
    async def get_download_status(self, download_id: str) -> Dict[str, Any]:
        """Get download status by ID."""
        pass


class MetadataPlugin(PluginBase):
    """Base class for metadata plugins."""
    
    @abstractmethod
    async def get_metadata(self, media_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get metadata for media."""
        pass
    
    @abstractmethod
    async def search_metadata(self, query: str, media_type: str) -> List[Dict[str, Any]]:
        """Search for metadata."""
        pass


class NotificationPlugin(PluginBase):
    """Base class for notification plugins."""
    
    @abstractmethod
    async def send_notification(self, title: str, message: str, **kwargs) -> bool:
        """Send a notification."""
        pass


class AnalyzerPlugin(PluginBase):
    """Base class for analyzer plugins."""
    
    @abstractmethod
    async def analyze_media(self, media_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze media content."""
        pass
    
    @abstractmethod
    async def generate_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate analysis report."""
        pass