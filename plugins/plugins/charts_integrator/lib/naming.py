"""
命名和查询构建工具
"""

import re
from typing import Optional


def build_music_query(artist: str, title: str) -> str:
    """
    构建音乐搜索查询
    
    Args:
        artist: 艺术家名称
        title: 歌曲标题
        
    Returns:
        搜索查询字符串
    """
    # 清理特殊字符
    artist = re.sub(r'[^\w\s\-]', '', artist).strip()
    title = re.sub(r'[^\w\s\-]', '', title).strip()
    
    # 构建查询："艺术家 - 歌曲名"
    if artist and title:
        return f"{artist} - {title}"
    elif title:
        return title
    else:
        return ""


def build_video_query(title: str, year: Optional[int] = None) -> str:
    """
    构建视频搜索查询
    
    Args:
        title: 视频标题
        year: 发布年份（可选）
        
    Returns:
        搜索查询字符串
    """
    # 清理特殊字符
    title = re.sub(r'[^\w\s\-]', '', title).strip()
    
    # 构建查询
    query = title
    if year:
        query += f" {year}"
    
    return query


def guess_is_tv_season(query: str) -> bool:
    """
    猜测查询是否为电视剧季
    
    Args:
        query: 搜索查询
        
    Returns:
        是否为电视剧季
    """
    # 电视剧季的常见模式
    tv_patterns = [
        r'S\d{1,2}E\d{1,2}',  # S01E01
        r'Season\s+\d+',       # Season 1
        r'第\s*\d+\s*季',     # 第1季
        r'\bS\d{1,2}\b',      # S1
        r'\b第\d+部\b',       # 第1部
    ]
    
    for pattern in tv_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return True
    
    # 检查常见电视剧关键词
    tv_keywords = [
        'season', 'episode', 'series', 'tv', '电视剧', '剧集',
        'seasonal', 'ep', 'complete season'
    ]
    
    query_lower = query.lower()
    for keyword in tv_keywords:
        if keyword in query_lower:
            return True
    
    return False


def extract_year_from_title(title: str) -> Optional[int]:
    """
    从标题中提取年份
    
    Args:
        title: 标题
        
    Returns:
        提取的年份，如果未找到则返回 None
    """
    # 匹配4位数字的年份（1900-2099）
    year_match = re.search(r'(19|20)\d{2}', title)
    if year_match:
        try:
            return int(year_match.group())
        except ValueError:
            pass
    
    return None


def normalize_title(title: str) -> str:
    """
    标准化标题
    
    Args:
        title: 原始标题
        
    Returns:
        标准化后的标题
    """
    # 移除特殊字符和多余空格
    title = re.sub(r'[^\w\s\-]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    
    return title