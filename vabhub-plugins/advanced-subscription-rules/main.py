#!/usr/bin/env python3
"""
高级订阅规则插件
提供类似MoviePilot的高级订阅功能
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class AdvancedSubscriptionRules:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rules = []
        self.load_rules()
    
    def load_rules(self):
        """加载订阅规则"""
        try:
            with open('subscription_rules.json', 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
        except FileNotFoundError:
            self.rules = []
    
    def save_rules(self):
        """保存订阅规则"""
        with open('subscription_rules.json', 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=2)
    
    def create_rule(self, name: str, conditions: List[Dict], actions: List[Dict]) -> Dict:
        """创建新规则"""
        rule = {
            "id": f"rule_{len(self.rules) + 1}",
            "name": name,
            "enabled": True,
            "conditions": conditions,
            "actions": actions,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.rules.append(rule)
        self.save_rules()
        return rule
    
    def evaluate_media(self, media_info: Dict[str, Any]) -> List[Dict]:
        """评估媒体是否符合订阅规则"""
        matched_rules = []
        
        for rule in self.rules:
            if not rule.get('enabled', True):
                continue
            
            if self._evaluate_conditions(rule['conditions'], media_info):
                matched_rules.append({
                    'rule_id': rule['id'],
                    'rule_name': rule['name'],
                    'actions': rule['actions']
                })
        
        return matched_rules
    
    def _evaluate_conditions(self, conditions: List[Dict], media_info: Dict) -> bool:
        """评估条件组合"""
        if not conditions:
            return True
        
        for condition in conditions:
            if not self._evaluate_single_condition(condition, media_info):
                return False
        
        return True
    
    def _evaluate_single_condition(self, condition: Dict, media_info: Dict) -> bool:
        """评估单个条件"""
        condition_type = condition.get('type')
        field = condition.get('field')
        operator = condition.get('operator')
        value = condition.get('value')
        
        if field not in media_info:
            return False
        
        actual_value = media_info[field]
        
        if operator == 'equals':
            return str(actual_value) == str(value)
        elif operator == 'contains':
            return str(value).lower() in str(actual_value).lower()
        elif operator == 'regex':
            return bool(re.search(value, str(actual_value)))
        elif operator == 'greater_than':
            try:
                return float(actual_value) > float(value)
            except (ValueError, TypeError):
                return False
        elif operator == 'less_than':
            try:
                return float(actual_value) < float(value)
            except (ValueError, TypeError):
                return False
        elif operator == 'in_list':
            return str(actual_value) in [str(v) for v in value]
        
        return False
    
    def get_rules(self) -> List[Dict]:
        """获取所有规则"""
        return self.rules
    
    def update_rule(self, rule_id: str, updates: Dict) -> bool:
        """更新规则"""
        for rule in self.rules:
            if rule['id'] == rule_id:
                rule.update(updates)
                rule['updated_at'] = datetime.now().isoformat()
                self.save_rules()
                return True
        return False
    
    def delete_rule(self, rule_id: str) -> bool:
        """删除规则"""
        self.rules = [rule for rule in self.rules if rule['id'] != rule_id]
        self.save_rules()
        return True

# 插件主函数
def main():
    # 示例配置
    config = {
        "auto_scan": True,
        "max_rules": 100,
        "log_level": "info"
    }
    
    plugin = AdvancedSubscriptionRules(config)
    
    # 示例：创建订阅规则
    example_rule = plugin.create_rule(
        name="高质量电影订阅",
        conditions=[
            {
                "type": "media",
                "field": "type",
                "operator": "equals",
                "value": "movie"
            },
            {
                "type": "quality",
                "field": "resolution",
                "operator": "equals",
                "value": "1080p"
            },
            {
                "type": "rating",
                "field": "rating",
                "operator": "greater_than",
                "value": 7.0
            }
        ],
        actions=[
            {
                "type": "download",
                "action": "auto_download",
                "priority": "high"
            }
        ]
    )
    
    print(f"创建规则: {example_rule['name']}")
    
    # 示例：评估媒体
    test_media = {
        "type": "movie",
        "title": "Inception",
        "resolution": "1080p",
        "rating": 8.8,
        "year": 2010
    }
    
    matched = plugin.evaluate_media(test_media)
    print(f"匹配规则数量: {len(matched)}")
    
    return plugin

if __name__ == "__main__":
    main()