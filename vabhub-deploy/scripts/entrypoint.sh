#!/bin/sh

# Lighthouse 容器入口脚本

set -e

# 等待应用启动
if [ -n "$WAIT_FOR_URL" ]; then
    echo "Waiting for $WAIT_FOR_URL to be ready..."
    until curl -f "$WAIT_FOR_URL" >/dev/null 2>&1; do
        echo "Waiting for $WAIT_FOR_URL..."
        sleep 5
    done
    echo "$WAIT_FOR_URL is ready!"
fi

# 设置默认URL
VABHUB_URL="${VABHUB_URL:-http://vabhub-frontend-service:80}"

# 运行 Lighthouse 监控
if [ "$RUN_MODE" = "monitor" ]; then
    echo "Starting Lighthouse monitoring mode..."
    exec /app/lighthouse.sh
else
    echo "Starting single Lighthouse test..."
    node /app/lighthouse-script.js "$VABHUB_URL"
fi