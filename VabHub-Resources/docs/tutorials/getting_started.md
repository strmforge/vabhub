# VabHub-Resources 入门指南

## 概述

VabHub-Resources 是 VabHub 生态系统的核心资源仓库，提供智能媒体管理的完整资源支持。本指南将帮助您快速上手使用 VabHub-Resources。

## 环境准备

### 系统要求
- Python 3.8+
- 至少 1GB 可用磁盘空间
- 网络连接（用于下载依赖）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/your-org/VabHub-Resources.git
cd VabHub-Resources
```

2. **运行安装脚本**
```bash
./scripts/install_resources.sh
```

3. **验证安装**
```bash
./scripts/validate_resources.sh
```

## 基础使用

### 1. 配置系统

创建配置文件：
```bash
cp config/config.example.yaml config/config.yaml
# 编辑配置文件
vim config/config.yaml
```

### 2. 初始化数据库

```bash
# 复制数据库模板
cp data/media_database.json /path/to/your/data/

# 初始化数据库
python -c "from vabhub_resources import MediaDatabase; db = MediaDatabase.init_database('/path/to/your/data/media_database.json')"
```

### 3. 启动服务

```bash
# 使用 Docker（推荐）
docker-compose up -d

# 或直接运行
python -m vabhub_resources.server
```

## 核心功能演示

### 媒体文件识别

```python
from vabhub_resources import MediaRecognizer

recognizer = MediaRecognizer()

# 识别单个文件
result = recognizer.recognize("/path/to/movie.mkv")
print(f"标题: {result.title}")
print(f"年份: {result.year}")
print(f"类型: {result.type}")

# 批量识别
results = recognizer.batch_recognize("/path/to/media/folder")
for result in results:
    print(f"{result.file_path} -> {result.title}")
```

### 智能重命名

```python
from vabhub_resources import MediaRenamer

renamer = MediaRenamer()

# 重命名单个文件
renamer.rename_file(
    "/path/to/old_name.mkv",
    template="{title} ({year})"
)

# 批量重命名
renamer.batch_rename(
    "/path/to/media/folder",
    template="{title} - S{season:02d}E{episode:02d}"
)
```

### 数据库管理

```python
from vabhub_resources import MediaDatabase

db = MediaDatabase("/path/to/media_database.json")

# 添加媒体记录
db.add_media({
    "title": "示例电影",
    "year": 2024,
    "type": "movie",
    "file_path": "/path/to/file.mkv",
    "metadata": {
        "duration": "02:15:30",
        "resolution": "1080p",
        "codec": "H.264"
    }
})

# 查询媒体
movies = db.search_media(type="movie", year=2024)
for movie in movies:
    print(f"{movie['title']} ({movie['year']})")
```

## 高级功能

### 自定义分类器

```python
from vabhub_resources import CustomClassifier

# 创建自定义分类器
classifier = CustomClassifier()

# 添加自定义规则
classifier.add_rule(
    pattern="*纪录片*",
    category="documentary",
    confidence=0.9
)

# 使用分类器
result = classifier.classify("/path/to/documentary.mkv")
print(f"分类结果: {result.category} (置信度: {result.confidence})")
```

### 插件开发

VabHub-Resources 支持插件扩展：

```python
from vabhub_resources import PluginBase

class MyCustomPlugin(PluginBase):
    def process_media(self, file_path):
        # 自定义处理逻辑
        return {"custom_data": "processed"}

# 注册插件
plugin = MyCustomPlugin()
plugin.register()
```

## 故障排除

### 常见问题

1. **资源文件无法加载**
   ```bash
   # 检查文件权限
   chmod +x scripts/*.sh
   
   # 重新安装资源
   ./scripts/install_resources.sh
   ```

2. **配置验证失败**
   ```bash
   # 验证配置文件
   ./scripts/validate_resources.sh
   
   # 查看详细错误
   tail -f /var/log/vabhub/resources.log
   ```

3. **数据库连接问题**
   ```bash
   # 检查数据库服务
   systemctl status postgresql
   
   # 重新初始化数据库
   python -c "from vabhub_resources import MediaDatabase; MediaDatabase.recreate_tables()"
   ```

## 下一步

- 查看 [API 文档](api/) 了解完整的功能接口
- 学习 [高级配置](tutorials/advanced_configuration.md) 进行系统优化
- 参与 [插件开发](tutorials/plugin_development.md) 扩展功能

---

**需要帮助？** 查看我们的 [支持页面](../SUPPORT.md) 或提交 [GitHub Issue](https://github.com/your-org/VabHub-Resources/issues)。