"""
排行榜演示数据源插件
在没有配置真实API密钥时提供演示数据
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random

from .charts_base import DataSourcePlugin, MusicDataSourcePlugin, MovieDataSourcePlugin, TVDataSourcePlugin


class DemoChartsPlugin(DataSourcePlugin):
    """排行榜演示数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "demo_charts"
        self.version = "1.0.0"
        self.description = "排行榜演示数据源（无需API密钥）"
        self.author = "VabHub Team"
        
        # 演示数据缓存
        self.demo_data = {}
        
    def initialize(self) -> bool:
        """初始化插件"""
        try:
            # 生成演示数据
            self._generate_demo_data()
            self.logger.info("🎯 排行榜演示插件初始化完成")
            return True
            
        except Exception as e:
            self.logger.error(f"演示插件初始化失败: {e}")
            return False
    
    def _generate_demo_data(self):
        """生成演示数据"""
        
        # 音乐演示数据
        self.demo_data["music"] = {
            "global_top_50": self._generate_music_data(50, "全球Top 50"),
            "new_releases": self._generate_music_data(20, "新歌榜"),
            "hot_songs": self._generate_music_data(100, "热门歌曲")
        }
        
        # 电影演示数据
        self.demo_data["movie"] = {
            "trending_movies": self._generate_movie_data(20, "热门电影"),
            "popular_movies": self._generate_movie_data(20, "流行电影"),
            "top_rated_movies": self._generate_movie_data(20, "高分电影")
        }
        
        # 电视剧演示数据
        self.demo_data["tv"] = {
            "trending_tv": self._generate_tv_data(20, "热门电视剧"),
            "popular_tv": self._generate_tv_data(20, "流行电视剧")
        }
    
    def _generate_music_data(self, count: int, chart_name: str) -> List[Dict]:
        """生成音乐演示数据"""
        
        # 热门歌曲列表（演示用）
        songs = [
            "Blinding Lights", "Shape of You", "Dance Monkey", "Bad Guy", "Levitating",
            "Stay", "Flowers", "As It Was", "Heat Waves", "Blinding Lights",
            "Good 4 U", "Save Your Tears", "Don't Start Now", "Watermelon Sugar",
            "drivers license", "Montero", "Peaches", "Butter", "Stay", "Industry Baby"
        ]
        
        artists = [
            "The Weeknd", "Ed Sheeran", "Tones and I", "Billie Eilish", "Dua Lipa",
            "The Kid LAROI & Justin Bieber", "Miley Cyrus", "Harry Styles",
            "Glass Animals", "Olivia Rodrigo", "Ariana Grande", "Doja Cat",
            "Justin Bieber", "BTS", "Lil Nas X", "Jack Harlow"
        ]
        
        data = []
        for i in range(min(count, len(songs))):
            data.append({
                "title": songs[i % len(songs)],
                "artist": artists[i % len(artists)],
                "rank": i + 1,
                "popularity": round(100 - i * 2 + random.uniform(-5, 5), 1),
                "duration": f"{random.randint(2, 4)}:{random.randint(10, 59):02d}",
                "album": f"Album {i + 1}",
                "release_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
            })
        
        return data
    
    def _generate_movie_data(self, count: int, chart_name: str) -> List[Dict]:
        """生成电影演示数据"""
        
        movies = [
            "阿凡达：水之道", "流浪地球2", "满江红", "深海", "无名",
            "交换人生", "中国乒乓", "黑豹2", "蚁人3", "银河护卫队3",
            "蜘蛛侠：纵横宇宙", "闪电侠", "奥本海默", "芭比", "碟中谍7"
        ]
        
        data = []
        for i in range(min(count, len(movies))):
            data.append({
                "title": movies[i % len(movies)],
                "rank": i + 1,
                "rating": round(8.0 + i * 0.1 + random.uniform(-0.3, 0.3), 1),
                "year": 2022 + (i // 5),
                "genre": random.choice(["动作", "科幻", "喜剧", "剧情", "悬疑"]),
                "director": f"导演 {i + 1}",
                "box_office": f"{random.randint(1, 50)}亿",
                "release_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
            })
        
        return data
    
    def _generate_tv_data(self, count: int, chart_name: str) -> List[Dict]:
        """生成电视剧演示数据"""
        
        tv_shows = [
            "三体", "狂飙", "漫长的季节", "去有风的地方", "黑暗荣耀",
            "莲花楼", "长相思", "云之羽", "护心", "长月烬明",
            "星汉灿烂", "苍兰诀", "梦华录", "开端", "人世间"
        ]
        
        data = []
        for i in range(min(count, len(tv_shows))):
            data.append({
                "title": tv_shows[i % len(tv_shows)],
                "rank": i + 1,
                "rating": round(8.0 + i * 0.1 + random.uniform(-0.3, 0.3), 1),
                "episodes": random.randint(24, 60),
                "genre": random.choice(["剧情", "悬疑", "古装", "都市", "科幻"]),
                "status": random.choice(["已完结", "连载中"]),
                "release_year": 2022 + (i // 5),
                "update_time": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            })
        
        return data
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行排行榜数据获取"""
        
        chart_type = data.get("chart_type", "global_top_50")
        limit = data.get("limit", 20)
        
        try:
            # 根据请求类型返回对应演示数据
            result = {
                "success": True,
                "data": [],
                "metadata": {
                    "chart_type": chart_type,
                    "source": "demo",
                    "timestamp": datetime.now().isoformat(),
                    "total": limit,
                    "is_demo": True  # 标记为演示数据
                }
            }
            
            # 根据请求类型返回对应数据
            if "music" in chart_type:
                chart_data = self.demo_data["music"].get(chart_type, [])
            elif "movie" in chart_type:
                chart_data = self.demo_data["movie"].get(chart_type, [])
            elif "tv" in chart_type:
                chart_data = self.demo_data["tv"].get(chart_type, [])
            else:
                # 默认返回音乐数据
                chart_data = self.demo_data["music"].get("global_top_50", [])
            
            result["data"] = chart_data[:limit]
            
            self.logger.info(f"📊 返回演示数据: {chart_type}, 数量: {len(result['data'])}")
            return result
            
        except Exception as e:
            self.logger.error(f"演示数据获取失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": []
            }
    
    def get_supported_charts(self) -> List[str]:
        """获取支持的排行榜类型"""
        return [
            "global_top_50", "new_releases", "hot_songs",
            "trending_movies", "popular_movies", "top_rated_movies",
            "trending_tv", "popular_tv"
        ]
    
    def get_health_status(self) -> Dict[str, Any]:
        """获取插件健康状态"""
        return {
            "status": "healthy",
            "message": "演示数据源运行正常",
            "is_demo": True,
            "data_available": len(self.demo_data) > 0
        }