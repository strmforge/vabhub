<#
.SYNOPSIS
    VabHub N100 一键部署脚本 (AUDIT-FOLLOWUP-DEPLOY-N100-1)

.DESCRIPTION
    从 Windows 通过 SSH 将 VabHub 部署到 N100 服务器
    所有 docker 命令只在 N100 远程执行，不会在本机执行
    
    流程：SSH → bootstrap → git pull → docker compose up

.PARAMETER Host
    目标服务器 IP（默认 192.168.50.102）

.PARAMETER User
    SSH 用户名（默认 haishuai）

.PARAMETER Dir
    远程项目目录（默认 /opt/vabhub）

.PARAMETER Port
    VabHub 端口（默认 52180）

.PARAMETER NoBuild
    跳过 build，只执行 docker compose up -d

.PARAMETER TailLogs
    部署后自动显示最近 200 行日志

.PARAMETER NoPull
    跳过 git pull

.PARAMETER BootstrapOnly
    只执行 bootstrap，不部署

.EXAMPLE
    .\deploy_n100.ps1
    # 完整部署：bootstrap + git pull + docker compose up -d --build

.EXAMPLE
    .\deploy_n100.ps1 -NoBuild
    # 快速重启：只 up，不 build

.EXAMPLE
    .\deploy_n100.ps1 -Host 192.168.1.100 -Port 8080
    # 部署到自定义服务器
#>

param(
    [string]$Host = "192.168.50.102",
    [string]$User = "haishuai",
    [string]$Dir = "/opt/vabhub",
    [int]$Port = 52180,
    [switch]$NoBuild,
    [switch]$TailLogs,
    [switch]$NoPull,
    [switch]$BootstrapOnly
)

# ==================== 配置 ====================
$N100_HOST = $Host
$N100_USER = $User
$N100_DIR = $Dir
$VABHUB_PORT = $Port

# ==================== 颜色输出 ====================
function Write-Step { param($msg) Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-OK { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

# ==================== 主逻辑 ====================
Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║           VabHub N100 部署脚本 (DEPLOY-N100-1)              ║
║                                                              ║
║  目标: $N100_USER@$N100_HOST:$N100_DIR
║  端口: $VABHUB_PORT
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# 构建远程命令
$buildFlag = if ($NoBuild) { "" } else { "--build" }
$pullCmd = if ($NoPull) { "" } else { "git pull origin main &&" }

# Bootstrap 脚本（内嵌，避免依赖远端文件）
$bootstrapScript = @'
set -e
VABHUB_DIR="$1"
VABHUB_PORT="$2"

echo "==> Bootstrap: 检查目录 ${VABHUB_DIR}"
if [ ! -d "${VABHUB_DIR}" ]; then
    echo "[ERROR] 目录不存在: ${VABHUB_DIR}"
    exit 1
fi
cd "${VABHUB_DIR}"

echo "==> Bootstrap: 检查 .env.docker"
if [ ! -f .env.docker ]; then
    if [ -f .env.docker.example ]; then
        cp .env.docker.example .env.docker
        echo "[WARN] 已从 .env.docker.example 创建 .env.docker"
    else
        cat > .env.docker << 'ENVEOF'
DB_PASSWORD=
VABHUB_PORT=52180
TZ=Asia/Shanghai
ENVEOF
        echo "[WARN] 已创建最小 .env.docker"
    fi
fi

echo "==> Bootstrap: 检查 DB_PASSWORD"
if ! grep -q '^DB_PASSWORD=.' .env.docker; then
    NEW_PWD=$(openssl rand -base64 24 | tr -d '/+=' | head -c 24)
    if grep -q '^DB_PASSWORD=' .env.docker; then
        sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=${NEW_PWD}/" .env.docker
    else
        echo "DB_PASSWORD=${NEW_PWD}" >> .env.docker
    fi
    echo "[OK] 已自动生成 DB_PASSWORD"
fi

echo "==> Bootstrap: 验证 compose config"
docker compose --env-file .env.docker config > /dev/null 2>&1 || {
    echo "[ERROR] docker compose config 失败"
    docker compose --env-file .env.docker config 2>&1
    exit 1
}
echo "[OK] Bootstrap 完成"
'@

# 部署脚本
$deployScript = @"
set -e
cd $N100_DIR

$pullCmd

echo '==> 执行 docker compose up $buildFlag'
docker compose --env-file .env.docker up -d $buildFlag

echo ''
echo '==> 容器状态'
docker compose ps

echo ''
echo '==> 健康检查 (等待 5 秒)'
sleep 5
curl -s http://localhost:$VABHUB_PORT/health || echo '[WARN] health 检查失败，服务可能还在启动'

echo ''
echo '==> 最近日志 (50 行)'
docker compose logs -n 50 vabhub 2>/dev/null | tail -30

echo ''
echo '==> 部署完成!'
echo "访问地址: http://${N100_HOST}:${VABHUB_PORT}/"
"@

Write-Step "连接 $N100_USER@$N100_HOST..."

# 1. 执行 Bootstrap
Write-Step "执行 Bootstrap..."
$bootstrapScript | ssh "$N100_USER@$N100_HOST" "bash -s '$N100_DIR' '$VABHUB_PORT'"
if ($LASTEXITCODE -ne 0) {
    Write-Err "Bootstrap 失败，退出码: $LASTEXITCODE"
    exit $LASTEXITCODE
}

# 如果只执行 bootstrap，到此结束
if ($BootstrapOnly) {
    Write-OK "Bootstrap 完成（跳过部署）"
    exit 0
}

# 2. 执行部署
Write-Step "执行部署..."
ssh "$N100_USER@$N100_HOST" $deployScript
if ($LASTEXITCODE -ne 0) {
    Write-Err "部署失败，退出码: $LASTEXITCODE"
    exit $LASTEXITCODE
}

# 3. 可选：显示更多日志
if ($TailLogs) {
    Write-Step "显示最近 200 行日志..."
    ssh "$N100_USER@$N100_HOST" "cd $N100_DIR && docker compose logs -n 200 vabhub"
}

Write-Host ""
Write-OK "部署完成！访问 http://${N100_HOST}:${VABHUB_PORT}/"
