"""
音乐订阅插件 - 集成ptmusic-sub v2功能
基于VabHub插件架构的音乐订阅和元数据管理插件
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from ..plugin_base import PluginBase, PluginType
from ..plugin_manager import PluginManager


class MusicSubscriptionPlugin(PluginBase):
    """音乐订阅插件"""
    
    def __init__(self):
        super().__init__()
        self.plugin_name = "music_subscription"
        self.plugin_type = PluginType.MUSIC
        self.plugin_version = "2.0.0"
        self.description = "音乐订阅和元数据管理插件"
        
        self.music_manager = None
        self.subscription_tasks = {}
        
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化插件"""
        try:
            self.config = config
            self.logger = logging.getLogger(f"plugin.{self.plugin_name}")
            
            # 初始化音乐管理器
            from VabHub_Core.core.music_manager import MusicManager
            from VabHub_Core.core.config import ConfigManager
            
            core_config = ConfigManager()
            self.music_manager = MusicManager(core_config)
            await self.music_manager.initialize()
            
            # 启动订阅任务
            await self._start_subscription_tasks()
            
            self.logger.info("音乐订阅插件初始化完成")
            return True
            
        except Exception as e:
            self.logger.error(f"音乐订阅插件初始化失败: {e}")
            return False
    
    async def _start_subscription_tasks(self):
        """启动订阅任务"""
        subscriptions_config = self.config.get('subscriptions', {})
        
        for sub_name, sub_config in subscriptions_config.items():
            if sub_config.get('enabled', True):
                task = asyncio.create_task(self._run_subscription_task(sub_name, sub_config))
                self.subscription_tasks[sub_name] = task
    
    async def _run_subscription_task(self, sub_name: str, sub_config: Dict[str, Any]):
        """运行订阅任务"""
        interval = sub_config.get('interval', 3600)  # 默认1小时
        
        while True:
            try:
                await self._process_subscription(sub_name, sub_config)
                await asyncio.sleep(interval)
            except Exception as e:
                self.logger.error(f"订阅任务 {sub_name} 执行失败: {e}")
                await asyncio.sleep(60)  # 出错后等待1分钟重试
    
    async def _process_subscription(self, sub_name: str, sub_config: Dict[str, Any]):
        """处理单个订阅"""
        self.logger.info(f"开始处理订阅: {sub_name}")
        
        # 执行搜索
        query = sub_config.get('query', '')
        filters = sub_config.get('filters', {})
        
        results = await self.music_manager.search_music(query, filters)
        
        # 应用规则过滤
        filtered_results = self._apply_rules(results, sub_config.get('rules', {}))
        
        # 自动下载（如果启用）
        if sub_config.get('auto_add', False):
            await self._auto_download_torrents(filtered_results, sub_config)
        
        # 保存结果
        await self._save_subscription_results(sub_name, filtered_results)
        
        self.logger.info(f"订阅 {sub_name} 处理完成，找到 {len(filtered_results)} 个结果")
    
    def _apply_rules(self, results: List[Dict], rules: Dict[str, Any]) -> List[Dict]:
        """应用规则过滤"""
        filtered = []
        
        for result in results:
            title = result.get('title', '').lower()
            
            # 包含关键词检查
            include_keywords = rules.get('include_keywords', [])
            if include_keywords:
                if not any(keyword.lower() in title for keyword in include_keywords):
                    continue
            
            # 排除关键词检查
            exclude_keywords = rules.get('exclude_keywords', [])
            if exclude_keywords:
                if any(keyword.lower() in title for keyword in exclude_keywords):
                    continue
            
            # 质量要求检查
            require_quality = rules.get('require_quality', [])
            if require_quality:
                if not any(quality.lower() in title for quality in require_quality):
                    continue
            
            # 拒绝合集检查
            if rules.get('reject_pack', False):
                if any(pack_keyword in title for pack_keyword in ['pack', '合集', 'collection']):
                    continue
            
            filtered.append(result)
        
        # 排序
        prefer_keywords = rules.get('prefer_keywords', [])
        if prefer_keywords:
            filtered.sort(key=lambda x: self._calculate_preference_score(x, prefer_keywords), reverse=True)
        
        return filtered
    
    def _calculate_preference_score(self, result: Dict, prefer_keywords: List[str]) -> int:
        """计算偏好分数"""
        title = result.get('title', '').lower()
        score = 0
        
        for i, keyword in enumerate(prefer_keywords):
            if keyword.lower() in title:
                score += len(prefer_keywords) - i  # 越靠前的关键词权重越高
        
        # 做种人数加分
        seeders = result.get('seeders', 0)
        score += min(seeders // 10, 10)  # 每10个做种者加1分，最多10分
        
        return score
    
    async def _auto_download_torrents(self, results: List[Dict], sub_config: Dict[str, Any]):
        """自动下载种子"""
        max_add = sub_config.get('max_add', 3)
        save_path = sub_config.get('save_path', '/downloads/music')
        
        # 获取下载器插件
        downloader_plugin = await PluginManager.get_plugin('downloader')
        if not downloader_plugin:
            self.logger.warning("未找到下载器插件，跳过自动下载")
            return
        
        # 下载前N个结果
        for i, result in enumerate(results[:max_add]):
            try:
                torrent_url = result.get('link')
                if torrent_url:
                    await downloader_plugin.add_torrent(torrent_url, save_path, category='music')
                    self.logger.info(f"已添加下载: {result.get('title')}")
            except Exception as e:
                self.logger.error(f"下载失败 {result.get('title')}: {e}")
    
    async def _save_subscription_results(self, sub_name: str, results: List[Dict]):
        """保存订阅结果"""
        output_dir = Path(self.config.get('runtime', {}).get('out_dir', '/tmp/ptmusic'))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{sub_name}_results.json"
        
        result_data = {
            'subscription': sub_name,
            'processed_at': asyncio.get_event_loop().time(),
            'results_count': len(results),
            'results': results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    async def enrich_metadata(self, artist: str, title: str) -> Dict[str, Any]:
        """丰富音乐元数据"""
        if not self.music_manager:
            raise RuntimeError("音乐管理器未初始化")
        
        return await self.music_manager.enrich_metadata(artist, title)
    
    async def generate_chart_subscriptions(self, chart_data: List[Dict], top_artists: int = 50) -> List[Dict]:
        """从榜单生成订阅"""
        if not self.music_manager:
            raise RuntimeError("音乐管理器未初始化")
        
        return await self.music_manager.generate_chart_subscriptions(chart_data, top_artists)
    
    async def get_subscription_status(self) -> Dict[str, Any]:
        """获取订阅状态"""
        status = {
            'plugin_name': self.plugin_name,
            'status': 'running',
            'subscription_count': len(self.subscription_tasks),
            'active_tasks': list(self.subscription_tasks.keys()),
            'last_processed': {}
        }
        
        return status
    
    async def stop(self):
        """停止插件"""
        # 取消所有订阅任务
        for task_name, task in self.subscription_tasks.items():
            task.cancel()
        
        # 等待任务完成
        await asyncio.gather(*self.subscription_tasks.values(), return_exceptions=True)
        
        self.logger.info("音乐订阅插件已停止")


# 插件注册
def create_plugin() -> MusicSubscriptionPlugin:
    """创建插件实例"""
    return MusicSubscriptionPlugin()