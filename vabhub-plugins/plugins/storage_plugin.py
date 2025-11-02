"""
存储插件 - 文件存储和资源管理
"""

from typing import Dict, Any, List
import os

class StoragePlugin:
    """存储插件类"""
    
    def __init__(self):
        self.name = "存储插件"
        self.version = "1.1.0"
        self.enabled = True
        self.description = "文件存储和资源管理"
        self.storage_path = "./storage"
    
    def initialize(self) -> Dict[str, Any]:
        """初始化插件"""
        # 创建存储目录
        os.makedirs(self.storage_path, exist_ok=True)
        return {
            "status": "initialized",
            "message": "存储插件已初始化",
            "storage_path": self.storage_path
        }
    
    def save_file(self, filename: str, content: bytes) -> Dict[str, Any]:
        """保存文件"""
        filepath = os.path.join(self.storage_path, filename)
        with open(filepath, 'wb') as f:
            f.write(content)
        return {
            "saved": True,
            "filename": filename,
            "filepath": filepath,
            "size": len(content)
        }
    
    def list_files(self) -> List[Dict[str, Any]]:
        """列出文件"""
        files = []
        for filename in os.listdir(self.storage_path):
            filepath = os.path.join(self.storage_path, filename)
            if os.path.isfile(filepath):
                files.append({
                    "filename": filename,
                    "size": os.path.getsize(filepath),
                    "modified": os.path.getmtime(filepath)
                })
        return files
    
    def get_info(self) -> Dict[str, Any]:
        """获取插件信息"""
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "description": self.description,
            "storage_path": self.storage_path
        }