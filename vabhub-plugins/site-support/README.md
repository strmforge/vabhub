# 站点支持插件

支持多个PT站点的自动搜索和下载功能，提供类似MoviePilot的站点管理体验。

## 功能特性

- **多站点支持**: 支持M-Team、HDChina、TTG等主流PT站点
- **智能搜索**: 跨站点搜索，按做种人数排序
- **自动下载**: 支持一键下载种子文件
- **站点状态监控**: 实时监控站点连通性
- **配置管理**: 灵活的站点配置和API密钥管理

## 支持的站点

- ✅ M-Team
- ✅ HDChina  
- ✅ TTG
- ⚠️ HDBits (需要配置)
- ✅ PterClub

## 配置选项

- `max_concurrent_searches`: 最大并发搜索数量
- `request_timeout`: 请求超时时间
- `retry_count`: 重试次数
- `cache_duration`: 缓存持续时间
- `auto_update_sites`: 自动更新站点列表

## 使用示例

```python
from main import SiteSupport

# 初始化插件
config = {
    "max_concurrent_searches": 3,
    "request_timeout": 10
}
plugin = SiteSupport(config)

# 搜索种子
results = plugin.search_torrents("Inception", "movie")
print(f"找到 {len(results)} 个种子")

# 下载种子
if results:
    torrent = results[0]
    success = plugin.download_torrent(
        torrent['site_id'], 
        torrent['torrent_id'],
        "/downloads"
    )

# 获取站点状态
status = plugin.get_site_status()
print("站点状态:", status)
```

## API接口

### 搜索种子
```python
search_torrents(query: str, category: str = "", site_id: str = "") -> List[Dict]
```

### 下载种子
```python
download_torrent(site_id: str, torrent_id: str, download_path: str = "") -> bool
```

### 获取站点状态
```python
get_site_status(site_id: str = "") -> Dict[str, Any]
```

### 更新站点配置
```python
update_site_config(site_id: str, updates: Dict) -> bool
```

## 种子信息格式

返回的种子信息包含以下字段：

- `site_id`: 站点ID
- `torrent_id`: 种子ID
- `title`: 种子标题
- `size`: 文件大小
- `seeders`: 做种人数
- `leechers`: 下载人数
- `download_url`: 下载链接
- `category`: 分类
- `upload_time`: 上传时间
- `free`: 是否免费

## 站点配置

每个站点的配置包含：
- `id`: 站点唯一标识
- `name`: 站点名称
- `url`: 站点URL
- `enabled`: 是否启用
- `api_key`: API密钥
- `search_endpoint`: 搜索接口
- `categories`: 支持的分类
- `priority`: 搜索优先级