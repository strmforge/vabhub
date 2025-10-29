#!/bin/bash

# VabHub 1.4.0 版本发布脚本
# 自动推送所有仓库到GitHub

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Git配置
check_git_config() {
    log_info "检查Git配置..."
    
    if ! git config --get user.name > /dev/null 2>&1; then
        git config user.name "VabHub Team"
        log_success "设置Git用户名"
    fi
    
    if ! git config --get user.email > /dev/null 2>&1; then
        git config user.email "team@vabhub.org"
        log_success "设置Git邮箱"
    fi
}

# 发布单个仓库
release_repo() {
    local repo_name=$1
    local repo_path=$2
    local github_url=$3
    
    log_info "发布仓库: $repo_name"
    
    cd "$repo_path"
    
    # 检查是否是Git仓库
    if [ ! -d ".git" ]; then
        log_info "初始化Git仓库..."
        git init
    fi
    
    # 检查远程仓库配置
    if ! git remote get-url origin > /dev/null 2>&1; then
        log_info "添加远程仓库..."
        git remote add origin "$github_url"
    fi
    
    # 添加所有文件
    log_info "添加文件到暂存区..."
    git add .
    
    # 提交更改
    log_info "提交更改..."
    git commit -m "release: v1.4.0 - 发现推荐系统重大升级" || {
        log_warning "没有新的更改需要提交"
        return 0
    }
    
    # 推送到主分支
    log_info "推送到GitHub..."
    git push -u origin main || git push -u origin master || {
        # 如果分支不存在，创建并推送
        git branch -M main
        git push -u origin main
    }
    
    # 创建版本标签
    log_info "创建版本标签 v1.4.0..."
    git tag -f v1.4.0 -m "Release $repo_name 1.4.0"
    git push -f origin v1.4.0
    
    log_success "$repo_name 发布完成"
}

# 主函数
main() {
    log_info "开始 VabHub 1.4.0 版本发布..."
    
    # 检查Git配置
    check_git_config
    
    # 定义仓库信息
    declare -A repos=(
        ["VabHub-Core"]="f:/VabHub/VabHub-Core"
        ["VabHub-Frontend"]="f:/VabHub/VabHub-Frontend"
        ["VabHub-Deploy"]="f:/VabHub/VabHub-Deploy"
        ["VabHub-Plugins"]="f:/VabHub/VabHub-Plugins"
    )
    
    declare -A github_urls=(
        ["VabHub-Core"]="https://github.com/vabhub/vabhub-core.git"
        ["VabHub-Frontend"]="https://github.com/vabhub/vabhub-frontend.git"
        ["VabHub-Deploy"]="https://github.com/vabhub/vabhub-deploy.git"
        ["VabHub-Plugins"]="https://github.com/vabhub/vabhub-plugins.git"
    )
    
    # 发布所有仓库
    for repo_name in "${!repos[@]}"; do
        repo_path="${repos[$repo_name]}"
        github_url="${github_urls[$repo_name]}"
        
        if [ -d "$repo_path" ]; then
            release_repo "$repo_name" "$repo_path" "$github_url"
        else
            log_error "仓库路径不存在: $repo_path"
        fi
    done
    
    log_success "所有仓库发布完成!"
    
    # 显示发布信息
    echo ""
    log_info "发布完成，请访问以下链接验证:"
    echo "  - VabHub-Core: https://github.com/vabhub/vabhub-core/releases/tag/v1.4.0"
    echo "  - VabHub-Frontend: https://github.com/vabhub/vabhub-frontend/releases/tag/v1.4.0"
    echo "  - VabHub-Deploy: https://github.com/vabhub/vabhub-deploy/releases/tag/v1.4.0"
    echo "  - VabHub-Plugins: https://github.com/vabhub/vabhub-plugins/releases/tag/v1.4.0"
    echo ""
    log_info "下一步: 在GitHub上创建Release页面并上传发布包"
}

# 执行主函数
main "$@"