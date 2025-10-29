"""
Spotify Charts 数据提供者
"""

import csv
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any
from .base import BaseProvider


class SpotifyChartsProvider(BaseProvider):
    """Spotify Charts 数据提供者"""
    
    def __init__(self):
        super().__init__()
        self.name = "spotify_charts"
        self.description = "Spotify Charts CSV数据"
    
    async def fetch_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取Spotify Charts数据"""
        region = config.get("region", "global")
        chart_kind = config.get("chart_kind", "daily")
        lookback_days = config.get("lookback_days", 7)
        
        # 尝试获取最近几天的数据
        for days_back in range(lookback_days):
            date = datetime.now() - timedelta(days=days_back)
            date_str = date.strftime("%Y-%m-%d")
            
            try:
                url = f"https://spotifycharts.com/regional/{region}/{chart_kind}/{date_str}/download"
                csv_data = await self._http_get(url)
                return self._parse_csv_data(csv_data, region, chart_kind, date_str)
            except Exception:
                continue
        
        raise Exception(f"无法获取最近{lookback_days}天的Spotify Charts数据")
    
    def _parse_csv_data(self, csv_data: str, region: str, chart_kind: str, date_str: str) -> List[Dict[str, Any]]:
        """解析CSV数据"""
        results = []
        
        # 跳过标题行
        lines = csv_data.strip().split('\n')[1:]
        
        reader = csv.reader(io.StringIO('\n'.join(lines)))
        
        for i, row in enumerate(reader, 1):
            if len(row) < 5:
                continue
            
            result = {
                "source": "spotify_charts",
                "region": region.upper(),
                "chart_type": f"{chart_kind}_top",
                "date_or_week": date_str,
                "rank": i,
                "title": row[1].strip('"'),  # 歌曲名
                "artist_or_show": row[2].strip('"'),  # 艺术家
                "id_or_url": row[0].strip('"'),  # Spotify ID
                "metrics": {
                    "streams": int(row[3]) if row[3].isdigit() else 0
                }
            }
            results.append(result)
        
        return results