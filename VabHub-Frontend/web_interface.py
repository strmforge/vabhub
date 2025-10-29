from fastapi import FastAPI, HTTPException, Form, UploadFile, File, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import uvicorn
import os
import json
import asyncio
import time
from typing import List, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VabHub", description="智能媒体管理平台")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 模板配置
templates = Jinja2Templates(directory="templates")

# 智能工作流管理器
class WorkflowManager:
    def __init__(self):
        self.tasks = {}
        
    def start_workflow(self, config):
        task_id = f"task_{int(time.time())}"
        self.tasks[task_id] = {
            "config": config,
            "status": "running",
            "progress": 0,
            "current_file": "",
            "start_time": time.time(),
            "processed_files": 0,
            "total_files": 5  # 模拟文件数量
        }
        return task_id
    
    def get_task_status(self, task_id):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            # 模拟进度更新
            if task["progress"] < 100:
                task["progress"] = min(task["progress"] + 5, 100)
                task["processed_files"] = min(task["processed_files"] + 1, task["total_files"])
                
                # 模拟当前处理文件
                files = [
                    "奥本海默.2023.2160p.BluRay.REMUX.mkv",
                    "最后生还者.S01E01.1080p.WEB-DL.mkv", 
                    "Taylor Swift - 1989 (2014) [FLAC].zip",
                    "阿凡达：水之道.2022.1080p.BluRay.mkv",
                    "权力的游戏.S08E06.1080p.BluRay.mkv"
                ]
                if task["processed_files"] < len(files):
                    task["current_file"] = files[task["processed_files"]]
                
                if task["progress"] >= 100:
                    task["status"] = "completed"
            
            return task
        return {"status": "not_found", "progress": 0, "current_file": ""}

# 全局实例
workflow_manager = WorkflowManager()

class VabHubAPI:
    def __init__(self):
        self.downloaders = {
            "qBittorrent": {"status": "online", "speed": "65%", "active_torrents": 12},
            "Transmission": {"status": "offline", "speed": "0%", "active_torrents": 0},
            "Aria2": {"status": "online", "speed": "30%", "active_torrents": 5}
        }
        
        self.pt_sites = {
            "M-Team": {"status": "connected", "free_torrents": ["奥本海默 4K REMUX", "最后生还者 S01"]},
            "HDChina": {"status": "connected", "free_torrents": ["Taylor Swift - 1989 FLAC"]},
            "PTHome": {"status": "connected", "free_torrents": ["经典电影合集"]},
            "TTG": {"status": "disconnected", "free_torrents": []}
        }
        
        self.hot_recommendations = [
            {
                "id": 1,
                "title": "奥本海默",
                "year": 2023,
                "type": "movie",
                "genre": "剧情/历史",
                "quality": "4K REMUX",
                "poster": "film",
                "download_url": "magnet:?xt=urn:btih:example1"
            },
            {
                "id": 2,
                "title": "最后生还者 S01",
                "year": 2023,
                "type": "tv",
                "genre": "剧情/科幻",
                "quality": "1080p",
                "poster": "tv",
                "download_url": "magnet:?xt=urn:btih:example2"
            },
            {
                "id": 3,
                "title": "Taylor Swift - 1989",
                "year": 2014,
                "type": "music",
                "genre": "流行音乐",
                "quality": "FLAC",
                "poster": "music",
                "download_url": "magnet:?xt=urn:btih:example3"
            }
        ]

vabhub_api = VabHubAPI()

@app.get("/")
async def dashboard(request: Request):
    """主仪表盘页面 - 使用增强版Vue 3 + Vuetify界面"""
    return templates.TemplateResponse("index_enhanced.html", {"request": request})

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """获取仪表盘统计数据"""
    return JSONResponse({
        "success": True,
        "data": {
            "media_files": 1284,
            "active_downloads": 86,
            "storage_used": "24.7TB",
            "active_plugins": 12,
            "cpu_usage": 24,
            "memory_usage": 68,
            "disk_usage": 82,
            "network_speed": "156M/s"
        }
    })

@app.get("/api/downloaders/status")
async def get_downloaders_status():
    """获取下载器状态"""
    return JSONResponse({
        "success": True,
        "data": vabhub_api.downloaders
    })

@app.get("/api/pt/sites")
async def get_pt_sites():
    """获取PT站点信息"""
    return JSONResponse({
        "success": True,
        "data": vabhub_api.pt_sites
    })

@app.get("/api/recommendations/hot")
async def get_hot_recommendations():
    """获取热门推荐"""
    return JSONResponse({
        "success": True,
        "data": vabhub_api.hot_recommendations
    })

