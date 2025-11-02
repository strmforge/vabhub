#!/bin/bash

# VabHub Resources 安装脚本
# 用于安装和配置系统资源

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

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python $PYTHON_VERSION 已安装"
    else
        log_error "Python3 未安装"
        exit 1
    fi
    
    # 检查必要的Python包
    REQUIRED_PACKAGES=("pyyaml" "requests" "python-dotenv")
    for package in "${REQUIRED_PACKAGES[@]}"; do
        if python3 -c "import $package" &> /dev/null; then
            log_success "Python包 $package 已安装"
        else
            log_warning "Python包 $package 未安装，将尝试安装..."
            pip3 install "$package"
        fi
    done
}

# 创建配置目录
create_directories() {
    log_info "创建配置目录..."
    
    DIRECTORIES=(
        "$HOME/.vabhub"
        "$HOME/.vabhub/config"
        "$HOME/.vabhub/data"
        "$HOME/.vabhub/cache"
        "$HOME/.vabhub/logs"
    )
    
    for dir in "${DIRECTORIES[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_success "创建目录: $dir"
        else
            log_info "目录已存在: $dir"
        fi
    done
}

# 复制配置文件
copy_config_files() {
    log_info "复制配置文件..."
    
    CONFIG_FILES=(
        "config/categories.yaml"
        "config/charts_config.yaml"
        "config/media_library.yaml"
        "config/storage_config.yaml"
        "config/config.example.yaml"
    )
    
    for config_file in "${CONFIG_FILES[@]}"; do
        if [ -f "$config_file" ]; then
            cp "$config_file" "$HOME/.vabhub/config/"
            log_success "复制配置文件: $config_file"
        else
            log_warning "配置文件不存在: $config_file"
        fi
    done
    
    # 创建默认配置文件
    if [ ! -f "$HOME/.vabhub/config/config.yaml" ]; then
        cp "config/config.example.yaml" "$HOME/.vabhub/config/config.yaml"
        log_success "创建默认配置文件"
    fi
}

# 安装数据文件
install_data_files() {
    log_info "安装数据文件..."
    
    DATA_FILES=(
        "data/media_database.json"
    )
    
    for data_file in "${DATA_FILES[@]}"; do
        if [ -f "$data_file" ]; then
            cp "$data_file" "$HOME/.vabhub/data/"
            log_success "安装数据文件: $data_file"
        else
            log_warning "数据文件不存在: $data_file"
        fi
    done
}

# 设置环境变量
setup_environment() {
    log_info "设置环境变量..."
    
    # 检查是否已设置环境变量
    if [ -z "$VABHUB_HOME" ]; then
        echo "export VABHUB_HOME=\$HOME/.vabhub" >> "$HOME/.bashrc"
        echo "export VABHUB_CONFIG=\$VABHUB_HOME/config" >> "$HOME/.bashrc"
        echo "export VABHUB_DATA=\$VABHUB_HOME/data" >> "$HOME/.bashrc"
        log_success "环境变量已添加到 .bashrc"
    else
        log_info "环境变量已设置"
    fi
    
    # 重新加载bashrc
    source "$HOME/.bashrc"
}

# 验证安装
verify_installation() {
    log_info "验证安装..."
    
    # 检查关键文件
    REQUIRED_FILES=(
        "$VABHUB_CONFIG/config.yaml"
        "$VABHUB_CONFIG/categories.yaml"
        "$VABHUB_CONFIG/charts_config.yaml"
        "$VABHUB_DATA/media_database.json"
    )
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            log_success "文件存在: $file"
        else
            log_error "文件不存在: $file"
            exit 1
        fi
    done
    
    # 检查目录权限
    REQUIRED_DIRS=("$VABHUB_HOME" "$VABHUB_CONFIG" "$VABHUB_DATA")
    for dir in "${REQUIRED_DIRS[@]}"; do
        if [ -w "$dir" ]; then
            log_success "目录可写: $dir"
        else
            log_error "目录不可写: $dir"
            exit 1
        fi
    done
}

# 主函数
main() {
    log_info "开始安装 VabHub Resources..."
    
    # 检查是否以root用户运行
    if [ "$EUID" -eq 0 ]; then
        log_warning "不建议以root用户运行此脚本"
        read -p "是否继续? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # 执行安装步骤
    check_dependencies
    create_directories
    copy_config_files
    install_data_files
    setup_environment
    verify_installation
    
    log_success "VabHub Resources 安装完成!"
    log_info "配置文件位置: $VABHUB_CONFIG"
    log_info "数据文件位置: $VABHUB_DATA"
    log_info "请编辑 $VABHUB_CONFIG/config.yaml 文件进行配置"
}

# 运行主函数
main "$@"