"""
日志配置
"""

import logging
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logging():
    """配置日志系统"""
    # 移除默认处理器
    logger.remove()
    
    # 控制台输出
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # 文件输出 (P6: 支持环境变量配置轮转)
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 使用配置的轮转设置
    rotation = getattr(settings, 'LOG_ROTATION', '50 MB')
    retention = getattr(settings, 'LOG_RETENTION', '14 days')
    compression = getattr(settings, 'LOG_COMPRESSION', 'zip')
    
    logger.add(
        log_dir / "vabhub_{time:YYYY-MM-DD}.log",
        rotation=rotation,
        retention=retention,
        compression=compression,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        encoding="utf-8"
    )
    
    # 错误日志单独记录
    logger.add(
        log_dir / "error_{time:YYYY-MM-DD}.log",
        rotation=rotation,
        retention=retention,
        compression=compression,
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        encoding="utf-8"
    )
    
    logger.info(f"日志配置: rotation={rotation}, retention={retention}, compression={compression}")
    
    logger.info("日志系统初始化完成")

