#!/usr/bin/env python3
"""
VabHub 统一版本管理器
管理多仓库项目的版本发布和协调
"""

import os
import sys
import json
import yaml
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class VersionType(Enum):
    """版本类型"""
    MAJOR = "major"
    MINOR = "minor" 
    PATCH = "patch"

class VabHubVersionManager:
    """VabHub 版本管理器"""
    
    def __init__(self, base_dir: Path = Path("f:\\VabHub")):
        self.base_dir = base_dir
        self.repositories = {
            "core": {
                "path": "VabHub-Core",
                "version_file": "setup.py",
                "package_file": "setup.py",
                "is_core": True,
                "release_order": 1
            },
            "frontend": {
                "path": "VabHub-Frontend", 
                "version_file": "package.json",
                "package_file": "package.json",
                "is_core": False,
                "release_order": 2
            },
            "plugins": {
                "path": "VabHub-Plugins",
                "version_file": "setup.py",
                "package_file": "setup.py",
                "is_core": False,
                "release_order": 3
            },
            "deploy": {
                "path": "VabHub-Deploy",
                "version_file": "VERSION",
                "package_file": None,
                "is_core": False,
                "release_order": 4
            },
            "resources": {
                "path": "VabHub-Resources",
                "version_file": "VERSION",
                "package_file": None,
                "is_core": False,
                "release_order": 5
            }
        }
    
    def get_version(self, repo_name: str) -> Optional[str]:
        """获取仓库版本"""
        repo_info = self.repositories[repo_name]
        repo_path = self.base_dir / repo_info["path"]
        version_file = repo_path / repo_info["version_file"]
        
        if not version_file.exists():
            return None
        
        try:
            if version_file.name == "package.json":
                with open(version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('version')
            else:
                # VERSION 文件或 setup.py
                content = version_file.read_text(encoding='utf-8')
                
                if version_file.name == "setup.py":
                    # 从 setup.py 中提取版本
                    version_match = re.search(r"version=['\"]([^'\"]+)['\"]", content)
                    if version_match:
                        return version_match.group(1)
                else:
                    # VERSION 文件
                    return content.strip()
        except Exception as e:
            print(f"读取 {repo_name} 版本时出错: {e}")
        
        return None
    
    def set_version(self, repo_name: str, new_version: str) -> bool:
        """设置仓库版本"""
        repo_info = self.repositories[repo_name]
        repo_path = self.base_dir / repo_info["path"]
        
        try:
            # 更新 VERSION 文件
            version_file = repo_path / repo_info["version_file"]
            if version_file.name == "package.json":
                with open(version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                data['version'] = new_version
                
                with open(version_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                version_file.write_text(new_version + "\n", encoding='utf-8')
            
            # 更新 package 文件（如果存在）
            if repo_info["package_file"]:
                package_file = repo_path / repo_info["package_file"]
                if package_file.exists():
                    content = package_file.read_text(encoding='utf-8')
                    
                    if package_file.name == "setup.py":
                        # 更新 setup.py 中的版本
                        new_content = re.sub(
                            r"version=['\"]([^'\"]+)['\"]",
                            f"version='{new_version}'",
                            content
                        )
                        package_file.write_text(new_content, encoding='utf-8')
            
            print(f"✅ {repo_name} 版本更新为: {new_version}")
            return True
            
        except Exception as e:
            print(f"❌ 设置 {repo_name} 版本时出错: {e}")
            return False
    
    def bump_version(self, repo_name: str, version_type: VersionType) -> Optional[str]:
        """递增版本号"""
        current_version = self.get_version(repo_name)
        if not current_version:
            print(f"❌ 无法获取 {repo_name} 的当前版本")
            return None
        
        # 解析版本号
        version_parts = current_version.split('.')
        if len(version_parts) != 3:
            print(f"❌ {repo_name} 的版本格式无效: {current_version}")
            return None
        
        try:
            major = int(version_parts[0])
            minor = int(version_parts[1])
            patch = int(version_parts[2])
            
            # 递增版本
            if version_type == VersionType.MAJOR:
                major += 1
                minor = 0
                patch = 0
            elif version_type == VersionType.MINOR:
                minor += 1
                patch = 0
            else:  # PATCH
                patch += 1
            
            new_version = f"{major}.{minor}.{patch}"
            
            # 设置新版本
            if self.set_version(repo_name, new_version):
                return new_version
            
        except ValueError as e:
            print(f"❌ 解析版本号时出错: {e}")
        
        return None
    
    def get_release_order(self) -> List[str]:
        """获取发布顺序"""
        return sorted(
            self.repositories.keys(),
            key=lambda x: self.repositories[x]["release_order"]
        )
    
    def check_version_compatibility(self) -> Dict:
        """检查版本兼容性"""
        results = {
            "compatible": True,
            "issues": [],
            "versions": {}
        }
        
        # 获取所有版本
        for repo_name in self.repositories:
            version = self.get_version(repo_name)
            results["versions"][repo_name] = version
            
            if not version:
                results["compatible"] = False
                results["issues"].append(f"{repo_name}: 无法获取版本")
        
        # 检查核心版本一致性
        core_version = results["versions"]["core"]
        if core_version:
            for repo_name in ["frontend", "plugins"]:
                repo_version = results["versions"][repo_name]
                if repo_version and repo_version != core_version:
                    results["compatible"] = False
                    results["issues"].append(
                        f"{repo_name} 版本 ({repo_version}) 与核心版本 ({core_version}) 不匹配"
                    )
        
        return results
    
    def create_release_branch(self, release_name: str) -> bool:
        """创建发布分支"""
        print(f"🌿 创建发布分支: {release_name}")
        
        for repo_name in self.get_release_order():
            repo_path = self.base_dir / self.repositories[repo_name]["path"]
            
            if repo_path.exists():
                try:
                    # 切换到主分支
                    subprocess.run(["git", "checkout", "main"], cwd=repo_path, check=True)
                    
                    # 拉取最新代码
                    subprocess.run(["git", "pull", "origin", "main"], cwd=repo_path, check=True)
                    
                    # 创建发布分支
                    subprocess.run(["git", "checkout", "-b", release_name], cwd=repo_path, check=True)
                    
                    print(f"✅ {repo_name} 创建发布分支成功")
                    
                except subprocess.CalledProcessError as e:
                    print(f"❌ {repo_name} 创建发布分支失败: {e}")
                    return False
        
        return True
    
    def commit_version_changes(self, release_name: str, message: str = "") -> bool:
        """提交版本变更"""
        if not message:
            message = f"Release {release_name}"
        
        print(f"💾 提交版本变更: {message}")
        
        for repo_name in self.get_release_order():
            repo_path = self.base_dir / self.repositories[repo_name]["path"]
            
            if repo_path.exists():
                try:
                    # 添加版本文件
                    version_files = [
                        self.repositories[repo_name]["version_file"],
                        self.repositories[repo_name]["package_file"]
                    ]
                    
                    for file in version_files:
                        if file:
                            file_path = repo_path / file
                            if file_path.exists():
                                subprocess.run(["git", "add", str(file_path)], cwd=repo_path, check=True)
                    
                    # 提交变更
                    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)
                    
                    print(f"✅ {repo_name} 提交版本变更成功")
                    
                except subprocess.CalledProcessError as e:
                    print(f"❌ {repo_name} 提交版本变更失败: {e}")
                    return False
        
        return True
    
    def create_release_tag(self, release_name: str) -> bool:
        """创建发布标签"""
        print(f"🏷️  创建发布标签: {release_name}")
        
        for repo_name in self.get_release_order():
            repo_path = self.base_dir / self.repositories[repo_name]["path"]
            
            if repo_path.exists():
                try:
                    # 创建标签
                    subprocess.run(["git", "tag", "-a", release_name, "-m", f"Release {release_name}"], 
                                  cwd=repo_path, check=True)
                    
                    # 推送标签
                    subprocess.run(["git", "push", "origin", release_name], cwd=repo_path, check=True)
                    
                    print(f"✅ {repo_name} 创建发布标签成功")
                    
                except subprocess.CalledProcessError as e:
                    print(f"❌ {repo_name} 创建发布标签失败: {e}")
                    return False
        
        return True
    
    def generate_release_notes(self, release_name: str) -> str:
        """生成发布说明"""
        notes = [f"# VabHub {release_name} 发布说明", "", f"发布日期: {datetime.now().strftime('%Y-%m-%d')}", "", "## 版本信息", ""]
        
        # 版本信息
        for repo_name in self.get_release_order():
            version = self.get_version(repo_name)
            if version:
                notes.append(f"- **{repo_name.upper()}**: v{version}")
        
        notes.extend(["", "## 变更内容", "", "### 新功能", "- TODO: 添加新功能描述", "", "### 修复", "- TODO: 添加修复描述", "", "### 改进", "- TODO: 添加改进描述", "", "## 升级说明", "", "1. 备份当前数据", "2. 更新所有仓库到最新版本", "3. 运行数据库迁移（如果需要）", "4. 重启服务", "", "## 已知问题", "- 暂无已知问题", ""])
        
        return "\n".join(notes)
    
    def release(self, version_type: VersionType, release_notes: str = "") -> bool:
        """执行发布流程"""
        print("🚀 开始 VabHub 发布流程")
        print("=" * 50)
        
        # 1. 检查版本兼容性
        compatibility = self.check_version_compatibility()
        if not compatibility["compatible"]:
            print("❌ 版本兼容性检查失败:")
            for issue in compatibility["issues"]:
                print(f"  - {issue}")
            return False
        
        print("✅ 版本兼容性检查通过")
        
        # 2. 递增核心版本
        core_new_version = self.bump_version("core", version_type)
        if not core_new_version:
            print("❌ 递增核心版本失败")
            return False
        
        release_name = f"v{core_new_version}"
        
        # 3. 同步其他仓库版本
        for repo_name in ["frontend", "plugins"]:
            if not self.set_version(repo_name, core_new_version):
                print(f"❌ 同步 {repo_name} 版本失败")
                return False
        
        # 4. 创建发布分支
        if not self.create_release_branch(release_name):
            print("❌ 创建发布分支失败")
            return False
        
        # 5. 提交版本变更
        if not self.commit_version_changes(release_name):
            print("❌ 提交版本变更失败")
            return False
        
        # 6. 创建发布标签
        if not self.create_release_tag(release_name):
            print("❌ 创建发布标签失败")
            return False
        
        # 7. 生成发布说明
        if not release_notes:
            release_notes = self.generate_release_notes(release_name)
        
        # 保存发布说明
        release_notes_file = self.base_dir / f"RELEASE_{release_name}.md"
        release_notes_file.write_text(release_notes, encoding='utf-8')
        
        print("\n🎉 VabHub 发布完成!")
        print(f"📦 发布版本: {release_name}")
        print(f"📄 发布说明: {release_notes_file}")
        print("\n下一步:")
        print("1. 检查 GitHub Actions 构建状态")
        print("2. 验证发布包")
        print("3. 发布到包管理器")
        print("4. 更新文档")
        
        return True

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='VabHub 统一版本管理器')
    parser.add_argument('command', choices=['bump', 'release', 'status', 'check'], 
                       help='命令: bump-递增版本, release-发布, status-状态, check-检查')
    parser.add_argument('--repo', help='指定仓库名称')
    parser.add_argument('--type', choices=['major', 'minor', 'patch'], default='patch',
                       help='版本类型: major-主版本, minor-次版本, patch-修订版本')
    parser.add_argument('--dir', default='f:\\VabHub', help='工作目录路径')
    parser.add_argument('--notes', help='发布说明文件路径')
    
    args = parser.parse_args()
    
    manager = VabHubVersionManager(Path(args.dir))
    
    if args.command == 'status':
        # 显示版本状态
        print("📊 VabHub 版本状态")
        print("=" * 50)
        
        for repo_name in manager.get_release_order():
            version = manager.get_version(repo_name)
            status = "✅" if version else "❌"
            print(f"{status} {repo_name.upper()}: {version or '未知'}")
        
        # 检查兼容性
        compatibility = manager.check_version_compatibility()
        print(f"\n🔗 兼容性: {'✅ 通过' if compatibility['compatible'] else '❌ 失败'}")
        
        if compatibility["issues"]:
            print("⚠️  问题:")
            for issue in compatibility["issues"]:
                print(f"  - {issue}")
    
    elif args.command == 'check':
        # 检查版本兼容性
        compatibility = manager.check_version_compatibility()
        
        if compatibility["compatible"]:
            print("✅ 所有版本兼容性检查通过")
            sys.exit(0)
        else:
            print("❌ 版本兼容性检查失败:")
            for issue in compatibility["issues"]:
                print(f"  - {issue}")
            sys.exit(1)
    
    elif args.command == 'bump':
        # 递增版本
        if not args.repo:
            print("❌ 请指定要递增版本的仓库 (--repo)")
            sys.exit(1)
        
        version_type = VersionType(args.type)
        new_version = manager.bump_version(args.repo, version_type)
        
        if new_version:
            print(f"✅ {args.repo} 版本已递增为: {new_version}")
        else:
            print(f"❌ {args.repo} 版本递增失败")
            sys.exit(1)
    
    elif args.command == 'release':
        # 执行发布
        version_type = VersionType(args.type)
        
        # 读取发布说明
        release_notes = ""
        if args.notes:
            notes_file = Path(args.notes)
            if notes_file.exists():
                release_notes = notes_file.read_text(encoding='utf-8')
        
        success = manager.release(version_type, release_notes)
        
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()