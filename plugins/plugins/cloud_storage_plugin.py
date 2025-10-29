#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云存储插件
支持多种云存储服务
"""

import os
import boto3
from aliyunsdkcore.client import AcsClient
from aliyunsdkoss.request.v20190517 import GetObjectRequest
from tencentcloud.common import credential
from tencentcloud.cos import CosS3Client
from typing import List, Dict, Any, Optional
from pathlib import Path

from core.plugin_base import CloudSource


class AWSS3Plugin(CloudSource):
    """AWS S3 云存储插件"""
    
    name = "aws_s3"
    version = "1.0.0"
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.s3_client = None
        self.bucket_name = self.config.get('bucket_name', '')
    
    def initialize(self) -> bool:
        """初始化AWS S3客户端"""
        try:
            aws_access_key = self.config.get('aws_access_key_id')
            aws_secret_key = self.config.get('aws_secret_access_key')
            region_name = self.config.get('region_name', 'us-east-1')
            
            if not aws_access_key or not aws_secret_key:
                print("AWS S3配置不完整")
                return False
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region_name
            )
            
            # 测试连接
            try:
                self.s3_client.list_buckets()
                print(f"AWS S3插件初始化成功，Bucket: {self.bucket_name}")
                return True
            except Exception as e:
                print(f"AWS S3连接测试失败: {e}")
                return False
                
        except Exception as e:
            print(f"AWS S3插件初始化失败: {e}")
            return False
    
    def walk(self, base_path: str = "") -> List[str]:
        """遍历S3存储桶"""
        if not self.s3_client or not self.bucket_name:
            return []
        
        try:
            objects = []
            paginator = self.s3_client.get_paginator('list_objects_v2')
            
            for page in paginator.paginate(Bucket=self.bucket_name, Prefix=base_path):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        objects.append(obj['Key'])
            
            return objects
            
        except Exception as e:
            print(f"遍历S3存储桶失败: {e}")
            return []
    
    def download(self, remote_path: str, local_path: str) -> bool:
        """从S3下载文件"""
        if not self.s3_client or not self.bucket_name:
            return False
        
        try:
            # 确保本地目录存在
            local_dir = Path(local_path).parent
            local_dir.mkdir(parents=True, exist_ok=True)
            
            self.s3_client.download_file(self.bucket_name, remote_path, local_path)
            print(f"下载成功: {remote_path} -> {local_path}")
            return True
            
        except Exception as e:
            print(f"下载文件失败: {e}")
            return False
    
    def upload(self, local_path: str, remote_path: str) -> bool:
        """上传文件到S3"""
        if not self.s3_client or not self.bucket_name:
            return False
        
        try:
            if not os.path.exists(local_path):
                print(f"本地文件不存在: {local_path}")
                return False
            
            self.s3_client.upload_file(local_path, self.bucket_name, remote_path)
            print(f"上传成功: {local_path} -> {remote_path}")
            return True
            
        except Exception as e:
            print(f"上传文件失败: {e}")
            return False
    
    def cleanup(self) -> None:
        """清理资源"""
        self.s3_client = None


class AliyunOSSPlugin(CloudSource):
    """阿里云OSS插件"""
    
    name = "aliyun_oss"
    version = "1.0.0"
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.oss_client = None
        self.bucket_name = self.config.get('bucket_name', '')
    
    def initialize(self) -> bool:
        """初始化阿里云OSS客户端"""
        try:
            access_key = self.config.get('access_key_id')
            secret_key = self.config.get('access_key_secret')
            endpoint = self.config.get('endpoint', 'oss-cn-hangzhou.aliyuncs.com')
            
            if not access_key or not secret_key:
                print("阿里云OSS配置不完整")
                return False
            
            self.oss_client = AcsClient(access_key, secret_key, endpoint)
            print(f"阿里云OSS插件初始化成功，Bucket: {self.bucket_name}")
            return True
            
        except Exception as e:
            print(f"阿里云OSS插件初始化失败: {e}")
            return False
    
    def walk(self, base_path: str = "") -> List[str]:
        """遍历OSS存储桶"""
        # 简化实现，实际需要调用OSS API
        return []
    
    def download(self, remote_path: str, local_path: str) -> bool:
        """从OSS下载文件"""
        # 简化实现，实际需要调用OSS API
        return False
    
    def upload(self, local_path: str, remote_path: str) -> bool:
        """上传文件到OSS"""
        # 简化实现，实际需要调用OSS API
        return False
    
    def cleanup(self) -> None:
        """清理资源"""
        self.oss_client = None


class TencentCOSPlugin(CloudSource):
    """腾讯云COS插件"""
    
    name = "tencent_cos"
    version = "1.0.0"
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.cos_client = None
        self.bucket_name = self.config.get('bucket_name', '')
    
    def initialize(self) -> bool:
        """初始化腾讯云COS客户端"""
        try:
            secret_id = self.config.get('secret_id')
            secret_key = self.config.get('secret_key')
            region = self.config.get('region', 'ap-beijing')
            
            if not secret_id or not secret_key:
                print("腾讯云COS配置不完整")
                return False
            
            cred = credential.Credential(secret_id, secret_key)
            self.cos_client = CosS3Client(cred, region)
            print(f"腾讯云COS插件初始化成功，Bucket: {self.bucket_name}")
            return True
            
        except Exception as e:
            print(f"腾讯云COS插件初始化失败: {e}")
            return False
    
    def walk(self, base_path: str = "") -> List[str]:
        """遍历COS存储桶"""
        # 简化实现，实际需要调用COS API
        return []
    
    def download(self, remote_path: str, local_path: str) -> bool:
        """从COS下载文件"""
        # 简化实现，实际需要调用COS API
        return False
    
    def upload(self, local_path: str, remote_path: str) -> bool:
        """上传文件到COS"""
        # 简化实现，实际需要调用COS API
        return False
    
    def cleanup(self) -> None:
        """清理资源"""
        self.cos_client = None


# 插件注册装饰器
def register_cloud_plugin(plugin_class):
    """云存储插件注册装饰器"""
    from core.plugin_base import register_plugin
    return register_plugin(plugin_class)


# 注册插件
@register_cloud_plugin
class LocalStoragePlugin(CloudSource):
    """本地存储插件（用于测试）"""
    
    name = "local_storage"
    version = "1.0.0"
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.base_path = self.config.get('base_path', '/tmp')
    
    def initialize(self) -> bool:
        """初始化本地存储"""
        try:
            if not os.path.exists(self.base_path):
                os.makedirs(self.base_path, exist_ok=True)
            print(f"本地存储插件初始化成功，路径: {self.base_path}")
            return True
        except Exception as e:
            print(f"本地存储插件初始化失败: {e}")
            return False
    
    def walk(self, base_path: str = "") -> List[str]:
        """遍历本地目录"""
        try:
            full_path = os.path.join(self.base_path, base_path)
            if not os.path.exists(full_path):
                return []
            
            files = []
            for root, dirs, filenames in os.walk(full_path):
                for filename in filenames:
                    rel_path = os.path.relpath(os.path.join(root, filename), self.base_path)
                    files.append(rel_path)
            
            return files
            
        except Exception as e:
            print(f"遍历本地目录失败: {e}")
            return []
    
    def download(self, remote_path: str, local_path: str) -> bool:
        """本地文件复制（模拟下载）"""
        try:
            source_path = os.path.join(self.base_path, remote_path)
            if not os.path.exists(source_path):
                return False
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # 复制文件
            import shutil
            shutil.copy2(source_path, local_path)
            print(f"文件复制成功: {source_path} -> {local_path}")
            return True
            
        except Exception as e:
            print(f"文件复制失败: {e}")
            return False
    
    def upload(self, local_path: str, remote_path: str) -> bool:
        """本地文件复制（模拟上传）"""
        try:
            if not os.path.exists(local_path):
                return False
            
            target_path = os.path.join(self.base_path, remote_path)
            # 确保目标目录存在
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # 复制文件
            import shutil
            shutil.copy2(local_path, target_path)
            print(f"文件复制成功: {local_path} -> {target_path}")
            return True
            
        except Exception as e:
            print(f"文件复制失败: {e}")
            return False
    
    def cleanup(self) -> None:
        """清理资源"""
        pass