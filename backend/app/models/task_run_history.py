"""
任务执行历史模型
SYSTEM-AUDIT-FOLLOWUP P4.1 实现

记录任意 Runner 的执行历史，支持：
- 订阅检查
- 音乐榜单同步
- 健康检查
- 清理任务
- 等等
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Index
from datetime import datetime
from app.core.database import Base


class TaskRunHistory(Base):
    """任务执行历史模型"""
    __tablename__ = "task_run_history"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 任务标识
    task_name = Column(String(255), nullable=False, index=True)  # 任务名称（如 subscription_checker, music_chart_sync）
    task_type = Column(String(100), nullable=True, index=True)  # 任务类型（runner, scheduled, manual）
    
    # 执行时间
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    finished_at = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)  # 执行耗时（毫秒）
    
    # 状态
    status = Column(String(50), nullable=False, default="running", index=True)  # running, success, failed
    
    # 结果信息
    message = Column(String(1000), nullable=True)  # 成功/失败摘要
    error_type = Column(String(255), nullable=True)  # 错误类型（如 ValueError, TimeoutError）
    error_traceback = Column(Text, nullable=True)  # 错误堆栈摘要（截断，不存全量）
    
    # 元数据
    meta_json = Column(JSON, nullable=True)  # 参数、触发来源、处理统计等
    
    # 执行环境（可选）
    host = Column(String(255), nullable=True)  # 执行主机
    pid = Column(Integer, nullable=True)  # 进程 ID
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_task_run_history_name_started', 'task_name', 'started_at'),
        Index('idx_task_run_history_status_started', 'status', 'started_at'),
    )
    
    def __repr__(self):
        return f"<TaskRunHistory(id={self.id}, task_name='{self.task_name}', status='{self.status}')>"
