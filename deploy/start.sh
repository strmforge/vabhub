#!/bin/bash

# VabHub 统一启动脚本
# 支持环境变量和可选功能

echo "🚀 启动 VabHub 统一系统..."

# 设置环境变量
export VABHUB_ENV=production
export API_HOST=0.0.0.0
export API_PORT=${API_PORT:-4001}
export FRONTEND_PORT=${FRONTEND_PORT:-4000}
export ENABLE_NGINX_PROXY=${ENABLE_NGINX_PROXY:-true}
export ENABLE_SSL=${ENABLE_SSL:-false}
export SSL_DOMAIN=${SSL_DOMAIN:-vabhub}
export NGINX_CLIENT_MAX_BODY_SIZE=${NGINX_CLIENT_MAX_BODY_SIZE:-10m}

# 生成HTTPS配置块
if [ "${ENABLE_SSL}" = "true" ]; then
    export HTTPS_SERVER_CONF=$(cat <<EOF
    server {
        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        listen ${SSL_FRONTEND_PORT:-443} ssl;
        listen [::]:${SSL_FRONTEND_PORT:-443} ssl;
        server_name ${SSL_DOMAIN:-vabhub};

        # SSL证书路径
        ssl_certificate /app/config/certs/latest/fullchain.pem;
        ssl_certificate_key /app/config/certs/latest/privkey.pem;

        # SSL安全配置
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # 公共配置
        include common.conf;
    }
EOF
)
else
    export HTTPS_SERVER_CONF="# HTTPS未启用"
fi

# 使用envsubst替换nginx配置模板中的环境变量
echo "📝 生成Nginx配置..."
envsubst '${FRONTEND_PORT}${API_PORT}${NGINX_CLIENT_MAX_BODY_SIZE}${ENABLE_SSL}${HTTPS_SERVER_CONF}' < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp
mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf

# 启动后端API
echo "📡 启动后端API服务..."
cd /app/core
python start.py &
BACKEND_PID=$!

# 等待后端启动
sleep 10

# 根据配置决定是否启动nginx代理
if [ "${ENABLE_NGINX_PROXY}" = "true" ]; then
    echo "🌐 启动Nginx代理服务..."
    sudo nginx
else
    echo "ℹ️  Nginx代理服务已禁用，用户需自行配置反向代理"
fi

# 启动插件系统
echo "🔌 启动插件系统..."
cd /app/plugins
python -c "from plugin_manager import PluginManager; pm = PluginManager(); pm.start_all_plugins()" &
PLUGIN_PID=$!

echo "✅ VabHub 系统启动完成!"
if [ "${ENABLE_NGINX_PROXY}" = "true" ]; then
    echo "📊 前端界面: http://localhost:${FRONTEND_PORT}"
    echo "🔧 后端API: http://localhost:${API_PORT}"
    echo "📚 API文档: http://localhost:${API_PORT}/docs"
else
    echo "🔧 后端API: http://localhost:${API_PORT}"
    echo "📚 API文档: http://localhost:${API_PORT}/docs"
    echo "ℹ️  前端需通过独立服务或反向代理访问"
fi

# 等待进程
wait $BACKEND_PID $PLUGIN_PID