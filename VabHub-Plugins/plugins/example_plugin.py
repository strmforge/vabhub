#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例插件
展示如何创建和使用插件系统
"""

from typing import Any
from core.event import Event, EventType
import structlog

logger = structlog.get_logger()


class Plugin:
    """示例插件"""
    
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.name = "示例插件"
        self.version = "1.0.0"
        
        # 注册事件监听器
        self._register_handlers()
    
    def _register_handlers(self):
        """注册事件处理器"""
        self.event_manager.subscribe(EventType.FILE_PROCESSING_STARTED, self.on_processing_started)
        self.event_manager.subscribe(EventType.FILE_PROCESSING_COMPLETED, self.on_processing_completed)
        self.event_manager.subscribe(EventType.FILE_RENAMED, self.on_file_renamed)
        self.event_manager.subscribe(EventType.ERROR_OCCURRED, self.on_error_occurred)
    
    def on_processing_started(self, event: Event):
        """处理开始事件"""
        logger.info("插件: 文件处理开始", file_count=event.data.get('file_count', 0))
    
    def on_processing_completed(self, event: Event):
        """处理完成事件"""
        logger.info("插件: 文件处理完成", 
                   total=event.data.get('total', 0),
                   successful=event.data.get('successful', 0),
                   failed=event.data.get('failed', 0))
    
    def on_file_renamed(self, event: Event):
        """文件重命名事件"""
        logger.info("插件: 文件已重命名", 
                   original_name=event.original_name,
                   new_name=event.new_name)
    
    def on_error_occurred(self, event: Event):
        """错误事件"""
        logger.error("插件: 处理错误", 
                    file_path=event.file_path,
                    error=event.error_message)