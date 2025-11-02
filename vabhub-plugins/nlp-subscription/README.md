# 自然语言订阅插件

使用自然语言处理技术解析用户指令，自动创建订阅规则。支持中文指令的智能解析和规则生成。

## 功能特性

- **智能解析**: 支持多种自然语言指令模式
- **多模式匹配**: 电影、电视剧、质量要求、年份等多种订阅模式
- **置信度评估**: 提供解析结果的置信度评分
- **自动规则生成**: 根据解析结果自动创建订阅规则
- **历史记录**: 保存解析和创建规则的历史

## 支持的指令模式

### 电影订阅
- "订阅诺兰的电影"
- "下载2023年的科幻电影"  
- "关注4K高清电影"

### 电视剧订阅
- "订阅权力的游戏第8季"
- "下载科幻剧集"

### 导演/演员订阅
- "订阅诺兰导演的电影"
- "关注汤姆·汉克斯主演的电影"

### 质量要求
- "只要1080p的电影"
- "不要标清内容"

## 配置选项

- `min_confidence`: 最小置信度阈值 (0.1-1.0)
- `auto_create_rules`: 是否自动创建规则
- `max_history_size`: 最大历史记录数量
- `enable_fuzzy_matching`: 是否启用模糊匹配
- `language`: 语言设置 (zh/en)
- `debug_mode`: 调试模式

## 使用示例

```python
from main import NLPSubscription

# 初始化插件
config = {
    "min_confidence": 0.5,
    "auto_create_rules": True
}
plugin = NLPSubscription(config)

# 解析命令
command = "订阅诺兰的4K电影"
parse_result = plugin.parse_command(command)

print(f"解析成功: {parse_result['parsed_successfully']}")
print(f"置信度: {parse_result['confidence']:.2f}")
print(f"规则类型: {parse_result['rule_type']}")

# 创建订阅规则
if parse_result['parsed_successfully']:
    creation_result = plugin.create_subscription_rule(command, "自定义规则名称")
    
    if creation_result['success']:
        rule = creation_result['rule']
        print(f"规则创建成功: {rule['name']}")
        print(f"条件数量: {len(rule['conditions'])}")
```

## API接口

### 解析命令
```python
parse_command(command: str) -> Dict[str, Any]
```

### 创建订阅规则
```python
create_subscription_rule(command: str, rule_name: str = "") -> Dict[str, Any]
```

### 获取历史记录
```python
get_rules_history() -> List[Dict]
```

### 测试命令
```python
test_commands() -> List[Dict]
```

## 解析结果格式

解析结果包含以下字段：

- `original_command`: 原始命令
- `parsed_successfully`: 是否解析成功
- `rule_type`: 规则类型 (movie/tv/mixed/unknown)
- `conditions`: 生成的条件列表
- `actions`: 默认操作列表
- `confidence`: 解析置信度 (0.0-1.0)
- `matched_patterns`: 匹配的模式列表

## 条件字段映射

插件支持以下条件字段的自动映射：

- `type`: 媒体类型 (movie/tv)
- `title`: 标题关键词
- `year`: 年份
- `resolution`: 分辨率
- `season`: 季数
- `director`: 导演
- `actor`: 演员
- `genre`: 类型/风格

## 性能优化

- 使用正则表达式进行高效的模式匹配
- 支持模糊匹配提高容错性
- 提供置信度评估避免错误规则
- 历史记录管理防止重复规则