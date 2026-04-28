"""
任务执行历史 API
SYSTEM-AUDIT-FOLLOWUP P4.4 实现

提供任务执行历史查询接口：
- GET /api/tasks/history - 列表查询
- GET /api/tasks/history/{id} - 详情查询
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.models.task_run_history import TaskRunHistory
from app.schemas.task_run_history import (
    TaskRunHistoryRead,
    TaskRunHistoryList,
)

router = APIRouter(prefix="/api/tasks", tags=["任务历史"])


@router.get("/history", response_model=TaskRunHistoryList)
async def list_task_history(
    task_name: Optional[str] = Query(None, description="任务名称过滤"),
    status: Optional[str] = Query(None, description="状态过滤 (running/success/failed)"),
    task_type: Optional[str] = Query(None, description="任务类型过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_async_session),
):
    """
    获取任务执行历史列表
    
    支持按任务名称、状态、类型过滤，分页返回
    """
    # 构建查询
    query = select(TaskRunHistory)
    count_query = select(func.count(TaskRunHistory.id))
    
    # 过滤条件
    if task_name:
        query = query.where(TaskRunHistory.task_name == task_name)
        count_query = count_query.where(TaskRunHistory.task_name == task_name)
    
    if status:
        query = query.where(TaskRunHistory.status == status)
        count_query = count_query.where(TaskRunHistory.status == status)
    
    if task_type:
        query = query.where(TaskRunHistory.task_type == task_type)
        count_query = count_query.where(TaskRunHistory.task_type == task_type)
    
    # 获取总数
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(desc(TaskRunHistory.started_at)).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return TaskRunHistoryList(
        items=[TaskRunHistoryRead.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        has_more=(offset + len(items)) < total,
    )


@router.get("/history/{history_id}", response_model=TaskRunHistoryRead)
async def get_task_history_detail(
    history_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """
    获取任务执行历史详情
    
    包含完整的元数据和错误信息
    """
    result = await db.execute(
        select(TaskRunHistory).where(TaskRunHistory.id == history_id)
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail="任务记录不存在")
    
    return TaskRunHistoryRead.model_validate(item)


@router.get("/names")
async def list_task_names(
    db: AsyncSession = Depends(get_async_session),
):
    """
    获取所有任务名称列表（用于前端过滤下拉）
    """
    result = await db.execute(
        select(TaskRunHistory.task_name)
        .distinct()
        .order_by(TaskRunHistory.task_name)
    )
    names = [row[0] for row in result.all()]
    return {"names": names}
