#!/usr/bin/env python3
"""
自然语言订阅插件
使用NLP技术解析用户指令，自动创建订阅规则
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class NLPSubscription:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.patterns = self._load_patterns()
        self.rules_history = []
    
    def _load_patterns(self) -> List[Dict]:
        """加载NLP模式"""
        return [
            # 电影订阅模式
            {
                "name": "movie_subscription",
                "pattern": r'(订阅|下载|关注)(.*?)(的电影|电影作品)',
                "type": "movie",
                "priority": "normal"
            },
            {
                "name": "movie_with_quality",
                "pattern": r'(订阅|下载)(.*?)(的)?(4K|1080p|720p)(电影|影片)',
                "type": "movie",
                "priority": "high"
            },
            {
                "name": "movie_by_year",
                "pattern": r'(订阅|下载)(\d{4})年(.*?)(的电影|影片)',
                "type": "movie",
                "priority": "normal"
            },
            
            # 电视剧订阅模式
            {
                "name": "tv_series",
                "pattern": r'(订阅|下载|关注)(.*?)(的电视剧|剧集|美剧)',
                "type": "tv",
                "priority": "normal"
            },
            {
                "name": "tv_season",
                "pattern": r'(订阅|下载)(.*?)第(\d+)季',
                "type": "tv",
                "priority": "normal"
            },
            
            # 导演/演员订阅模式
            {
                "name": "director_subscription",
                "pattern": r'(订阅|下载|关注)(.*?)(导演|执导)(的电影|作品)',
                "type": "movie",
                "priority": "normal"
            },
            {
                "name": "actor_subscription",
                "pattern": r'(订阅|下载|关注)(.*?)(主演|出演|参演)(的电影|作品)',
                "type": "movie",
                "priority": "normal"
            },
            
            # 质量要求模式
            {
                "name": "quality_requirement",
                "pattern": r'(只要|仅下载)(4K|1080p|720p|高清|蓝光)',
                "type": "quality",
                "priority": "high"
            },
            {
                "name": "exclude_quality",
                "pattern": r'(不要|排除)(标清|480p|低质量)',
                "type": "quality",
                "priority": "normal"
            }
        ]
    
    def parse_command(self, command: str) -> Dict[str, Any]:
        """解析自然语言命令"""
        command = command.strip().lower()
        
        # 初始化解析结果
        result = {
            "original_command": command,
            "parsed_successfully": False,
            "rule_type": "unknown",
            "conditions": [],
            "actions": [{"type": "download", "action": "auto_download", "priority": "normal"}],
            "confidence": 0.0,
            "matched_patterns": []
        }
        
        # 尝试匹配各种模式
        matched_patterns = []
        
        for pattern in self.patterns:
            matches = re.finditer(pattern["pattern"], command)
            for match in matches:
                matched_patterns.append({
                    "pattern_name": pattern["name"],
                    "pattern_type": pattern["type"],
                    "priority": pattern["priority"],
                    "matches": match.groups()
                })
        
        if not matched_patterns:
            # 如果没有匹配到模式，尝试通用解析
            return self._generic_parse(command)
        
        # 处理匹配到的模式
        result["matched_patterns"] = matched_patterns
        result["parsed_successfully"] = True
        result["confidence"] = self._calculate_confidence(matched_patterns)
        
        # 根据匹配的模式生成订阅规则
        conditions = self._generate_conditions(matched_patterns)
        result["conditions"] = conditions
        
        # 确定规则类型
        if any(p["pattern_type"] == "movie" for p in matched_patterns):
            result["rule_type"] = "movie"
        elif any(p["pattern_type"] == "tv" for p in matched_patterns):
            result["rule_type"] = "tv"
        else:
            result["rule_type"] = "mixed"
        
        # 设置优先级
        if any(p["priority"] == "high" for p in matched_patterns):
            result["actions"][0]["priority"] = "high"
        
        return result
    
    def _generic_parse(self, command: str) -> Dict[str, Any]:
        """通用解析方法"""
        # 简单的关键词匹配
        keywords = {
            "movie": ["电影", "影片", "movie"],
            "tv": ["电视剧", "剧集", "tv", "美剧"],
            "quality": ["4K", "1080p", "720p", "高清", "蓝光"],
            "year": [r"\d{4}年", "今年", "去年"],
            "director": ["导演", "执导"],
            "actor": ["主演", "演员", "出演"]
        }
        
        conditions = []
        rule_type = "unknown"
        
        # 检测媒体类型
        if any(keyword in command for keyword in keywords["movie"]):
            rule_type = "movie"
            conditions.append({
                "field": "type",
                "operator": "equals",
                "value": "movie"
            })
        elif any(keyword in command for keyword in keywords["tv"]):
            rule_type = "tv"
            conditions.append({
                "field": "type",
                "operator": "equals",
                "value": "tv"
            })
        
        # 检测质量要求
        for quality in keywords["quality"]:
            if quality in command:
                conditions.append({
                    "field": "resolution",
                    "operator": "equals",
                    "value": quality
                })
        
        # 检测年份
        year_match = re.search(r'(\d{4})年', command)
        if year_match:
            conditions.append({
                "field": "year",
                "operator": "equals",
                "value": int(year_match.group(1))
            })
        
        # 提取标题关键词
        # 移除已知关键词，剩下的可能是标题
        title_keywords = command
        for category in keywords.values():
            for keyword in category:
                title_keywords = title_keywords.replace(keyword, "")
        
        title_keywords = re.sub(r'[订阅下载关注只要不要排除]+', '', title_keywords).strip()
        
        if title_keywords:
            conditions.append({
                "field": "title",
                "operator": "contains",
                "value": title_keywords
            })
        
        return {
            "original_command": command,
            "parsed_successfully": len(conditions) > 0,
            "rule_type": rule_type,
            "conditions": conditions,
            "actions": [{"type": "download", "action": "auto_download", "priority": "normal"}],
            "confidence": 0.3 if conditions else 0.0,
            "matched_patterns": []
        }
    
    def _calculate_confidence(self, matched_patterns: List[Dict]) -> float:
        """计算解析置信度"""
        if not matched_patterns:
            return 0.0
        
        base_confidence = 0.7
        
        # 根据匹配模式数量调整置信度
        pattern_count = len(matched_patterns)
        if pattern_count >= 3:
            base_confidence = 0.9
        elif pattern_count == 2:
            base_confidence = 0.8
        
        # 根据优先级调整
        high_priority_count = sum(1 for p in matched_patterns if p["priority"] == "high")
        if high_priority_count > 0:
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _generate_conditions(self, matched_patterns: List[Dict]) -> List[Dict]:
        """根据匹配的模式生成条件"""
        conditions = []
        
        for pattern in matched_patterns:
            pattern_type = pattern["pattern_type"]
            matches = pattern["matches"]
            
            if pattern_type == "movie":
                conditions.append({
                    "field": "type",
                    "operator": "equals",
                    "value": "movie"
                })
                
                # 提取电影名称
                if len(matches) >= 2 and matches[1]:
                    conditions.append({
                        "field": "title",
                        "operator": "contains",
                        "value": matches[1].strip()
                    })
            
            elif pattern_type == "tv":
                conditions.append({
                    "field": "type",
                    "operator": "equals",
                    "value": "tv"
                })
                
                # 提取剧集名称
                if len(matches) >= 2 and matches[1]:
                    conditions.append({
                        "field": "title",
                        "operator": "contains",
                        "value": matches[1].strip()
                    })
                
                # 提取季数
                if len(matches) >= 3 and matches[2] and matches[2].isdigit():
                    conditions.append({
                        "field": "season",
                        "operator": "equals",
                        "value": int(matches[2])
                    })
            
            elif pattern_type == "quality":
                # 提取质量要求
                if len(matches) >= 2 and matches[1]:
                    quality_map = {
                        "4K": "4K",
                        "1080p": "1080p", 
                        "720p": "720p",
                        "高清": "1080p",
                        "蓝光": "1080p"
                    }
                    
                    quality = matches[1]
                    if quality in quality_map:
                        conditions.append({
                            "field": "resolution",
                            "operator": "equals",
                            "value": quality_map[quality]
                        })
        
        return conditions
    
    def create_subscription_rule(self, command: str, rule_name: str = "") -> Dict[str, Any]:
        """根据自然语言命令创建订阅规则"""
        parse_result = self.parse_command(command)
        
        if not parse_result["parsed_successfully"]:
            return {
                "success": False,
                "error": "无法解析命令",
                "parse_result": parse_result
            }
        
        # 生成规则名称
        if not rule_name:
            rule_name = f"NLP规则_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 创建规则
        rule = {
            "id": f"nlp_rule_{len(self.rules_history) + 1}",
            "name": rule_name,
            "original_command": command,
            "enabled": True,
            "conditions": parse_result["conditions"],
            "actions": parse_result["actions"],
            "confidence": parse_result["confidence"],
            "created_at": datetime.now().isoformat(),
            "rule_type": parse_result["rule_type"]
        }
        
        # 保存到历史
        self.rules_history.append(rule)
        
        return {
            "success": True,
            "rule": rule,
            "parse_result": parse_result
        }
    
    def get_rules_history(self) -> List[Dict]:
        """获取规则历史"""
        return self.rules_history
    
    def test_commands(self) -> List[Dict]:
        """测试各种命令的解析效果"""
        test_commands = [
            "订阅诺兰的电影",
            "下载2023年的科幻电影",
            "关注4K高清电影",
            "订阅权力的游戏第8季",
            "只要1080p的电影",
            "下载漫威的电影",
            "订阅李安导演的作品",
            "关注汤姆·汉克斯主演的电影",
            "订阅2024年新上映的电影",
            "下载Netflix原创剧集",
            "关注国产悬疑电视剧"
        ]
        
        results = []
        for cmd in test_commands:
            result = self.parse_command(cmd)
            results.append({
                "command": cmd,
                "result": result
            })
        
        return results

# 插件主函数
def main():
    # 示例配置
    config = {
        "min_confidence": 0.5,
        "auto_create_rules": True,
        "max_history_size": 100
    }
    
    plugin = NLPSubscription(config)
    
    # 测试命令解析
    print("=== NLP订阅插件测试 ===")
    
    test_results = plugin.test_commands()
    
    for test in test_results:
        cmd = test["command"]
        result = test["result"]
        
        print(f"\n命令: {cmd}")
        print(f"解析成功: {result['parsed_successfully']}")
        print(f"置信度: {result['confidence']:.2f}")
        print(f"规则类型: {result['rule_type']}")
        print(f"生成条件: {len(result['conditions'])} 个")
        
        if result['conditions']:
            for i, condition in enumerate(result['conditions'], 1):
                print(f"  条件{i}: {condition['field']} {condition['operator']} {condition['value']}")
    
    # 示例：创建订阅规则
    example_command = "订阅诺兰的4K电影"
    creation_result = plugin.create_subscription_rule(example_command, "诺兰4K电影订阅")
    
    if creation_result["success"]:
        print(f"\n✅ 规则创建成功: {creation_result['rule']['name']}")
    else:
        print(f"\n❌ 规则创建失败: {creation_result['error']}")
    
    return plugin

if __name__ == "__main__":
    main()