# MediaRecognizer API 文档

## 概述

MediaRecognizer 是 VabHub-Resources 的核心组件，负责智能识别媒体文件的元数据信息。

## 类定义

```python
class MediaRecognizer:
    def __init__(self, config_path=None):
        """
        初始化媒体识别器
        
        Args:
            config_path (str, optional): 配置文件路径
        """
```

## 方法

### recognize

识别单个媒体文件。

```python
def recognize(self, file_path, options=None):
    """
    识别媒体文件
    
    Args:
        file_path (str): 媒体文件路径
        options (dict, optional): 识别选项
        
    Returns:
        MediaResult: 识别结果对象
        
    Raises:
        FileNotFoundError: 文件不存在
        MediaFormatError: 不支持的媒体格式
    """
```

**选项参数 (options):**
- `use_cache` (bool): 是否使用缓存，默认 True
- `force_refresh` (bool): 强制刷新缓存，默认 False
- `timeout` (int): 识别超时时间（秒），默认 30

**返回值 (MediaResult):**
```python
{
    "title": str,           # 媒体标题
    "year": int,           # 发布年份
    "type": str,           # 媒体类型 (movie/tv_show/anime)
    "season": int,         # 季数 (电视剧)
    "episode": int,        # 集数 (电视剧)
    "file_path": str,      # 文件路径
    "duration": str,       # 时长 (HH:MM:SS)
    "resolution": str,     # 分辨率
    "codec": str,         # 视频编码
    "confidence": float,   # 识别置信度 (0.0-1.0)
    "metadata": dict       # 原始元数据
}
```

### batch_recognize

批量识别媒体文件。

```python
def batch_recognize(self, directory_path, options=None):
    """
    批量识别媒体文件
    
    Args:
        directory_path (str): 目录路径
        options (dict, optional): 识别选项
        
    Returns:
        List[MediaResult]: 识别结果列表
        
    Raises:
        DirectoryNotFoundError: 目录不存在
    """
```

**批量识别选项 (options):**
- `max_workers` (int): 最大工作线程数，默认 4
- `recursive` (bool): 是否递归搜索子目录，默认 True
- `file_patterns` (list): 文件模式匹配，默认 ['*.mp4', '*.mkv', '*.avi']

### get_supported_formats

获取支持的媒体格式列表。

```python
def get_supported_formats(self):
    """
    获取支持的媒体格式
    
    Returns:
        List[str]: 支持的格式列表
    """
```

## 使用示例

### 基础使用

```python
from vabhub_resources import MediaRecognizer

# 创建识别器实例
recognizer = MediaRecognizer()

# 识别单个文件
result = recognizer.recognize("/path/to/movie.mkv")
print(f"标题: {result.title}")
print(f"年份: {result.year}")
print(f"类型: {result.type}")
print(f"置信度: {result.confidence}")

# 获取支持的格式
formats = recognizer.get_supported_formats()
print(f"支持的格式: {formats}")
```

### 批量识别

```python
# 批量识别目录中的媒体文件
results = recognizer.batch_recognize(
    "/path/to/media/library",
    options={
        "recursive": True,
        "max_workers": 8,
        "file_patterns": ["*.mp4", "*.mkv", "*.avi", "*.mov"]
    }
)

# 处理识别结果
for result in results:
    if result.confidence > 0.8:
        print(f"高置信度: {result.title}")
    else:
        print(f"低置信度: {result.title} (需要手动确认)")
```

### 高级配置

```python
# 使用自定义配置
recognizer = MediaRecognizer(config_path="/path/to/custom/config.yaml")

# 带选项的识别
result = recognizer.recognize(
    "/path/to/file.mkv",
    options={
        "use_cache": False,
        "force_refresh": True,
        "timeout": 60
    }
)
```

## 错误处理

```python
try:
    result = recognizer.recognize("/path/to/nonexistent/file.mkv")
except FileNotFoundError as e:
    print(f"文件不存在: {e}")
except MediaFormatError as e:
    print(f"不支持的格式: {e}")
except Exception as e:
    print(f"识别错误: {e}")
```

## 性能优化

### 缓存机制

MediaRecognizer 使用缓存机制提高识别效率：

```python
# 禁用缓存（用于调试）
result = recognizer.recognize(
    "/path/to/file.mkv",
    options={"use_cache": False}
)

# 强制刷新缓存
result = recognizer.recognize(
    "/path/to/file.mkv", 
    options={"force_refresh": True}
)
```

### 并行处理

对于大量文件，使用批量识别和并行处理：

```python
# 使用更多工作线程
results = recognizer.batch_recognize(
    "/path/to/large/library",
    options={"max_workers": 16}
)
```

## 配置参考

### 配置文件示例

```yaml
# config/recognizer.yaml
recognizer:
  # 缓存设置
  cache:
    enabled: true
    ttl: 3600  # 缓存生存时间（秒）
    
  # 识别器设置
  detectors:
    - name: "filename"
      enabled: true
      weight: 0.3
      
    - name: "metadata"
      enabled: true
      weight: 0.5
      
    - name: "online"
      enabled: false
      weight: 0.2
      
  # 格式支持
  supported_formats:
    video: ["mp4", "mkv", "avi", "mov", "wmv"]
    audio: ["mp3", "flac", "wav"]
    
  # 性能设置
  performance:
    max_file_size: "2GB"
    timeout: 30
    max_workers: 4
```

---

**相关文档:**
- [MediaRenamer API](media_renamer.md) - 媒体重命名功能
- [MediaDatabase API](media_database.md) - 数据库管理功能
- [配置指南](../tutorials/configuration.md) - 完整配置说明