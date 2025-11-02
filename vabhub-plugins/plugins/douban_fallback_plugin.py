"""
豆瓣回退插件 - 当主要数据源不可用时，使用豆瓣作为备用数据源
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from plugin_base import BasePlugin

logger = logging.getLogger(__name__)


class DoubanFallbackPlugin(BasePlugin):
    """豆瓣回退插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "douban_fallback"
        self.version = "1.0.0"
        self.description = "豆瓣数据源回退插件"
        self.enabled = True
        
        # 豆瓣API配置
        self.douban_api_base = "https://api.douban.com/v2"
        self.fallback_priority = ["tmdb", "imdb", "douban"]
        
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化插件"""
        try:
            self.config = config
            self.api_key = config.get("douban_api_key", "")
            self.max_retries = config.get("max_retries", 3)
            self.timeout = config.get("timeout", 10)
            
            logger.info("豆瓣回退插件初始化成功")
            return True
        except Exception as e:
            logger.error(f"豆瓣回退插件初始化失败: {e}")
            return False
    
    async def get_movie_info(self, title: str, year: Optional[int] = None) -> Dict[str, Any]:
        """获取电影信息（豆瓣回退）"""
        try:
            # 首先尝试主要数据源
            primary_result = await self._try_primary_sources(title, year)
            if primary_result:
                return primary_result
            
            # 主要数据源失败，使用豆瓣回退
            return await self._get_douban_movie_info(title, year)
        except Exception as e:
            logger.error(f"获取电影信息失败: {e}")
            return {}
    
    async def get_tv_info(self, title: str, year: Optional[int] = None) -> Dict[str, Any]:
        """获取电视剧信息（豆瓣回退）"""
        try:
            # 首先尝试主要数据源
            primary_result = await self._try_primary_sources(title, year)
            if primary_result:
                return primary_result
            
            # 主要数据源失败，使用豆瓣回退
            return await self._get_douban_tv_info(title, year)
        except Exception as e:
            logger.error(f"获取电视剧信息失败: {e}")
            return {}
    
    async def _try_primary_sources(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """尝试主要数据源"""
        for source in self.fallback_priority:
            if source == "douban":
                continue  # 跳过豆瓣，因为这是回退源
            
            try:
                result = await self._call_primary_api(source, title, year)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"数据源 {source} 失败: {e}")
        
        return None
    
    async def _call_primary_api(self, source: str, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """调用主要API"""
        # 这里应该调用实际的API服务
        # 为了演示，返回空结果
        return None
    
    async def _get_douban_movie_info(self, title: str, year: Optional[int] = None) -> Dict[str, Any]:
        """从豆瓣获取电影信息"""
        try:
            # 模拟豆瓣API调用
            search_url = f"{self.douban_api_base}/movie/search"
            params = {"q": title}
            if year:
                params["year"] = year
            
            # 这里应该使用实际的HTTP请求
            # 为了演示，返回模拟数据
            return {
                "title": title,
                "original_title": title,
                "year": year or 2024,
                "douban_rating": 8.5,
                "genres": ["剧情", "动作"],
                "directors": ["导演"],
                "actors": ["演员1", "演员2"],
                "plot": "电影简介",
                "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2616355133.jpg",
                "source": "douban",
                "is_fallback": True
            }
        except Exception as e:
            logger.error(f"豆瓣电影信息获取失败: {e}")
            return {}
    
    async def _get_douban_tv_info(self, title: str, year: Optional[int] = None) -> Dict[str, Any]:
        """从豆瓣获取电视剧信息"""
        try:
            # 模拟豆瓣API调用
            search_url = f"{self.douban_api_base}/tv/search"
            params = {"q": title}
            if year:
                params["year"] = year
            
            # 这里应该使用实际的HTTP请求
            # 为了演示，返回模拟数据
            return {
                "title": title,
                "original_title": title,
                "year": year or 2024,
                "douban_rating": 8.2,
                "genres": ["剧情", "悬疑"],
                "directors": ["导演"],
                "actors": ["演员1", "演员2"],
                "plot": "电视剧简介",
                "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2616355133.jpg",
                "total_seasons": 1,
                "total_episodes": 12,
                "source": "douban",
                "is_fallback": True
            }
        except Exception as e:
            logger.error(f"豆瓣电视剧信息获取失败: {e}")
            return {}
    
    async def cleanup(self) -> bool:
        """清理资源"""
        logger.info("豆瓣回退插件清理完成")
        return True