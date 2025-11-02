"""
Tests for {{ cookiecutter.plugin_name }} plugin
"""

import pytest
from main import {{ cookiecutter.plugin_name|replace(' ', '')|replace('-', '') }}Plugin


class Test{{ cookiecutter.plugin_name|replace(' ', '')|replace('-', '') }}Plugin:
    """Test plugin functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.plugin = {{ cookiecutter.plugin_name|replace(' ', '')|replace('-', '') }}Plugin()
    
    def test_plugin_initialization(self):
        """Test plugin initialization"""
        assert self.plugin.plugin_id == "{{ cookiecutter.plugin_id }}"
        assert self.plugin.plugin_name == "{{ cookiecutter.plugin_name }}"
        assert self.plugin.plugin_version == "{{ cookiecutter.plugin_version }}"
    
    def test_plugin_lifecycle(self):
        """Test plugin lifecycle methods"""
        # Test initialization
        self.plugin.initialize()
        
        # Test enabling
        self.plugin.enable()
        assert self.plugin.enabled == True
        
        # Test disabling
        self.plugin.disable()
        assert self.plugin.enabled == False
        
        # Test cleanup
        self.plugin.cleanup()
    
    def test_example_method(self):
        """Test example method"""
        self.plugin.initialize()
        self.plugin.enable()
        
        result = self.plugin.example_method("test")
        assert result == "Processed: test"
        
        self.plugin.disable()
        
        # Test disabled state
        with pytest.raises(RuntimeError):
            self.plugin.example_method("test")