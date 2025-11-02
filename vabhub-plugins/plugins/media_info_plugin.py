#!/usr/bin/env python3
"""
媒体信息插件 - 获取电影、电视剧的详细信息
"""

import httpx
import asyncio
from typing import Dict, Any, List, Optional
from plugin_base import BasePlugin


class MediaInfoPlugin(BasePlugin):
    """媒体信息插件"""
    
    name = "media_info"
    version = "1.0.0"
    description = "获取电影、电视剧的详细信息"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.tmdb_api_key = config.get('tmdb_api_key', '')
        self.douban_api_key = config.get('douban_api_key', '')
        self.client = httpx.AsyncClient()
    
    def setup(self) -> None:
        """插件初始化"""
        self.logger.info("MediaInfo plugin setup completed")
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行媒体信息查询"""
        operation = data.get('operation', 'search')
        
        if operation == 'search':
            return await self.search_media(data.get('query', ''))
        elif operation == 'get_details':
            return await self.get_media_details(data.get('media_id', ''), data.get('media_type', 'movie'))
        elif operation == 'get_trending':
            return await self.get_trending_media(data.get('media_type', 'movie'))
        else:
            return {'error': f'Unknown operation: {operation}'}
    
    async def search_media(self, query: str) -> Dict[str, Any]:
        """搜索媒体"""
        try:
            # 尝试从TMDB搜索
            tmdb_results = await self._search_tmdb(query)
            
            # 尝试从豆瓣搜索
            douban_results = await self._search_douban(query)
            
            return {
                'query': query,
                'tmdb_results': tmdb_results,
                'douban_results': douban_results,
                'total_results': len(tmdb_results.get('results', [])) + len(douban_results.get('results', []))
            }
        except Exception as e:
            self.logger.error(f"Search media failed: {e}")
            return {'error': str(e)}
    
    async def get_media_details(self, media_id: str, media_type: str = 'movie') -> Dict[str, Any]:
        """获取媒体详细信息"""
        try:
            details = {}
            
            # 从TMDB获取详细信息
            if self.tmdb_api_key:
                tmdb_details = await self._get_tmdb_details(media_id, media_type)
                details['tmdb'] = tmdb_details
            
            # 从豆瓣获取详细信息
            if self.douban_api_key:
                douban_details = await self._get_douban_details(media_id, media_type)
                details['douban'] = douban_details
            
            return {
                'media_id': media_id,
                'media_type': media_type,
                'details': details
            }
        except Exception as e:
            self.logger.error(f"Get media details failed: {e}")
            return {'error': str(e)}
    
    async def get_trending_media(self, media_type: str = 'movie') -> Dict[str, Any]:
        """获取热门媒体"""
        try:
            trending = {}
            
            # 从TMDB获取热门内容
            if self.tmdb_api_key:
                tmdb_trending = await self._get_tmdb_trending(media_type)
                trending['tmdb'] = tmdb_trending
            
            # 从豆瓣获取热门内容
            if self.douban_api_key:
                douban_trending = await self._get_douban_trending(media_type)
                trending['douban'] = douban_trending
            
            return {
                'media_type': media_type,
                'trending': trending
            }
        except Exception as e:
            self.logger.error(f"Get trending media failed: {e}")
            return {'error': str(e)}
    
    async def _search_tmdb(self, query: str) -> Dict[str, Any]:
        """从TMDB搜索"""
        if not self.tmdb_api_key:
            return {'results': [], 'total': 0}
        
        try:
            url = f"https://api.themoviedb.org/3/search/multi"
            params = {
                'api_key': self.tmdb_api_key,
                'query': query,
                'language': 'zh-CN'
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'results': data.get('results', []),
                'total': data.get('total_results', 0)
            }
        except Exception as e:
            self.logger.error(f"TMDB search failed: {e}")
            return {'results': [], 'total': 0, 'error': str(e)}
    
    async def _search_douban(self, query: str) -> Dict[str, Any]:
        """从豆瓣搜索"""
        if not self.douban_api_key:
            return {'results': [], 'total': 0}
        
        try:
            url = f"https://api.douban.com/v2/movie/search"
            params = {
                'apikey': self.douban_api_key,
                'q': query
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'results': data.get('subjects', []),
                'total': data.get('total', 0)
            }
        except Exception as e:
            self.logger.error(f"Douban search failed: {e}")
            return {'results': [], 'total': 0, 'error': str(e)}
    
    async def _get_tmdb_details(self, media_id: str, media_type: str) -> Dict[str, Any]:
        """从TMDB获取详细信息"""
        if not self.tmdb_api_key:
            return {}
        
        try:
            url = f"https://api.themoviedb.org/3/{media_type}/{media_id}"
            params = {
                'api_key': self.tmdb_api_key,
                'language': 'zh-CN',
                'append_to_response': 'credits,videos,images'
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            self.logger.error(f"TMDB details failed: {e}")
            return {'error': str(e)}
    
    async def _get_douban_details(self, media_id: str, media_type: str) -> Dict[str, Any]:
        """从豆瓣获取详细信息"""
        if not self.douban_api_key:
            return {}
        
        try:
            # 豆瓣API根据媒体类型使用不同的端点
            if media_type == 'movie':
                url = f"https://api.douban.com/v2/movie/subject/{media_id}"
            else:
                url = f"https://api.douban.com/v2/tv/subject/{media_id}"
            
            params = {'apikey': self.douban_api_key}
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            self.logger.error(f"Douban details failed: {e}")
            return {'error': str(e)}
    
    async def _get_tmdb_trending(self, media_type: str) -> Dict[str, Any]:
        """从TMDB获取热门内容"""
        if not self.tmdb_api_key:
            return {'results': []}
        
        try:
            url = f"https://api.themoviedb.org/3/trending/{media_type}/week"
            params = {
                'api_key': self.tmdb_api_key,
                'language': 'zh-CN'
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'results': data.get('results', []),
                'total': len(data.get('results', []))
            }
        except Exception as e:
            self.logger.error(f"TMDB trending failed: {e}")
            return {'results': [], 'error': str(e)}
    
    async def _get_douban_trending(self, media_type: str) -> Dict[str, Any]:
        """从豆瓣获取热门内容"""
        if not self.douban_api_key:
            return {'results': []}
        
        try:
            # 豆瓣热门电影
            if media_type == 'movie':
                url = "https://api.douban.com/v2/movie/in_theaters"
            else:
                url = "https://api.douban.com/v2/tv/search"
            
            params = {'apikey': self.douban_api_key}
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'results': data.get('subjects', []),
                'total': len(data.get('subjects', []))
            }
        except Exception as e:
            self.logger.error(f"Douban trending failed: {e}")
            return {'results': [], 'error': str(e)}
    
    def health_check(self) -> bool:
        """健康检查"""
        try:
            # 检查API密钥配置
            if not self.tmdb_api_key and not self.douban_api_key:
                self.logger.warning("No API keys configured")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    async def cleanup(self) -> None:
        """清理资源"""
        await self.client.aclose()
        self.logger.info("MediaInfo plugin cleanup completed")