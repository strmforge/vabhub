"""
数据提供者基类
"""

import aiohttp
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseProvider(ABC):
    """数据提供者基类"""
    
    def __init__(self):
        self.name = ""
        self.description = ""
    
    @abstractmethod
    async def fetch_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取数据"""
        pass
    
    async def _http_get(self, url: str, headers: Dict[str, str] = None) -> str:
        """HTTP GET请求"""
        headers = headers or {}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    
    async def _http_get_json(self, url: str, headers: Dict[str, str] = None) -> Dict[str, Any]:
        """HTTP GET请求返回JSON"""
        headers = headers or {}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()