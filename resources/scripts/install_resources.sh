#!/bin/bash

# VabHub 资源文件安装脚本
# 将资源文件复制到 VabHub-Core 的适当位置

set -e

# 配置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="$PROJECT_ROOT/../VabHub-Core/app/helper"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# 检查目标目录
check_target_dir() {
    if [ ! -d "$TARGET_DIR" ]; then
        error "目标目录不存在: $TARGET_DIR"
        echo "请确保 VabHub-Core 项目已正确克隆"
        exit 1
    fi
    
    log "目标目录: $TARGET_DIR"
}

# 备份现有文件
backup_existing_files() {
    local backup_dir="$TARGET_DIR/backup_$(date +%Y%m%d_%H%M%S)"
    
    mkdir -p "$backup_dir"
    
    # 备份配置文件
    if [ -f "$TARGET_DIR/config.yaml" ]; then
        cp "$TARGET_DIR/config.yaml" "$backup_dir/"
        log "备份现有配置文件"
    fi
    
    # 备份数据文件
    if [ -d "$TARGET_DIR/data" ]; then
        cp -r "$TARGET_DIR/data" "$backup_dir/" 2>/dev/null || true
        log "备份现有数据文件"
    fi
    
    # 备份二进制文件
    if [ -d "$TARGET_DIR/binaries" ]; then
        cp -r "$TARGET_DIR/binaries" "$backup_dir/" 2>/dev/null || true
        log "备份现有二进制文件"
    fi
    
    if [ "$(ls -A "$backup_dir" 2>/dev/null)" ]; then
        log "备份完成: $backup_dir"
    else
        rmdir "$backup_dir"
    fi
}

# 安装配置文件
install_config_files() {
    log "安装配置文件..."
    
    # 创建配置目录
    mkdir -p "$TARGET_DIR/config"
    
    # 复制配置文件模板
    if [ -d "$PROJECT_ROOT/config" ]; then
        cp -r "$PROJECT_ROOT/config/"* "$TARGET_DIR/config/" 2>/dev/null || true
        log "✓ 配置文件安装完成"
    else
        warn "配置文件目录不存在"
    fi
    
    # 如果不存在主配置文件，创建示例配置
    if [ ! -f "$TARGET_DIR/config/config.yaml" ] && [ -f "$PROJECT_ROOT/config/config.example.yaml" ]; then
        cp "$PROJECT_ROOT/config/config.example.yaml" "$TARGET_DIR/config/config.yaml"
        log "✓ 创建示例配置文件"
    fi
}

# 安装数据模板
install_data_templates() {
    log "安装数据模板..."
    
    # 创建数据目录
    mkdir -p "$TARGET_DIR/data"
    
    # 复制数据模板
    if [ -d "$PROJECT_ROOT/data" ]; then
        cp -r "$PROJECT_ROOT/data/"* "$TARGET_DIR/data/" 2>/dev/null || true
        log "✓ 数据模板安装完成"
    else
        warn "数据模板目录不存在"
    fi
}

# 安装平台二进制文件
install_binaries() {
    log "安装平台二进制文件..."
    
    # 检测当前平台
    local platform=""
    case "$(uname -s)" in
        Linux*)     platform="linux" ;;
        Darwin*)    platform="macos" ;;
        CYGWIN*|MINGW*|MSYS*) platform="windows" ;;
        *)          platform="unknown" ;;
    esac
    
    if [ "$platform" != "unknown" ]; then
        # 创建二进制文件目录
        mkdir -p "$TARGET_DIR/binaries"
        
        # 复制对应平台的二进制文件
        if [ -d "$PROJECT_ROOT/binaries/$platform" ]; then
            cp -r "$PROJECT_ROOT/binaries/$platform/"* "$TARGET_DIR/binaries/" 2>/dev/null || true
            
            # 设置执行权限（Linux/macOS）
            if [ "$platform" != "windows" ]; then
                chmod +x "$TARGET_DIR/binaries/"* 2>/dev/null || true
            fi
            
            log "✓ $platform 平台二进制文件安装完成"
        else
            warn "$platform 平台二进制文件目录不存在"
        fi
    else
        warn "未知平台，跳过二进制文件安装"
    fi
}

