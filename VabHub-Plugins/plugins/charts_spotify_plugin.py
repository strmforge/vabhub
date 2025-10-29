"""
Spotify排行榜数据源插件
提供Spotify全球Top 50、新歌榜、流派榜等榜单数据
"""

import json
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime

from .charts_base import DataSourcePlugin, MusicDataSourcePlugin


class SpotifyChartsPlugin(MusicDataSourcePlugin):
    """Spotify排行榜数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "spotify_charts"
        self.version = "1.0.0"
        self.description = "Spotify音乐排行榜数据源"
        self.author = "VabHub Team"
        
        # Spotify API配置
        self.api_base = "https://api.spotify.com/v1"
        self.charts_endpoints = {
            "global_top_50": "/playlists/37i9dQZEVXbMDoHDwVN2tF",  # 全球Top 50
            "new_releases": "/browse/new-releases",  # 新歌榜
            "top_hits": "/playlists/37i9dQZEVXbLRQDuF5jeBp",  # 热门歌曲
        }
    
    def initialize(self) -> bool:
        """初始化插件"""
        try:
            # 检查配置
            if not self.config.get("api_key"):
                self.logger.warning("Spotify API密钥未配置")
                return False
            
            self.logger.info("🎵 Spotify排行榜插件初始化完成")
            return True
            
        except Exception as e:
            self.logger.error(f"Spotify插件初始化失败: {e}")
            return False
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行排行榜数据获取"""
        
        chart_type = data.get("chart_type", "global_top_50")
        limit = data.get("limit", 50)
        
        try:
            charts_data = await self._fetch_spotify_charts(chart_type, limit)
            
            return {
                "success": True,
                "chart_type": chart_type,
                "data": charts_data,
                "timestamp": datetime.now().isoformat(),
                "source": "spotify"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chart_type": chart_type,
                "source": "spotify"
            }
    
    async def _fetch_spotify_charts(self, chart_type: str, limit: int) -> List[Dict[str, Any]]:
        """获取Spotify排行榜数据"""
        
        endpoint = self.charts_endpoints.get(chart_type)
        if not endpoint:
            raise ValueError(f"不支持的榜单类型: {chart_type}")
        
        headers = {
            "Authorization": f"Bearer {self.config.get('api_key')}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            if "playlists" in endpoint:
                # 获取播放列表详情
                response = await client.get(f"{self.api_base}{endpoint}", headers=headers)
                response.raise_for_status()
                
                playlist_data = response.json()
                tracks = playlist_data.get("tracks", {}).get("items", [])[:limit]
                
                return [self._parse_track_data(track["track"]) for track in tracks if track.get("track")]
                
            elif "new-releases" in endpoint:
                # 获取新歌榜
                response = await client.get(f"{self.api_base}{endpoint}?limit={limit}", headers=headers)
                response.raise_for_status()
                
                new_releases = response.json().get("albums", {}).get("items", [])
                
                return [self._parse_album_data(album) for album in new_releases]
    
    def _parse_track_data(self, track_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析歌曲数据"""
        
        artists = [artist["name"] for artist in track_data.get("artists", [])]
        
        return {
            "id": track_data.get("id"),
            "title": track_data.get("name"),
            "artists": artists,
            "album": track_data.get("album", {}).get("name"),
            "duration_ms": track_data.get("duration_ms"),
            "popularity": track_data.get("popularity", 0),
            "preview_url": track_data.get("preview_url"),
            "external_url": track_data.get("external_urls", {}).get("spotify"),
            "thumbnail_url": track_data.get("album", {}).get("images", [{}])[0].get("url") if track_data.get("album", {}).get("images") else None
        }
    
    def _parse_album_data(self, album_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析专辑数据"""
        
        artists = [artist["name"] for artist in album_data.get("artists", [])]
        
        return {
            "id": album_data.get("id"),
            "title": album_data.get("name"),
            "artists": artists,
            "release_date": album_data.get("release_date"),
            "total_tracks": album_data.get("total_tracks"),
            "external_url": album_data.get("external_urls", {}).get("spotify"),
            "thumbnail_url": album_data.get("images", [{}])[0].get("url") if album_data.get("images") else None
        }
    
    def get_supported_charts(self) -> List[Dict[str, Any]]:
        """获取支持的榜单类型"""
        
        return [
            {
                "id": "global_top_50",
                "name": "全球Top 50",
                "description": "Spotify全球热门歌曲Top 50",
                "limit": 50
            },
            {
                "id": "new_releases",
                "name": "新歌榜",
                "description": "最新发布的音乐专辑",
                "limit": 20
            },
            {
                "id": "top_hits",
                "name": "热门歌曲",
                "description": "当前热门歌曲榜单",
                "limit": 100
            }
        ]
    
    def cleanup(self):
        """清理资源"""
        self.logger.info("🧹 清理Spotify排行榜插件资源")