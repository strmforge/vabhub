#!/bin/bash

# VabHub 1.3.0 GitHub 发布脚本
# 用于自动化创建 GitHub Release 和推送版本

set -e

# 配置变量
VERSION="1.3.0"
REPO_NAME="vabhub/vabhub"
MAIN_BRANCH="main"
RELEASE_TAG="v${VERSION}"
RELEASE_NOTES="GITHUB_RELEASE_1.3.0.md"
CHANGELOG="CHANGELOG.md"

# 颜色输出
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

# 检查依赖
check_dependencies() {
    log_info "检查依赖工具..."
    
    if ! command -v git &> /dev/null; then
        log_error "Git 未安装"
        exit 1
    fi
    
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI 未安装，请先安装: https://cli.github.com"
        exit 1
    fi
    
    log_success "依赖检查通过"
}

# 检查Git状态
check_git_status() {
    log_info "检查Git状态..."
    
    # 检查是否在Git仓库中
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "当前目录不是Git仓库"
        exit 1
    fi
    
    # 检查是否有未提交的更改
    if [[ -n $(git status --porcelain) ]]; then
        log_warning "检测到未提交的更改"
        echo "建议先提交更改再发布版本"
        read -p "是否继续? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "发布取消"
            exit 0
        fi
    fi
    
    # 检查远程仓库
    if ! git ls-remote --get-url origin | grep -q "github.com"; then
        log_warning "远程仓库可能不是GitHub"
    fi
    
    log_success "Git状态检查通过"
}

# 更新版本号
update_versions() {
    log_info "更新版本号..."
    
    # 更新前端版本
    sed -i 's/"version": "1.2.0"/"version": "1.3.0"/' VabHub-Frontend/package.json
    
    # 更新后端版本
    sed -i 's/version="1.0.0"/version="1.3.0"/' VabHub-Core/setup.py
    
    # 提交版本更新
    git add VabHub-Frontend/package.json VabHub-Core/setup.py
    git commit -m "chore: bump version to 1.3.0"
    
    log_success "版本号更新完成"
}

# 创建标签
create_tag() {
    log_info "创建版本标签 ${RELEASE_TAG}..."
    
    # 检查标签是否已存在
    if git rev-parse "${RELEASE_TAG}" >/dev/null 2>&1; then
        log_warning "标签 ${RELEASE_TAG} 已存在"
        read -p "是否删除并重新创建? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git tag -d "${RELEASE_TAG}"
            git push --delete origin "${RELEASE_TAG}" 2>/dev/null || true
        else
            log_info "跳过标签创建"
            return
        fi
    fi
    
    # 创建带注释的标签
    git tag -a "${RELEASE_TAG}" -m "Release version ${VERSION}"
    
    log_success "标签创建完成"
}

# 推送更改
push_changes() {
    log_info "推送更改到远程仓库..."
    
    git push origin "${MAIN_BRANCH}"
    git push origin "${RELEASE_TAG}"
    
    log_success "更改推送完成"
}

# 创建GitHub Release
create_release() {
    log_info "创建GitHub Release..."
    
    # 检查发布说明文件是否存在
    if [[ ! -f "${RELEASE_NOTES}" ]]; then
        log_error "发布说明文件 ${RELEASE_NOTES} 不存在"
        exit 1
    fi
    
    # 创建发布
    gh release create "${RELEASE_TAG}" \
        --title "VabHub ${VERSION}" \
        --notes-file "${RELEASE_NOTES}" \
        --target "${MAIN_BRANCH}"
    
    log_success "GitHub Release 创建完成"
}

# 生成发布包
create_release_package() {
    log_info "生成发布包..."
    
    # 创建临时目录
    TEMP_DIR=$(mktemp -d)
    PACKAGE_NAME="vabhub-${VERSION}.zip"
    
    # 复制必要文件
    cp -r VabHub-Core "${TEMP_DIR}/"
    cp -r VabHub-Frontend "${TEMP_DIR}/"
    cp -r VabHub-Plugins "${TEMP_DIR}/"
    cp -r VabHub-Deploy "${TEMP_DIR}/"
    cp -r VabHub-Resources "${TEMP_DIR}/"
    cp README.md "${TEMP_DIR}/"
    cp CHANGELOG.md "${TEMP_DIR}/"
    cp RELEASE_v1.3.0.md "${TEMP_DIR}/"
    
    # 清理不必要的文件
    find "${TEMP_DIR}" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find "${TEMP_DIR}" -name "*.pyc" -delete
    find "${TEMP_DIR}" -name ".git" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # 创建压缩包
    cd "${TEMP_DIR}"
    zip -r "${PACKAGE_NAME}" .
    cd -
    
    # 移动压缩包到当前目录
    mv "${TEMP_DIR}/${PACKAGE_NAME}" .
    
    # 清理临时目录
    rm -rf "${TEMP_DIR}"
    
    log_success "发布包生成完成: ${PACKAGE_NAME}"
}

# 上传发布包
upload_release_assets() {
    log_info "上传发布包到GitHub Release..."
    
    PACKAGE_NAME="vabhub-${VERSION}.zip"
    
    if [[ -f "${PACKAGE_NAME}" ]]; then
        gh release upload "${RELEASE_TAG}" "${PACKAGE_NAME}"
        log_success "发布包上传完成"
    else
        log_warning "发布包 ${PACKAGE_NAME} 不存在，跳过上传"
    fi
}

# 更新README版本信息
update_readme() {
    log_info "更新README版本信息..."
    
    # 备份原文件
    cp README.md README.md.backup
    
    # 更新版本信息
    sed -i 's/版本 1.2.0/版本 1.3.0/g' README.md
    sed -i 's/v1.2.0/v1.3.0/g' README.md
    
    # 提交更新
    git add README.md
    git commit -m "docs: update README for version 1.3.0"
    git push origin "${MAIN_BRANCH}"
    
    log_success "README更新完成"
}

# 主函数
main() {
    log_info "开始 VabHub ${VERSION} 发布流程"
    
    # 检查依赖
    check_dependencies
    
    # 检查Git状态
    check_git_status
    
    # 更新版本号
    update_versions
    
    # 创建标签
    create_tag
    
    # 推送更改
    push_changes
    
    # 生成发布包
    create_release_package
    
    # 创建GitHub Release
    create_release
    
    # 上传发布包
    upload_release_assets
    
    # 更新README
    update_readme
    
    log_success "VabHub ${VERSION} 发布完成!"
    echo ""
    echo "发布信息:"
    echo "- 版本: ${VERSION}"
    echo "- 标签: ${RELEASE_TAG}"
    echo "- 发布包: vabhub-${VERSION}.zip"
    echo "- GitHub Release: https://github.com/${REPO_NAME}/releases/tag/${RELEASE_TAG}"
    echo ""
    echo "下一步:"
    echo "1. 验证发布内容"
    echo "2. 更新文档网站"
    echo "3. 通知社区成员"
}

# 执行主函数
main "$@"