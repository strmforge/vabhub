#!/usr/bin/env python3
"""
VabHub 新建仓库流程工具
用于创建和管理 VabHub 多仓库架构中的新仓库
"""

import os
import sys
import json
import yaml
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
from enum import Enum

class RepoType(Enum):
    """仓库类型"""
    CORE = "core"           # 核心功能模块
    FRONTEND = "frontend"   # 前端界面
    PLUGIN = "plugin"       # 插件系统
    DEPLOY = "deploy"       # 部署配置
    RESOURCE = "resource"   # 资源文件
    SERVICE = "service"     # 微服务
    TOOL = "tool"          # 开发工具

class RepoCreator:
    """VabHub 仓库创建器"""
    
    def __init__(self, base_dir: Path = Path("f:\\VabHub")):
        self.base_dir = base_dir
        self.existing_repos = self._scan_existing_repos()
        
        # 仓库模板配置
        self.repo_templates = {
            RepoType.CORE: {
                "name_pattern": "VabHub-{name}",
                "description": "VabHub 核心功能模块",
                "files": [
                    "README.md",
                    "VERSION",
                    "setup.py",
                    "requirements.txt",
                    "src/{name}/__init__.py",
                    "src/{name}/core.py",
                    "tests/__init__.py",
                    "tests/test_core.py",
                    ".gitignore",
                    ".github/workflows/ci.yml"
                ],
                "dependencies": ["VabHub-Core"]
            },
            RepoType.FRONTEND: {
                "name_pattern": "VabHub-{name}",
                "description": "VabHub 前端界面模块",
                "files": [
                    "README.md",
                    "package.json",
                    "package-lock.json",
                    "src/main.js",
                    "src/App.vue",
                    "src/components/HelloWorld.vue",
                    "public/index.html",
                    ".gitignore",
                    "vite.config.js",
                    ".github/workflows/ci.yml"
                ],
                "dependencies": ["VabHub-Frontend"]
            },
            RepoType.PLUGIN: {
                "name_pattern": "VabHub-{name}-Plugin",
                "description": "VabHub 插件模块",
                "files": [
                    "README.md",
                    "VERSION",
                    "setup.py",
                    "src/{name}_plugin/__init__.py",
                    "src/{name}_plugin/plugin.py",
                    "config/config.yaml",
                    "tests/__init__.py",
                    "tests/test_plugin.py",
                    ".gitignore",
                    ".github/workflows/ci.yml"
                ],
                "dependencies": ["VabHub-Core", "VabHub-Plugins"]
            },
            RepoType.DEPLOY: {
                "name_pattern": "VabHub-{name}-Deploy",
                "description": "VabHub 部署配置模块",
                "files": [
                    "README.md",
                    "VERSION",
                    "docker-compose.yml",
                    "Dockerfile",
                    "config/deploy.yaml",
                    "scripts/deploy.sh",
                    ".gitignore",
                    ".github/workflows/deploy.yml"
                ],
                "dependencies": ["VabHub-Deploy"]
            },
            RepoType.RESOURCE: {
                "name_pattern": "VabHub-{name}-Resources",
                "description": "VabHub 资源文件模块",
                "files": [
                    "README.md",
                    "VERSION",
                    "resources/README.md",
                    "config/resources.yaml",
                    ".gitignore"
                ],
                "dependencies": ["VabHub-Resources"]
            },
            RepoType.SERVICE: {
                "name_pattern": "VabHub-{name}-Service",
                "description": "VabHub 微服务模块",
                "files": [
                    "README.md",
                    "VERSION",
                    "setup.py",
                    "src/{name}_service/__init__.py",
                    "src/{name}_service/service.py",
                    "src/{name}_service/api.py",
                    "config/service.yaml",
                    "tests/__init__.py",
                    "tests/test_service.py",
                    "Dockerfile",
                    ".gitignore",
                    ".github/workflows/ci.yml"
                ],
                "dependencies": ["VabHub-Core"]
            },
            RepoType.TOOL: {
                "name_pattern": "VabHub-{name}-Tool",
                "description": "VabHub 开发工具模块",
                "files": [
                    "README.md",
                    "VERSION",
                    "src/{name}_tool/__init__.py",
                    "src/{name}_tool/tool.py",
                    "config/tool.yaml",
                    "scripts/run.py",
                    ".gitignore"
                ],
                "dependencies": []
            }
        }
    
    def _scan_existing_repos(self) -> Set[str]:
        """扫描现有仓库"""
        existing = set()
        for item in self.base_dir.iterdir():
            if item.is_dir() and item.name.startswith("VabHub-"):
                existing.add(item.name)
        return existing
    
    def validate_repo_name(self, name: str, repo_type: RepoType) -> Dict[str, str]:
        """验证仓库名称"""
        errors = []
        
        # 基本验证
        if not name:
            errors.append("仓库名称不能为空")
        
        if len(name) < 2:
            errors.append("仓库名称至少需要2个字符")
        
        if len(name) > 50:
            errors.append("仓库名称不能超过50个字符")
        
        # 命名规范验证
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name):
            errors.append("仓库名称只能包含字母、数字、下划线和连字符，且必须以字母开头")
        
        # 生成完整仓库名称
        template = self.repo_templates[repo_type]["name_pattern"]
        full_name = template.format(name=name)
        
        # 检查是否已存在
        if full_name in self.existing_repos:
            errors.append(f"仓库 '{full_name}' 已存在")
        
        return {
            "valid": len(errors) == 0,
            "full_name": full_name,
            "errors": errors
        }
    
    def generate_repo_structure(self, name: str, repo_type: RepoType, description: str = "") -> Dict:
        """生成仓库结构"""
        # 验证名称
        validation = self.validate_repo_name(name, repo_type)
        if not validation["valid"]:
            return {"success": False, "errors": validation["errors"]}
        
        full_name = validation["full_name"]
        repo_path = self.base_dir / full_name
        
        # 创建仓库目录
        repo_path.mkdir(exist_ok=True)
        
        # 生成文件内容
        template_config = self.repo_templates[repo_type]
        
        # 文件模板内容
        file_templates = {
            "README.md": self._generate_readme(name, repo_type, description or template_config["description"]),
            "VERSION": "0.1.0\n",
            "setup.py": self._generate_setup_py(name, repo_type),
            "package.json": self._generate_package_json(name, repo_type),
            "src/{name}/__init__.py": self._generate_init_py(name, repo_type),
            "src/{name}/core.py": self._generate_core_py(name, repo_type),
            "docker-compose.yml": self._generate_docker_compose(name, repo_type),
            "Dockerfile": self._generate_dockerfile(name, repo_type),
            ".gitignore": self._generate_gitignore(repo_type),
            ".github/workflows/ci.yml": self._generate_ci_workflow(name, repo_type)
        }
        
        # 创建文件结构
        created_files = []
        
        for file_pattern in template_config["files"]:
            # 替换模板变量
            file_path = file_pattern.format(name=name)
            full_file_path = repo_path / file_path
            
            # 创建目录
            full_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 获取文件内容模板
            content = ""
            for template_key, template_content in file_templates.items():
                if template_key in file_path or file_path.endswith(template_key):
                    content = template_content
                    break
            
            # 如果没有找到模板，创建空文件
            if not content:
                content = f"# {file_path}\n\nThis file was auto-generated by VabHub Repo Creator.\n"
            
            # 写入文件
            full_file_path.write_text(content, encoding='utf-8')
            created_files.append(str(full_file_path.relative_to(self.base_dir)))
        
        return {
            "success": True,
            "repo_path": str(repo_path),
            "full_name": full_name,
            "created_files": created_files,
            "repo_type": repo_type.value
        }
    
    def initialize_git_repo(self, repo_name: str) -> Dict:
        """初始化 Git 仓库"""
        repo_path = self.base_dir / repo_name
        
        if not repo_path.exists():
            return {"success": False, "error": f"仓库 '{repo_name}' 不存在"}
        
        try:
            # 初始化 Git 仓库
            subprocess.run(["git", "init"], cwd=repo_path, check=True)
            
            # 添加初始提交
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit: Repository created by VabHub Repo Creator"], 
                          cwd=repo_path, check=True)
            
            return {"success": True, "message": "Git 仓库初始化成功"}
            
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"Git 初始化失败: {e}"}
    
    def create_github_repo(self, repo_name: str, is_public: bool = True, description: str = "") -> Dict:
        """创建 GitHub 仓库（需要 GitHub CLI）"""
        repo_path = self.base_dir / repo_name
        
        if not repo_path.exists():
            return {"success": False, "error": f"仓库 '{repo_name}' 不存在"}
        
        try:
            # 检查是否已安装 GitHub CLI
            result = subprocess.run(["gh", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                return {"success": False, "error": "GitHub CLI (gh) 未安装，请先安装 gh 命令行工具"}
            
            # 创建 GitHub 仓库
            visibility = "--public" if is_public else "--private"
            
            cmd = ["gh", "repo", "create", repo_name, visibility, "--description", description or repo_name]
            subprocess.run(cmd, cwd=repo_path, check=True)
            
            # 添加远程仓库
            subprocess.run(["git", "remote", "add", "origin", f"https://github.com/VabHub/{repo_name}.git"], 
                          cwd=repo_path, check=True)
            
            # 推送代码
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path, check=True)
            
            return {
                "success": True, 
                "message": "GitHub 仓库创建成功",
                "url": f"https://github.com/VabHub/{repo_name}"
            }
            
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"GitHub 仓库创建失败: {e}"}
    
    def generate_dependency_config(self, repo_name: str, dependencies: List[str]) -> Dict:
        """生成依赖配置"""
        repo_path = self.base_dir / repo_name
        
        if not repo_path.exists():
            return {"success": False, "error": f"仓库 '{repo_name}' 不存在"}
        
        # 创建依赖配置文件
        config = {
            "repo_name": repo_name,
            "dependencies": dependencies,
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        
        config_file = repo_path / "dependencies.json"
        config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
        
        return {"success": True, "config_file": str(config_file.relative_to(self.base_dir))}
    
    def _generate_readme(self, name: str, repo_type: RepoType, description: str) -> str:
        """生成 README.md"""
        template_config = self.repo_templates[repo_type]
        full_name = template_config["name_pattern"].format(name=name)
        
        return f"""# {full_name}

{description}

## 功能特性

- TODO: 添加功能特性描述

## 快速开始

### 安装依赖

```bash
# 根据仓库类型选择安装方式
pip install -r requirements.txt  # Python 项目
npm install  # Node.js 项目
```

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/VabHub/{full_name}.git
cd {full_name}

# 安装依赖
# 根据项目类型执行相应命令

# 运行测试
python -m pytest  # Python 项目
npm test  # Node.js 项目
```

## 项目结构

```
{full_name}/
├── src/           # 源代码
├── tests/         # 测试代码
├── config/        # 配置文件
├── docs/          # 文档
├── scripts/       # 脚本文件
└── README.md      # 项目说明
```

## 开发指南

### 代码规范

- 遵循 PEP 8 (Python) 或相应的代码规范
- 使用类型注解
- 编写单元测试
- 保持文档更新

### 提交规范

- feat: 新功能
- fix: 修复问题
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具变动

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！
"""
    
    def _generate_setup_py(self, name: str, repo_type: RepoType) -> str:
        """生成 setup.py"""
        return f"""#!/usr/bin/env python3
"""
VabHub {name} - {self.repo_templates[repo_type]['description']}
"""

from setuptools import setup, find_packages

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read().strip()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="vabhub-{name.lower()}",
    version=version,
    description="{self.repo_templates[repo_type]['description']}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="VabHub Team",
    author_email="team@vabhub.org",
    url=f"https://github.com/VabHub/VabHub-{name}",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    python_requires=">=3.8",
    install_requires=[
        # 添加项目依赖
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
"""
    
    def _generate_package_json(self, name: str, repo_type: RepoType) -> str:
        """生成 package.json"""
        return f"""{{
  "name": "@vabhub/{name.lower()}",
  "version": "0.1.0",
  "description": "{self.repo_templates[repo_type]['description']}",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest"
  }},
  "dependencies": {{
    "vue": "^3.3.0"
  }},
  "devDependencies": {{
    "@vitejs/plugin-vue": "^4.0.0",
    "vite": "^4.0.0",
    "vitest": "^0.25.0"
  }},
  "keywords": ["vabhub", "{name}", "frontend"],
  "author": "VabHub Team",
  "license": "MIT"
}}
"""
    
    def _generate_init_py(self, name: str, repo_type: RepoType) -> str:
        """生成 __init__.py"""
        return f""""""
VabHub {name} Module
"""

__version__ = "0.1.0"
__author__ = "VabHub Team"

from .core import {name.title()}Core

__all__ = ["{name.title()}Core"]
"""
    
    def _generate_core_py(self, name: str, repo_type: RepoType) -> str:
        """生成 core.py"""
        return f""""""
{name.title()} Core Module
"""

class {name.title()}Core:
    """{name.title()} 核心功能类"""
    
    def __init__(self):
        self.name = "{name}"
        self.version = "0.1.0"
    
    def hello(self) -> str:
        """示例方法"""
        return f"Hello from {{self.name}} v{{self.version}}"
"""
    
    def _generate_docker_compose(self, name: str, repo_type: RepoType) -> str:
        """生成 docker-compose.yml"""
        return f"""version: '3.8'

services:
  {name.lower()}:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=development
    volumes:
      - ./config:/app/config
"""
    
    def _generate_dockerfile(self, name: str, repo_type: RepoType) -> str:
        """生成 Dockerfile"""
        return f"""FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "{name}"]
"""
    
    def _generate_gitignore(self, repo_type: RepoType) -> str:
        """生成 .gitignore"""
        return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# OS
.DS_Store
Thumbs.db
"""
    
    def _generate_ci_workflow(self, name: str, repo_type: RepoType) -> str:
        """生成 CI 工作流"""
        return f"""name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest
"""

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='VabHub 新建仓库流程工具')
    parser.add_argument('name', help='新仓库的名称（不含VabHub前缀）')
    parser.add_argument('--type', choices=[t.value for t in RepoType], required=True,
                       help='仓库类型')
    parser.add_argument('--description', help='仓库描述')
    parser.add_argument('--init-git', action='store_true', help='初始化 Git 仓库')
    parser.add_argument('--create-github', action='store_true', help='创建 GitHub 仓库')
    parser.add_argument('--public', action='store_true', help='创建公开仓库（默认私有）')
    parser.add_argument('--dir', default='f:\\VabHub', help='工作目录路径')
    
    args = parser.parse_args()
    
    creator = RepoCreator(Path(args.dir))
    
    # 生成仓库结构
    repo_type = RepoType(args.type)
    result = creator.generate_repo_structure(args.name, repo_type, args.description)
    
    if not result["success"]:
        print("❌ 创建仓库失败:")
        for error in result["errors"]:
            print(f"  - {error}")
        sys.exit(1)
    
    print(f"✅ 仓库创建成功: {result['full_name']}")
    print(f"📁 位置: {result['repo_path']}")
    print(f"📄 创建的文件:")
    for file in result["created_files"]:
        print(f"  - {file}")
    
    # 初始化 Git 仓库
    if args.init_git:
        git_result = creator.initialize_git_repo(result["full_name"])
        if git_result["success"]:
            print(f"✅ {git_result['message']}")
        else:
            print(f"⚠️  Git 初始化失败: {git_result['error']}")
    
    # 创建 GitHub 仓库
    if args.create_github:
        github_result = creator.create_github_repo(
            result["full_name"], 
            args.public, 
            args.description or result["full_name"]
        )
        if github_result["success"]:
            print(f"✅ {github_result['message']}")
            print(f"🌐 仓库地址: {github_result['url']}")
        else:
            print(f"⚠️  GitHub 仓库创建失败: {github_result['error']}")
    
    print("\n🎉 新建仓库流程完成!")
    print("\n下一步建议:")
    print("1. 完善代码实现")
    print("2. 添加测试用例")
    print("3. 更新文档")
    print("4. 配置持续集成")

if __name__ == "__main__":
    main()