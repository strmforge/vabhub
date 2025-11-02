# 高级订阅规则插件

提供类似MoviePilot的高级订阅功能，支持复杂条件组合和自动下载。

## 功能特性

- **多条件组合**: 支持AND逻辑的多条件组合
- **多种操作符**: 等于、包含、正则匹配、大于、小于等
- **自动下载**: 匹配规则后自动触发下载
- **优先级管理**: 支持不同优先级的下载任务
- **规则管理**: 支持规则的创建、编辑、删除

## 配置选项

- `auto_scan`: 是否自动扫描新内容
- `max_rules`: 最大规则数量限制
- `log_level`: 日志级别设置
- `notification_enabled`: 是否启用通知

## 使用示例

```python
from main import AdvancedSubscriptionRules

# 初始化插件
plugin = AdvancedSubscriptionRules(config)

# 创建订阅规则
rule = plugin.create_rule(
    name="高质量电影订阅",
    conditions=[
        {"field": "type", "operator": "equals", "value": "movie"},
        {"field": "rating", "operator": "greater_than", "value": 7.0}
    ],
    actions=[{"type": "download", "action": "auto_download"}]
)

# 评估媒体
media_info = {
    "type": "movie",
    "title": "Inception",
    "rating": 8.8,
    "year": 2010
}

matched_rules = plugin.evaluate_media(media_info)
```

## 规则格式

### 条件字段
- `type`: 媒体类型 (movie/tv)
- `title`: 标题
- `year`: 年份
- `rating`: 评分
- `resolution`: 分辨率
- `video_codec`: 视频编码

### 操作符
- `equals`: 等于
- `contains`: 包含
- `regex`: 正则匹配
- `greater_than`: 大于
- `less_than`: 小于
- `in_list`: 在列表中

## API接口

- `get_rules()`: 获取所有规则
- `create_rule(name, conditions, actions)`: 创建规则
- `update_rule(rule_id, updates)`: 更新规则
- `delete_rule(rule_id)`: 删除规则
- `evaluate_media(media_info)`: 评估媒体