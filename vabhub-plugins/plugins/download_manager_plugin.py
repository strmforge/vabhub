#!/usr/bin/env python3
"""
下载管理插件 - 管理下载任务和状态
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from enum import Enum
from plugin_base import BasePlugin


class DownloadStatus(Enum):
    """下载状态枚举"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class DownloadTask:
    """下载任务类"""
    
    def __init__(self, task_id: str, url: str, destination: str, **kwargs):
        self.task_id = task_id
        self.url = url
        self.destination = destination
        self.status = DownloadStatus.PENDING
        self.progress = 0.0
        self.speed = 0.0
        self.size = 0
        self.downloaded = 0
        self.eta = 0
        self.error = None
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
        self.metadata = kwargs
    
    def update_progress(self, downloaded: int, total: int, speed: float = 0.0):
        """更新下载进度"""
        self.downloaded = downloaded
        self.size = total
        self.speed = speed
        
        if total > 0:
            self.progress = (downloaded / total) * 100
            if speed > 0:
                remaining = total - downloaded
                self.eta = remaining / speed
        
        if self.status == DownloadStatus.PENDING:
            self.status = DownloadStatus.DOWNLOADING
            self.started_at = time.time()
    
    def complete(self):
        """标记任务完成"""
        self.status = DownloadStatus.COMPLETED
        self.progress = 100.0
        self.completed_at = time.time()
    
    def fail(self, error: str):
        """标记任务失败"""
        self.status = DownloadStatus.FAILED
        self.error = error
        self.completed_at = time.time()
    
    def pause(self):
        """暂停任务"""
        self.status = DownloadStatus.PAUSED
    
    def resume(self):
        """恢复任务"""
        self.status = DownloadStatus.DOWNLOADING
    
    def cancel(self):
        """取消任务"""
        self.status = DownloadStatus.CANCELLED
        self.completed_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'task_id': self.task_id,
            'url': self.url,
            'destination': self.destination,
            'status': self.status.value,
            'progress': self.progress,
            'speed': self.speed,
            'size': self.size,
            'downloaded': self.downloaded,
            'eta': self.eta,
            'error': self.error,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'metadata': self.metadata
        }


