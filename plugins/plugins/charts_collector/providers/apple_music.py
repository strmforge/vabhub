"""
Apple Music 排行榜数据提供者
"""

import json
from typing import Dict, List, Any
from .base import BaseProvider


class AppleMusicProvider(BaseProvider):
    """Apple Music 排行榜数据提供者"""
    
    def __init__(self):
        super().__init__()
        self.name = "apple_music"
        self.description = "Apple Music / iTunes 排行榜数据"
    
    async def fetch_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取Apple Music排行榜数据"""
        country = config.get("country", "us")
        limit = config.get("limit", 100)
        
        # Apple Music API URL
        url = f"https://rss.applemarketingtools.com/api/v2/{country}/music/most-played/{limit}/songs.json"
        
        try:
            data = await self._http_get_json(url)
            return self._parse_data(data, country)
        except Exception as e:
            raise Exception(f"获取Apple Music数据失败: {e}")
    
    def _parse_data(self, data: Dict[str, Any], country: str) -> List[Dict[str, Any]]:
        """解析Apple Music数据"""
        results = []
        
        feed = data.get("feed", {})
        chart_data = feed.get("results", [])
        
        for i, item in enumerate(chart_data, 1):
            result = {
                "source": "apple_music",
                "region": country.upper(),
                "chart_type": "most_played_songs",
                "date_or_week": feed.get("updated", ""),
                "rank": i,
                "title": item.get("name", ""),
                "artist_or_show": item.get("artistName", ""),
                "id_or_url": item.get("url", ""),
                "metrics": {
                    "plays": item.get("playCount", 0)
                }
            }
            results.append(result)
        
        return results