# STRM文件使用指南

## 概述

STRM（Stream）文件是一种轻量级的媒体文件格式，它不包含实际的媒体数据，而是包含指向实际媒体文件的URL。通过STRM文件，用户可以在本地保存指向云存储中媒体文件的链接，从而大大减少本地存储空间的占用。

## 核心功能

### 1. STRM文件生成
- 为云存储中的媒体文件生成STRM文件
- 支持批量生成和按类型自动分类
- 智能识别媒体类型（电影、电视剧、动漫等）

### 2. 302跳转代理
- 通过本地服务代理云存储的流媒体请求
- 支持断点续传和流媒体播放
- 自动处理认证和权限验证

### 3. 文件管理
- STRM文件验证和修复
- 批量操作支持
- 与现有媒体库系统集成

## 使用方法

### API接口

#### 1. 生成STRM文件
```bash
POST /api/strm/generate
Content-Type: application/json

{
  "storage_type": "u115",
  "file_ids": ["file_id_1", "file_id_2"],
  "output_dir": "/path/to/strm/files",
  "organize_by_type": true,
  "strm_type": "proxy"
}
```

#### 2. 流媒体重定向
```bash
GET /api/strm/stream/{storage_type}/{file_id}
```

#### 3. 验证STRM文件
```bash
POST /api/strm/validate
Content-Type: application/json

{
  "strm_paths": ["/path/to/file1.strm", "/path/to/file2.strm"]
}
```

#### 4. 修复STRM文件
```bash
POST /api/strm/repair
Content-Type: application/json

{
  "strm_path": "/path/to/file.strm",
  "new_url": "https://new-url.com/file.mp4"
}
```

### Python代码示例

#### 基本使用
```python
from core.strm_generator import STRMGenerator, STRMType

# 创建STRM生成器
strm_gen = STRMGenerator(base_url="http://localhost:8000")

# 生成单个STRM文件
success = strm_gen.create_strm_file(
    output_path="/path/to/movie.strm",
    file_url="http://localhost:8000/api/strm/stream/u115/file123",
    strm_type=STRMType.PROXY,
    metadata={"media_type": "movie"}
)

# 批量生成STRM文件
file_list = [
    {
        "storage_type": "u115",
        "file_id": "file123",
        "file_name": "movie.mp4",
        "metadata": {"media_type": "movie"}
    }
]

results = strm_gen.batch_generate_strm(
    file_list=file_list,
    output_base_dir="/path/to/strm/files",
    organize_by_type=True
)
```

#### 与存储适配器集成
```python
from core.storage_115 import U115Storage

# 初始化115网盘存储
storage = U115Storage()
storage.init_storage()

# 获取文件列表
files = storage.list_files("/电影")

# 为文件生成STRM
for file_item in files:
    if not file_item.is_dir:
        strm_path = storage.generate_strm_file(
            file_item=file_item,
            output_path=Path(f"/strm/{file_item.name}.strm")
        )
        print(f"生成STRM文件: {strm_path}")
```

## STRM文件格式

### 直接跳转格式
```
#STRM Direct Redirect
https://example.com/file.mp4
```

### 代理跳转格式（推荐）
```
#STRM Proxy Redirect
http://localhost:8000/api/strm/proxy?url=https://example.com/file.mp4
```

### 自定义格式（包含元数据）
```
#STRM Custom Redirect
http://localhost:8000/api/strm/stream/u115/file123
#METADATA
{
  "storage_type": "u115",
  "file_id": "file123",
  "file_name": "movie.mp4",
  "size": 1024000,
  "media_type": "movie"
}
```

## 集成到媒体播放器

### 支持STRM的播放器
- **Plex**: 原生支持STRM文件
- **Jellyfin**: 原生支持STRM文件
- **Kodi**: 通过插件支持
- **VLC**: 直接播放STRM文件

### 播放器配置示例

#### Plex配置
1. 将STRM文件目录添加到Plex媒体库
2. 确保Plex服务器可以访问STRM代理服务
3. 配置正确的媒体类型识别

#### Jellyfin配置
1. 添加STRM文件目录到媒体库
2. 配置网络访问权限
3. 设置媒体元数据刮削器

## 性能优化

### 缓存策略
- STRM代理服务支持HTTP缓存头
- 可配置缓存时间和大小限制
- 支持CDN集成

### 并发处理
- 多线程STRM文件生成
- 异步流媒体代理
- 连接池管理

### 错误处理
- 自动重试机制
- 优雅降级策略
- 详细的错误日志

## 安全考虑

### 认证授权
- OAuth2.0认证集成
- API密钥管理
- 访问权限控制

### 数据安全
- HTTPS加密传输
- 文件访问日志
- 异常访问检测

## 故障排除

### 常见问题

#### STRM文件无法播放
1. 检查STRM文件格式是否正确
2. 验证代理服务是否正常运行
3. 检查网络连接和防火墙设置

#### 播放卡顿
1. 检查网络带宽
2. 调整代理服务的缓存设置
3. 考虑使用CDN加速

#### 认证失败
1. 检查API密钥和令牌
2. 验证存储服务的访问权限
3. 查看详细的错误日志

### 调试工具

使用STRM验证工具检查文件状态：
```bash
# 验证单个STRM文件
curl -X POST http://localhost:8000/api/strm/validate \
  -H "Content-Type: application/json" \
  -d '{"strm_paths": ["/path/to/file.strm"]}'
```

## 最佳实践

### 文件组织
- 按媒体类型分类存储
- 使用有意义的文件名
- 定期清理无效的STRM文件

### 备份策略
- 定期备份STRM文件目录
- 保存文件生成日志
- 配置自动修复机制

### 监控告警
- 监控代理服务状态
- 设置文件访问告警
- 定期性能检查

## 扩展功能

### 自定义插件
可以开发自定义的STRM处理器来支持更多存储服务：

```python
class CustomStorageSTRM:
    def generate_strm_url(self, file_item):
        # 自定义URL生成逻辑
        pass
    
    def validate_access(self, file_id):
        # 自定义访问验证
        pass
```

### Web界面
提供图形化的STRM文件管理界面：
- 文件浏览和选择
- 批量操作界面
- 实时状态监控

## 技术支持

如有问题，请参考：
- API文档：`/docs`
- 错误日志：查看服务日志文件
- 社区支持：项目GitHub页面