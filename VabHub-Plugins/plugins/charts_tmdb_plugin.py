"""
TMDB影视数据源插件
基于MoviePilot的最佳实践实现
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import httpx
from .charts_base import VideoDataSourcePlugin


class ChartsTMDBPlugin(VideoDataSourcePlugin):
    """TMDB影视数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "tmdb"
        self.description = "TMDB影视排行榜数据源"
        self.author = "VabHub Team"
        self.version = "1.0.0"
        
        # TMDB API配置
        self.base_url = "https://api.themoviedb.org/3/"
        self.image_base_url = "https://image.tmdb.org/t/p/"
        self.api_endpoints = {
            "trending": "trending/{media_type}/{time_window}",
            "movie_popular": "movie/popular",
            "movie_top_rated": "movie/top_rated",
            "movie_now_playing": "movie/now_playing",
            "movie_upcoming": "movie/upcoming",
            "tv_popular": "tv/popular",
            "tv_top_rated": "tv/top_rated",
            "tv_on_the_air": "tv/on_the_air",
            "tv_airing_today": "tv/airing_today",
            "discover_movie": "discover/movie",
            "discover_tv": "discover/tv",
            "search_multi": "search/multi"
        }
        
        # 支持的榜单类型
        self.supported_chart_types = [
            "trending_all",  # 全部流行趋势
            "trending_movies",  # 电影流行趋势
            "trending_tv",  # 电视剧流行趋势
            "movie_popular",  # 热门电影
            "movie_top_rated",  # 高分电影
            "movie_now_playing",  # 正在热映
            "movie_upcoming",  # 即将上映
            "tv_popular",  # 热门电视剧
            "tv_top_rated",  # 高分电视剧
            "tv_on_the_air",  # 正在播出
            "tv_airing_today"  # 今日播出
        ]
        
        # 请求配置
        self.timeout = 30
        self.retry_count = 3
        
        # API密钥（使用MoviePilot的默认密钥）
        self.api_key = "db55373b1b8f4f6a8654d6a0c1d37a8f"
        
        # 代理配置
        self.proxy_enabled = False
        self.proxy_url = ""
        self.proxy_type = "http"
        
    def initialize(self) -> bool:
        """初始化插件"""
        try:
            self.logger.info(f"初始化 {self.name} 插件")
            
            # 设置默认配置
            default_config = {
                "enabled": True,
                "api_key": self.api_key,
                "language": "zh-CN",
                "region": "CN",
                "timeout": self.timeout,
                "retry_count": self.retry_count,
                "cache_duration": 3600,  # 1小时缓存
                "proxy_enabled": False,
                "proxy_url": "",
                "proxy_type": "http"
            }
            
            # 合并用户配置
            if self.config:
                default_config.update(self.config)
            self.config = default_config
            
            # 验证API密钥
            if not self.config.get("api_key"):
                self.logger.warning("TMDB API密钥未配置，使用默认密钥")
            
            # 配置代理设置
            self.proxy_enabled = self.config.get("proxy_enabled", False)
            self.proxy_url = self.config.get("proxy_url", "")
            self.proxy_type = self.config.get("proxy_type", "http")
            
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
            chart_type = data.get("chart_type", "trending_all")
            params = data.get("params", {})
            
            self.logger.info(f"执行 {chart_type} 榜单数据获取")
            
            # 根据榜单类型调用不同的方法
            if chart_type == "trending_all":
                result = await self._get_trending("all", "day", params)
            elif chart_type == "trending_movies":
                result = await self._get_trending("movie", "day", params)
            elif chart_type == "trending_tv":
                result = await self._get_trending("tv", "day", params)
            elif chart_type == "movie_popular":
                result = await self._get_movie_popular(params)
            elif chart_type == "movie_top_rated":
                result = await self._get_movie_top_rated(params)
            elif chart_type == "movie_now_playing":
                result = await self._get_movie_now_playing(params)
            elif chart_type == "movie_upcoming":
                result = await self._get_movie_upcoming(params)
            elif chart_type == "tv_popular":
                result = await self._get_tv_popular(params)
            elif chart_type == "tv_top_rated":
                result = await self._get_tv_top_rated(params)
            elif chart_type == "tv_on_the_air":
                result = await self._get_tv_on_the_air(params)
            elif chart_type == "tv_airing_today":
                result = await self._get_tv_airing_today(params)
            else:
                return {"error": f"不支持的榜单类型: {chart_type}"}
            
            self.last_update = datetime.now()
            return result
            
        except Exception as e:
            self.logger.error(f"执行 {self.name} 插件失败: {e}")
            self.error_count += 1
            return {"error": str(e)}
    
    async def _make_tmdb_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送TMDB API请求"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            # 基础参数
            query_params = {
                "api_key": self.config.get("api_key", self.api_key),
                "language": self.config.get("language", "zh-CN"),
                "region": self.config.get("region", "CN")
            }
            
            # 添加额外参数
            if params:
                query_params.update(params)
            
            headers = {
                "Accept": "application/json",
                "User-Agent": "VabHub Charts/1.0.0"
            }
            
            # 配置代理设置
            proxies = None
            if self.proxy_enabled and self.proxy_url:
                if self.proxy_type == "socks5":
                    proxies = f"socks5://{self.proxy_url}"
                else:
                    proxies = f"http://{self.proxy_url}"
                self.logger.info(f"使用代理访问TMDB: {proxies}")
            
            # 创建HTTP客户端
            client_kwargs = {"timeout": self.timeout}
            if proxies:
                client_kwargs["proxies"] = proxies
            
            async with httpx.AsyncClient(**client_kwargs) as client:
                response = await client.get(url, params=query_params, headers=headers)
                response.raise_for_status()
                
                return response.json()
                
        except httpx.HTTPStatusError as e:
            self.logger.error(f"TMDB API请求失败: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            self.logger.error(f"TMDB API请求异常: {e}")
            raise
    
    async def _get_trending(self, media_type: str, time_window: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取流行趋势"""
        try:
            endpoint = self.api_endpoints["trending"].format(
                media_type=media_type, 
                time_window=time_window
            )
            
            data = await self._make_tmdb_request(endpoint, {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": f"trending_{media_type}",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取流行趋势失败: {e}")
            return {"error": str(e)}
    
    async def _get_movie_popular(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取热门电影"""
        try:
            data = await self._make_tmdb_request(self.api_endpoints["movie_popular"], {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_item["type"] = "movie"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "movie_popular",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取热门电影失败: {e}")
            return {"error": str(e)}
    
    async def _get_movie_top_rated(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取高分电影"""
        try:
            data = await self._make_tmdb_request(self.api_endpoints["movie_top_rated"], {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_item["type"] = "movie"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "movie_top_rated",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取高分电影失败: {e}")
            return {"error": str(e)}
    
    async def _get_movie_now_playing(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取正在热映"""
        try:
            data = await self._make_tmdb_request(self.api_endpoints["movie_now_playing"], {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_item["type"] = "movie"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "movie_now_playing",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取正在热映失败: {e}")
            return {"error": str(e)}
    
    async def _get_movie_upcoming(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取即将上映"""
        try:
            data = await self._make_tmdb_request(self.api_endpoints["movie_upcoming"], {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_item["type"] = "movie"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "movie_upcoming",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取即将上映失败: {e}")
            return {"error": str(e)}
    
    async def _get_tv_popular(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取热门电视剧"""
        try:
            data = await self._make_tmdb_request(self.api_endpoints["tv_popular"], {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_item["type"] = "tv"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "tv_popular",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取热门电视剧失败: {e}")
            return {"error": str(e)}
    
    async def _get_tv_top_rated(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取高分电视剧"""
        try:
            data = await self._make_tmdb_request(self.api_endpoints["tv_top_rated"], {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_item["type"] = "tv"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "tv_top_rated",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取高分电视剧失败: {e}")
            return {"error": str(e)}
    
    async def _get_tv_on_the_air(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取正在播出"""
        try:
            data = await self._make_tmdb_request(self.api_endpoints["tv_on_the_air"], {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_item["type"] = "tv"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "tv_on_the_air",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取正在播出失败: {e}")
            return {"error": str(e)}
    
    async def _get_tv_airing_today(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取今日播出"""
        try:
            data = await self._make_tmdb_request(self.api_endpoints["tv_airing_today"], {
                "page": params.get("page", 1)
            })
            
            processed_data = []
            for item in data.get("results", [])[:params.get("limit", 20)]:
                processed_item = self._process_tmdb_item(item)
                processed_item["type"] = "tv"
                processed_data.append(processed_item)
            
            return {
                "success": True,
                "data": processed_data,
                "total": len(processed_data),
                "chart_type": "tv_airing_today",
                "source": "tmdb",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"获取今日播出失败: {e}")
            return {"error": str(e)}
    
    def _process_tmdb_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """处理TMDB数据项"""
        return {
            "id": item.get("id"),
            "title": item.get("title") or item.get("name"),
            "original_title": item.get("original_title") or item.get("original_name"),
            "type": "movie" if "title" in item else "tv",
            "popularity": item.get("popularity"),
            "vote_average": item.get("vote_average"),
            "vote_count": item.get("vote_count"),
            "release_date": item.get("release_date") or item.get("first_air_date"),
            "overview": item.get("overview", ""),
            "poster_path": f"{self.image_base_url}w500{item.get('poster_path', '')}" if item.get("poster_path") else "",
            "backdrop_path": f"{self.image_base_url}w780{item.get('backdrop_path', '')}" if item.get("backdrop_path") else "",
            "genre_ids": item.get("genre_ids", []),
            "original_language": item.get("original_language"),
            "adult": item.get("adult", False),
            "source": "tmdb"
        }
    
    def get_supported_charts(self) -> List[Dict[str, Any]]:
        """获取支持的榜单类型"""
        return [
            {
                "id": "trending_all",
                "name": "全部流行趋势",
                "description": "TMDB全部内容流行趋势",
                "category": "trending",
                "source": "tmdb"
            },
            {
                "id": "trending_movies",
                "name": "电影流行趋势",
                "description": "TMDB电影流行趋势",
                "category": "trending",
                "source": "tmdb"
            },
            {
                "id": "trending_tv",
                "name": "电视剧流行趋势",
                "description": "TMDB电视剧流行趋势",
                "category": "trending",
                "source": "tmdb"
            },
            {
                "id": "movie_popular",
                "name": "热门电影",
                "description": "TMDB热门电影排行榜",
                "category": "movie",
                "source": "tmdb"
            },
            {
                "id": "movie_top_rated",
                "name": "高分电影",
                "description": "TMDB高分评价电影排行榜",
                "category": "movie",
                "source": "tmdb"
            },
            {
                "id": "movie_now_playing",
                "name": "正在热映",
                "description": "影院正在上映的电影",
                "category": "movie",
                "source": "tmdb"
            },
            {
                "id": "movie_upcoming",
                "name": "即将上映",
                "description": "即将上映的电影作品",
                "category": "movie",
                "source": "tmdb"
            },
            {
                "id": "tv_popular",
                "name": "热门电视剧",
                "description": "TMDB热门电视剧排行榜",
                "category": "tv",
                "source": "tmdb"
            },
            {
                "id": "tv_top_rated",
                "name": "高分电视剧",
                "description": "TMDB高分评价电视剧排行榜",
                "category": "tv",
                "source": "tmdb"
            },
            {
                "id": "tv_on_the_air",
                "name": "正在播出",
                "description": "正在播出的电视剧",
                "category": "tv",
                "source": "tmdb"
            },
            {
                "id": "tv_airing_today",
                "name": "今日播出",
                "description": "今日播出的电视剧",
                "category": "tv",
                "source": "tmdb"
            }
        ]
    
    async def search_media(self, query: str, media_type: str = "multi", limit: int = 10) -> List[Dict[str, Any]]:
        """搜索媒体内容"""
        try:
            if media_type == "multi":
                endpoint = self.api_endpoints["search_multi"]
            else:
                endpoint = f"search/{media_type}"
            
            data = await self._make_tmdb_request(endpoint, {
                "query": query,
                "page": 1
            })
            
            results = []
            for item in data.get("results", [])[:limit]:
                result = self._process_tmdb_item(item)
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"搜索媒体内容失败: {e}")
            return []
    
    async def get_media_detail(self, media_id: str, media_type: str = "movie") -> Optional[Dict[str, Any]]:
        """获取媒体详情"""
        try:
            endpoint = f"{media_type}/{media_id}"
            data = await self._make_tmdb_request(endpoint)
            
            return {
                "id": data.get("id"),
                "title": data.get("title") or data.get("name"),
                "original_title": data.get("original_title") or data.get("original_name"),
                "type": media_type,
                "popularity": data.get("popularity"),
                "vote_average": data.get("vote_average"),
                "vote_count": data.get("vote_count"),
                "release_date": data.get("release_date") or data.get("first_air_date"),
                "overview": data.get("overview", ""),
                "poster_path": f"{self.image_base_url}w500{data.get('poster_path', '')}" if data.get("poster_path") else "",
                "backdrop_path": f"{self.image_base_url}w780{data.get('backdrop_path', '')}" if data.get("backdrop_path") else "",
                "genres": [genre.get("name") for genre in data.get("genres", [])],
                "runtime": data.get("runtime"),
                "budget": data.get("budget"),
                "revenue": data.get("revenue"),
                "status": data.get("status"),
                "tagline": data.get("tagline", ""),
                "homepage": data.get("homepage", ""),
                "imdb_id": data.get("imdb_id"),
                "production_companies": [company.get("name") for company in data.get("production_companies", [])],
                "production_countries": [country.get("name") for country in data.get("production_countries", [])],
                "spoken_languages": [language.get("name") for language in data.get("spoken_languages", [])],
                "source": "tmdb",
                "details": data
            }
            
        except Exception as e:
            self.logger.error(f"获取媒体详情失败: {e}")
            return None