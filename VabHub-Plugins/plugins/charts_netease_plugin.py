"""
网易云音乐排行榜数据源插件
提供网易云音乐热歌榜、新歌榜、原创榜等榜单数据
"""

import json
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime

from .charts_base import MusicDataSourcePlugin


class NeteaseChartsPlugin(MusicDataSourcePlugin):
    """网易云音乐排行榜数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "netease_charts"
        self.version = "1.0.0"
        self.description = "网易云音乐排行榜数据源"
        self.author = "VabHub Team"
        
        # 网易云音乐API配置
        self.api_base = "https://music.163.com/api"
        self.charts_endpoints = {
            "hot_songs": "/playlist/detail",  # 热歌榜
            "new_songs": "/top/list",  # 新歌榜
            "original": "/toplist/artist",  # 原创榜
            "billboard": "/toplist/detail"  # 排行榜详情
        }
    
    def initialize(self) -> bool:
        """初始化插件"""
        try:
            # 检查配置
            if not self.config.get("cookie"):
                self.logger.warning("网易云音乐Cookie未配置")
                return False
            
            self.logger.info("🎵 网易云音乐排行榜插件初始化完成")
            self.initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"网易云音乐插件初始化失败: {e}")
            return False
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行排行榜数据获取"""
        
        chart_type = data.get("chart_type", "hot_songs")
        limit = data.get("limit", 50)
        
        try:
            charts_data = await self._fetch_netease_charts(chart_type, limit)
            
            return {
                "success": True,
                "chart_type": chart_type,
                "data": charts_data,
                "timestamp": datetime.now().isoformat(),
                "source": "netease"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chart_type": chart_type,
                "source": "netease"
            }
    
    async def _fetch_netease_charts(self, chart_type: str, limit: int) -> List[Dict[str, Any]]:
        """获取网易云音乐排行榜数据"""
        
        headers = {
            "Cookie": self.config.get("cookie", ""),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        async with httpx.AsyncClient() as client:
            if chart_type == "hot_songs":
                # 热歌榜 - 官方热歌榜ID: 3778678
                params = {"id": 3778678}
                response = await client.get(f"{self.api_base}/playlist/detail", 
                                          params=params, headers=headers)
                response.raise_for_status()
                
                playlist_data = response.json()
                tracks = playlist_data.get("playlist", {}).get("tracks", [])[:limit]
                
                return [self._parse_track_data(track) for track in tracks]
                
            elif chart_type == "new_songs":
                # 新歌榜
                params = {"idx": 0, "limit": limit}
                response = await client.get(f"{self.api_base}/top/list", 
                                          params=params, headers=headers)
                response.raise_for_status()
                
                top_data = response.json()
                tracks = top_data.get("playlist", {}).get("tracks", [])[:limit]
                
                return [self._parse_track_data(track) for track in tracks]
                
            elif chart_type == "original":
                # 原创榜
                response = await client.get(f"{self.api_base}/toplist/artist", 
                                          headers=headers)
                response.raise_for_status()
                
                artist_data = response.json()
                artists = artist_data.get("list", {}).get("artists", [])[:limit]
                
                return [self._parse_artist_data(artist) for artist in artists]
    
    def _parse_track_data(self, track_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析歌曲数据"""
        
        artists = [artist["name"] for artist in track_data.get("ar", [])]
        album = track_data.get("al", {})
        
        return {
            "id": track_data.get("id"),
            "title": track_data.get("name"),
            "artists": artists,
            "album": album.get("name"),
            "duration": track_data.get("dt"),  # 毫秒
            "popularity": track_data.get("pop", 0),
            "external_url": f"https://music.163.com/song?id={track_data.get('id')}",
            "thumbnail_url": album.get("picUrl") if album else None
        }
    
    def _parse_artist_data(self, artist_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析艺术家数据"""
        
        return {
            "id": artist_data.get("id"),
            "name": artist_data.get("name"),
            "popularity": artist_data.get("score", 0),
            "thumbnail_url": artist_data.get("picUrl"),
            "external_url": f"https://music.163.com/artist?id={artist_data.get('id')}"
        }
    
    def get_supported_charts(self) -> List[Dict[str, Any]]:
        """获取支持的榜单类型"""
        
        return [
            {
                "id": "hot_songs",
                "name": "热歌榜",
                "description": "网易云音乐官方热歌榜",
                "limit": 100
            },
            {
                "id": "new_songs",
                "name": "新歌榜",
                "description": "最新发布的歌曲榜单",
                "limit": 50
            },
            {
                "id": "original",
                "name": "原创榜",
                "description": "原创音乐人榜单",
                "limit": 30
            }
        ]
    
    async def get_track_info(self, track_id: str) -> Optional[Dict[str, Any]]:
        """获取歌曲详细信息"""
        
        try:
            headers = {
                "Cookie": self.config.get("cookie", ""),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base}/song/detail", 
                                          params={"ids": track_id}, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                songs = data.get("songs", [])
                if songs:
                    return self._parse_track_data(songs[0])
                
        except Exception as e:
            self.logger.error(f"获取歌曲信息失败: {e}")
        
        return None
    
    async def search_tracks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索歌曲"""
        
        try:
            headers = {
                "Cookie": self.config.get("cookie", ""),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            params = {
                "keywords": query,
                "type": 1,  # 歌曲类型
                "limit": limit
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base}/search/get", 
                                          params=params, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                songs = data.get("result", {}).get("songs", [])
                
                return [self._parse_track_data(song) for song in songs]
                
        except Exception as e:
            self.logger.error(f"搜索歌曲失败: {e}")
            return []
    
    def cleanup(self):
        """清理资源"""
        self.logger.info("🧹 清理网易云音乐排行榜插件资源")