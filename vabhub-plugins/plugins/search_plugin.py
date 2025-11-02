#!/usr/bin/env python3
"""
搜索插件 - 提供媒体内容搜索功能
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from enum import Enum
from plugin_base import BasePlugin


class SearchSource(Enum):
    """搜索源枚举"""
    LOCAL = "local"
    TMDB = "tmdb"
    DOUBAN = "douban"
    IMDB = "imdb"
    CUSTOM = "custom"


class SearchResult:
    """搜索结果类"""
    
    def __init__(self, result_id: str, title: str, year: Optional[int] = None,
                 media_type: str = "movie", source: SearchSource = SearchSource.TMDB,
                 **kwargs):
        self.result_id = result_id
        self.title = title
        self.year = year
        self.media_type = media_type  # movie, tv, music, etc.
        self.source = source
        self.score = kwargs.get('score', 0.0)
        self.poster = kwargs.get('poster', '')
        self.overview = kwargs.get('overview', '')
        self.external_id = kwargs.get('external_id', '')
        self.metadata = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'result_id': self.result_id,
            'title': self.title,
            'year': self.year,
            'media_type': self.media_type,
            'source': self.source.value,
            'score': self.score,
            'poster': self.poster,
            'overview': self.overview,
            'external_id': self.external_id,
            'metadata': self.metadata
        }


class SearchPlugin(BasePlugin):
    """搜索管理插件"""
    
    name = "search"
    version = "1.0.0"
    description = "提供媒体内容搜索功能"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.search_sources = config.get('sources', ['tmdb', 'douban'])
        self.api_keys = config.get('api_keys', {})
        self.search_history: List[Dict[str, Any]] = []
        self.max_history = config.get('max_history', 100)
    
    def setup(self) -> None:
        """插件初始化"""
        # 初始化搜索源
        self._setup_sources()
        self.logger.info("Search plugin setup completed")
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行搜索操作"""
        operation = data.get('operation', 'search')
        
        if operation == 'search':
            return await self.search_media(
                data.get('query', ''),
                data.get('media_type', 'movie'),
                data.get('sources', None),
                data.get('year', None),
                data.get('limit', 20)
            )
        elif operation == 'get_details':
            return await self.get_media_details(
                data.get('result_id', ''),
                data.get('source', 'tmdb')
            )
        elif operation == 'get_history':
            return await self.get_search_history(
                data.get('limit', 20)
            )
        elif operation == 'clear_history':
            return await self.clear_search_history()
        elif operation == 'get_sources':
            return await self.get_available_sources()
        elif operation == 'test_source':
            return await self.test_search_source(data.get('source', ''))
        else:
            return {'error': f'Unknown operation: {operation}'}
    
    async def search_media(self, query: str, media_type: str = 'movie',
                         sources: List[str] = None, year: Optional[int] = None,
                         limit: int = 20) -> Dict[str, Any]:
        """搜索媒体内容"""
        try:
            if not query:
                return {'error': 'Search query is required'}
            
            # 记录搜索历史
            await self._add_to_history(query, media_type, sources)
            
            # 确定搜索源
            search_sources = sources or self.search_sources
            
            # 并行搜索各个源
            search_tasks = []
            for source in search_sources:
                task = self._search_single_source(query, media_type, source, year, limit)
                search_tasks.append(task)
            
            # 等待所有搜索完成
            results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # 合并结果
            combined_results = []
            for result in results:
                if isinstance(result, Exception):
                    self.logger.error(f"Search failed: {result}")
                    continue
                if result and 'results' in result:
                    combined_results.extend(result['results'])
            
            # 去重和排序
            deduplicated_results = self._deduplicate_results(combined_results)
            sorted_results = self._sort_results(deduplicated_results, query)
            
            # 限制结果数量
            final_results = sorted_results[:limit]
            
            self.logger.info(f"Search completed: '{query}' found {len(final_results)} results")
            return {
                'query': query,
                'media_type': media_type,
                'sources': search_sources,
                'results': final_results,
                'total': len(final_results)
            }
        except Exception as e:
            self.logger.error(f"Search media failed: {e}")
            return {'error': str(e)}
    
    async def get_media_details(self, result_id: str, source: str = 'tmdb') -> Dict[str, Any]:
        """获取媒体详情"""
        try:
            if not result_id:
                return {'error': 'Result ID is required'}
            
            # 根据源获取详情
            if source == 'tmdb':
                details = await self._get_tmdb_details(result_id)
            elif source == 'douban':
                details = await self._get_douban_details(result_id)
            elif source == 'imdb':
                details = await self._get_imdb_details(result_id)
            else:
                return {'error': f'Unsupported source: {source}'}
            
            return {
                'result_id': result_id,
                'source': source,
                'details': details
            }
        except Exception as e:
            self.logger.error(f"Get media details failed: {e}")
            return {'error': str(e)}
    
    async def get_search_history(self, limit: int = 20) -> Dict[str, Any]:
        """获取搜索历史"""
        try:
            # 按时间倒序排列
            sorted_history = sorted(self.search_history, 
                                  key=lambda x: x.get('timestamp', 0), reverse=True)
            
            limited_history = sorted_history[:limit]
            
            return {
                'history': limited_history,
                'total': len(self.search_history),
                'limit': limit
            }
        except Exception as e:
            self.logger.error(f"Get search history failed: {e}")
            return {'error': str(e)}
    
    async def clear_search_history(self) -> Dict[str, Any]:
        """清空搜索历史"""
        try:
            count = len(self.search_history)
            self.search_history.clear()
            
            self.logger.info(f"Cleared {count} search history items")
            return {
                'cleared_count': count,
                'status': 'cleared'
            }
        except Exception as e:
            self.logger.error(f"Clear search history failed: {e}")
            return {'error': str(e)}
    
    async def get_available_sources(self) -> Dict[str, Any]:
        """获取可用的搜索源"""
        try:
            sources_info = []
            
            for source in ['tmdb', 'douban', 'imdb', 'local']:
                source_info = {
                    'name': source,
                    'enabled': source in self.search_sources,
                    'configured': await self._is_source_configured(source)
                }
                sources_info.append(source_info)
            
            return {
                'sources': sources_info,
                'total': len(sources_info)
            }
        except Exception as e:
            self.logger.error(f"Get available sources failed: {e}")
            return {'error': str(e)}
    
    async def test_search_source(self, source: str) -> Dict[str, Any]:
        """测试搜索源"""
        try:
            if source not in ['tmdb', 'douban', 'imdb', 'local']:
                return {'error': f'Unsupported source: {source}'}
            
            # 测试搜索
            test_query = "test"
            test_results = await self._search_single_source(test_query, 'movie', source, None, 1)
            
            return {
                'source': source,
                'status': 'success' if test_results else 'failed',
                'test_query': test_query,
                'results_count': len(test_results.get('results', [])) if test_results else 0
            }
        except Exception as e:
            self.logger.error(f"Test search source failed: {e}")
            return {'error': str(e)}
    
    def _setup_sources(self):
        """设置搜索源"""
        # 这里可以初始化各种搜索源的连接
        # 例如：TMDB API客户端、豆瓣API等
        pass
    
    async def _search_single_source(self, query: str, media_type: str, 
                                  source: str, year: Optional[int], limit: int) -> Dict[str, Any]:
        """在单个源中搜索"""
        try:
            if source == 'tmdb':
                return await self._search_tmdb(query, media_type, year, limit)
            elif source == 'douban':
                return await self._search_douban(query, media_type, year, limit)
            elif source == 'imdb':
                return await self._search_imdb(query, media_type, year, limit)
            elif source == 'local':
                return await self._search_local(query, media_type, limit)
            else:
                return {'error': f'Unsupported source: {source}', 'results': []}
        except Exception as e:
            self.logger.error(f"Search single source failed ({source}): {e}")
            return {'error': str(e), 'results': []}
    
    async def _search_tmdb(self, query: str, media_type: str, year: Optional[int], limit: int) -> Dict[str, Any]:
        """搜索TMDB"""
        # 模拟TMDB搜索
        results = []
        
        # 这里应该调用实际的TMDB API
        # 暂时使用模拟数据
        if "test" not in query.lower():
            for i in range(min(limit, 5)):
                result_id = f"tmdb_{int(time.time())}_{i}"
                result = SearchResult(
                    result_id, f"{query} Result {i+1}", 
                    year or 2020 + i, media_type, SearchSource.TMDB,
                    score=0.9 - i*0.1,
                    overview=f"This is a sample {media_type} description for {query}",
                    external_id=f"tt{1000000 + i}"
                )
                results.append(result.to_dict())
        
        return {'source': 'tmdb', 'results': results}
    
    async def _search_douban(self, query: str, media_type: str, year: Optional[int], limit: int) -> Dict[str, Any]:
        """搜索豆瓣"""
        # 模拟豆瓣搜索
        results = []
        
        # 这里应该调用实际的豆瓣API
        # 暂时使用模拟数据
        if "test" not in query.lower():
            for i in range(min(limit, 5)):
                result_id = f"douban_{int(time.time())}_{i}"
                result = SearchResult(
                    result_id, f"{query} 结果 {i+1}", 
                    year or 2018 + i, media_type, SearchSource.DOUBAN,
                    score=0.85 - i*0.1,
                    overview=f"这是{query}的示例描述",
                    external_id=f"{2000000 + i}"
                )
                results.append(result.to_dict())
        
        return {'source': 'douban', 'results': results}
    
    async def _search_imdb(self, query: str, media_type: str, year: Optional[int], limit: int) -> Dict[str, Any]:
        """搜索IMDB"""
        # 模拟IMDB搜索
        results = []
        
        # 这里应该调用实际的IMDB API
        # 暂时使用模拟数据
        if "test" not in query.lower():
            for i in range(min(limit, 5)):
                result_id = f"imdb_{int(time.time())}_{i}"
                result = SearchResult(
                    result_id, f"{query} Movie {i+1}", 
                    year or 2015 + i, media_type, SearchSource.IMDB,
                    score=0.8 - i*0.1,
                    overview=f"IMDB description for {query}",
                    external_id=f"tt{3000000 + i}"
                )
                results.append(result.to_dict())
        
        return {'source': 'imdb', 'results': results}
    
    async def _search_local(self, query: str, media_type: str, limit: int) -> Dict[str, Any]:
        """搜索本地库"""
        results = []
        
        try:
            # 这里应该搜索本地媒体库
            # 暂时使用模拟数据，但根据媒体类型提供更真实的搜索结果
            
            if media_type == "music":
                # 音乐搜索模拟数据
                music_samples = [
                    {"title": "周杰伦 - 七里香", "artist": "周杰伦", "album": "七里香"},
                    {"title": "林俊杰 - 江南", "artist": "林俊杰", "album": "第二天堂"},
                    {"title": "邓紫棋 - 光年之外", "artist": "邓紫棋", "album": "新的心跳"},
                    {"title": "Taylor Swift - Shake It Off", "artist": "Taylor Swift", "album": "1989"},
                    {"title": "Ed Sheeran - Shape of You", "artist": "Ed Sheeran", "album": "÷"}
                ]
                
                for i, music in enumerate(music_samples):
                    if query.lower() in music["title"].lower() or query.lower() in music["artist"].lower():
                        result_id = f"local_music_{int(time.time())}_{i}"
                        result = SearchResult(
                            result_id, music["title"], 
                            None, media_type, SearchSource.LOCAL,
                            score=1.0 - i*0.1,
                            artist=music["artist"],
                            album=music["album"]
                        )
                        results.append(result.to_dict())
                        
                        if len(results) >= limit:
                            break
                            
            elif media_type == "movie":
                # 电影搜索模拟数据
                movie_samples = [
                    {"title": "肖申克的救赎", "year": 1994},
                    {"title": "阿甘正传", "year": 1994},
                    {"title": "泰坦尼克号", "year": 1997},
                    {"title": "盗梦空间", "year": 2010},
                    {"title": "星际穿越", "year": 2014}
                ]
                
                for i, movie in enumerate(movie_samples):
                    if query.lower() in movie["title"].lower():
                        result_id = f"local_movie_{int(time.time())}_{i}"
                        result = SearchResult(
                            result_id, f"{movie['title']} ({movie['year']})", 
                            None, media_type, SearchSource.LOCAL,
                            score=1.0 - i*0.1,
                            year=movie["year"]
                        )
                        results.append(result.to_dict())
                        
                        if len(results) >= limit:
                            break
            
            else:
                # 其他媒体类型的通用搜索
                for i in range(min(limit, 3)):
                    result_id = f"local_{int(time.time())}_{i}"
                    result = SearchResult(
                        result_id, f"Local {query} {i+1}", 
                        None, media_type, SearchSource.LOCAL,
                        score=1.0 - i*0.2
                    )
                    results.append(result.to_dict())
        
        except Exception as e:
            self.logger.error(f"本地搜索失败: {e}")
        
        return {'source': 'local', 'results': results}
    
    async def _get_tmdb_details(self, result_id: str) -> Dict[str, Any]:
        """获取TMDB详情"""
        # 模拟TMDB详情获取
        return {
            'title': 'Sample Movie',
            'overview': 'This is a sample movie description from TMDB',
            'release_date': '2023-01-01',
            'runtime': 120,
            'genres': ['Action', 'Adventure'],
            'rating': 7.5,
            'poster_path': '/sample_poster.jpg'
        }
    
    async def _get_douban_details(self, result_id: str) -> Dict[str, Any]:
        """获取豆瓣详情"""
        # 模拟豆瓣详情获取
        return {
            'title': '示例电影',
            'overview': '这是来自豆瓣的示例电影描述',
            'release_date': '2023-01-01',
            'runtime': 120,
            'genres': ['动作', '冒险'],
            'rating': 8.0,
            'poster_path': '/sample_poster_cn.jpg'
        }
    
    async def _get_imdb_details(self, result_id: str) -> Dict[str, Any]:
        """获取IMDB详情"""
        # 模拟IMDB详情获取
        return {
            'title': 'Sample Movie',
            'overview': 'This is a sample movie description from IMDB',
            'release_date': '2023-01-01',
            'runtime': 120,
            'genres': ['Action', 'Adventure'],
            'rating': 7.2,
            'poster_path': '/sample_poster_imdb.jpg'
        }
    
    async def _is_source_configured(self, source: str) -> bool:
        """检查搜索源是否已配置"""
        if source == 'local':
            return True  # 本地搜索总是可用
        
        # 检查API密钥配置
        required_keys = {
            'tmdb': ['tmdb_api_key'],
            'douban': ['douban_api_key'],
            'imdb': ['imdb_api_key']
        }
        
        if source in required_keys:
            for key in required_keys[source]:
                if key not in self.api_keys or not self.api_keys[key]:
                    return False
            return True
        
        return False
    
    async def _add_to_history(self, query: str, media_type: str, sources: List[str] = None):
        """添加到搜索历史"""
        history_item = {
            'query': query,
            'media_type': media_type,
            'sources': sources or self.search_sources,
            'timestamp': time.time()
        }
        
        self.search_history.append(history_item)
        
        # 限制历史记录数量
        if len(self.search_history) > self.max_history:
            self.search_history = self.search_history[-self.max_history:]
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去重搜索结果"""
        seen_titles = set()
        deduplicated = []
        
        for result in results:
            title_key = f"{result.get('title', '')}_{result.get('year', '')}"
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                deduplicated.append(result)
        
        return deduplicated
    
    def _sort_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """排序搜索结果"""
        # 按分数排序
        return sorted(results, key=lambda x: x.get('score', 0), reverse=True)
    
    def health_check(self) -> bool:
        """健康检查"""
        try:
            # 检查基本配置
            if not isinstance(self.search_sources, list):
                return False
            
            # 检查历史记录数量是否在合理范围内
            if len(self.search_history) > self.max_history * 2:
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def cleanup(self) -> None:
        """清理资源"""
        # 清理搜索历史
        self.search_history.clear()
        self.logger.info("Search plugin cleanup completed")