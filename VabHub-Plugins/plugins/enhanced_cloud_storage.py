#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版云存储插件
支持AWS S3、阿里云OSS、腾讯云COS等多种云存储服务
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import boto3
import oss2
from qcloud_cos import CosConfig, CosS3Client

from core.plugin_base import PluginBase

logger = logging.getLogger(__name__)

class EnhancedCloudStoragePlugin(PluginBase):
    """增强版云存储插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "enhanced_cloud_storage"
        self.version = "2.0.0"
        self.description = "增强版云存储插件 - 支持多平台云存储服务"
        self.author = "VabHub Team"
        
        # 云存储客户端
        self.s3_clients = {}
        self.oss_clients = {}
        self.cos_clients = {}
        
        # 配置
        self.config_file = Path("config/cloud_storage.json")
        self.config = self._load_config()
        
        # 统计信息
        self.stats = {
            "total_uploads": 0,
            "total_downloads": 0,
            "total_size_uploaded": 0,
            "total_size_downloaded": 0,
            "failed_operations": 0
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "aws": {
                "enabled": False,
                "access_key": "",
                "secret_key": "",
                "region": "us-east-1",
                "buckets": {}
            },
            "aliyun": {
                "enabled": False,
                "access_key": "",
                "secret_key": "",
                "endpoint": "oss-cn-hangzhou.aliyuncs.com",
                "buckets": {}
            },
            "tencent": {
                "enabled": False,
                "secret_id": "",
                "secret_key": "",
                "region": "ap-beijing",
                "buckets": {}
            },
            "sync_settings": {
                "auto_sync": False,
                "sync_interval": 3600,  # 1小时
                "include_patterns": ["*.mp4", "*.mkv", "*.mp3", "*.flac"],
                "exclude_patterns": ["*.tmp", "*.log"],
                "max_file_size": 1024 * 1024 * 1024  # 1GB
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 合并配置
                    self._merge_config(default_config, loaded_config)
            except Exception as e:
                logger.error(f"加载云存储配置失败: {e}")
        
        return default_config
    
    def _merge_config(self, default: Dict, loaded: Dict):
        """合并配置"""
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
    
    def save_config(self):
        """保存配置"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info("云存储配置已保存")
        except Exception as e:
            logger.error(f"保存云存储配置失败: {e}")
    
    def initialize_clients(self):
        """初始化云存储客户端"""
        try:
            # AWS S3客户端
            if self.config["aws"]["enabled"]:
                self.s3_clients = {}
                for bucket_name, bucket_config in self.config["aws"]["buckets"].items():
                    try:
                        session = boto3.Session(
                            aws_access_key_id=self.config["aws"]["access_key"],
                            aws_secret_access_key=self.config["aws"]["secret_key"],
                            region_name=self.config["aws"]["region"]
                        )
                        self.s3_clients[bucket_name] = session.client('s3')
                        logger.info(f"AWS S3客户端初始化成功: {bucket_name}")
                    except Exception as e:
                        logger.error(f"AWS S3客户端初始化失败 {bucket_name}: {e}")
            
            # 阿里云OSS客户端
            if self.config["aliyun"]["enabled"]:
                self.oss_clients = {}
                for bucket_name, bucket_config in self.config["aliyun"]["buckets"].items():
                    try:
                        auth = oss2.Auth(
                            self.config["aliyun"]["access_key"],
                            self.config["aliyun"]["secret_key"]
                        )
                        self.oss_clients[bucket_name] = oss2.Bucket(
                            auth, 
                            self.config["aliyun"]["endpoint"], 
                            bucket_name
                        )
                        logger.info(f"阿里云OSS客户端初始化成功: {bucket_name}")
                    except Exception as e:
                        logger.error(f"阿里云OSS客户端初始化失败 {bucket_name}: {e}")
            
            # 腾讯云COS客户端
            if self.config["tencent"]["enabled"]:
                self.cos_clients = {}
                for bucket_name, bucket_config in self.config["tencent"]["buckets"].items():
                    try:
                        config = CosConfig(
                            Region=self.config["tencent"]["region"],
                            SecretId=self.config["tencent"]["secret_id"],
                            SecretKey=self.config["tencent"]["secret_key"]
                        )
                        self.cos_clients[bucket_name] = CosS3Client(config)
                        logger.info(f"腾讯云COS客户端初始化成功: {bucket_name}")
                    except Exception as e:
                        logger.error(f"腾讯云COS客户端初始化失败 {bucket_name}: {e}")
            
            logger.info("云存储客户端初始化完成")
            
        except Exception as e:
            logger.error(f"云存储客户端初始化失败: {e}")
    
    async def upload_file(self, file_path: str, service: str, bucket: str, 
                         remote_path: str = None) -> Dict[str, Any]:
        """上传文件到云存储"""
        try:
            if not os.path.exists(file_path):
                return {"success": False, "error": "文件不存在"}
            
            file_size = os.path.getsize(file_path)
            file_name = Path(file_path).name
            
            if remote_path is None:
                remote_path = file_name
            
            result = {
                "service": service,
                "bucket": bucket,
                "local_path": file_path,
                "remote_path": remote_path,
                "file_size": file_size,
                "start_time": datetime.now().isoformat()
            }
            
            if service == "aws":
                if bucket not in self.s3_clients:
                    return {"success": False, "error": "AWS S3客户端未初始化"}
                
                try:
                    self.s3_clients[bucket].upload_file(file_path, bucket, remote_path)
                    result["success"] = True
                    self.stats["total_uploads"] += 1
                    self.stats["total_size_uploaded"] += file_size
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
                    self.stats["failed_operations"] += 1
            
            elif service == "aliyun":
                if bucket not in self.oss_clients:
                    return {"success": False, "error": "阿里云OSS客户端未初始化"}
                
                try:
                    self.oss_clients[bucket].put_object_from_file(remote_path, file_path)
                    result["success"] = True
                    self.stats["total_uploads"] += 1
                    self.stats["total_size_uploaded"] += file_size
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
                    self.stats["failed_operations"] += 1
            
            elif service == "tencent":
                if bucket not in self.cos_clients:
                    return {"success": False, "error": "腾讯云COS客户端未初始化"}
                
                try:
                    self.cos_clients[bucket].upload_file(
                        Bucket=bucket,
                        LocalFilePath=file_path,
                        Key=remote_path
                    )
                    result["success"] = True
                    self.stats["total_uploads"] += 1
                    self.stats["total_size_uploaded"] += file_size
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
                    self.stats["failed_operations"] += 1
            
            else:
                return {"success": False, "error": f"不支持的云存储服务: {service}"}
            
            result["end_time"] = datetime.now().isoformat()
            
            if result["success"]:
                logger.info(f"文件上传成功: {file_path} -> {service}:{bucket}/{remote_path}")
            else:
                logger.error(f"文件上传失败: {file_path} -> {service}:{bucket}/{remote_path}: {result['error']}")
            
            return result
            
        except Exception as e:
            logger.error(f"文件上传异常: {e}")
            return {"success": False, "error": str(e)}
    
    async def download_file(self, service: str, bucket: str, remote_path: str, 
                           local_path: str) -> Dict[str, Any]:
        """从云存储下载文件"""
        try:
            result = {
                "service": service,
                "bucket": bucket,
                "remote_path": remote_path,
                "local_path": local_path,
                "start_time": datetime.now().isoformat()
            }
            
            if service == "aws":
                if bucket not in self.s3_clients:
                    return {"success": False, "error": "AWS S3客户端未初始化"}
                
                try:
                    self.s3_clients[bucket].download_file(bucket, remote_path, local_path)
                    result["success"] = True
                    self.stats["total_downloads"] += 1
                    if os.path.exists(local_path):
                        result["file_size"] = os.path.getsize(local_path)
                        self.stats["total_size_downloaded"] += result["file_size"]
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
                    self.stats["failed_operations"] += 1
            
            elif service == "aliyun":
                if bucket not in self.oss_clients:
                    return {"success": False, "error": "阿里云OSS客户端未初始化"}
                
                try:
                    self.oss_clients[bucket].get_object_to_file(remote_path, local_path)
                    result["success"] = True
                    self.stats["total_downloads"] += 1
                    if os.path.exists(local_path):
                        result["file_size"] = os.path.getsize(local_path)
                        self.stats["total_size_downloaded"] += result["file_size"]
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
                    self.stats["failed_operations"] += 1
            
            elif service == "tencent":
                if bucket not in self.cos_clients:
                    return {"success": False, "error": "腾讯云COS客户端未初始化"}
                
                try:
                    self.cos_clients[bucket].download_file(
                        Bucket=bucket,
                        Key=remote_path,
                        DestFilePath=local_path
                    )
                    result["success"] = True
                    self.stats["total_downloads"] += 1
                    if os.path.exists(local_path):
                        result["file_size"] = os.path.getsize(local_path)
                        self.stats["total_size_downloaded"] += result["file_size"]
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
                    self.stats["failed_operations"] += 1
            
            else:
                return {"success": False, "error": f"不支持的云存储服务: {service}"}
            
            result["end_time"] = datetime.now().isoformat()
            
            if result["success"]:
                logger.info(f"文件下载成功: {service}:{bucket}/{remote_path} -> {local_path}")
            else:
                logger.error(f"文件下载失败: {service}:{bucket}/{remote_path} -> {local_path}: {result['error']}")
            
            return result
            
        except Exception as e:
            logger.error(f"文件下载异常: {e}")
            return {"success": False, "error": str(e)}
    
    async def list_files(self, service: str, bucket: str, prefix: str = "") -> Dict[str, Any]:
        """列出云存储中的文件"""
        try:
            result = {
                "service": service,
                "bucket": bucket,
                "prefix": prefix,
                "files": []
            }
            
            if service == "aws":
                if bucket not in self.s3_clients:
                    return {"success": False, "error": "AWS S3客户端未初始化"}
                
                try:
                    response = self.s3_clients[bucket].list_objects_v2(
                        Bucket=bucket,
                        Prefix=prefix
                    )
                    if 'Contents' in response:
                        for obj in response['Contents']:
                            result["files"].append({
                                "key": obj['Key'],
                                "size": obj['Size'],
                                "last_modified": obj['LastModified'].isoformat()
                            })
                    result["success"] = True
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
            
            elif service == "aliyun":
                if bucket not in self.oss_clients:
                    return {"success": False, "error": "阿里云OSS客户端未初始化"}
                
                try:
                    for obj in oss2.ObjectIterator(self.oss_clients[bucket], prefix=prefix):
                        result["files"].append({
                            "key": obj.key,
                            "size": obj.size,
                            "last_modified": obj.last_modified.isoformat()
                        })
                    result["success"] = True
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
            
            elif service == "tencent":
                if bucket not in self.cos_clients:
                    return {"success": False, "error": "腾讯云COS客户端未初始化"}
                
                try:
                    response = self.cos_clients[bucket].list_objects(
                        Bucket=bucket,
                        Prefix=prefix
                    )
                    if 'Contents' in response:
                        for obj in response['Contents']:
                            result["files"].append({
                                "key": obj['Key'],
                                "size": obj['Size'],
                                "last_modified": obj['LastModified']
                            })
                    result["success"] = True
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
            
            else:
                return {"success": False, "error": f"不支持的云存储服务: {service}"}
            
            return result
            
        except Exception as e:
            logger.error(f"列出文件异常: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_file(self, service: str, bucket: str, remote_path: str) -> Dict[str, Any]:
        """删除云存储中的文件"""
        try:
            result = {
                "service": service,
                "bucket": bucket,
                "remote_path": remote_path
            }
            
            if service == "aws":
                if bucket not in self.s3_clients:
                    return {"success": False, "error": "AWS S3客户端未初始化"}
                
                try:
                    self.s3_clients[bucket].delete_object(Bucket=bucket, Key=remote_path)
                    result["success"] = True
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
            
            elif service == "aliyun":
                if bucket not in self.oss_clients:
                    return {"success": False, "error": "阿里云OSS客户端未初始化"}
                
                try:
                    self.oss_clients[bucket].delete_object(remote_path)
                    result["success"] = True
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
            
            elif service == "tencent":
                if bucket not in self.cos_clients:
                    return {"success": False, "error": "腾讯云COS客户端未初始化"}
                
                try:
                    self.cos_clients[bucket].delete_object(Bucket=bucket, Key=remote_path)
                    result["success"] = True
                except Exception as e:
                    result["success"] = False
                    result["error"] = str(e)
            
            else:
                return {"success": False, "error": f"不支持的云存储服务: {service}"}
            
            if result["success"]:
                logger.info(f"文件删除成功: {service}:{bucket}/{remote_path}")
            else:
                logger.error(f"文件删除失败: {service}:{bucket}/{remote_path}: {result['error']}")
            
            return result
            
        except Exception as e:
            logger.error(f"删除文件异常: {e}")
            return {"success": False, "error": str(e)}
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "stats": self.stats,
            "config": {
                "aws_enabled": self.config["aws"]["enabled"],
                "aliyun_enabled": self.config["aliyun"]["enabled"],
                "tencent_enabled": self.config["tencent"]["enabled"],
                "total_buckets": len(self.config["aws"]["buckets"]) + 
                               len(self.config["aliyun"]["buckets"]) + 
                               len(self.config["tencent"]["buckets"])
            }
        }
    
    async def sync_directory(self, local_dir: str, service: str, bucket: str, 
                            remote_prefix: str = "") -> Dict[str, Any]:
        """同步目录到云存储"""
        try:
            if not os.path.exists(local_dir):
                return {"success": False, "error": "本地目录不存在"}
            
            results = {
                "total_files": 0,
                "uploaded_files": 0,
                "failed_files": 0,
                "details": []
            }
            
            for root, dirs, files in os.walk(local_dir):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, local_dir)
                    remote_path = os.path.join(remote_prefix, relative_path).replace("\\", "/")
                    
                    # 检查文件大小限制
                    file_size = os.path.getsize(local_file_path)
                    if file_size > self.config["sync_settings"]["max_file_size"]:
                        results["details"].append({
                            "file": local_file_path,
                            "status": "skipped",
                            "reason": "文件大小超过限制"
                        })
                        continue
                    
                    # 检查文件模式
                    skip = False
                    for pattern in self.config["sync_settings"]["exclude_patterns"]:
                        if file.endswith(pattern.replace("*", "")):
                            skip = True
                            break
                    
                    if skip:
                        results["details"].append({
                            "file": local_file_path,
                            "status": "skipped",
                            "reason": "文件模式被排除"
                        })
                        continue
                    
                    results["total_files"] += 1
                    
                    # 上传文件
                    upload_result = await self.upload_file(local_file_path, service, bucket, remote_path)
                    
                    if upload_result["success"]:
                        results["uploaded_files"] += 1
                        results["details"].append({
                            "file": local_file_path,
                            "status": "uploaded",
                            "remote_path": remote_path
                        })
                    else:
                        results["failed_files"] += 1
                        results["details"].append({
                            "file": local_file_path,
                            "status": "failed",
                            "error": upload_result["error"]
                        })
            
            results["success"] = True
            logger.info(f"目录同步完成: {local_dir} -> {service}:{bucket}/{remote_prefix}")
            return results
            
        except Exception as e:
            logger.error(f"目录同步异常: {e}")
            return {"success": False, "error": str(e)}

# 插件实例
plugin_instance = EnhancedCloudStoragePlugin()