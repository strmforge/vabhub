#!/usr/bin/env python3
"""
站点支持插件
支持多个PT站点的自动搜索和下载功能
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urlencode

class SiteSupport:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sites = self.load_sites()
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        })
    
    def load_sites(self) -> List[Dict]:
        """加载支持的站点配置"""
        try:
            with open('sites_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_sites()
    
    def _get_default_sites(self) -> List[Dict]:
        """获取默认支持的站点"""
        return [
            {
                "id": "mteam",
                "name": "M-Team",
                "url": "https://tp.m-team.cc",
                "enabled": True,
                "api_key": "",
                "search_endpoint": "/api/torrent/search",
                "categories": ["movie", "tv", "music"]
            },
            {
                "id": "hdchina",
                "name": "HDChina",
                "url": "https://hdchina.org",
                "enabled": True,
                "api_key": "",
                "search_endpoint": "/api.php",
                "categories": ["movie", "tv"]
            },
            {
                "id": "ttg",
                "name": "TTG",
                "url": "https://totheglory.im",
                "enabled": True,
                "api_key": "",
                "search_endpoint": "/json.php",
                "categories": ["movie", "tv", "game"]
            }
        ]
    
    def search_torrents(self, query: str, category: str = "", site_id: str = "") -> List[Dict]:
        """搜索种子"""
        results = []
        
        for site in self.sites:
            if not site['enabled']:
                continue
            
            if site_id and site['id'] != site_id:
                continue
            
            if category and category not in site.get('categories', []):
                continue
            
            try:
                site_results = self._search_site(site, query, category)
                results.extend(site_results)
                
                # 避免请求过快
                time.sleep(0.5)
                
            except Exception as e:
                print(f"搜索站点 {site['name']} 失败: {e}")
        
        # 按种子数量排序
        results.sort(key=lambda x: x.get('seeders', 0), reverse=True)
        return results
    
    def _search_site(self, site: Dict, query: str, category: str) -> List[Dict]:
        """搜索单个站点"""
        # 这里实现具体的站点搜索逻辑
        # 由于不同站点的API不同，这里提供通用模板
        
        search_params = {
            'search': query,
            'category': category,
            'api_key': site.get('api_key', '')
        }
        
        # 构建请求URL
        url = f"{site['url']}{site['search_endpoint']}"
        
        try:
            response = self.session.get(url, params=search_params, timeout=10)
            response.raise_for_status()
            
            # 解析响应数据
            data = response.json()
            return self._parse_site_response(site['id'], data)
            
        except requests.RequestException as e:
            print(f"请求站点 {site['name']} 失败: {e}")
            return []
    
    def _parse_site_response(self, site_id: str, data: Dict) -> List[Dict]:
        """解析站点响应数据"""
        # 这里根据不同的站点格式进行解析
        # 返回标准化的种子信息
        
        torrents = []
        
        if site_id == "mteam":
            # M-Team格式解析
            for item in data.get('data', []):
                torrent = {
                    'site_id': site_id,
                    'torrent_id': item.get('id'),
                    'title': item.get('name'),
                    'size': item.get('size'),
                    'seeders': item.get('seeders', 0),
                    'leechers': item.get('leechers', 0),
                    'download_url': item.get('download_url'),
                    'category': item.get('category'),
                    'upload_time': item.get('upload_time'),
                    'free': item.get('freeleech', False)
                }
                torrents.append(torrent)
        
        elif site_id == "hdchina":
            # HDChina格式解析
            for item in data.get('torrents', []):
                torrent = {
                    'site_id': site_id,
                    'torrent_id': item.get('id'),
                    'title': item.get('name'),
                    'size': item.get('size'),
                    'seeders': item.get('seeders', 0),
                    'leechers': item.get('leechers', 0),
                    'download_url': item.get('download_link'),
                    'category': item.get('category'),
                    'upload_time': item.get('added'),
                    'free': item.get('free', False)
                }
                torrents.append(torrent)
        
        else:
            # 通用格式解析
            for item in data.get('data', data.get('torrents', [])):
                torrent = {
                    'site_id': site_id,
                    'torrent_id': item.get('id'),
                    'title': item.get('title') or item.get('name'),
                    'size': item.get('size'),
                    'seeders': item.get('seeders', 0),
                    'leechers': item.get('leechers', 0),
                    'download_url': item.get('download_url') or item.get('download_link'),
                    'category': item.get('category'),
                    'upload_time': item.get('upload_time') or item.get('added'),
                    'free': item.get('freeleech') or item.get('free', False)
                }
                torrents.append(torrent)
        
        return torrents
    
    def download_torrent(self, site_id: str, torrent_id: str, download_path: str = "") -> bool:
        """下载种子文件"""
        site = next((s for s in self.sites if s['id'] == site_id), None)
        if not site or not site['enabled']:
            return False
        
        try:
            # 构建下载URL
            download_url = f"{site['url']}/api/torrent/download/{torrent_id}"
            
            # 添加API密钥
            params = {'apikey': site.get('api_key', '')}
            
            response = self.session.get(download_url, params=params, timeout=30)
            response.raise_for_status()
            
            # 保存种子文件
            filename = f"{site_id}_{torrent_id}.torrent"
            if download_path:
                filename = f"{download_path}/{filename}"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"种子下载成功: {filename}")
            return True
            
        except Exception as e:
            print(f"下载种子失败: {e}")
            return False
    
    def get_site_status(self, site_id: str = "") -> Dict[str, Any]:
        """获取站点状态"""
        status = {}
        
        for site in self.sites:
            if site_id and site['id'] != site_id:
                continue
            
            try:
                # 测试站点连通性
                test_url = f"{site['url']}/api/test"
                response = self.session.get(test_url, timeout=5)
                
                status[site['id']] = {
                    'name': site['name'],
                    'enabled': site['enabled'],
                    'online': response.status_code == 200,
                    'last_check': datetime.now().isoformat()
                }
                
            except Exception as e:
                status[site['id']] = {
                    'name': site['name'],
                    'enabled': site['enabled'],
                    'online': False,
                    'error': str(e),
                    'last_check': datetime.now().isoformat()
                }
        
        return status
    
    def update_site_config(self, site_id: str, updates: Dict) -> bool:
        """更新站点配置"""
        for site in self.sites:
            if site['id'] == site_id:
                site.update(updates)
                self._save_sites_config()
                return True
        return False
    
    def _save_sites_config(self):
        """保存站点配置"""
        with open('sites_config.json', 'w', encoding='utf-8') as f:
            json.dump(self.sites, f, ensure_ascii=False, indent=2)

# 插件主函数
def main():
    # 示例配置
    config = {
        "max_concurrent_searches": 3,
        "request_timeout": 10,
        "retry_count": 3,
        "cache_duration": 300
    }
    
    plugin = SiteSupport(config)
    
    # 示例：搜索种子
    results = plugin.search_torrents("Inception", "movie")
    print(f"找到 {len(results)} 个种子")
    
    # 示例：获取站点状态
    status = plugin.get_site_status()
    print("站点状态:", status)
    
    return plugin

if __name__ == "__main__":
    main()