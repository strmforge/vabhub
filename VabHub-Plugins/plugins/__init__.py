"""
VabHub Plugins Package

This package contains the plugin system for VabHub, including plugin base classes,
manager, and built-in plugins.
"""

__version__ = "1.0.0"
__author__ = "VabHub Team"
__email__ = "team@vabhub.org"

from .base import PluginBase, PluginManager
from .manager import PluginManager

__all__ = ["PluginBase", "PluginManager"]