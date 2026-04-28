"""
健康检查API
SYSTEM-AUDIT-FOLLOWUP-1 P2/P3 实现

关键设计：
- /health 端点永远返回 200（即使 DB 异常也不 500）
- DB 异常时 status="degraded"，db.ok=false
- 包含 DB 连接池状态监控
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.version import APP_VERSION

router = APIRouter()

# 模块级启动时间，用于计算 uptime
_START_TS = time.time()


@router.get("/")
async def health_check() -> dict[str, Any]:
    """
    简单健康检查端点
    
    SYSTEM-AUDIT-FOLLOWUP-1 P2/P3 实现：
    - 永远返回 200（即使 DB 异常也不 500）
    - DB 异常时 status="degraded"，db.ok=false
    - 包含 DB 连接池状态监控
    """
    now = datetime.now(timezone.utc).isoformat()
    uptime = int(time.time() - _START_TS)
    
    db_ok = True
    db_latency_ms: int | None = None
    pool_status: str | None = None
    db_error: str | None = None
    
    # P3: DB 连接池监控
    try:
        from app.core.database import engine
        from sqlalchemy import text
        
        t0 = time.perf_counter()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_latency_ms = int((time.perf_counter() - t0) * 1000)
        
        # 获取连接池状态
        try:
            pool_status = str(engine.sync_engine.pool.status())
        except Exception:
            pool_status = None
            
    except Exception as e:
        db_ok = False
        db_error = str(e)
        logger.warning(f"健康检查: 数据库连接失败 - {e}")
    
    # 确定总体状态
    status = "ok" if db_ok else "degraded"
    
    return {
        "status": status,
        "version": APP_VERSION,
        "time": now,
        "uptime_seconds": uptime,
        "db": {
            "ok": db_ok,
            "latency_ms": db_latency_ms,
            "pool": pool_status,
            "error": db_error,
        },
    }


@router.get("/full")
async def health_check_full():
    """
    完整健康检查（兼容旧版）
    
    检查数据库、缓存、磁盘等
    """
    import shutil
    import os
    
    now = datetime.now(timezone.utc).isoformat()
    uptime = int(time.time() - _START_TS)
    
    # 检查数据库连接
    db_ok = True
    db_latency_ms: int | None = None
    pool_status: str | None = None
    
    try:
        from app.core.database import engine
        from sqlalchemy import text
        
        t0 = time.perf_counter()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_latency_ms = int((time.perf_counter() - t0) * 1000)
        
        try:
            pool_status = str(engine.sync_engine.pool.status())
        except Exception:
            pool_status = None
    except Exception as e:
        db_ok = False
        logger.warning(f"健康检查: 数据库连接失败 - {e}")
    
    # 检查缓存系统
    cache_ok = True
    try:
        from app.core.cache import get_cache
        cache = get_cache()
        test_key = "health_check_test"
        await cache.set(test_key, "test", ttl=10)
        value = await cache.get(test_key)
        cache_ok = value == "test"
        if cache_ok:
            await cache.delete(test_key)
    except Exception as e:
        cache_ok = False
        logger.warning(f"健康检查: 缓存系统异常 - {e}")
    
    # 检查磁盘空间
    disk_ok = True
    disk_used_percent: float | None = None
    try:
        from app.core.config import settings
        storage_path = settings.STORAGE_PATH
        if os.path.exists(storage_path):
            stat = shutil.disk_usage(storage_path)
            disk_used_percent = round((stat.used / stat.total) * 100, 2)
            disk_ok = disk_used_percent < 90
    except Exception as e:
        disk_ok = False
        logger.warning(f"健康检查: 磁盘检查失败 - {e}")
    
    # 确定总体状态
    all_ok = db_ok and cache_ok and disk_ok
    status = "ok" if all_ok else "degraded"
    
    return {
        "status": status,
        "version": APP_VERSION,
        "time": now,
        "uptime_seconds": uptime,
        "db": {
            "ok": db_ok,
            "latency_ms": db_latency_ms,
            "pool": pool_status,
        },
        "cache": {
            "ok": cache_ok,
        },
        "disk": {
            "ok": disk_ok,
            "used_percent": disk_used_percent,
        },
    }


@router.get("/{check_name}")
async def health_check_item(check_name: str) -> dict[str, Any]:
    """
    单项健康检查
    
    支持的检查项: db, cache, disk
    永远返回 200，异常时 ok=false
    """
    now = datetime.now(timezone.utc).isoformat()
    
    if check_name == "db":
        try:
            from app.core.database import engine
            from sqlalchemy import text
            
            t0 = time.perf_counter()
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            latency_ms = int((time.perf_counter() - t0) * 1000)
            
            pool_status = None
            try:
                pool_status = str(engine.sync_engine.pool.status())
            except Exception:
                pass
            
            return {"check": "db", "ok": True, "latency_ms": latency_ms, "pool": pool_status, "time": now}
        except Exception as e:
            return {"check": "db", "ok": False, "error": str(e), "time": now}
    
    elif check_name == "cache":
        try:
            from app.core.cache import get_cache
            cache = get_cache()
            test_key = "health_check_test"
            await cache.set(test_key, "test", ttl=10)
            value = await cache.get(test_key)
            ok = value == "test"
            if ok:
                await cache.delete(test_key)
            return {"check": "cache", "ok": ok, "time": now}
        except Exception as e:
            return {"check": "cache", "ok": False, "error": str(e), "time": now}
    
    elif check_name == "disk":
        try:
            import shutil
            import os
            from app.core.config import settings
            storage_path = settings.STORAGE_PATH
            if os.path.exists(storage_path):
                stat = shutil.disk_usage(storage_path)
                used_percent = round((stat.used / stat.total) * 100, 2)
                return {"check": "disk", "ok": used_percent < 90, "used_percent": used_percent, "time": now}
            return {"check": "disk", "ok": False, "error": "存储路径不存在", "time": now}
        except Exception as e:
            return {"check": "disk", "ok": False, "error": str(e), "time": now}
    
    else:
        return {"check": check_name, "ok": False, "error": f"未知检查项: {check_name}", "time": now}

