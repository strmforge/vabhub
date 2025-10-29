"""
SmartMedia Hub - Web界面启动脚本
启动现代化媒体文件管理Web界面
"""

import os
import sys
import time
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    required_packages = ['fastapi', 'uvicorn', 'jinja2']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 SmartMedia Hub Web界面启动中...")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查核心文件
    required_files = ['core_simple.py', 'web_interface.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少核心文件: {file}")
            sys.exit(1)
    
    # 检查模板目录
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("❌ 缺少模板目录")
        sys.exit(1)
    
    print("✅ 所有依赖和文件检查通过")
    print("🌐 启动Web服务器...")
    
    try:
        # 导入并启动Web服务器
        from web_interface import app
        import uvicorn
        
        print("📊 服务器信息:")
        print(f"   • 地址: http://0.0.0.0:8095")
        print(f"   • 本地访问: http://localhost:8095")
        print(f"   • 主页: http://localhost:8095/")
        print(f"   • 扫描页面: http://localhost:8095/scan")
        print(f"   • 重命名页面: http://localhost:8095/rename")
        print(f"   • 批量处理: http://localhost:8095/batch")
        print(f"   • 设置页面: http://localhost:8095/settings")
        print("=" * 50)
        print("🎯 服务器已启动，按 Ctrl+C 停止")
        
        # 启动服务器
        uvicorn.run(app, host="0.0.0.0", port=8095, log_level="info")
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()