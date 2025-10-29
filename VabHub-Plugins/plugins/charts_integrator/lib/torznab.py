"""
Torznab API 客户端
支持 Jackett/Prowlarr 的 Torznab API
"""

import aiohttp
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from urllib.parse import urlencode


class TorznabClient:
    """Torznab API 客户端"""
    
    def __init__(self, endpoints: List[str], timeout: int = 30):
        self.endpoints = endpoints
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search(self, query: str, category: int = None, limit: int = 100) -> List[Dict[str, Any]]:
        """搜索资源"""
        if not self.session:
            async with self:
                return await self.search(query, category, limit)
        
        results = []
        
        for endpoint in self.endpoints:
            try:
                # 构建查询参数
                params = {
                    't': 'search',
                    'q': query,
                    'limit': limit
                }
                
                if category:
                    params['cat'] = category
                
                url = f"{endpoint}&{urlencode(params)}"
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        xml_data = await response.text()
                        endpoint_results = self._parse_torznab_xml(xml_data)
                        results.extend(endpoint_results)
                    else:
                        print(f"Torznab endpoint {endpoint} returned status {response.status}")
                        
            except Exception as e:
                print(f"Error searching endpoint {endpoint}: {e}")
                continue
        
        # 去重并排序（按做种数）
        unique_results = {}
        for result in results:
            key = result.get("Link", "") + result.get("Title", "")
            if key not in unique_results or result.get("Seeders", 0) > unique_results[key].get("Seeders", 0):
                unique_results[key] = result
        
        return sorted(unique_results.values(), key=lambda x: x.get("Seeders", 0), reverse=True)
    
    def _parse_torznab_xml(self, xml_data: str) -> List[Dict[str, Any]]:
        """解析 Torznab XML 响应"""
        try:
            root = ET.fromstring(xml_data)
            results = []
            
            for item in root.findall('.//item'):
                result = {}
                
                # 基本字段
                result["Title"] = item.findtext('title', '')
                result["Link"] = item.findtext('link', '')
                result["Description"] = item.findtext('description', '')
                
                # Torznab 命名空间属性
                for attr in item.findall('.//{http://torznab.com/schemas/2015/feed}attr'):
                    name = attr.get('name', '')
                    value = attr.get('value', '')
                    
                    if name == 'seeders':
                        result["Seeders"] = int(value) if value.isdigit() else 0
                    elif name == 'peers':
                        result["Peers"] = int(value) if value.isdigit() else 0
                    elif name == 'size':
                        result["Size"] = int(value) if value.isdigit() else 0
                    elif name == 'category':
                        result["Category"] = value
                
                # 如果没有找到做种数，尝试从 enclosure 获取
                if "Seeders" not in result:
                    enclosure = item.find('enclosure')
                    if enclosure is not None:
                        result["Size"] = int(enclosure.get('length', 0))
                
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error parsing Torznab XML: {e}")
            return []
    
    async def test_connection(self) -> bool:
        """测试连接"""
        if not self.endpoints:
            return False
        
        try:
            async with self:
                # 简单的搜索测试
                results = await self.search("test", limit=1)
                return len(results) > 0
        except Exception:
            return False