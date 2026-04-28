#!/bin/bash
# ============================================================================
# VabHub N100 本机自检脚本 (DEPLOY-N100-1 P2)
# ============================================================================
# 部署后在 N100 本机运行，检查服务状态
#
# 使用方法:
#   chmod +x scripts/n100_selfcheck.sh
#   ./scripts/n100_selfcheck.sh
# ============================================================================

set -e

VABHUB_PORT=${VABHUB_PORT:-52180}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${SCRIPT_DIR}/.."

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

step() { echo -e "\n${CYAN}==> $1${NC}"; }
ok() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }

# ==================== 开始检查 ====================
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           VabHub N100 自检脚本 (DEPLOY-N100-1)              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

cd "${PROJECT_DIR}" 2>/dev/null || cd /opt/vabhub

FAILED=0

# ==================== 1. 容器状态 ====================
step "检查容器状态"
if docker compose ps 2>/dev/null; then
    # 检查 vabhub 容器是否运行
    if docker compose ps | grep -q "vabhub.*Up"; then
        ok "vabhub 容器运行中"
    else
        err "vabhub 容器未运行"
        FAILED=1
    fi
else
    err "docker compose ps 失败"
    FAILED=1
fi

# ==================== 2. 健康检查 ====================
step "健康检查 /health"
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "http://localhost:${VABHUB_PORT}/health" 2>/dev/null || echo -e "\n000")
HEALTH_BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)
HEALTH_CODE=$(echo "$HEALTH_RESPONSE" | tail -n 1)

if [ "$HEALTH_CODE" = "200" ]; then
    ok "/health 返回 200"
    echo "$HEALTH_BODY" | head -c 500
    echo ""
else
    err "/health 返回 $HEALTH_CODE"
    FAILED=1
fi

# ==================== 3. 版本检查 ====================
step "版本检查 /api/version"
VERSION_RESPONSE=$(curl -s -w "\n%{http_code}" "http://localhost:${VABHUB_PORT}/api/version" 2>/dev/null || echo -e "\n000")
VERSION_BODY=$(echo "$VERSION_RESPONSE" | head -n -1)
VERSION_CODE=$(echo "$VERSION_RESPONSE" | tail -n 1)

if [ "$VERSION_CODE" = "200" ]; then
    ok "/api/version 返回 200"
    echo "$VERSION_BODY"
elif [ "$VERSION_CODE" = "404" ]; then
    warn "/api/version 不存在 (404)，可忽略"
else
    warn "/api/version 返回 $VERSION_CODE"
fi

# ==================== 4. 端口检查 ====================
step "端口检查"
if netstat -tlnp 2>/dev/null | grep -q ":${VABHUB_PORT}" || ss -tlnp 2>/dev/null | grep -q ":${VABHUB_PORT}"; then
    ok "端口 ${VABHUB_PORT} 已监听"
else
    err "端口 ${VABHUB_PORT} 未监听"
    FAILED=1
fi

# ==================== 5. 磁盘空间 ====================
step "磁盘空间检查"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_USAGE" -lt 90 ]; then
    ok "磁盘使用率 ${DISK_USAGE}%"
else
    warn "磁盘使用率较高: ${DISK_USAGE}%"
fi

# ==================== 结果汇总 ====================
echo ""
echo "════════════════════════════════════════════════════════════════"

if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}✅ 自检通过！${NC}"
    echo ""
    echo "访问地址: http://$(hostname -I | awk '{print $1}'):${VABHUB_PORT}/"
    exit 0
else
    echo -e "${RED}❌ 自检失败！${NC}"
    echo ""
    step "显示最近 200 行日志..."
    docker compose logs -n 200 vabhub 2>/dev/null || docker logs -n 200 vabhub 2>/dev/null || true
    exit 1
fi
