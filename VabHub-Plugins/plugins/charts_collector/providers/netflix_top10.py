"""
Netflix Top 10 数据提供者
"""

import pandas as pd
from typing import Dict, List, Any
from .base import BaseProvider


class NetflixTop10Provider(BaseProvider):
    """Netflix Top 10 数据提供者"""
    
    def __init__(self):
        super().__init__()
        self.name = "netflix_top10"
        self.description = "Netflix Top 10 排行榜数据"
    
    async def fetch_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取Netflix Top 10数据"""
        url = config.get("all_weeks_url", "https://www.netflix.com/tudum/top10/data/all-weeks-global.xlsx")
        
        try:
            # 下载Excel文件
            excel_data = await self._http_get(url)
            
            # 使用pandas解析Excel
            import io
            df = pd.read_excel(io.BytesIO(excel_data.encode('utf-8')))
            
            return self._parse_excel_data(df)
        except Exception as e:
            raise Exception(f"获取Netflix Top 10数据失败: {e}")
    
    def _parse_excel_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """解析Excel数据"""
        results = []
        
        # 获取最新一周的数据
        latest_week = df['week'].max()
        latest_data = df[df['week'] == latest_week]
        
        for _, row in latest_data.iterrows():
            result = {
                "source": "netflix_top10",
                "region": "global",
                "chart_type": "top_10",
                "date_or_week": str(latest_week),
                "rank": int(row.get('rank', 0)),
                "title": row.get('show_title', row.get('movie_title', '')),
                "artist_or_show": row.get('category', ''),
                "id_or_url": "",
                "metrics": {
                    "weekly_hours_viewed": int(row.get('weekly_hours_viewed', 0)),
                    "cumulative_weeks_in_top_10": int(row.get('cumulative_weeks_in_top_10', 0))
                }
            }
            results.append(result)
        
        return results