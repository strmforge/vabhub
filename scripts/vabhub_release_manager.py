#!/usr/bin/env python3
"""
VabHub 发布管理器
用于管理多仓库项目的版本发布和GitHub发布流程
"""

import os
import sys
import json
import yaml
import re
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class ReleaseType(Enum):
    """发布类型"""
    MAJOR = "major"
    MINOR = "minor" 
    PATCH = "patch"

class VabHubReleaseManager:
    """VabHub 发布管理器"""
    
    def __init__(self, base_dir: Path = Path("f:\\VabHub"), github_org: str = "strmforge"):
        self.base_dir = base_dir
        self.github_org = github_org
        self.repositories = {
            "core": {
                "path": "VabHub-Core",
                "version_file": "setup.py",
                "changelog_file": "CHANGELOG.md",
                "release_file": "RELEASE_v1.2.0.md",
                "github_repo": "vabhub-core",
                "release_order": 1
            },
            "frontend": {
                "path": "VabHub-Frontend", 
                "version_file": "package.json",
                "changelog_file": "CHANGELOG.md",
                "release_file": "RELEASE_v1.2.0.md",
                "github_repo": "vabhub-frontend",
                "release_order": 2
            },
            "plugins": {
                "path": "VabHub-Plugins",
                "version_file": "setup.py",
                "changelog_file": "CHANGELOG.md",
                "release_file": "RELEASE_v1.2.0.md",
                "github_repo": "vabhub-plugins",
                "release_order": 3
            },
            "deploy": {
                "path": "VabHub-Deploy",
                "version_file": "VERSION",
                "changelog_file": "CHANGELOG.md",
                "release_file": "RELEASE_v1.2.0.md",
                "github_repo": "vabhub-deploy",
                "release_order": 4
            },
            "resources": {
                "path": "VabHub-Resources",
                "version_file": "VERSION",
                "changelog_file": "CHANGELOG.md",
                "release_file": "RELEASE_v1.2.0.md",
                "github_repo": "vabhub-resources",
                "release_order": 5
            }
        }
    
    def get_current_version(self, repo_name: str) -> Optional[str]:
        """获取仓库当前版本"""
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
            elif version_file.name == "setup.py":
                content = version_file.read_text(encoding='utf-8')
                version_match = re.search(r"version=['\"]([^'\"]+)['\"]", content)
                if version_match:
                    return version_match.group(1)
            else:
                # VERSION 文件
                return version_file.read_text(encoding='utf-8').strip()
        except Exception as e:
            print(f"❌ 读取 {repo_name} 版本时出错: {e}")
        
        return None
    
    def set_version(self, repo_name: str, new_version: str) -> bool:
        """设置仓库版本"""
        repo_info = self.repositories[repo_name]
        repo_path = self.base_dir / repo_info["path"]
        
        try:
            version_file = repo_path / repo_info["version_file"]
            
            if version_file.name == "package.json":
                with open(version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                data['version'] = new_version
                
                with open(version_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif version_file.name == "setup.py":
                content = version_file.read_text(encoding='utf-8')
                new_content = re.sub(
                    r"version=['\"]([^'\"]+)['\"]",
                    f"version='{new_version}'",
                    content
                )
                version_file.write_text(new_content, encoding='utf-8')
            else:
                # VERSION 文件
                version_file.write_text(new_version + "\n", encoding='utf-8')
            
            print(f"✅ {repo_name} 版本更新为: {new_version}")
            return True
            
        except Exception as e:
            print(f"❌ 设置 {repo_name} 版本时出错: {e}")
            return False
    
    def bump_version(self, repo_name: str, release_type: ReleaseType) -> Optional[str]:
        """递增版本号"""
        current_version = self.get_current_version(repo_name)
        if not current_version:
            print(f"❌ 无法获取 {repo_name} 的当前版本")
            return None
        
        version_parts = current_version.split('.')
        if len(version_parts) != 3:
            print(f"❌ {repo_name} 的版本格式无效: {current_version}")
            return None
        
        try:
            major = int(version_parts[0])
            minor = int(version_parts[1])
            patch = int(version_parts[2])
            
            if release_type == ReleaseType.MAJOR:
                major += 1
                minor = 0
                patch = 0
            elif release_type == ReleaseType.MINOR:
                minor += 1
                patch = 0
            else:  # PATCH
                patch += 1
            
            new_version = f"{major}.{minor}.{patch}"
            
            if self.set_version(repo_name, new_version):
                return new_version
            
        except ValueError as e:
            print(f"❌ 解析版本号时出错: {e}")
        
        return None
    
    def update_changelog(self, repo_name: str, new_version: str, release_notes: str) -> bool:
        """更新更新日志"""
        repo_info = self.repositories[repo_name]
        repo_path = self.base_dir / repo_info["path"]
        changelog_file = repo_path / repo_info["changelog_file"]
        
        if not changelog_file.exists():
            print(f"⚠️  {repo_name} 的更新日志文件不存在，跳过更新")
            return True
        
        try:
            content = changelog_file.read_text(encoding='utf-8')
            
            # 查找版本标题位置
            version_pattern = r"## \[?\d+\.\d+\.\d+\]?"
            match = re.search(version_pattern, content)
            
            if match:
                # 在现有版本前插入新版本
                insert_pos = match.start()
                new_changelog = content[:insert_pos] + release_notes + "\n\n" + content[insert_pos:]
            else:
                # 在文件开头插入
                new_changelog = release_notes + "\n\n" + content
            
            changelog_file.write_text(new_changelog, encoding='utf-8')
            print(f"✅ {repo_name} 更新日志已更新")
            return True
            
        except Exception as e:
            print(f"❌ 更新 {repo_name} 更新日志时出错: {e}")
            return False
    
    def create_release_branch(self, release_name: str) -> bool:
        """创建发布分支"""
        print(f"🌿 创建发布分支: {release_name}")
        
        for repo_name in self.get_release_order():
            repo_path = self.base_dir / self.repositories[repo_name]["path"]
            
            if repo_path.exists():
                try:
                    # 检查是否在main分支
                    result = subprocess.run(
                        ["git", "branch", "--show-current"], 
                        cwd=repo_path, 
                        capture_output=True, 
                        text=True
                    )
                    
                    current_branch = result.stdout.strip()
                    if current_branch != "main":
                        print(f"⚠️  {repo_name} 不在main分支，切换到main分支")
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
    
    def commit_changes(self, repo_name: str, commit_message: str) -> bool:
        """提交变更"""
        repo_info = self.repositories[repo_name]
        repo_path = self.base_dir / repo_info["path"]
        
        if repo_path.exists():
            try:
                # 添加版本相关文件
                files_to_add = [
                    repo_info["version_file"],
                    repo_info["changelog_file"],
                    repo_info["release_file"]
                ]
                
                for file in files_to_add:
                    if file:
                        file_path = repo_path / file
                        if file_path.exists():
                            subprocess.run(["git", "add", str(file_path)], cwd=repo_path, check=True)
                
                # 提交变更
                subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
                
                print(f"✅ {repo_name} 提交变更成功")
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"❌ {repo_name} 提交变更失败: {e}")
        
        return False
    
    def push_changes(self, repo_name: str, branch_name: str) -> bool:
        """推送变更到远程仓库"""
        repo_path = self.base_dir / self.repositories[repo_name]["path"]
        
        if repo_path.exists():
            try:
                # 推送分支
                subprocess.run(["git", "push", "origin", branch_name], cwd=repo_path, check=True)
                
                print(f"✅ {repo_name} 推送变更成功")
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"❌ {repo_name} 推送变更失败: {e}")
        
        return False
    
    def create_release_tag(self, repo_name: str, tag_name: str) -> bool:
        """创建发布标签"""
        repo_path = self.base_dir / self.repositories[repo_name]["path"]
        
        if repo_path.exists():
            try:
                # 创建标签
                subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], 
                              cwd=repo_path, check=True)
                
                # 推送标签
                subprocess.run(["git", "push", "origin", tag_name], cwd=repo_path, check=True)
                
                print(f"✅ {repo_name} 创建发布标签成功")
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"❌ {repo_name} 创建发布标签失败: {e}")
        
        return False
    
    def get_release_order(self) -> List[str]:
        """获取发布顺序"""
        return sorted(
            self.repositories.keys(),
            key=lambda x: self.repositories[x]["release_order"]
        )
    
    def generate_release_notes(self, repo_name: str, new_version: str) -> str:
        """生成发布说明"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        if repo_name == "core":
            return f"""## 版本 {new_version} ({current_date})

