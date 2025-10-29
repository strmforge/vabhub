# 排行榜数据收集器插件

VabHub 排行榜数据收集器插件，支持从多个数据源收集排行榜数据。

## 支持的数据源

- **Apple Music / iTunes**: 热门歌曲排行榜
- **Spotify Charts**: 全球/地区排行榜
- **Netflix Top 10**: 全球热门影视
- **IMDb Datasets**: 高评分电影排行榜

## 快速开始

### 1. 安装插件

```bash
# 在 VabHub-Core 目录下
pip install -e ../VabHub-Plugins
```

### 2. 配置插件

编辑 `config.yaml` 文件：

```yaml
collection_interval: 3600  # 数据收集间隔（秒）
output_dir: "/vol1/charts"  # 输出目录

providers:
  apple_music:
    enabled: true
    country: "us"
    
  spotify_charts:
    enabled: true
    region: "global"
```

### 3. 启用插件

在 VabHub-Core 的插件管理界面中启用此插件。

## 数据格式

收集的数据采用标准化 JSONL 格式：

```json
{
  "source": "apple_music",
  "region": "US",
  "chart_type": "most_played_songs",
  "date_or_week": "2025-10-27",
  "rank": 1,
  "title": "歌曲名",
  "artist_or_show": "艺术家名",
  "id_or_url": "https://...",
  "metrics": {
    "plays": 123456
  },
  "search_query": "艺术家 - 歌曲名",
  "collected_at": "2025-10-27T10:00:00"
}
```

## 输出文件

- 原始数据: `/vol1/charts/raw/`
- 标准化数据: `/vol1/charts/normalized/charts_normalized_YYYYMMDD.jsonl`

## API 接口

插件提供以下 API 接口：

- `GET /api/plugins/charts_collector/data` - 获取最新排行榜数据
- `POST /api/plugins/charts_collector/collect` - 手动触发数据收集
- `GET /api/plugins/charts_collector/config` - 获取插件配置

## 集成功能

插件支持与 Jackett/Prowlarr 和 qBittorrent 集成，实现自动化下载：

1. 收集排行榜数据
2. 根据规则筛选候选内容
3. 通过 Torznab API 搜索资源
4. 自动添加到下载器

## 故障排除

### 数据收集失败
- 检查网络连接
- 验证 API 端点是否可访问
- 查看插件日志

### 文件权限问题
- 确保输出目录有写入权限
- 检查磁盘空间

## 开发说明

### 添加新的数据提供者

1. 在 `providers/` 目录下创建新的提供者类
2. 继承 `BaseProvider` 基类
3. 实现 `fetch_data` 方法
4. 在 `plugin.py` 中注册提供者