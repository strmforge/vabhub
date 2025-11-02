#!/bin/bash

# Lighthouse 监控脚本
# 用于定期运行性能测试和生成报告

set -e

# 配置变量
VABHUB_URL="${VABHUB_URL:-http://localhost:8090}"
OUTPUT_DIR="${OUTPUT_DIR:-/app/reports}"
INTERVAL="${INTERVAL:-3600}"  # 默认每小时运行一次

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 运行 Lighthouse 测试
run_lighthouse_test() {
    local url="$1"
    local output_file="$OUTPUT_DIR/$(date +%Y%m%d_%H%M%S)_lighthouse.json"
    
    echo "Running Lighthouse test for: $url"
    
    lighthouse "$url" \
        --output json \
        --output-path "$output_file" \
        --chrome-flags="--no-sandbox --headless" \
        --only-categories=performance,accessibility,best-practices,seo \
        --throttling.cpuSlowdownMultiplier=4 \
        --throttling.downloadThroughputKbps=1638.4 \
        --throttling.uploadThroughputKbps=675 \
        --throttling.rttMs=150
    
    echo "Lighthouse report generated: $output_file"
    
    # 提取关键指标
    local score=$(jq -r '.categories.performance.score' "$output_file")
    local fcp=$(jq -r '.audits["first-contentful-paint"].numericValue' "$output_file")
    local lcp=$(jq -r '.audits["largest-contentful-paint"].numericValue' "$output_file")
    
    echo "Performance Score: $score"
    echo "First Contentful Paint: ${fcp}ms"
    echo "Largest Contentful Paint: ${lcp}ms"
    
    # 发送到监控系统（可选）
    if [ -n "$MONITORING_URL" ]; then
        curl -X POST "$MONITORING_URL" \
            -H "Content-Type: application/json" \
            -d "{\"score\":$score,\"fcp\":$fcp,\"lcp\":$lcp,\"timestamp\":\"$(date -Iseconds)\"}"
    fi
}

# 主循环
while true; do
    echo "Starting Lighthouse monitoring cycle at $(date)"
    
    # 测试首页
    run_lighthouse_test "$VABHUB_URL"
    
    # 测试发现页面
    run_lighthouse_test "$VABHUB_URL/discover"
    
    # 测试仪表板
    run_lighthouse_test "$VABHUB_URL/dashboard"
    
    echo "Lighthouse monitoring cycle completed. Sleeping for $INTERVAL seconds..."
    sleep "$INTERVAL"
done