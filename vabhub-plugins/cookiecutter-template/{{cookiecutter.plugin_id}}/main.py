"""
{{ cookiecutter.plugin_name }} - VabHub Plugin
"""

import logging
from typing import Dict, Any, Optional
from core.plugin_manager import BasePlugin

logger = logging.getLogger(__name__)


class {{ cookiecutter.plugin_name|replace(' ', '')|replace('-', '') }}Plugin(BasePlugin):
    """{{ cookiecutter.plugin_name }} Plugin"""
    
    plugin_id = "{{ cookiecutter.plugin_id }}"
    plugin_name = "{{ cookiecutter.plugin_name }}"
    plugin_version = "{{ cookiecutter.plugin_version }}"
    plugin_description = "{{ cookiecutter.plugin_description }}"
    plugin_author = "{{ cookiecutter.plugin_author }}"
    
    def __init__(self):
        super().__init__()
        self.config: Optional[Dict[str, Any]] = None
        self.enabled = False
    
    def initialize(self):
        """Initialize the plugin"""
        logger.info(f"Initializing {self.plugin_name} v{self.plugin_version}")
        
        # Load configuration
        try:
            import json
            config_path = f"plugins/{self.plugin_id}/config.json"
            with open(config_path, 'r') as f:
                self.config = json.load(f)
            self.enabled = self.config.get('enabled', True)
            logger.info(f"Configuration loaded: {self.config}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            self.enabled = False
    
    def cleanup(self):
        """Cleanup the plugin"""
        logger.info(f"Cleaning up {self.plugin_name}")
        self.enabled = False
    
    def enable(self):
        """Enable the plugin"""
        logger.info(f"Enabling {self.plugin_name}")
        self.enabled = True
    
    def disable(self):
        """Disable the plugin"""
        logger.info(f"Disabling {self.plugin_name}")
        self.enabled = False
    
    def get_status(self) -> Dict[str, Any]:
        """Get plugin status"""
        return {
            "enabled": self.enabled,
            "config": self.config,
            "version": self.plugin_version
        }
    
    # Add your plugin methods here
    def example_method(self, param: str) -> str:
        """Example plugin method"""
        if not self.enabled:
            raise RuntimeError("Plugin is not enabled")
        
        logger.info(f"Executing example method with param: {param}")
        return f"Processed: {param}"