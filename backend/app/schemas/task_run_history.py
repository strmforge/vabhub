"""
任务执行历史 Schema
SYSTEM-AUDIT-FOLLOWUP P4.4 实现
"""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class TaskRunHistoryBase(BaseModel):
    """任务执行历史基础模型"""
    task_name: str
    task_type: Optional[str] = None
    status: str
    message: Optional[str] = None
    duration_ms: Optional[int] = None
    meta_json: Optional[dict[str, Any]] = None


class TaskRunHistoryCreate(TaskRunHistoryBase):
    """创建任务执行历史"""
    pass


class TaskRunHistoryRead(TaskRunHistoryBase):
    """读取任务执行历史"""
    id: int
    started_at: datetime
    finished_at: Optional[datetime] = None
    error_type: Optional[str] = None
    error_traceback: Optional[str] = None
    host: Optional[str] = None
    pid: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TaskRunHistoryList(BaseModel):
    """任务执行历史列表响应"""
    items: list[TaskRunHistoryRead]
    total: int
    page: int
    page_size: int
    has_more: bool


class TaskRunHistoryFilter(BaseModel):
    """任务执行历史过滤参数"""
    task_name: Optional[str] = None
    status: Optional[str] = None
    task_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
