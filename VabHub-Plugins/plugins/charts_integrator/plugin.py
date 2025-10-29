"""
排行榜自动化集成插件主类
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..base import PluginBase
from .lib.torznab import TorznabClient
from .lib.qb import QBClient
from .lib.naming import build_music_query, build_video_query, guess_is_tv_season


class ChartsIntegratorPlugin(PluginBase):
    """排行榜自动化集成插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "charts_integrator"
        self.version = "1.0.0"
        self.description = "排行榜自动化集成，支持 Jackett/Prowlarr 和 qBittorrent"
        self.author = "VabHub Team"
        
        # 默认配置
        self.default_config = {
            "enabled": False,
            "integration_interval": 3600,  # 1小时
            "collector": {
                "normalized_dir": "/vol1/charts/normalized"
            },
            "work_dirs": {
                "out_dir": "/vol1/charts/integrations/out",
                "state_dir": "/vol1/charts/integrations/state"
            },
            "torznab": {
                "endpoints": [
                    "http://jackett:9117/api/v2.0/indexers/all/results/torznab/api?apikey=REPLACE"
                ],
                "timeout": 20
            },
            "qbittorrent": {
                "base_url": "http://127.0.0.1:8080",
                "username": "admin",
                "password": "adminadmin"
            },
            "rules": {
                "music": {
                    "max_rank": 50,
                    "torznab_category": 3000
                },
                "video": {
                    "netflix_max_rank": 10,
                    "imdb_top_k": 100,
                    "torznab_category": 2000,
                    "prefer_keywords": ["2160p", "1080p", "WEB-DL", "WEBRip", "BluRay", "x265", "HEVC"]
                }
            },
            "auto_add": False,
            "music": {
                "save_path": "/vol02/incoming/music",
                "qb_category": "music"
            },
            "video": {
                "save_path_movies": "/vol02/incoming/movies",
                "save_path_tv": "/vol02/incoming/tv",
                "qb_category_movies": "movies",
                "qb_category_tv": "tv"
            }
        }
        
        self.torznab_client = None
        self.qb_client = None
        self.is_running = False
        self.integration_task = None
    
    async def on_load(self) -> None:
        """插件加载时调用"""
        self.logger = logging.getLogger(f"plugin.{self.name}")
        
        # 确保配置存在
        if not self.config:
            self.config = self.default_config.copy()
        
        # 初始化客户端
        await self._init_clients()
        
        self.logger.info("排行榜集成插件已加载")
    
    async def on_unload(self) -> None:
        """插件卸载时调用"""
        await self.stop_integration()
        self.logger.info("排行榜集成插件已卸载")
    
    async def _init_clients(self) -> None:
        """初始化客户端"""
        try:
            # 初始化 Torznab 客户端
            endpoints = self.config.get("torznab", {}).get("endpoints", [])
            timeout = self.config.get("torznab", {}).get("timeout", 20)
            
            if endpoints:
                self.torznab_client = TorznabClient(endpoints, timeout)
                self.logger.info("Torznab 客户端已初始化")
            
            # 初始化 qBittorrent 客户端
            qb_config = self.config.get("qbittorrent", {})
            if qb_config.get("base_url"):
                self.qb_client = QBClient(
                    base_url=qb_config["base_url"],
                    username=qb_config.get("username", "admin"),
                    password=qb_config.get("password", "adminadmin")
                )
                self.logger.info("qBittorrent 客户端已初始化")
                
        except Exception as e:
            self.logger.error(f"初始化客户端失败: {e}")
    
    async def start_integration(self) -> None:
        """开始集成任务"""
        if self.is_running:
            return
        
        self.is_running = True
        interval = self.config.get("integration_interval", 3600)
        
        self.integration_task = asyncio.create_task(self._integration_loop(interval))
        self.logger.info(f"排行榜集成任务已启动，间隔: {interval}秒")
    
    async def stop_integration(self) -> None:
        """停止集成任务"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.integration_task:
            self.integration_task.cancel()
            try:
                await self.integration_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("排行榜集成任务已停止")
    
    async def _integration_loop(self, interval: int) -> None:
        """集成任务循环"""
        while self.is_running:
            try:
                await self.run_integration()
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"集成任务出错: {e}")
                await asyncio.sleep(60)  # 出错后等待1分钟
    
    async def run_integration(self) -> None:
        """执行一次集成任务"""
        if not self.config.get("enabled", False):
            return
        
        # 读取最新的标准化数据
        normalized_dir = self.config.get("collector", {}).get("normalized_dir", "/vol1/charts/normalized")
        rows = self._read_latest_normalized(normalized_dir)
        
        if not rows:
            self.logger.warning("没有找到可用的排行榜数据")
            return
        
        # 筛选候选内容
        music_candidates, video_candidates = self._select_candidates(rows, self.config.get("rules", {}))
        
        # 搜索和下载
        if self.torznab_client and self.qb_client:
            await self._search_and_download(music_candidates, video_candidates)
        
        self.logger.info(f"集成任务完成: 音乐候选 {len(music_candidates)} 个, 视频候选 {len(video_candidates)} 个")
    
    def _read_latest_normalized(self, normalized_dir: str) -> List[Dict[str, Any]]:
        """读取最新的标准化数据"""
        import glob
        
        if not os.path.exists(normalized_dir):
            return []
        
        # 找到最新的文件
        files = sorted(glob.glob(os.path.join(normalized_dir, "charts_normalized_*.jsonl")), reverse=True)
        if not files:
            return []
        
        rows = []
        latest_file = files[0]
        
        try:
            with open(latest_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        row = json.loads(line.strip())
                        rows.append(row)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            self.logger.error(f"读取数据文件失败: {e}")
        
        return rows
    
    def _select_candidates(self, rows: List[Dict], rules: Dict) -> tuple:
        """筛选候选内容"""
        music, video = [], []
        
        for row in rows:
            source = row.get("source")
            rank = row.get("rank", 0)
            
            if source in ["apple_music", "spotify_charts"]:
                # 音乐候选
                if rank <= rules.get("music", {}).get("max_rank", 50):
                    music.append(row)
            elif source == "netflix_top10":
                # Netflix 候选
                if rank <= rules.get("video", {}).get("netflix_max_rank", 10):
                    video.append(row)
            elif source == "imdb_datasets":
                # IMDb 候选
                if rank <= rules.get("video", {}).get("imdb_top_k", 100):
                    video.append(row)
        
        return music, video
    
    async def _search_and_download(self, music_candidates: List[Dict], video_candidates: List[Dict]) -> None:
        """搜索和下载候选内容"""
        auto_add = self.config.get("auto_add", False)
        out_dir = self.config.get("work_dirs", {}).get("out_dir", "/vol1/charts/integrations/out")
        
        # 确保输出目录存在
        os.makedirs(out_dir, exist_ok=True)
        
        added_count = 0
        
        # 处理音乐候选
        for candidate in music_candidates:
            try:
                query = candidate.get("search_query", "")
                if not query:
                    continue
                
                # 搜索资源
                results = await self.torznab_client.search(
                    query, 
                    category=self.config["rules"]["music"]["torznab_category"],
                    limit=5
                )
                
                if results:
                    # 选择最佳结果
                    best_result = max(results, key=lambda x: x.get("Seeders", 0))
                    
                    if auto_add:
                        # 自动添加到下载器
                        await self.qb_client.add_by_url(
                            best_result["Link"],
                            save_path=self.config["music"]["save_path"],
                            category=self.config["music"]["qb_category"]
                        )
                        added_count += 1
                        self.logger.info(f"已添加音乐下载: {query}")
                    
                    # 记录到文件
                    self._log_candidate(out_dir, "music", candidate, best_result)
                    
            except Exception as e:
                self.logger.error(f"处理音乐候选失败: {e}")
        
        # 处理视频候选
        for candidate in video_candidates:
            try:
                query = candidate.get("search_query", "")
                if not query:
                    continue
                
                # 搜索资源
                results = await self.torznab_client.search(
                    query,
                    category=self.config["rules"]["video"]["torznab_category"],
                    limit=5
                )
                
                if results:
                    # 选择最佳结果
                    best_result = max(results, key=lambda x: x.get("Seeders", 0))
                    
                    if auto_add:
                        # 判断是电影还是电视剧
                        is_tv = guess_is_tv_season(query)
                        
                        if is_tv:
                            save_path = self.config["video"]["save_path_tv"]
                            category = self.config["video"]["qb_category_tv"]
                        else:
                            save_path = self.config["video"]["save_path_movies"]
                            category = self.config["video"]["qb_category_movies"]
                        
                        await self.qb_client.add_by_url(
                            best_result["Link"],
                            save_path=save_path,
                            category=category
                        )
                        added_count += 1
                        self.logger.info(f"已添加视频下载: {query}")
                    
                    # 记录到文件
                    self._log_candidate(out_dir, "video", candidate, best_result)
                    
            except Exception as e:
                self.logger.error(f"处理视频候选失败: {e}")
        
        if added_count > 0:
            self.logger.info(f"本次集成任务添加了 {added_count} 个下载任务")
    
    def _log_candidate(self, out_dir: str, candidate_type: str, candidate: Dict, result: Dict) -> None:
        """记录候选内容到文件"""
        import csv
        
        file_path = os.path.join(out_dir, f"candidates_{candidate_type}.tsv")
        file_exists = os.path.exists(file_path)
        
        with open(file_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            
            if not file_exists:
                # 写入表头
                writer.writerow([
                    "rank", "source", "artist", "title", "query",
                    "result_title", "seeders", "size", "link"
                ])
            
            writer.writerow([
                candidate.get("rank", ""),
                candidate.get("source", ""),
                candidate.get("artist_or_show", ""),
                candidate.get("title", ""),
                candidate.get("search_query", ""),
                result.get("Title", ""),
                result.get("Seeders", ""),
                result.get("Size", ""),
                result.get("Link", "")
            ])