@app.post("/api/download/start")
async def start_download(magnet_url: str = Form(...), downloader: str = Form("qBittorrent")):
    """开始下载任务"""
    try:
        # 模拟下载开始
        logger.info(f"开始下载: {magnet_url} 使用下载器: {downloader}")
        
        return JSONResponse({
            "success": True,
            "message": "下载任务已开始",
            "task_id": f"task_{len(vabhub_api.downloaders)}"
        })
    except Exception as e:
        logger.error(f"下载开始失败: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/api/download/queue")
async def get_download_queue():
    """获取下载队列"""
    queue = [
        {
            "id": "task_1",
            "name": "奥本海默.2023.2160p",
            "progress": 85,
            "status": "downloading",
            "speed": "12.5 MB/s",
            "size": "45.2 GB"
        },
        {
            "id": "task_2", 
            "name": "最后生还者.S01E01",
            "progress": 45,
            "status": "downloading",
            "speed": "8.3 MB/s",
            "size": "2.1 GB"
        },
        {
            "id": "task_3",
            "name": "Taylor Swift - 1989",
            "progress": 20,
            "status": "downloading", 
            "speed": "5.1 MB/s",
            "size": "350 MB"
        }
    ]
    
    return JSONResponse({
        "success": True,
        "data": queue
    })

@app.post("/api/scan-directory")
async def scan_directory(path: str = Form(...)):
    """扫描目录获取文件列表"""
    try:
        # 模拟文件扫描
        files = [
            {"name": "奥本海默.2023.2160p.BluRay.REMUX.mkv", "path": f"{path}/movies", "size": "45.2 GB"},
            {"name": "最后生还者.S01E01.1080p.WEB-DL.mkv", "path": f"{path}/tv", "size": "2.1 GB"},
            {"name": "Taylor Swift - 1989 (2014) [FLAC].zip", "path": f"{path}/music", "size": "350 MB"},
            {"name": "阿凡达：水之道.2022.1080p.BluRay.mkv", "path": f"{path}/movies", "size": "15.8 GB"},
            {"name": "权力的游戏.S08E06.1080p.BluRay.mkv", "path": f"{path}/tv", "size": "3.2 GB"}
        ]
        
        return JSONResponse({
            "success": True,
            "files": files,
            "total": len(files)
        })
    except Exception as e:
        logger.error(f"目录扫描失败: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.post("/api/process/start")
async def start_processing(
    directory: str = Form(...),
    enable_scan: bool = Form(True),
    enable_recognize: bool = Form(True), 
    enable_rename: bool = Form(True),
    enable_metadata: bool = Form(False),
    enable_move: bool = Form(False)
):
    """开始智能处理工作流"""
    try:
        # 构建处理配置
        config = {
            "directory": directory,
            "steps": {
                "scan": enable_scan,
                "recognize": enable_recognize,
                "rename": enable_rename,
                "metadata": enable_metadata,
                "move": enable_move
            }
        }
        
        # 启动处理任务
        task_id = workflow_manager.start_workflow(config)
        
        return JSONResponse({
            "success": True,
            "task_id": task_id,
            "message": "智能处理任务已开始"
        })
    except Exception as e:
        logger.error(f"处理开始失败: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/api/process/status/{task_id}")
async def get_process_status(task_id: str):
    """获取处理任务状态"""
    try:
        status = workflow_manager.get_task_status(task_id)
        return JSONResponse({
            "success": True,
            "status": status
        })
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/download")
async def download_manager(request: Request):
    """下载管理页面"""
    return templates.TemplateResponse("download.html", {"request": request})

@app.get("/pt") 
async def pt_manager(request: Request):
    """PT站点管理页面"""
    return templates.TemplateResponse("pt.html", {"request": request})

@app.get("/media")
async def media_library(request: Request):
    """媒体库页面"""
    return templates.TemplateResponse("media.html", {"request": request})

@app.get("/tasks")
async def task_center(request: Request):
    """任务中心页面"""
    return templates.TemplateResponse("tasks.html", {"request": request})

@app.get("/plugins")
async def plugin_market(request: Request):
    """插件市场页面"""
    return templates.TemplateResponse("plugins.html", {"request": request})

@app.get("/settings")
async def system_settings(request: Request):
    """系统设置页面"""
    return templates.TemplateResponse("settings.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接用于实时数据推送"""
    await websocket.accept()
    try:
        while True:
            # 发送实时数据更新
            import random
            data = {
                "type": "stats_update",
                "data": {
                    "cpu": random.randint(20, 40),
                    "memory": random.randint(60, 80),
                    "disk": random.randint(75, 90),
                    "network": f"{random.randint(100, 200)}M/s"
                }
            }
            await websocket.send_json(data)
            await asyncio.sleep(3)  # 每3秒更新一次
    except Exception as e:
        logger.error(f"WebSocket错误: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)