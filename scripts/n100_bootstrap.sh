#!/bin/bash
# ============================================================================
# VabHub N100 Bootstrap 脚本 (AUDIT-FOLLOWUP-DEPLOY-N100-1 P1-1)
# ============================================================================
# 在 N100 端执行的初始化脚本，确保部署环境就绪
#
# 职责：
#   1. 确保 /opt/vabhub 存在且是 git 仓库
#   2. 确保 .env.docker 存在（从 .env.docker.example 复制）
#   3. 确保 DB_PASSWORD 存在（不存在则生成）
#   4. docker compose config 验证（提前报错）
#   5. 输出诊断信息（不打印密码）
#
# 使用方法:
#   chmod +x scripts/n100_bootstrap.sh
#   ./scripts/n100_bootstrap.sh
# ============================================================================

set -e

# ==================== 配置 ====================
VABHUB_DIR="${VABHUB_DIR:-/opt/vabhub}"
VABHUB_PORT="${VABHUB_PORT:-52180}"

# ==================== 颜色输出 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

step() { echo -e "\n${CYAN}==> $1${NC}"; }
ok() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ==================== 开始 Bootstrap ====================
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        VabHub N100 Bootstrap (AUDIT-FOLLOWUP)               ║"
echo "║                                                              ║"
echo "║  目录: ${VABHUB_DIR}"
echo "║  端口: ${VABHUB_PORT}"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ==================== 1. 检查目录 ====================
step "检查项目目录"

if [ ! -d "${VABHUB_DIR}" ]; then
    err "目录不存在: ${VABHUB_DIR}\n请先克隆仓库: git clone https://github.com/strmforge/VabHub.git ${VABHUB_DIR}"
fi

cd "${VABHUB_DIR}"

if [ ! -d ".git" ]; then
    err "${VABHUB_DIR} 不是 git 仓库\n请先克隆仓库: git clone https://github.com/strmforge/VabHub.git ${VABHUB_DIR}"
fi

ok "项目目录存在且是 git 仓库"

# ==================== 2. 检查 Docker ====================
step "检查 Docker 环境"

if ! command -v docker >/dev/null 2>&1; then
    err "Docker 未安装"
fi
ok "Docker 已安装: $(docker --version | head -1)"

if ! docker compose version >/dev/null 2>&1; then
    err "Docker Compose V2 未安装"
fi
ok "Docker Compose 已安装: $(docker compose version | head -1)"

# ==================== 3. 检查 .env.docker ====================
step "检查 .env.docker"

if [ ! -f ".env.docker" ]; then
    if [ -f ".env.docker.example" ]; then
        cp .env.docker.example .env.docker
        warn "已从 .env.docker.example 创建 .env.docker"
    else
        # 创建最小 .env.docker
        cat > .env.docker << 'EOF'
# VabHub Docker 环境变量
# 由 bootstrap 脚本自动创建

# 数据库密码（必填）
DB_PASSWORD=

# 端口（默认 52180）
VABHUB_PORT=52180

# 时区
TZ=Asia/Shanghai
EOF
        warn "已创建最小 .env.docker 模板"
    fi
else
    ok ".env.docker 已存在"
fi

# ==================== 4. 检查 DB_PASSWORD ====================
step "检查 DB_PASSWORD"

# 读取当前 DB_PASSWORD
CURRENT_DB_PWD=""
if grep -q '^DB_PASSWORD=' .env.docker; then
    CURRENT_DB_PWD=$(grep '^DB_PASSWORD=' .env.docker | cut -d'=' -f2-)
fi

if [ -z "${CURRENT_DB_PWD}" ]; then
    # 生成随机密码
    NEW_PWD=$(openssl rand -base64 24 | tr -d '/+=' | head -c 24)
    
    if grep -q '^DB_PASSWORD=' .env.docker; then
        # 替换空的 DB_PASSWORD
        sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=${NEW_PWD}/" .env.docker
    else
        # 追加 DB_PASSWORD
        echo "DB_PASSWORD=${NEW_PWD}" >> .env.docker
    fi
    
    warn "已自动生成 DB_PASSWORD（24 位随机字符串）"
    echo -e "${YELLOW}请妥善保管密码，可在 .env.docker 中查看${NC}"
else
    ok "DB_PASSWORD 已设置"
fi

# ==================== 5. 验证 compose config ====================
step "验证 docker-compose 配置"

# 使用 --env-file 显式指定
if docker compose --env-file .env.docker config >/dev/null 2>&1; then
    ok "docker compose config 验证通过"
else
    err "docker compose config 验证失败！\n$(docker compose --env-file .env.docker config 2>&1)"
fi

# ==================== 6. 输出诊断信息 ====================
step "诊断信息"

echo "-------------------------------------------"
echo "Git 分支: $(git branch --show-current)"
echo "Git Commit: $(git rev-parse --short HEAD)"
echo "Docker: $(docker --version | head -1)"
echo "Compose: $(docker compose version | head -1)"
echo "端口: ${VABHUB_PORT}"
echo "-------------------------------------------"

# 检查端口占用
if command -v ss >/dev/null 2>&1; then
    if ss -tlnp 2>/dev/null | grep -q ":${VABHUB_PORT}"; then
        warn "端口 ${VABHUB_PORT} 已被占用（可能是已运行的 VabHub）"
    fi
elif command -v netstat >/dev/null 2>&1; then
    if netstat -tlnp 2>/dev/null | grep -q ":${VABHUB_PORT}"; then
        warn "端口 ${VABHUB_PORT} 已被占用（可能是已运行的 VabHub）"
    fi
fi

# ==================== 完成 ====================
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Bootstrap 完成！环境已就绪。${NC}"
echo ""
echo "下一步："
echo "  git pull origin main"
echo "  docker compose --env-file .env.docker up -d --build"
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
