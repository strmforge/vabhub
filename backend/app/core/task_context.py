"""
任务执行上下文管理器
SYSTEM-AUDIT-FOLLOWUP P4.2 实现

提供统一的任务执行记录封装：
- 进入时 insert running 记录
- 正常退出更新 success
- 异常退出更新 failed + message + traceback 摘要
"""
from __future__ import annotations

import os
import socket
import time
import traceback
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, AsyncGenerator, Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_run_history import TaskRunHistory


def _truncate_traceback(tb: str, max_length: int = 2000) -> str:
    """截断 traceback，保留头尾"""
    if len(tb) <= max_length:
        return tb
    half = max_length // 2
    return tb[:half] + "\n... [truncated] ...\n" + tb[-half:]


def _get_host() -> str:
    """获取主机名"""
    try:
        return socket.gethostname()
    except Exception:
        return "unknown"


@asynccontextmanager
async def task_run_context(
    db: AsyncSession,
    task_name: str,
    task_type: str = "runner",
    meta: Optional[dict[str, Any]] = None,
    auto_commit: bool = True,
) -> AsyncGenerator[TaskRunHistory, None]:
    """
    任务执行上下文管理器
    
    用法：
        async with task_run_context(db, "subscription_checker") as run:
            # 执行任务逻辑
            run.meta_json = {"checked": 10, "created": 3}
    
    Args:
        db: 数据库会话
        task_name: 任务名称
        task_type: 任务类型 (runner, scheduled, manual)
        meta: 初始元数据
        auto_commit: 是否自动提交（默认 True）
    
    Yields:
        TaskRunHistory: 任务执行记录对象，可在任务中更新 meta_json
    """
    start_time = time.perf_counter()
    
    # 创建运行记录
    run = TaskRunHistory(
        task_name=task_name,
        task_type=task_type,
        started_at=datetime.utcnow(),
        status="running",
        meta_json=meta or {},
        host=_get_host(),
        pid=os.getpid(),
    )
    
    db.add(run)
    await db.flush()  # 获取 ID
    
    logger.info(f"[TaskRun #{run.id}] 开始执行: {task_name}")
    
    try:
        yield run
        
        # 正常完成
        run.status = "success"
        run.finished_at = datetime.utcnow()
        run.duration_ms = int((time.perf_counter() - start_time) * 1000)
        run.message = run.message or "执行成功"
        
        logger.info(
            f"[TaskRun #{run.id}] 执行成功: {task_name}, "
            f"耗时 {run.duration_ms}ms"
        )
        
    except Exception as e:
        # 异常退出
        run.status = "failed"
        run.finished_at = datetime.utcnow()
        run.duration_ms = int((time.perf_counter() - start_time) * 1000)
        run.error_type = type(e).__name__
        run.message = str(e)[:1000]  # 截断错误消息
        run.error_traceback = _truncate_traceback(traceback.format_exc())
        
        logger.error(
            f"[TaskRun #{run.id}] 执行失败: {task_name}, "
            f"错误: {run.error_type}: {run.message}"
        )
        
        # 重新抛出异常，让调用方处理
        raise
    
    finally:
        if auto_commit:
            try:
                await db.commit()
            except Exception as commit_err:
                logger.error(f"[TaskRun #{run.id}] 提交失败: {commit_err}")
                await db.rollback()


async def record_task_run(
    db: AsyncSession,
    task_name: str,
    status: str,
    duration_ms: Optional[int] = None,
    message: Optional[str] = None,
    error_type: Optional[str] = None,
    error_traceback: Optional[str] = None,
    meta: Optional[dict[str, Any]] = None,
    task_type: str = "runner",
) -> TaskRunHistory:
    """
    直接记录任务执行结果（不使用上下文管理器）
    
    适用于无法使用 async with 的场景
    """
    run = TaskRunHistory(
        task_name=task_name,
        task_type=task_type,
        started_at=datetime.utcnow(),
        finished_at=datetime.utcnow(),
        status=status,
        duration_ms=duration_ms,
        message=message[:1000] if message else None,
        error_type=error_type,
        error_traceback=_truncate_traceback(error_traceback) if error_traceback else None,
        meta_json=meta or {},
        host=_get_host(),
        pid=os.getpid(),
    )
    
    db.add(run)
    await db.commit()
    
    return run
