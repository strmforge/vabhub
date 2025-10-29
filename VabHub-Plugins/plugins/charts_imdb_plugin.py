"""
IMDb影视数据源插件
集成IMDb Top 250、热门电影等数据源
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import httpx
from .charts_base import VideoDataSourcePlugin


class ChartsIMDbPlugin(VideoDataSourcePlugin):
    """IMDb影视数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "imdb"
        self.description = "IMDb影视排行榜数据源"
        self.author = "VabHub Team"
        self.version = "1.0.0"
        
        # IMDb API配置（使用第三方API服务）
        self.base_url = "https://imdb-api.com/api/"
        self.api_endpoints = {
            "top_250_movies": "Top250Movies",
            "top_250_tv": "Top250TVs",
            "most_popular_movies": "MostPopularMovies",
            "most_popular_tv": "MostPopularTVs",
            "coming_soon": "ComingSoon",
            "in_theaters": "InTheaters",
            "box_office": "BoxOffice",
            "search": "SearchMovie"
        }
        
        # 支持的榜单类型
        self.supported_chart_types = [
            "top_250_movies",  # IMDb Top 250电影
            "top_250_tv",  # IMDb Top 250电视剧
            "most_popular_movies",  # 最受欢迎电影
            "most_popular_tv",  # 最受欢迎电视剧
            "coming_soon",  # 即将上映
            "in_theaters",  # 正在上映
            "box_office"  # 票房排行
        ]
        
        # API密钥（需要用户配置）
        self.api_key = None
        
        # 请求配置
        self.timeout = 30
        self.retry_count = 3
        
        self.logger = logging.getLogger(__name__)

    async def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化插件"""
        try:
            self.api_key = config.get("api_key")
            if not self.api_key:
                self.logger.warning("IMDb API密钥未配置，部分功能可能受限")
            
            self.logger.info("IMDb数据源插件初始化成功")
            return True
        except Exception as e:
            self.logger.error(f"IMDb插件初始化失败: {e}")
            return False

    async def get_chart_data(self, chart_type: str, limit: int = 50, **kwargs) -> List[Dict[str, Any]]:
        """获取榜单数据"""
        if chart_type not in self.supported_chart_types:
            raise ValueError(f"不支持的榜单类型: {chart_type}")
        
        if not self.api_key:
            raise ValueError("IMDb API密钥未配置")
        
        try:
            endpoint = self.api_endpoints[chart_type]
            url = f"{self.base_url}{endpoint}/{self.api_key}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                data = response.json()
                
                # 转换数据格式
                items = data.get("items", [])
                if not items:
                    items = data.get("results", [])
                
                return self._transform_data(items[:limit], chart_type)
                
        except Exception as e:
            self.logger.error(f"获取IMDb {chart_type}数据失败: {e}")
            raise

    def _transform_data(self, items: List[Dict], chart_type: str) -> List[Dict[str, Any]]:
        """转换数据格式为统一格式"""
        transformed = []
        
        for item in items:
            # IMDb API返回字段映射
            transformed_item = {
                "id": item.get("id") or item.get("imdbID"),
                "title": item.get("title") or item.get("fullTitle"),
                "original_title": item.get("originalTitle"),
                "year": item.get("year"),
                "rating": item.get("imDbRating") or item.get("rating"),
                "rating_count": item.get("imDbRatingCount") or item.get("ratingCount"),
                "rank": item.get("rank"),
                "image": item.get("image"),
                "description": item.get("description"),
                "genres": item.get("genres", "").split(", ") if item.get("genres") else [],
                "directors": item.get("directors", "").split(", ") if item.get("directors") else [],
                "stars": item.get("stars", "").split(", ") if item.get("stars") else [],
                "runtime": item.get("runtimeStr"),
                "release_date": item.get("releaseDate"),
                "plot": item.get("plot"),
                "data_source": "imdb",
                "chart_type": chart_type,
                "fetch_time": datetime.now().isoformat()
            }
            
            # 清理空值
            transformed_item = {k: v for k, v in transformed_item.items() if v is not None}
            transformed.append(transformed_item)
        
        return transformed

    async def search_content(self, query: str, content_type: str = "movie", **kwargs) -> List[Dict[str, Any]]:
        """搜索内容"""
        if not self.api_key:
            raise ValueError("IMDb API密钥未配置")
        
        try:
            url = f"{self.base_url}{self.api_endpoints['search']}/{self.api_key}/{query}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])
                
                # 根据类型过滤结果
                if content_type != "all":
                    results = [r for r in results if r.get("resultType") == content_type]
                
                return self._transform_data(results, "search")
                
        except Exception as e:
            self.logger.error(f"IMDb搜索失败: {e}")
            raise

    def get_supported_chart_types(self) -> List[str]:
        """获取支持的榜单类型"""
        return self.supported_chart_types

    def get_config_schema(self) -> Dict[str, Any]:
        """获取配置模式"""
        return {
            "api_key": {
                "type": "string",
                "required": True,
                "description": "IMDb API密钥",
                "placeholder": "输入您的IMDb API密钥"
            }
        }

    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            if not self.api_key:
                return {"status": "warning", "message": "API密钥未配置"}
            
            # 测试API连接
            url = f"{self.base_url}MostPopularMovies/{self.api_key}"
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                
            if response.status_code == 200:
                return {"status": "healthy", "message": "IMDb API连接正常"}
            else:
                return {"status": "error", "message": f"API响应异常: {response.status_code}"}
                
        except Exception as e:
            return {"status": "error", "message": f"健康检查失败: {e}"}