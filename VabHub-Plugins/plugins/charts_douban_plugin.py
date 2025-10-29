"""
豆瓣影视数据源插件
基于MoviePilot的最佳实践实现
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import httpx
from .charts_base import VideoDataSourcePlugin


class ChartsDoubanPlugin(VideoDataSourcePlugin):
    """豆瓣影视数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "douban"
        self.description = "豆瓣影视排行榜数据源"
        self.author = "VabHub Team"
        self.version = "1.0.0"
        
        # 豆瓣API配置（使用MoviePilot的API端点）
        self.base_url = "https://frodo.douban.com/api/v2/"
        self.api_endpoints = {
            "movie_showing": "subject_collection/movie_showing/items",  # 正在热映
            "movie_hot_gaia": "subject_collection/movie_hot_gaia/items",  # 热门电影
            "movie_top250": "subject_collection/movie_top250/items",  # 电影TOP250
            "tv_hot": "subject_collection/tv_hot/items",  # 热门电视剧
            "tv_variety_show": "subject_collection/tv_variety_show/items",  # 综艺
            "search_movie": "search/movie",  # 搜索电影
            "search_tv": "search/tv",  # 搜索电视剧
            "movie_detail": "movie/{id}",  # 电影详情
            "tv_detail": "tv/{id}"  # 电视剧详情
        }
        
        # 支持的榜单类型
        self.supported_chart_types = [
            "movie_showing",  # 正在热映
            "movie_hot",  # 热门电影
            "movie_top250",  # 电影TOP250
            "tv_hot",  # 热门电视剧
            "tv_variety"  # 综艺节目
        ]
        
        # 请求配置
        self.timeout = 30
        self.retry_count = 3
        
        # API密钥（使用MoviePilot的默认密钥）
        self.api_key = "0ac44ae016490db2204ce0a042db2916"
        
    def initialize(self) -> bool:
        """初始化插件"""
        try:
            self.logger.info(f"初始化 {self.name} 插件")
            
            # 设置默认配置
            default_config = {
                "enabled": True,
                "api_key": self.api_key,
                "timeout": self.timeout,
                "retry_count": self.retry_count,
                "cache_duration": 3600,  # 1小时缓存
                "user_agent": "api-client/1 com.douban.frodo/7.22.0.beta9(230) Android/23 product/Mate 40 vendor/HUAWEI model/Mate 40 brand/HUAWEI"
            }
            
            # 合并用户配置
            if self.config:
                default_config.update(self.config)
            self.config = default_config
            
            # 验证API密钥
            if not self.config.get("api_key"):
                self.logger.warning("豆瓣API密钥未配置，使用默认密钥")
            
            self.initialized = True
            self.last_update = datetime.now()
            
            self.logger.info(f"{self.name} 插件初始化成功")
            return True
            
        except Exception as e:
            self.logger.error(f"初始化 {self.name} 插件失败: {e}")
            self.initialized = False
            return False
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行排行榜数据获取"""
        if not self.enabled or not self.initialized:
            return {"error": "插件未启用或未初始化"}
        
        try:
            chart_type = data.get("chart_type", "movie_showing")
            params = data.get("params", {})
            
            self.logger.info(f"执行 {chart_type} 榜单数据获取")
            
            # 根据榜单类型调用不同的方法
            if chart_type == "movie_showing":
                result = await self._get_movie_showing(params)
            elif chart_type == "movie_hot":
                result = await self._get_movie_hot(params)
            elif chart_type == "movie_top250":
                result = await self._get_movie_top250(params)
            elif chart_type == "tv_hot":
                result = await self._get_tv_hot(params)
            elif chart_type == "tv_variety":
                result = await self._get_tv_variety(params)
            else:
                return {"error": f"不支持的榜单类型: {chart_type}"}
            
            self.last_update = datetime.now()
            return result
            
        except Exception as e:
            self.logger.error(f"执行 {self.name} 插件失败: {e}")
            self.error_count += 1
            return {"error": str(e)}
    
    async def _make_douban_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送豆瓣API请求"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            # 基础参数
            query_params = {
                "apikey": self.config.get("api_key", self.api_key),
                "start": params.get("start", 0) if params else 0,
                "count": params.get("count", 20) if params else 20
            }
            
            headers = {
                "User-Agent": self.config.get("user_agent", "VabHub Charts"),
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=query_params, headers=headers)
                response.raise_for_status()
                
                return response.json()
                
        except httpx.HTTPStatusError as e:
            self.logger.error(f"豆瓣API请求失败: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            self.logger.error(f"豆瓣API请求异常: {e}")
            raise
    
    async def _get_movie_showing(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取正在热映"""
        try:
            data = await self._make_douban_request(self.api_endpoints["movie_showing"], params)
            
            processed_data = []
            for item in data.get("subject_collection_items", [])[:params.get("limit", 20)]:
                processed_item = self._process_douban_item(item)
                processed_item["type"] = "movie"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "movie_showing",
                "source": "douban",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取正在热映失败: {e}")
            return {"error": str(e)}
    
    async def _get_movie_hot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取热门电影"""
        try:
            data = await self._make_douban_request(self.api_endpoints["movie_hot_gaia"], params)
            
            processed_data = []
            for item in data.get("subject_collection_items", [])[:params.get("limit", 20)]:
                processed_item = self._process_douban_item(item)
                processed_item["type"] = "movie"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "movie_hot",
                "source": "douban",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取热门电影失败: {e}")
            return {"error": str(e)}
    
    async def _get_movie_top250(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取电影TOP250"""
        try:
            data = await self._make_douban_request(self.api_endpoints["movie_top250"], params)
            
            processed_data = []
            for item in data.get("subject_collection_items", [])[:params.get("limit", 20)]:
                processed_item = self._process_douban_item(item)
                processed_item["type"] = "movie"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "movie_top250",
                "source": "douban",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取电影TOP250失败: {e}")
            return {"error": str(e)}
    
    async def _get_tv_hot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取热门电视剧"""
        try:
            data = await self._make_douban_request(self.api_endpoints["tv_hot"], params)
            
            processed_data = []
            for item in data.get("subject_collection_items", [])[:params.get("limit", 20)]:
                processed_item = self._process_douban_item(item)
                processed_item["type"] = "tv"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "tv_hot",
                "source": "douban",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取热门电视剧失败: {e}")
            return {"error": str(e)}
    
    async def _get_tv_variety(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取综艺节目"""
        try:
            data = await self._make_douban_request(self.api_endpoints["tv_variety_show"], params)
            
            processed_data = []
            for item in data.get("subject_collection_items", [])[:params.get("limit", 20)]:
                processed_item = self._process_douban_item(item)
                processed_item["type"] = "variety"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "tv_variety",
                "source": "douban",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取综艺节目失败: {e}")
            return {"error": str(e)}
    
    def _process_douban_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """处理豆瓣数据项"""
        # 处理评分信息
        rating_info = item.get("rating", {})
        score = rating_info.get("value", 0)
        
        # 处理图片信息
        pic_info = item.get("pic", {})
        poster_url = pic_info.get("large") or pic_info.get("normal") or ""
        
        # 处理基本信息
        return {
            "id": item.get("id"),
            "title": item.get("title"),
            "original_title": item.get("original_title"),
            "type": "movie",  # 默认类型，具体类型由调用方设置
            "score": score,
            "rating_count": rating_info.get("count", 0),
            "release_date": item.get("release_date") or item.get("pubdate"),
            "year": item.get("year"),
            "genres": item.get("genres", []),
            "durations": item.get("durations", []),
            "summary": item.get("intro", ""),
            "poster_url": poster_url,
            "actors": [actor.get("name") for actor in item.get("actors", [])[:5]],
            "directors": [director.get("name") for director in item.get("directors", [])],
            "countries": item.get("countries", []),
            "languages": item.get("languages", []),
            "episodes_count": item.get("episodes_count"),
            "url": f"https://movie.douban.com/subject/{item.get('id')}/" if item.get("id") else "",
            "source": "douban"
        }
    
    def get_supported_charts(self) -> List[Dict[str, Any]]:
        """获取支持的榜单类型"""
        return [
            {
                "id": "movie_showing",
                "name": "正在热映",
                "description": "豆瓣正在热映的电影",
                "category": "movie",
                "source": "douban"
            },
            {
                "id": "movie_hot",
                "name": "热门电影",
                "description": "豆瓣热门电影排行榜",
                "category": "movie",
                "source": "douban"
            },
            {
                "id": "movie_top250",
                "name": "电影TOP250",
                "description": "豆瓣电影TOP250经典榜单",
                "category": "movie",
                "source": "douban"
            },
            {
                "id": "tv_hot",
                "name": "热门电视剧",
                "description": "豆瓣热门电视剧排行榜",
                "category": "tv",
                "source": "douban"
            },
            {
                "id": "tv_variety",
                "name": "综艺节目",
                "description": "豆瓣热门综艺节目排行榜",
                "category": "variety",
                "source": "douban"
            }
        ]
    
    async def search_movie(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索电影"""
        try:
            data = await self._make_douban_request(self.api_endpoints["search_movie"], {
                "q": query,
                "count": limit
            })
            
            results = []
            for item in data.get("items", [])[:limit]:
                result = self._process_douban_item(item)
                result["type"] = "movie"
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"搜索电影失败: {e}")
            return []
    
    async def search_tv(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索电视剧"""
        try:
            data = await self._make_douban_request(self.api_endpoints["search_tv"], {
                "q": query,
                "count": limit
            })
            
            results = []
            for item in data.get("items", [])[:limit]:
                result = self._process_douban_item(item)
                result["type"] = "tv"
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"搜索电视剧失败: {e}")
            return []
    
    async def get_movie_detail(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """获取电影详情"""
        try:
            endpoint = self.api_endpoints["movie_detail"].format(id=movie_id)
            data = await self._make_douban_request(endpoint)
            
            return {
                "id": data.get("id"),
                "title": data.get("title"),
                "original_title": data.get("original_title"),
                "type": "movie",
                "score": data.get("rating", {}).get("value", 0),
                "rating_count": data.get("rating", {}).get("count", 0),
                "release_date": data.get("release_date"),
                "year": data.get("year"),
                "genres": data.get("genres", []),
                "durations": data.get("durations", []),
                "summary": data.get("summary", ""),
                "poster_url": data.get("pic", {}).get("large"),
                "actors": [actor.get("name") for actor in data.get("actors", [])],
                "directors": [director.get("name") for director in data.get("directors", [])],
                "countries": data.get("countries", []),
                "languages": data.get("languages", []),
                "aka": data.get("aka", []),
                "imdb_id": data.get("imdb_id"),
                "url": f"https://movie.douban.com/subject/{movie_id}/",
                "source": "douban",
                "details": data
            }
            
        except Exception as e:
            self.logger.error(f"获取电影详情失败: {e}")
            return None
    
    async def get_tv_detail(self, tv_id: str) -> Optional[Dict[str, Any]]:
        """获取电视剧详情"""
        try:
            endpoint = self.api_endpoints["tv_detail"].format(id=tv_id)
            data = await self._make_douban_request(endpoint)
            
            return {
                "id": data.get("id"),
                "title": data.get("title"),
                "original_title": data.get("original_title"),
                "type": "tv",
                "score": data.get("rating", {}).get("value", 0),
                "rating_count": data.get("rating", {}).get("count", 0),
                "release_date": data.get("release_date"),
                "year": data.get("year"),
                "genres": data.get("genres", []),
                "durations": data.get("durations", []),
                "summary": data.get("summary", ""),
                "poster_url": data.get("pic", {}).get("large"),
                "actors": [actor.get("name") for actor in data.get("actors", [])],
                "directors": [director.get("name") for director in data.get("directors", [])],
                "countries": data.get("countries", []),
                "languages": data.get("languages", []),
                "episodes_count": data.get("episodes_count"),
                "aka": data.get("aka", []),
                "url": f"https://movie.douban.com/subject/{tv_id}/",
                "source": "douban",
                "details": data
            }
            
        except Exception as e:
            self.logger.error(f"获取电视剧详情失败: {e}")
            return None