class DownloadManagerPlugin(BasePlugin):
    """下载管理插件"""
    
    name = "download_manager"
    version = "1.0.0"
    description = "管理下载任务和状态"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.tasks: Dict[str, DownloadTask] = {}
        self.max_concurrent_downloads = config.get('max_concurrent_downloads', 3)
        self.download_dir = config.get('download_dir', './downloads')
        self.active_downloads: List[str] = []
    
    def setup(self) -> None:
        """插件初始化"""
        import os
        os.makedirs(self.download_dir, exist_ok=True)
        self.logger.info("DownloadManager plugin setup completed")
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行下载管理操作"""
        operation = data.get('operation', 'add_task')
        
        if operation == 'add_task':
            return await self.add_download_task(
                data.get('url', ''),
                data.get('destination', ''),
                data.get('metadata', {})
            )
        elif operation == 'list_tasks':
            return await self.list_download_tasks(data.get('status_filter', None))
        elif operation == 'get_task':
            return await self.get_download_task(data.get('task_id', ''))
        elif operation == 'pause_task':
            return await self.pause_download_task(data.get('task_id', ''))
        elif operation == 'resume_task':
            return await self.resume_download_task(data.get('task_id', ''))
        elif operation == 'cancel_task':
            return await self.cancel_download_task(data.get('task_id', ''))
        elif operation == 'get_stats':
            return await self.get_download_stats()
        else:
            return {'error': f'Unknown operation: {operation}'}
    
    async def add_download_task(self, url: str, destination: str = '', metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """添加下载任务"""
        try:
            if not url:
                return {'error': 'URL is required'}
            
            # 生成任务ID
            task_id = f"download_{int(time.time())}_{len(self.tasks)}"
            
            # 如果没有指定目标路径，使用默认下载目录
            if not destination:
                filename = url.split('/')[-1] or 'download'
                destination = f"{self.download_dir}/{filename}"
            
            # 创建下载任务
            task = DownloadTask(task_id, url, destination, **(metadata or {}))
            self.tasks[task_id] = task
            
            # 如果并发下载数未满，立即开始下载
            if len(self.active_downloads) < self.max_concurrent_downloads:
                await self._start_download(task_id)
            
            self.logger.info(f"Added download task: {task_id}")
            return {
                'task_id': task_id,
                'status': 'added',
                'task': task.to_dict()
            }
        except Exception as e:
            self.logger.error(f"Add download task failed: {e}")
            return {'error': str(e)}
    
    async def list_download_tasks(self, status_filter: Optional[str] = None) -> Dict[str, Any]:
        """列出下载任务"""
        try:
            tasks_list = []
            
            for task in self.tasks.values():
                if status_filter and task.status.value != status_filter:
                    continue
                tasks_list.append(task.to_dict())
            
            return {
                'tasks': tasks_list,
                'total': len(tasks_list),
                'filter': status_filter
            }
        except Exception as e:
            self.logger.error(f"List download tasks failed: {e}")
            return {'error': str(e)}
    
    async def get_download_task(self, task_id: str) -> Dict[str, Any]:
        """获取下载任务详情"""
        try:
            if task_id not in self.tasks:
                return {'error': 'Task not found'}
            
            task = self.tasks[task_id]
            return {
                'task': task.to_dict(),
                'active': task_id in self.active_downloads
            }
        except Exception as e:
            self.logger.error(f"Get download task failed: {e}")
            return {'error': str(e)}
    
    async def pause_download_task(self, task_id: str) -> Dict[str, Any]:
        """暂停下载任务"""
        try:
            if task_id not in self.tasks:
                return {'error': 'Task not found'}
            
            task = self.tasks[task_id]
            
            if task.status not in [DownloadStatus.DOWNLOADING, DownloadStatus.PAUSED]:
                return {'error': f'Cannot pause task in {task.status.value} status'}
            
            task.pause()
            
            # 从活跃下载列表中移除
            if task_id in self.active_downloads:
                self.active_downloads.remove(task_id)
            
            # 启动下一个等待中的任务
            await self._start_next_download()
            
            self.logger.info(f"Paused download task: {task_id}")
            return {'task_id': task_id, 'status': 'paused'}
        except Exception as e:
            self.logger.error(f"Pause download task failed: {e}")
            return {'error': str(e)}
    
    async def resume_download_task(self, task_id: str) -> Dict[str, Any]:
        """恢复下载任务"""
        try:
            if task_id not in self.tasks:
                return {'error': 'Task not found'}
            
            task = self.tasks[task_id]
            
            if task.status != DownloadStatus.PAUSED:
                return {'error': f'Cannot resume task in {task.status.value} status'}
            
            # 如果并发下载数未满，立即开始下载
            if len(self.active_downloads) < self.max_concurrent_downloads:
                await self._start_download(task_id)
            else:
                task.resume()
            
            self.logger.info(f"Resumed download task: {task_id}")
            return {'task_id': task_id, 'status': 'resumed'}
        except Exception as e:
            self.logger.error(f"Resume download task failed: {e}")
            return {'error': str(e)}
    
    async def cancel_download_task(self, task_id: str) -> Dict[str, Any]:
        """取消下载任务"""
        try:
            if task_id not in self.tasks:
                return {'error': 'Task not found'}
            
            task = self.tasks[task_id]
            task.cancel()
            
            # 从活跃下载列表中移除
            if task_id in self.active_downloads:
                self.active_downloads.remove(task_id)
            
            # 启动下一个等待中的任务
            await self._start_next_download()
            
            self.logger.info(f"Cancelled download task: {task_id}")
            return {'task_id': task_id, 'status': 'cancelled'}
        except Exception as e:
            self.logger.error(f"Cancel download task failed: {e}")
            return {'error': str(e)}
    
    async def get_download_stats(self) -> Dict[str, Any]:
        """获取下载统计信息"""
        try:
            stats = {
                'total_tasks': len(self.tasks),
                'active_downloads': len(self.active_downloads),
                'max_concurrent': self.max_concurrent_downloads,
                'status_counts': {},
                'total_downloaded': 0,
                'average_speed': 0
            }
            
            # 统计各状态的任务数量
            for task in self.tasks.values():
                status = task.status.value
                stats['status_counts'][status] = stats['status_counts'].get(status, 0) + 1
                
                if task.status == DownloadStatus.COMPLETED:
                    stats['total_downloaded'] += task.size
            
            # 计算平均速度
            active_speeds = [task.speed for task in self.tasks.values() 
                           if task.status == DownloadStatus.DOWNLOADING and task.speed > 0]
            if active_speeds:
                stats['average_speed'] = sum(active_speeds) / len(active_speeds)
            
            return stats
        except Exception as e:
            self.logger.error(f"Get download stats failed: {e}")
            return {'error': str(e)}
    
    async def _start_download(self, task_id: str):
        """开始下载任务"""
        try:
            task = self.tasks[task_id]
            
            # 模拟下载过程
            task.status = DownloadStatus.DOWNLOADING
            self.active_downloads.append(task_id)
            
            # 在实际实现中，这里应该调用实际的下载逻辑
            # 这里使用模拟下载
            await self._simulate_download(task)
            
        except Exception as e:
            self.logger.error(f"Start download failed: {e}")
            task.fail(str(e))
        finally:
            # 从活跃下载列表中移除
            if task_id in self.active_downloads:
                self.active_downloads.remove(task_id)
            
            # 启动下一个等待中的任务
            await self._start_next_download()
    
    async def _simulate_download(self, task: DownloadTask):
        """模拟下载过程"""
        try:
            # 模拟文件大小（1MB-100MB）
            import random
            task.size = random.randint(1024 * 1024, 100 * 1024 * 1024)
            
            # 模拟下载进度
            chunk_size = 1024 * 1024  # 1MB chunks
            downloaded = 0
            
            while downloaded < task.size:
                if task.status != DownloadStatus.DOWNLOADING:
                    break
                
                # 模拟下载速度（100KB/s - 10MB/s）
                speed = random.randint(100 * 1024, 10 * 1024 * 1024)
                chunk = min(chunk_size, task.size - downloaded)
                
                # 模拟下载时间
                await asyncio.sleep(chunk / speed)
                
                downloaded += chunk
                task.update_progress(downloaded, task.size, speed)
                
                self.logger.debug(f"Download progress: {task.progress:.1f}%")
            
            if downloaded >= task.size:
                task.complete()
                self.logger.info(f"Download completed: {task.task_id}")
            
        except Exception as e:
            self.logger.error(f"Simulate download failed: {e}")
            task.fail(str(e))
    
    async def _start_next_download(self):
        """启动下一个等待中的下载任务"""
        try:
            # 查找等待中的任务
            pending_tasks = [task_id for task_id, task in self.tasks.items()
                           if task.status == DownloadStatus.PENDING and 
                           task_id not in self.active_downloads]
            
            # 如果有等待中的任务且并发数未满，启动下一个
            while pending_tasks and len(self.active_downloads) < self.max_concurrent_downloads:
                next_task_id = pending_tasks.pop(0)
                await self._start_download(next_task_id)
        except Exception as e:
            self.logger.error(f"Start next download failed: {e}")
    
    def health_check(self) -> bool:
        """健康检查"""
        try:
            # 检查下载目录是否可写
            import os
            test_file = os.path.join(self.download_dir, 'test_write')
            
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def cleanup(self) -> None:
        """清理资源"""
        # 取消所有活跃下载
        for task_id in list(self.active_downloads):
            if task_id in self.tasks:
                self.tasks[task_id].cancel()
        
        self.active_downloads.clear()
        self.logger.info("DownloadManager plugin cleanup completed")