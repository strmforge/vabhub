#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件管理器 - 重定向到核心插件管理器

注意：此文件已废弃，请使用 VabHub-Core/core/plugin_manager.py
"""

import sys
from pathlib import Path

# 重定向到核心插件管理器
core_path = Path(__file__).parent.parent / "VabHub-Core"
sys.path.insert(0, str(core_path))

# 导入核心插件管理器
try:
    from core.plugin_manager import PluginManager, PluginBase, DataSourcePlugin, ProcessorPlugin, NotificationPlugin
    print("✅ 已成功导入核心插件管理器")
except ImportError as e:
    print(f"❌ 导入核心插件管理器失败: {e}")
    print("请确保 VabHub-Core 仓库已正确配置")

# 保持向后兼容性
__all__ = ['PluginManager', 'PluginBase', 'DataSourcePlugin', 'ProcessorPlugin', 'NotificationPlugin']