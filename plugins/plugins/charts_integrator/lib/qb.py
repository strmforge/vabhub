"""
qBittorrent Web API 客户端
"""

import aiohttp
import json
from typing import Dict, Any, Optional


class QBClient:
    """qBittorrent Web API 客户端"""
    
    def __init__(self, base_url: str, username: str = "admin", password: str = "adminadmin"):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = None
        self.cookies = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self._login()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _login(self) -> bool:
        """登录 qBittorrent"""
        try:
            login_data = {
                'username': self.username,
                'password': self.password
            }
            
            async with self.session.post(f"{self.base_url}/api/v2/auth/login", data=login_data) as response:
                if response.status == 200:
                    self.cookies = response.cookies
                    return True
                else:
                    print(f"Login failed with status {response.status}")
                    return False
                    
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    async def add_by_url(self, url: str, save_path: str = None, category: str = None) -> bool:
        """通过 URL 添加下载"""
        if not self.session:
            async with self:
                return await self.add_by_url(url, save_path, category)
        
        try:
            data = {
                'urls': url
            }
            
            if save_path:
                data['savepath'] = save_path
            if category:
                data['category'] = category
            
            async with self.session.post(
                f"{self.base_url}/api/v2/torrents/add",
                data=data,
                cookies=self.cookies
            ) as response:
                return response.status == 200
                
        except Exception as e:
            print(f"Error adding torrent: {e}")
            return False
    
    async def get_torrents(self) -> list:
        """获取当前下载列表"""
        if not self.session:
            async with self:
                return await self.get_torrents()
        
        try:
            async with self.session.get(
                f"{self.base_url}/api/v2/torrents/info",
                cookies=self.cookies
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return []
                    
        except Exception as e:
            print(f"Error getting torrents: {e}")
            return []
    
    async def get_categories(self) -> Dict[str, Any]:
        """获取分类列表"""
        if not self.session:
            async with self:
                return await self.get_categories()
        
        try:
            async with self.session.get(
                f"{self.base_url}/api/v2/torrents/categories",
                cookies=self.cookies
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {}
                    
        except Exception as e:
            print(f"Error getting categories: {e}")
            return {}
    
    async def test_connection(self) -> bool:
        """测试连接"""
        try:
            async with self:
                categories = await self.get_categories()
                return isinstance(categories, dict)
        except Exception:
            return False