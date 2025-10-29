#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MusicBrainz音乐元数据插件
"""

import requests
from typing import Dict, Any, Optional
from pathlib import Path

from core.plugin_base import MusicMetadataProvider


class MusicBrainzPlugin(MusicMetadataProvider):
    """MusicBrainz音乐元数据插件"""
    
    name = "musicbrainz"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://musicbrainz.org/ws/2"
        self.user_agent = "StrataMedia/2.0.0 (you@example.com)"
    
    def initialize(self) -> bool:
        """初始化插件"""
        try:
            # 测试连接
            response = requests.get(
                f"{self.base_url}/artist/query?fmt=json&limit=1",
                headers={'User-Agent': self.user_agent}
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def search_track(self, artist: str, title: str, album: Optional[str] = None) -> Dict[str, Any]:
        """搜索音乐轨道"""
        try:
            # 构建查询
            query_parts = []
            if artist:
                query_parts.append(f"artist:{artist}")
            if title:
                query_parts.append(f"recording:{title}")
            if album:
                query_parts.append(f"release:{album}")
            
            query = " AND ".join(query_parts)
            
            response = requests.get(
                f"{self.base_url}/recording",
                params={
                    'query': query,
                    'fmt': 'json',
                    'limit': 5
                },
                headers={'User-Agent': self.user_agent}
            )
            
            if response.status_code == 200:
                data = response.json()
                recordings = data.get('recordings', [])
                
                if recordings:
                    # 返回最佳匹配
                    best_match = recordings[0]
                    return self._parse_recording(best_match)
            
            return {}
            
        except Exception as e:
            print(f"MusicBrainz搜索失败: {e}")
            return {}
    
    def get_audio_fingerprint(self, file_path: str) -> Optional[str]:
        """获取音频指纹（需要pyacoustid）"""
        try:
            import acoustid
            
            # 计算音频指纹
            duration, fingerprint = acoustid.fingerprint_file(file_path)
            return fingerprint
            
        except ImportError:
            print("警告: pyacoustid未安装，无法生成音频指纹")
            return None
        except Exception as e:
            print(f"音频指纹生成失败: {e}")
            return None
    
    def lookup_by_fingerprint(self, fingerprint: str) -> Dict[str, Any]:
        """通过指纹查找音乐"""
        try:
            import acoustid
            
            # 使用AcoustID服务查找
            results = acoustid.lookup(
                'YOUR_ACOUSTID_API_KEY',  # 需要申请API密钥
                fingerprint,
                meta='recordings releases'
            )
            
            if results:
                best_result = results[0]
                return self._parse_acoustid_result(best_result)
            
            return {}
            
        except Exception as e:
            print(f"指纹查找失败: {e}")
            return {}
    
    def _parse_recording(self, recording: Dict[str, Any]) -> Dict[str, Any]:
        """解析录音信息"""
        metadata = {
            'title': recording.get('title'),
            'artist': recording.get('artist-credit', [{}])[0].get('artist', {}).get('name'),
            'album': recording.get('releases', [{}])[0].get('title') if recording.get('releases') else None,
            'year': recording.get('releases', [{}])[0].get('date') if recording.get('releases') else None,
            'genre': recording.get('tags', [{}])[0].get('name') if recording.get('tags') else None,
            'mbid': recording.get('id'),
            'duration': recording.get('length'),
            'source': 'musicbrainz'
        }
        
        # 清理空值
        return {k: v for k, v in metadata.items() if v is not None}
    
    def _parse_acoustid_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """解析AcoustID结果"""
        recordings = result.get('recordings', [])
        if not recordings:
            return {}
        
        recording = recordings[0]
        return {
            'title': recording.get('title'),
            'artist': recording.get('artists', [{}])[0].get('name'),
            'album': recording.get('releasegroups', [{}])[0].get('title'),
            'mbid': recording.get('id'),
            'source': 'acoustid'
        }
    
    def cleanup(self) -> None:
        """清理资源"""
        pass