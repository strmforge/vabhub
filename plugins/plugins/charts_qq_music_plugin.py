"""
QQ音乐排行榜数据源插件
提供QQ音乐热歌榜、新歌榜、飙升榜等榜单数据
"""

import json
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime

from .charts_base import MusicDataSourcePlugin


class QQMusicChartsPlugin(MusicDataSourcePlugin):
    """QQ音乐排行榜数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "qq_music_charts"
        self.version = "1.0.0"
        self.description = "QQ音乐排行榜数据源"
        self.author = "VabHub Team"
        
        # QQ音乐API配置
        self.api_base = "https://c.y.qq.com"
        self.charts_endpoints = {
            "hot_songs": "/v8/fcg-bin/fcg_v8_toplist_cp.fcg",  # 热歌榜
            "new_songs": "/v8/fcg-bin/fcg_v8_toplist_cp.fcg",  # 新歌榜
            "rising_songs": "/v8/fcg-bin/fcg_v8_toplist_cp.fcg",  # 飙升榜
        }
    
    def initialize(self) -> bool:
        """初始化插件"""
        try:
            # 检查配置
            if not self.config.get("api_key"):
                self.logger.warning("QQ音乐API密钥未配置")
                return False
            
            self.logger.info("🎵 QQ音乐排行榜插件初始化完成")
            self.initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"QQ音乐插件初始化失败: {e}")
            return False
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行排行榜数据获取"""
        
        chart_type = data.get("chart_type", "hot_songs")
        limit = data.get("limit", 50)
        
        try:
            charts_data = await self._fetch_qq_music_charts(chart_type, limit)
            
            return {
                "success": True,
                "chart_type": chart_type,
                "data": charts_data,
                "timestamp": datetime.now().isoformat(),
                "source": "qq_music"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chart_type": chart_type,
                "source": "qq_music"
            }
    
    async def _fetch_qq_music_charts(self, chart_type: str, limit: int) -> List[Dict[str, Any]]:
        """获取QQ音乐排行榜数据"""
        
        # 不同榜单的topid参数
        topid_mapping = {
            "hot_songs": 26,  # 热歌榜
            "new_songs": 27,  # 新歌榜
            "rising_songs": 62,  # 飙升榜
        }
        
        topid = topid_mapping.get(chart_type, 26)
        
        params = {
            "topid": topid,
            "format": "json",
            "g_tk": self.config.get("api_key", ""),
            "uin": "0",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "h5",
            "needNewCode": 1,
            "type": "top",
            "page": "detail",
            "tpl": 3
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "Referer": "https://y.qq.com/"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_base}/v8/fcg-bin/fcg_v8_toplist_cp.fcg", 
                                      params=params, headers=headers)
            response.raise_for_status()
            
            chart_data = response.json()
            song_list = chart_data.get("songlist", [])[:limit]
            
            return [self._parse_song_data(song) for song in song_list]
    
    def _parse_song_data(self, song_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析歌曲数据"""
        
        song_info = song_data.get("data", {})
        
        artists = [artist["name"] for artist in song_info.get("singer", [])]
        album = song_info.get("album", {})
        
        return {
            "id": song_info.get("songid"),
            "mid": song_info.get("songmid"),
            "title": song_info.get("songname"),
            "artists": artists,
            "album": album.get("name"),
            "album_id": album.get("albummid"),
            "duration": song_info.get("interval"),  # 秒
            "popularity": song_data.get("cur_count", 0),
            "external_url": f"https://y.qq.com/n/ryqq/song/{song_info.get('songmid')}",
            "thumbnail_url": f"https://y.gtimg.cn/music/photo_new/T002R300x300M000{album.get('albummid')}.jpg" if album.get("albummid") else None
        }
    
    def get_supported_charts(self) -> List[Dict[str, Any]]:
        """获取支持的榜单类型"""
        
        return [
            {
                "id": "hot_songs",
                "name": "热歌榜",
                "description": "QQ音乐热歌榜",
                "limit": 100
            },
            {
                "id": "new_songs",
                "name": "新歌榜",
                "description": "QQ音乐新歌榜",
                "limit": 100
            },
            {
                "id": "rising_songs",
                "name": "飙升榜",
                "description": "QQ音乐飙升榜",
                "limit": 100
            }
        ]
    
    async def get_track_info(self, track_id: str) -> Optional[Dict[str, Any]]:
        """获取歌曲详细信息"""
        
        try:
            params = {
                "songmid": track_id,
                "format": "json",
                "g_tk": self.config.get("api_key", ""),
                "uin": "0",
                "inCharset": "utf-8",
                "outCharset": "utf-8",
                "notice": 0,
                "platform": "h5",
                "needNewCode": 1
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                "Referer": "https://y.qq.com/"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base}/v8/fcg-bin/fcg_play_single_song.fcg", 
                                          params=params, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                if data.get("code") == 0:
                    song_data = data.get("data", [{}])[0]
                    return self._parse_song_data({"data": song_data})
                
        except Exception as e:
            self.logger.error(f"获取歌曲信息失败: {e}")
        
        return None
    
    async def search_tracks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索歌曲"""
        
        try:
            params = {
                "w": query,
                "format": "json",
                "g_tk": self.config.get("api_key", ""),
                "uin": "0",
                "inCharset": "utf-8",
                "outCharset": "utf-8",
                "notice": 0,
                "platform": "h5",
                "needNewCode": 1,
                "catZhida": 1,
                "t": 0,
                "flag": 1,
                "ie": "utf-8",
                "sem": 1,
                "aggr": 0,
                "perpage": limit,
                "n": limit,
                "p": 1,
                "remoteplace": "txt.mqq.all"
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                "Referer": "https://y.qq.com/"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base}/soso/fcgi-bin/client_search_cp", 
                                          params=params, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                songs = data.get("data", {}).get("song", {}).get("list", [])
                
                return [self._parse_song_data({"data": song}) for song in songs]
                
        except Exception as e:
            self.logger.error(f"搜索歌曲失败: {e}")
            return []
    
    def cleanup(self):
        """清理资源"""
        self.logger.info("🧹 清理QQ音乐排行榜插件资源")