# 安装文档资源
install_docs() {
    log "安装文档资源..."
    
    # 创建文档目录
    mkdir -p "$TARGET_DIR/docs"
    
    # 复制文档资源
    if [ -d "$PROJECT_ROOT/docs" ]; then
        cp -r "$PROJECT_ROOT/docs/"* "$TARGET_DIR/docs/" 2>/dev/null || true
        log "✓ 文档资源安装完成"
    else
        warn "文档资源目录不存在"
    fi
}

# 创建版本文件
create_version_file() {
    log "创建版本文件..."
    
    local version_file="$TARGET_DIR/resources.version"
    
    cat > "$version_file" << EOF
# VabHub 资源文件版本信息
install_date: $(date -Iseconds)
resources_version: 1.0.0
platform: $(uname -s)
architecture: $(uname -m)
installed_components:
  - config
  - data
  - binaries
  - docs
EOF
    
    log "✓ 版本文件创建完成"
}

# 验证安装结果
verify_installation() {
    log "验证安装结果..."
    
    local errors=0
    
    # 检查关键文件
    local critical_files=(
        "$TARGET_DIR/config/config.yaml"
        "$TARGET_DIR/resources.version"
    )
    
    for file in "${critical_files[@]}"; do
        if [ ! -f "$file" ]; then
            warn "关键文件缺失: $(basename "$file")"
            ((errors++))
        fi
    done
    
    # 检查目录结构
    local required_dirs=("config" "data" "binaries" "docs")
    
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$TARGET_DIR/$dir" ]; then
            warn "目录缺失: $dir"
            ((errors++))
        fi
    done
    
    if [ $errors -eq 0 ]; then
        log "✅ 资源文件安装验证通过"
    else
        warn "⚠️ 安装完成，但发现 $errors 个问题"
    fi
}

# 显示安装摘要
show_summary() {
    echo ""
    echo "=== VabHub 资源文件安装摘要 ==="
    echo "安装时间: $(date)"
    echo "目标目录: $TARGET_DIR"
    echo ""
    echo "已安装组件:"
    
    if [ -d "$TARGET_DIR/config" ]; then
        echo "  ✓ 配置文件 ($(find "$TARGET_DIR/config" -type f | wc -l) 个文件)"
    fi
    
    if [ -d "$TARGET_DIR/data" ]; then
        echo "  ✓ 数据模板 ($(find "$TARGET_DIR/data" -type f | wc -l) 个文件)"
    fi
    
    if [ -d "$TARGET_DIR/binaries" ]; then
        echo "  ✓ 二进制文件 ($(find "$TARGET_DIR/binaries" -type f | wc -l) 个文件)"
    fi
    
    if [ -d "$TARGET_DIR/docs" ]; then
        echo "  ✓ 文档资源 ($(find "$TARGET_DIR/docs" -type f | wc -l) 个文件)"
    fi
    
    echo ""
    echo "下一步操作:"
    echo "1. 检查配置文件: $TARGET_DIR/config/config.yaml"
    echo "2. 启动 VabHub 服务"
    echo "3. 验证资源文件加载"
    echo ""
}

# 主安装函数
main() {
    log "开始安装 VabHub 资源文件..."
    
    check_target_dir
    backup_existing_files
    install_config_files
    install_data_templates
    install_binaries
    install_docs
    create_version_file
    verify_installation
    show_summary
    
    log "资源文件安装完成"
}

# 显示帮助信息
show_help() {
    echo "VabHub 资源文件安装脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -t, --target DIR   指定目标目录"
    echo "  -h, --help         显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                    # 使用默认目标目录"
    echo "  $0 -t /path/to/core  # 指定目标目录"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--target)
            TARGET_DIR="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            show_help
            exit 1
            ;;
    esac
done

# 执行安装
main