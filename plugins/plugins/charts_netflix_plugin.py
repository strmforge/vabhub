"""
Netflix数据源插件
集成Netflix热门内容、排行榜等数据
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import httpx
from .charts_base import VideoDataSourcePlugin


class ChartsNetflixPlugin(VideoDataSourcePlugin):
    """Netflix数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "netflix"
        self.description = "Netflix热门内容数据源"
        self.author = "VabHub Team"
        self.version = "1.0.0"
        
        # Netflix数据源配置（使用第三方API）
        self.base_url = "https://netflix-data.p.rapidapi.com/"
        self.api_endpoints = {
            "top_10_today": "top_10/today",
            "top_10_weekly": "top_10/weekly",
            "most_popular": "most_popular",
            "new_releases": "new_releases",
            "coming_soon": "coming_soon",
            "trending": "trending",
            "search": "search"
        }
        
        # 支持的榜单类型
        self.supported_chart_types = [
            "top_10_today",  # 今日Top 10
            "top_10_weekly",  # 本周Top 10
            "most_popular",  # 最受欢迎
            "new_releases",  # 新上线内容
            "coming_soon",  # 即将上线
            "trending"  # 趋势内容
        ]
        
        # API配置
        self.api_key = None
        self.api_host = "netflix-data.p.rapidapi.com"
        
        # 请求配置
        self.timeout = 30
        self.retry_count = 3
        
        self.logger = logging.getLogger(__name__)

    async def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化插件"""
        try:
            self.api_key = config.get("api_key")
            if not self.api_key:
                self.logger.warning("Netflix API密钥未配置，部分功能可能受限")
            
            self.logger.info("Netflix数据源插件初始化成功")
            return True
        except Exception as e:
            self.logger.error(f"Netflix插件初始化失败: {e}")
            return False

    async def get_chart_data(self, chart_type: str, limit: int = 50, **kwargs) -> List[Dict[str, Any]]:
        """获取榜单数据"""
        if chart_type not in self.supported_chart_types:
            raise ValueError(f"不支持的榜单类型: {chart_type}")
        
        if not self.api_key:
            raise ValueError("Netflix API密钥未配置")
        
        try:
            endpoint = self.api_endpoints[chart_type]
            url = f"{self.base_url}{endpoint}"
            
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": self.api_host
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                # 处理不同API返回格式
                items = self._extract_items(data, chart_type)
                
                return self._transform_data(items[:limit], chart_type)
                
        except Exception as e:
            self.logger.error(f"获取Netflix {chart_type}数据失败: {e}")
            raise

    def _extract_items(self, data: Dict, chart_type: str) -> List[Dict]:
        """从API响应中提取项目列表"""
        if chart_type.startswith("top_10"):
            # Top 10榜单格式
            return data.get("data", [])
        elif chart_type == "most_popular":
            return data.get("popular", [])
        elif chart_type == "new_releases":
            return data.get("new", [])
        elif chart_type == "coming_soon":
            return data.get("upcoming", [])
        elif chart_type == "trending":
            return data.get("trending", [])
        else:
            return data.get("results", []) or data.get("items", [])

    def _transform_data(self, items: List[Dict], chart_type: str) -> List[Dict[str, Any]]:
        """转换数据格式为统一格式"""
        transformed = []
        
        for item in items:
            # Netflix数据字段映射
            transformed_item = {
                "id": item.get("netflix_id") or item.get("id"),
                "title": item.get("title"),
                "original_title": item.get("original_title"),
                "year": item.get("year") or item.get("release_year"),
                "rating": item.get("rating") or item.get("imdb_rating"),
                "rank": item.get("rank"),
                "image": item.get("image") or item.get("poster"),
                "description": item.get("description") or item.get("synopsis"),
                "genres": item.get("genres", []),
                "directors": item.get("directors", []),
                "cast": item.get("cast", []),
                "runtime": item.get("runtime"),
                "release_date": item.get("release_date"),
                "netflix_release": item.get("netflix_release"),
                "type": item.get("type"),  # movie/tv
                "seasons": item.get("seasons"),
                "episodes": item.get("episodes"),
                "country": item.get("country"),
                "language": item.get("language"),
                "data_source": "netflix",
                "chart_type": chart_type,
                "fetch_time": datetime.now().isoformat()
            }
            
            # 处理字符串类型的列表字段
            if isinstance(transformed_item["genres"], str):
                transformed_item["genres"] = transformed_item["genres"].split(", ")
            if isinstance(transformed_item["directors"], str):
                transformed_item["directors"] = transformed_item["directors"].split(", ")
            if isinstance(transformed_item["cast"], str):
                transformed_item["cast"] = transformed_item["cast"].split(", ")
            
            # 清理空值
            transformed_item = {k: v for k, v in transformed_item.items() if v is not None}
            transformed.append(transformed_item)
        
        return transformed

    async def search_content(self, query: str, content_type: str = "all", **kwargs) -> List[Dict[str, Any]]:
        """搜索Netflix内容"""
        if not self.api_key:
            raise ValueError("Netflix API密钥未配置")
        
        try:
            url = f"{self.base_url}{self.api_endpoints['search']}"
            params = {"query": query}
            
            if content_type != "all":
                params["type"] = content_type
            
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": self.api_host
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])
                
                return self._transform_data(results, "search")
                
        except Exception as e:
            self.logger.error(f"Netflix搜索失败: {e}")
            raise

    async def get_content_details(self, content_id: str, **kwargs) -> Dict[str, Any]:
        """获取内容详情"""
        if not self.api_key:
            raise ValueError("Netflix API密钥未配置")
        
        try:
            url = f"{self.base_url}title/{content_id}"
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": self.api_host
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                # 转换详情数据格式
                return self._transform_detail_data(data)
                
        except Exception as e:
            self.logger.error(f"获取Netflix内容详情失败: {e}")
            raise

    def _transform_detail_data(self, data: Dict) -> Dict[str, Any]:
        """转换详情数据格式"""
        return {
            "id": data.get("netflix_id"),
            "title": data.get("title"),
            "original_title": data.get("original_title"),
            "year": data.get("year"),
            "rating": data.get("rating"),
            "description": data.get("description"),
            "genres": data.get("genres", []),
            "directors": data.get("directors", []),
            "cast": data.get("cast", []),
            "runtime": data.get("runtime"),
            "release_date": data.get("release_date"),
            "netflix_release": data.get("netflix_release"),
            "type": data.get("type"),
            "seasons": data.get("seasons"),
            "episodes": data.get("episodes"),
            "country": data.get("country"),
            "language": data.get("language"),
            "imdb_id": data.get("imdb_id"),
            "tmdb_id": data.get("tmdb_id"),
            "poster": data.get("poster"),
            "backdrop": data.get("backdrop"),
            "trailer": data.get("trailer"),
            "age_rating": data.get("age_rating"),
            "awards": data.get("awards"),
            "box_office": data.get("box_office")
        }

    def get_supported_chart_types(self) -> List[str]:
        """获取支持的榜单类型"""
        return self.supported_chart_types

    def get_config_schema(self) -> Dict[str, Any]:
        """获取配置模式"""
        return {
            "api_key": {
                "type": "string",
                "required": True,
                "description": "Netflix API密钥",
                "placeholder": "输入您的Netflix API密钥"
            }
        }

    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            if not self.api_key:
                return {"status": "warning", "message": "API密钥未配置"}
            
            # 测试API连接
            url = f"{self.base_url}{self.api_endpoints['top_10_today']}"
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": self.api_host
            }
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, headers=headers)
                
            if response.status_code == 200:
                return {"status": "healthy", "message": "Netflix API连接正常"}
            else:
                return {"status": "error", "message": f"API响应异常: {response.status_code}"}
                
        except Exception as e:
            return {"status": "error", "message": f"健康检查失败: {e}"}