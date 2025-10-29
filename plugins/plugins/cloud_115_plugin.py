#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
115网盘云存储插件
"""

import requests
from typing import List, Dict, Any
from pathlib import Path

from core.plugin_base import CloudSource


class Cloud115Plugin(CloudSource):
    """115网盘云存储插件"""
    
    name = "115"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://webapi.115.com"
        self.cookie = ""
        self.user_id = ""
    
    def initialize(self) -> bool:
        """初始化插件"""
        # 从配置获取cookie
        from core.config_loader import get_config_loader
        config = get_config_loader()
        
        plugin_configs = config.get_plugin_config('cloud')
        for plugin_config in plugin_configs:
            if plugin_config.get('name') == '115':
                self.cookie = plugin_config.get('cookie', '')
                break
        
        if not self.cookie:
            print("警告: 115网盘cookie未配置")
            return False
        
        # 验证cookie有效性
        return self._verify_cookie()
    
    def _verify_cookie(self) -> bool:
        """验证cookie有效性"""
        try:
            response = requests.get(
                f"{self.base_url}/files",
                headers={
                    'Cookie': self.cookie,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            return response.status_code == 200
        except Exception as e:
            print(f"115网盘cookie验证失败: {e}")
            return False
    
    def walk(self, base_path: str = "/") -> List[str]:
        """遍历云存储目录"""
        try:
            # 获取目录文件列表
            response = requests.post(
                f"{self.base_url}/files",
                data={
                    'aid': 1,
                    'cid': self._get_cid(base_path),
                    'o': 'file_name',
                    'asc': 1,
                    'offset': 0,
                    'show_dir': 1,
                    'limit': 1000
                },
                headers={
                    'Cookie': self.cookie,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                files = data.get('data', [])
                
                file_paths = []
                for file_info in files:
                    file_path = f"{base_path.rstrip('/')}/{file_info.get('n')}"
                    file_paths.append(file_path)
                    
                    # 如果是目录，递归遍历
                    if file_info.get('ico') == 'folder':
                        sub_files = self.walk(file_path)
                        file_paths.extend(sub_files)
                
                return file_paths
            
            return []
            
        except Exception as e:
            print(f"115网盘遍历失败: {e}")
            return []
    
    def download(self, remote_path: str, local_path: str) -> bool:
        """下载文件"""
        try:
            # 获取下载链接
            download_url = self._get_download_url(remote_path)
            if not download_url:
                return False
            
            # 下载文件
            response = requests.get(
                download_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://115.com'
                },
                stream=True
            )
            
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            
            return False
            
        except Exception as e:
            print(f"115网盘下载失败: {e}")
            return False
    
    def upload(self, local_path: str, remote_path: str) -> bool:
        """上传文件"""
        try:
            # 获取上传参数
            upload_info = self._get_upload_info(remote_path)
            if not upload_info:
                return False
            
            # 分片上传（大文件）
            file_size = Path(local_path).stat().st_size
            if file_size > 100 * 1024 * 1024:  # 100MB以上分片
                return self._chunked_upload(local_path, upload_info)
            else:
                # 直接上传
                return self._direct_upload(local_path, upload_info)
            
        except Exception as e:
            print(f"115网盘上传失败: {e}")
            return False
    
    def _get_cid(self, path: str) -> str:
        """获取路径对应的CID"""
        # 根目录CID为0
        if path == "/":
            return "0"
        
        # 这里需要实现路径到CID的映射
        # 简化实现：返回固定值
        return "0"
    
    def _get_download_url(self, remote_path: str) -> str:
        """获取文件下载链接"""
        try:
            response = requests.post(
                f"{self.base_url}/files/download",
                data={
                    'pickcode': self._get_pickcode(remote_path)
                },
                headers={
                    'Cookie': self.cookie,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('file_url', '')
            
            return ""
            
        except Exception as e:
            print(f"获取下载链接失败: {e}")
            return ""
    
    def _get_pickcode(self, remote_path: str) -> str:
        """获取文件的pickcode"""
        # 这里需要实现根据路径获取pickcode的逻辑
        # 简化实现：返回空字符串
        return ""
    
    def _get_upload_info(self, remote_path: str) -> Dict[str, Any]:
        """获取上传信息"""
        try:
            response = requests.post(
                f"{self.base_url}/files/upload_info",
                headers={
                    'Cookie': self.cookie,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code == 200:
                return response.json()
            
            return {}
            
        except Exception as e:
            print(f"获取上传信息失败: {e}")
            return {}
    
    def _direct_upload(self, local_path: str, upload_info: Dict[str, Any]) -> bool:
        """直接上传"""
        try:
            with open(local_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    upload_info.get('url', ''),
                    files=files,
                    data=upload_info.get('params', {}),
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"直接上传失败: {e}")
            return False
    
    def _chunked_upload(self, local_path: str, upload_info: Dict[str, Any]) -> bool:
        """分片上传"""
        # 简化实现：调用直接上传
        return self._direct_upload(local_path, upload_info)
    
    def cleanup(self) -> None:
        """清理资源"""
        pass