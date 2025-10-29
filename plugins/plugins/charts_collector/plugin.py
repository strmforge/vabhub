"""
排行榜数据收集器插件主类
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..base import PluginBase
from .providers.apple_music import AppleMusicProvider
from .providers.spotify_charts import SpotifyChartsProvider
from .providers.netflix_top10 import NetflixTop10Provider
from .providers.imdb_datasets import IMDBDatasetsProvider


class ChartsCollectorPlugin(PluginBase):
    """排行榜数据收集器插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "charts_collector"
        self.version = "1.0.0"
        self.description = "排行榜数据收集器，支持 Apple Music、Spotify、Netflix、IMDb"
        self.author = "VabHub Team"
        
        # 数据提供者
        self.providers = {
            "apple_music": AppleMusicProvider(),
            "spotify_charts": SpotifyChartsProvider(),
            "netflix_top10": NetflixTop10Provider(),
            "imdb_datasets": IMDBDatasetsProvider()
        }
        
        # 默认配置
        self.default_config = {
            "collection_interval": 3600,  # 1小时
            "output_dir": "/vol1/charts",
            "providers": {
                "apple_music": {
                    "enabled": True,
                    "country": "us",
                    "limit": 100
                },
                "spotify_charts": {
                    "enabled": True,
                    "region": "global",
                    "chart_kind": "daily"
                },
                "netflix_top10": {
                    "enabled": True
                },
                "imdb_datasets": {
                    "enabled": True,
                    "min_votes": 10000,
                    "top_n": 500
                }
            }
        }
        
        self.is_running = False
        self.collection_task = None
    
    async def on_load(self) -> None:
        """插件加载时调用"""
        self.logger = logging.getLogger(f"plugin.{self.name}")
        
        # 确保配置存在
        if not self.config:
            self.config = self.default_config.copy()
        
        # 创建输出目录
        output_dir = Path(self.config.get("output_dir", "/vol1/charts"))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"排行榜数据收集器插件已加载，输出目录: {output_dir}")
    
    async def on_unload(self) -> None:
        """插件卸载时调用"""
        await self.stop_collection()
        self.logger.info("排行榜数据收集器插件已卸载")
    
    async def start_collection(self) -> None:
        """开始数据收集"""
        if self.is_running:
            return
        
        self.is_running = True
        interval = self.config.get("collection_interval", 3600)
        
        self.collection_task = asyncio.create_task(self._collection_loop(interval))
        self.logger.info(f"排行榜数据收集已启动，间隔: {interval}秒")
    
    async def stop_collection(self) -> None:
        """停止数据收集"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.collection_task:
            self.collection_task.cancel()
            try:
                await self.collection_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("排行榜数据收集已停止")
    
    async def _collection_loop(self, interval: int) -> None:
        """数据收集循环"""
        while self.is_running:
            try:
                await self.collect_all_data()
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"数据收集出错: {e}")
                await asyncio.sleep(60)  # 出错后等待1分钟
    
    async def collect_all_data(self) -> None:
        """收集所有数据源的数据"""
        all_data = []
        
        for provider_name, provider in self.providers.items():
            if not self.config.get("providers", {}).get(provider_name, {}).get("enabled", False):
                continue
            
            try:
                provider_config = self.config["providers"][provider_name]
                data = await provider.fetch_data(provider_config)
                normalized_data = self._normalize_data(data, provider_name)
                all_data.extend(normalized_data)
                
                self.logger.info(f"{provider_name} 数据收集完成: {len(data)} 条记录")
            except Exception as e:
                self.logger.error(f"{provider_name} 数据收集失败: {e}")
        
        # 保存数据
        if all_data:
            await self._save_data(all_data)
    
    def _normalize_data(self, data: List[Dict], source: str) -> List[Dict]:
        """标准化数据格式"""
        normalized = []
        
        for item in data:
            normalized_item = {
                "source": source,
                "region": item.get("region", ""),
                "chart_type": item.get("chart_type", ""),
                "date_or_week": item.get("date_or_week", ""),
                "rank": item.get("rank", 0),
                "title": item.get("title", ""),
                "artist_or_show": item.get("artist_or_show", ""),
                "id_or_url": item.get("id_or_url", ""),
                "metrics": item.get("metrics", {}),
                "search_query": self._build_search_query(item, source),
                "collected_at": datetime.now().isoformat()
            }
            normalized.append(normalized_item)
        
        return normalized
    
    def _build_search_query(self, item: Dict, source: str) -> str:
        """构建搜索查询"""
        if source in ["apple_music", "spotify_charts"]:
            # 音乐: "艺术家 - 歌曲名"
            artist = item.get("artist_or_show", "")
            title = item.get("title", "")
            return f"{artist} - {title}" if artist and title else title
        else:
            # 影视: 直接使用标题
            return item.get("title", "")
    
    async def _save_data(self, data: List[Dict]) -> None:
        """保存数据到文件"""
        output_dir = Path(self.config.get("output_dir", "/vol1/charts"))
        normalized_dir = output_dir / "normalized"
        normalized_dir.mkdir(exist_ok=True)
        
        # 按日期保存
        date_str = datetime.now().strftime("%Y%m%d")
        file_path = normalized_dir / f"charts_normalized_{date_str}.jsonl"
        
        with open(file_path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        
        self.logger.info(f"数据已保存: {file_path} ({len(data)} 条记录)")
    
    async def get_latest_data(self, limit: int = 100) -> List[Dict]:
        """获取最新的排行榜数据"""
        output_dir = Path(self.config.get("output_dir", "/vol1/charts"))
        normalized_dir = output_dir / "normalized"
        
        if not normalized_dir.exists():
            return []
        
        # 找到最新的文件
        jsonl_files = sorted(normalized_dir.glob("charts_normalized_*.jsonl"), reverse=True)
        if not jsonl_files:
            return []
        
        latest_file = jsonl_files[0]
        data = []
        
        try:
            with open(latest_file, "r", encoding="utf-8") as f:
                for line in f:
                    if len(data) >= limit:
                        break
                    try:
                        item = json.loads(line.strip())
                        data.append(item)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            self.logger.error(f"读取数据文件失败: {e}")
        
        return data