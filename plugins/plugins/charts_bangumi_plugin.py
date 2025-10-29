"""
Bangumi动漫数据源插件
基于MoviePilot的最佳实践实现
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import httpx
from .charts_base import VideoDataSourcePlugin


class ChartsBangumiPlugin(VideoDataSourcePlugin):
    """Bangumi动漫数据源插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "bangumi"
        self.description = "Bangumi动漫排行榜数据源"
        self.author = "VabHub Team"
        self.version = "1.0.0"
        
        # Bangumi API配置
        self.base_url = "https://api.bgm.tv/"
        self.api_endpoints = {
            "calendar": "calendar",  # 每日放送
            "search": "search/subject/{query}",  # 搜索
            "detail": "v0/subjects/{id}",  # 详情
            "top_anime": "v0/subjects?type=2&sort=rank",  # 动漫排行
            "top_manga": "v0/subjects?type=1&sort=rank",  # 漫画排行
        }
        
        # 支持的榜单类型
        self.supported_chart_types = [
            "daily_calendar",  # 每日放送
            "top_anime",  # 热门动漫
            "top_manga",  # 热门漫画
            "new_anime",  # 新番动漫
            "trending_anime"  # 趋势动漫
        ]
        
        # 请求配置
        self.timeout = 30
        self.retry_count = 3
        self.rate_limit_delay = 1.0
        
        # 缓存配置
        self.cache_duration = 3600  # 1小时缓存
        
    def initialize(self) -> bool:
        """初始化插件"""
        try:
            self.logger.info(f"初始化 {self.name} 插件")
            
            # 设置默认配置
            default_config = {
                "enabled": True,
                "timeout": self.timeout,
                "retry_count": self.retry_count,
                "cache_duration": self.cache_duration,
                "user_agent": "VabHub Charts/1.0.0 (https://github.com/VabHub)"
            }
            
            # 合并用户配置
            if self.config:
                default_config.update(self.config)
            self.config = default_config
            
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
            chart_type = data.get("chart_type", "daily_calendar")
            params = data.get("params", {})
            
            self.logger.info(f"执行 {chart_type} 榜单数据获取")
            
            # 根据榜单类型调用不同的方法
            if chart_type == "daily_calendar":
                result = await self._get_daily_calendar(params)
            elif chart_type == "top_anime":
                result = await self._get_top_anime(params)
            elif chart_type == "top_manga":
                result = await self._get_top_manga(params)
            elif chart_type == "new_anime":
                result = await self._get_new_anime(params)
            elif chart_type == "trending_anime":
                result = await self._get_trending_anime(params)
            else:
                return {"error": f"不支持的榜单类型: {chart_type}"}
            
            self.last_update = datetime.now()
            return result
            
        except Exception as e:
            self.logger.error(f"执行 {self.name} 插件失败: {e}")
            self.error_count += 1
            return {"error": str(e)}
    
    async def _get_daily_calendar(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取每日放送数据"""
        try:
            url = f"{self.base_url}{self.api_endpoints['calendar']}"
            
            # 添加时间戳避免缓存
            timestamp = int(datetime.now().timestamp())
            url = f"{url}?_ts={timestamp}"
            
            headers = {
                "User-Agent": self.config.get("user_agent", "VabHub Charts"),
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                # 处理每日放送数据
                processed_data = []
                for day_data in data:
                    weekday = day_data.get("weekday", {})
                    items = day_data.get("items", [])
                    
                    for item in items:
                        processed_item = {
                            "id": item.get("id"),
                            "title": item.get("name_cn") or item.get("name"),
                            "original_title": item.get("name"),
                            "type": "anime",
                            "rank": item.get("rank"),
                            "score": item.get("rating", {}).get("score"),
                            "air_date": item.get("air_date"),
                            "air_weekday": item.get("air_weekday"),
                            "weekday_cn": weekday.get("cn", ""),
                            "weekday_en": weekday.get("en", ""),
                            "images": item.get("images", {}),
                            "summary": item.get("summary", ""),
                            "collection_count": item.get("collection", {}).get("doing", 0),
                            "url": item.get("url", ""),
                            "source": "bangumi"
                        }
                        processed_data.append(processed_item)
                
                return {
                    "success": True,
                    "data": processed_data,
                    "total": len(processed_data),
                    "chart_type": "daily_calendar",
                    "source": "bangumi",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"获取每日放送数据失败: {e}")
            return {"error": str(e)}
    
    async def _get_top_anime(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取热门动漫排行"""
        try:
            page = params.get("page", 1)
            limit = params.get("limit", 50)
            
            url = f"{self.base_url}{self.api_endpoints['top_anime']}"
            url = f"{url}&limit={limit}&offset={(page-1)*limit}"
            
            headers = {
                "User-Agent": self.config.get("user_agent", "VabHub Charts"),
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                processed_data = []
                for item in data.get("data", [])[:limit]:
                    processed_item = {
                        "id": item.get("id"),
                        "title": item.get("name_cn") or item.get("name"),
                        "original_title": item.get("name"),
                        "type": "anime",
                        "rank": item.get("rank"),
                        "score": item.get("rating", {}).get("score"),
                        "images": item.get("images", {}),
                        "summary": item.get("summary", ""),
                        "collection_count": item.get("collection", {}).get("doing", 0),
                        "url": item.get("url", ""),
                        "source": "bangumi"
                    }
                    processed_data.append(processed_item)
                
                return {
                    "success": True,
                    "data": processed_data,
                    "total": len(processed_data),
                    "chart_type": "top_anime",
                    "source": "bangumi",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"获取热门动漫排行失败: {e}")
            return {"error": str(e)}
    
    async def _get_top_manga(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取热门漫画排行"""
        try:
            page = params.get("page", 1)
            limit = params.get("limit", 50)
            
            url = f"{self.base_url}{self.api_endpoints['top_manga']}"
            url = f"{url}&limit={limit}&offset={(page-1)*limit}"
            
            headers = {
                "User-Agent": self.config.get("user_agent", "VabHub Charts"),
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                processed_data = []
                for item in data.get("data", [])[:limit]:
                    processed_item = {
                        "id": item.get("id"),
                        "title": item.get("name_cn") or item.get("name"),
                        "original_title": item.get("name"),
                        "type": "manga",
                        "rank": item.get("rank"),
                        "score": item.get("rating", {}).get("score"),
                        "images": item.get("images", {}),
                        "summary": item.get("summary", ""),
                        "collection_count": item.get("collection", {}).get("doing", 0),
                        "url": item.get("url", ""),
                        "source": "bangumi"
                    }
                    processed_data.append(processed_item)
                
                return {
                    "success": True,
                    "data": processed_data,
                    "total": len(processed_data),
                    "chart_type": "top_manga",
                    "source": "bangumi",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"获取热门漫画排行失败: {e}")
            return {"error": str(e)}
    
    async def _get_new_anime(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取新番动漫"""
        # 使用每日放送数据中的最新动漫作为新番
        calendar_data = await self._get_daily_calendar({})
        if "error" in calendar_data:
            return calendar_data
        
        # 按播出日期排序，获取最新的动漫
        all_anime = calendar_data.get("data", [])
        new_anime = sorted(
            all_anime, 
            key=lambda x: x.get("air_date", ""), 
            reverse=True
        )[:params.get("limit", 20)]
        
        return {
            "success": True,
            "data": new_anime,
            "total": len(new_anime),
            "chart_type": "new_anime",
            "source": "bangumi",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_trending_anime(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取趋势动漫"""
        # 使用收藏数作为趋势指标
        calendar_data = await self._get_daily_calendar({})
        if "error" in calendar_data:
            return calendar_data
        
        # 按收藏数排序，获取最受欢迎的动漫
        all_anime = calendar_data.get("data", [])
        trending_anime = sorted(
            all_anime, 
            key=lambda x: x.get("collection_count", 0), 
            reverse=True
        )[:params.get("limit", 20)]
        
        return {
            "success": True,
            "data": trending_anime,
            "total": len(trending_anime),
            "chart_type": "trending_anime",
            "source": "bangumi",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_supported_charts(self) -> List[Dict[str, Any]]:
        """获取支持的榜单类型"""
        return [
            {
                "id": "daily_calendar",
                "name": "每日放送",
                "description": "Bangumi每日动漫放送日历",
                "category": "anime",
                "source": "bangumi"
            },
            {
                "id": "top_anime",
                "name": "热门动漫",
                "description": "Bangumi热门动漫排行榜",
                "category": "anime",
                "source": "bangumi"
            },
            {
                "id": "top_manga",
                "name": "热门漫画",
                "description": "Bangumi热门漫画排行榜",
                "category": "manga",
                "source": "bangumi"
            },
            {
                "id": "new_anime",
                "name": "新番动漫",
                "description": "最新播出的动漫作品",
                "category": "anime",
                "source": "bangumi"
            },
            {
                "id": "trending_anime",
                "name": "趋势动漫",
                "description": "当前最受欢迎的动漫作品",
                "category": "anime",
                "source": "bangumi"
            }
        ]
    
    async def search_anime(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索动漫"""
        try:
            url = f"{self.base_url}{self.api_endpoints['search'].format(query=query)}"
            headers = {
                "User-Agent": self.config.get("user_agent", "VabHub Charts"),
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                results = []
                for item in data.get("list", [])[:limit]:
                    result = {
                        "id": item.get("id"),
                        "title": item.get("name_cn") or item.get("name"),
                        "original_title": item.get("name"),
                        "type": "anime",
                        "score": item.get("rating", {}).get("score"),
                        "images": item.get("images", {}),
                        "summary": item.get("summary", ""),
                        "url": item.get("url", ""),
                        "source": "bangumi"
                    }
                    results.append(result)
                
                return results
                
        except Exception as e:
            self.logger.error(f"搜索动漫失败: {e}")
            return []
    
    async def get_anime_detail(self, anime_id: str) -> Optional[Dict[str, Any]]:
        """获取动漫详情"""
        try:
            url = f"{self.base_url}{self.api_endpoints['detail'].format(id=anime_id)}"
            headers = {
                "User-Agent": self.config.get("user_agent", "VabHub Charts"),
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                return {
                    "id": data.get("id"),
                    "title": data.get("name_cn") or data.get("name"),
                    "original_title": data.get("name"),
                    "type": "anime",
                    "score": data.get("rating", {}).get("score"),
                    "rank": data.get("rank"),
                    "images": data.get("images", {}),
                    "summary": data.get("summary", ""),
                    "collection_count": data.get("collection", {}).get("doing", 0),
                    "url": data.get("url", ""),
                    "source": "bangumi",
                    "details": data
                }
                
        except Exception as e:
            self.logger.error(f"获取动漫详情失败: {e}")
            return None