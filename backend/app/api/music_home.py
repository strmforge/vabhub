"""
音乐首页 API

提供音乐中心首页榜单/推荐数据

Created: 0.0.3 DISCOVER-MUSIC-HOME P4
Updated: P5 缓存 TTL 统一 + refresh 机制
"""

from datetime import datetime
from fastapi import APIRouter, Query
from loguru import logger

from app.core.config import settings
from app.core.schemas import success_response
from app.services.music_discover_service import get_music_discover_service

router = APIRouter()


@router.get("/home", summary="获取音乐首页内容")
async def get_music_home(
    refresh: bool = Query(False, description="强制刷新缓存")
):
    """
    获取音乐首页聚合内容
    
    P5: 支持 ?refresh=1 强制刷新缓存
    
    聚合 RSSHub 榜单和本地配置的榜单源：
    - 网易云热歌榜
    - QQ 音乐热歌榜
    - 本地配置的榜单
    
    返回：
    - sections: 各榜单区块
    - has_rsshub: RSSHub 是否可用
    - has_local_charts: 是否有本地榜单
    - message: 状态提示
    - last_updated: 最后更新时间
    - cache_ttl: 缓存 TTL（秒）
    """
    try:
        service = get_music_discover_service()
        result = await service.get_home(refresh=refresh)
        
        return {
            "sections": [s.model_dump() for s in result.sections],
            "has_rsshub": result.has_rsshub,
            "has_local_charts": result.has_local_charts,
            "message": result.message,
            "last_updated": datetime.utcnow().isoformat(),
            "cache_ttl": settings.MUSIC_HOME_CACHE_TTL_SECONDS,
        }
        
    except Exception as e:
        logger.error(f"获取音乐首页内容失败: {e}")
        return {
            "sections": [],
            "has_rsshub": False,
            "has_local_charts": False,
            "message": f"获取内容失败: {str(e)}",
        }
