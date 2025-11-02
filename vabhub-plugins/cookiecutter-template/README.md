# VabHub Plugin CookieCutter Template

A template for creating VabHub plugins using Cookiecutter.

## Usage

1. Install Cookiecutter:
```bash
pip install cookiecutter
```

2. Generate a new plugin:
```bash
cookiecutter vabhub-plugins/cookiecutter-template/
```

3. Follow the prompts to customize your plugin.

4. Copy the generated plugin folder to `vabhub-Core/plugins/`

5. Install dependencies and restart VabHub Core.

## Template Structure

```
{{cookiecutter.plugin_id}}/
├── plugin.json          # Plugin manifest
├── config.json          # Plugin configuration
├── main.py             # Main plugin code
├── requirements.txt     # Dependencies
├── README.md           # Plugin documentation
└── tests/              # Test files
    └── test_plugin.py
```

## Plugin Development Guide

### Plugin Manifest (plugin.json)

Required fields:
- `id`: Unique plugin identifier
- `name`: Human-readable plugin name
- `version`: Plugin version
- `description`: Plugin description
- `author`: Plugin author
- `dependencies`: List of required plugins
- `config_schema`: Configuration schema

### Plugin Base Class

All plugins should inherit from `BasePlugin` and implement:
- `initialize()`: Plugin initialization
- `cleanup()`: Plugin cleanup
- `enable()`: Enable plugin
- `disable()`: Disable plugin

### Configuration

Plugins can access configuration through `self.config` after initialization.

### Logging

Use the standard logging module:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Plugin message")
```

### Testing

Write tests in the `tests/` directory using pytest.

## Best Practices

1. **Error Handling**: Always handle exceptions gracefully
2. **Configuration Validation**: Validate configuration on initialization
3. **Resource Management**: Clean up resources in cleanup() method
4. **Documentation**: Provide clear documentation for users
5. **Testing**: Write comprehensive tests for your plugin

## Example Plugin

See the generated plugin template for a complete example.