### 🚀 新功能
- **增强的媒体识别算法**：改进的智能识别准确率
- **插件性能优化**：提升插件加载和运行效率
- **API响应优化**：减少API响应时间

### 🔧 技术改进
- **数据库查询优化**：提升数据库查询性能
- **缓存机制增强**：改进Redis缓存策略
- **错误处理改进**：更详细的错误信息和日志

### 🐛 问题修复
- 修复媒体文件重复识别问题
- 修复插件配置保存异常
- 优化内存使用和垃圾回收
"""
        elif repo_name == "frontend":
            return f"""## 版本 {new_version} ({current_date})

### 🚀 新功能
- **响应式布局优化**：改进移动端用户体验
- **主题定制增强**：支持更多主题选项
- **实时通知系统**：WebSocket实时消息推送

### 🔧 技术改进
- **组件性能优化**：减少组件重新渲染
- **打包体积优化**：减小前端包体积
- **加载速度优化**：提升页面加载速度

### 🐛 问题修复
- 修复路由跳转异常
- 修复表单验证问题
- 优化图片懒加载
"""
        else:
            return f"""## 版本 {new_version} ({current_date})

### 🚀 新功能
- 功能增强和性能优化

### 🔧 技术改进
- 代码质量和稳定性提升

### 🐛 问题修复
- 修复已知问题和bug
"""
    
    def create_github_release(self, repo_name: str, tag_name: str, release_notes: str) -> bool:
        """创建GitHub发布版本"""
        print(f"📦 为 {repo_name} 创建GitHub发布版本: {tag_name}")
        
        # 这里需要GitHub token来创建发布
        # 在实际使用中，需要配置GITHUB_TOKEN环境变量
        github_token = os.getenv('GITHUB_TOKEN')
        
        if not github_token:
            print(f"⚠️  未设置GITHUB_TOKEN，跳过GitHub发布创建")
            print(f"   请手动在GitHub上创建发布版本: {tag_name}")
            return True
        
        repo_full_name = f"{self.github_org}/{self.repositories[repo_name]['github_repo']}"
        
        release_data = {
            "tag_name": tag_name,
            "name": f"VabHub {repo_name.title()} {tag_name}",
            "body": release_notes,
            "draft": False,
            "prerelease": False
        }
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"https://api.github.com/repos/{repo_full_name}/releases"
        
        try:
            response = requests.post(url, json=release_data, headers=headers)
            
            if response.status_code == 201:
                print(f"✅ {repo_name} GitHub发布创建成功")
                return True
            else:
                print(f"❌ {repo_name} GitHub发布创建失败: {response.status_code}")
                print(f"   响应: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ {repo_name} GitHub发布创建异常: {e}")
            return False
    
    def release(self, release_type: ReleaseType, create_github_release: bool = False) -> bool:
        """执行发布流程"""
        print("🚀 开始 VabHub 发布流程")
        print("=" * 50)
        
        # 1. 递增核心版本
        core_new_version = self.bump_version("core", release_type)
        if not core_new_version:
            print("❌ 递增核心版本失败")
            return False
        
        release_name = f"v{core_new_version}"
        tag_name = release_name
        
        print(f"📦 发布版本: {release_name}")
        
        # 2. 同步其他仓库版本
        for repo_name in ["frontend", "plugins", "deploy", "resources"]:
            if not self.set_version(repo_name, core_new_version):
                print(f"❌ 同步 {repo_name} 版本失败")
                return False
        
        # 3. 生成发布说明并更新更新日志
        for repo_name in self.get_release_order():
            release_notes = self.generate_release_notes(repo_name, core_new_version)
            
            if not self.update_changelog(repo_name, core_new_version, release_notes):
                print(f"❌ 更新 {repo_name} 更新日志失败")
                return False
        
        # 4. 创建发布分支
        if not self.create_release_branch(release_name):
            print("❌ 创建发布分支失败")
            return False
        
        # 5. 提交变更
        commit_message = f"Release {release_name}"
        for repo_name in self.get_release_order():
            if not self.commit_changes(repo_name, commit_message):
                print(f"❌ {repo_name} 提交变更失败")
                return False
        
        # 6. 推送变更
        for repo_name in self.get_release_order():
            if not self.push_changes(repo_name, release_name):
                print(f"❌ {repo_name} 推送变更失败")
                return False
        
        # 7. 创建发布标签
        for repo_name in self.get_release_order():
            if not self.create_release_tag(repo_name, tag_name):
                print(f"❌ {repo_name} 创建发布标签失败")
                return False
        
        # 8. 创建GitHub发布（可选）
        if create_github_release:
            for repo_name in self.get_release_order():
                release_notes = self.generate_release_notes(repo_name, core_new_version)
                
                if not self.create_github_release(repo_name, tag_name, release_notes):
                    print(f"⚠️  {repo_name} GitHub发布创建失败，请手动创建")
        
        print("\n🎉 VabHub 发布流程完成!")
        print(f"📦 发布版本: {release_name}")
        print(f"🏷️  发布标签: {tag_name}")
        print("\n下一步:")
        print("1. 检查GitHub Actions构建状态")
        print("2. 验证发布包")
        print("3. 合并发布分支到main")
        print("4. 更新文档")
        
        return True

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='VabHub 发布管理器')
    parser.add_argument('command', choices=['release', 'status', 'bump'], 
                       help='命令: release-发布, status-状态, bump-递增版本')
    parser.add_argument('--type', choices=['major', 'minor', 'patch'], default='minor',
                       help='发布类型: major-主版本, minor-次版本, patch-修订版本')
    parser.add_argument('--repo', help='指定仓库名称（仅bump命令使用）')
    parser.add_argument('--github', action='store_true', help='创建GitHub发布版本')
    parser.add_argument('--dir', default='f:\\VabHub', help='工作目录路径')
    
    args = parser.parse_args()
    
    manager = VabHubReleaseManager(Path(args.dir))
    
    if args.command == 'status':
        # 显示版本状态
        print("📊 VabHub 版本状态")
        print("=" * 50)
        
        for repo_name in manager.get_release_order():
            version = manager.get_current_version(repo_name)
            status = "✅" if version else "❌"
            print(f"{status} {repo_name.upper()}: {version or '未知'}")
    
    elif args.command == 'bump':
        # 递增版本
        if not args.repo:
            print("❌ 请指定要递增版本的仓库 (--repo)")
            sys.exit(1)
        
        release_type = ReleaseType(args.type)
        new_version = manager.bump_version(args.repo, release_type)
        
        if new_version:
            print(f"✅ {args.repo} 版本已递增为: {new_version}")
        else:
            print(f"❌ {args.repo} 版本递增失败")
            sys.exit(1)
    
    elif args.command == 'release':
        # 执行发布
        release_type = ReleaseType(args.type)
        success = manager.release(release_type, args.github)
        
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()