#!/bin/bash

# VabHub 部署脚本
# 用于自动化部署VabHub系统

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

# 显示帮助信息
show_help() {
    echo "VabHub 部署脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -e, --environment ENV   部署环境 (dev/prod) 默认: dev"
    echo "  -c, --compose-file FILE Docker Compose文件 默认: docker-compose.yml"
    echo "  -b, --build             重新构建镜像"
    echo "  -f, --force             强制部署（忽略检查）"
    echo "  -h, --help              显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 -e prod -b          生产环境部署并重新构建"
    echo "  $0 --environment dev   开发环境部署"
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装"
        exit 1
    fi
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装"
        exit 1
    fi
    
    log_success "Docker 和 Docker Compose 已安装"
}

# 检查环境配置
check_environment() {
    log_info "检查环境配置..."
    
    # 检查环境变量文件
    if [ ! -f ".env" ]; then
        log_warning ".env 文件不存在，使用默认配置"
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_success "从 .env.example 创建 .env 文件"
        fi
    fi
    
    # 加载环境变量
    if [ -f ".env" ]; then
        set -a
        source .env
        set +a
        log_success "环境变量已加载"
    fi
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 检查端口占用
    local core_port=${CORE_PORT:-8080}
    local web_port=${WEB_PORT:-8090}
    
    if lsof -i :$core_port &> /dev/null; then
        if [ "$FORCE_DEPLOY" != "true" ]; then
            log_error "端口 $core_port 已被占用"
            exit 1
        else
            log_warning "端口 $core_port 已被占用，强制部署"
        fi
    fi
    
    if lsof -i :$web_port &> /dev/null; then
        if [ "$FORCE_DEPLOY" != "true" ]; then
            log_error "端口 $web_port 已被占用"
            exit 1
        else
            log_warning "端口 $web_port 已被占用，强制部署"
        fi
    fi
    
    log_success "健康检查通过"
}

# 构建镜像
build_images() {
    if [ "$BUILD_IMAGES" = "true" ]; then
        log_info "构建Docker镜像..."
        
        # 构建核心服务镜像
        if [ -d "workspace/vabhub-Core" ]; then
            log_info "构建核心服务镜像..."
            docker-compose build core
            log_success "核心服务镜像构建完成"
        fi
        
        # 构建前端服务镜像
        if [ -d "workspace/vabhub-frontend" ]; then
            log_info "构建前端服务镜像..."
            docker-compose build web
            log_success "前端服务镜像构建完成"
        fi
    fi
}

# 部署服务
deploy_services() {
    log_info "部署服务..."
    
    local compose_files="-f $COMPOSE_FILE"
    
    # 添加环境特定的Compose文件
    if [ "$ENVIRONMENT" = "prod" ] && [ -f "docker-compose.prod.yml" ]; then
        compose_files="$compose_files -f docker-compose.prod.yml"
    elif [ "$ENVIRONMENT" = "dev" ] && [ -f "docker-compose.dev.yml" ]; then
        compose_files="$compose_files -f docker-compose.dev.yml"
    fi
    
    # 停止现有服务
    log_info "停止现有服务..."
    docker-compose $compose_files down
    
    # 启动服务
    log_info "启动服务..."
    docker-compose $compose_files up -d
    
    log_success "服务部署完成"
}

# 等待服务就绪
wait_for_services() {
    log_info "等待服务就绪..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps | grep -q "Up"; then
            log_success "所有服务已启动"
            return 0
        fi
        
        log_info "等待服务启动... ($attempt/$max_attempts)"
        sleep 5
        ((attempt++))
    done
    
    log_error "服务启动超时"
    return 1
}

# 验证部署
verify_deployment() {
    log_info "验证部署..."
    
    local core_url="http://localhost:${CORE_PORT:-8080}/health"
    local web_url="http://localhost:${WEB_PORT:-8090}"
    
    # 检查核心服务健康状态
    if curl -s --retry 3 --retry-delay 5 "$core_url" | grep -q "healthy"; then
        log_success "核心服务健康检查通过"
    else
        log_error "核心服务健康检查失败"
        return 1
    fi
    
    # 检查前端服务
    if curl -s --retry 3 --retry-delay 5 "$web_url" &> /dev/null; then
        log_success "前端服务访问正常"
    else
        log_error "前端服务访问失败"
        return 1
    fi
    
    log_success "部署验证通过"
}

# 显示部署信息
show_deployment_info() {
    echo ""
    echo "========================================"
    echo "          VabHub 部署完成"
    echo "========================================"
    echo ""
    echo "🌐 前端界面: http://localhost:${WEB_PORT:-8090}"
    echo "🔧 API文档: http://localhost:${CORE_PORT:-8080}/docs"
    echo "📊 健康检查: http://localhost:${CORE_PORT:-8080}/health"
    echo ""
    echo "📋 服务状态:"
    docker-compose ps
    echo ""
    echo "📈 服务日志:"
    echo "  docker-compose logs -f core"
    echo "  docker-compose logs -f web"
    echo ""
    echo "🛑 停止服务:"
    echo "  docker-compose down"
    echo ""
    echo "========================================"
}

# 主函数
main() {
    # 默认参数
    local ENVIRONMENT="dev"
    local COMPOSE_FILE="docker-compose.yml"
    local BUILD_IMAGES=false
    local FORCE_DEPLOY=false
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            -c|--compose-file)
                COMPOSE_FILE="$2"
                shift 2
                ;;
            -b|--build)
                BUILD_IMAGES=true
                shift
                ;;
            -f|--force)
                FORCE_DEPLOY=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    log_info "开始 VabHub 部署 (环境: $ENVIRONMENT)"
    
    # 执行部署步骤
    check_dependencies
    check_environment
    health_check
    build_images
    deploy_services
    wait_for_services
    verify_deployment
    show_deployment_info
    
    log_success "VabHub 部署完成!"
}

# 运行主函数
main "$@"