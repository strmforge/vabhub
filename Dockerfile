# VabHub v1.5.0 统一Docker镜像
# 将所有组件整合到一个镜像中，用户只需拉取这一个镜像

FROM python:3.11-slim AS builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js (用于前端构建)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 复制所有组件到镜像中
COPY VabHub-Core/ ./core/
COPY VabHub-Frontend/ ./frontend/
COPY VabHub-Plugins/ ./plugins/
COPY VabHub-Resources/ ./resources/
COPY VabHub-Deploy/ ./deploy/

# 构建前端
WORKDIR /app/frontend
RUN npm install && npm run build

# 安装Python依赖
WORKDIR /app/core
RUN pip install --no-cache-dir -r requirements.txt

# 安装插件依赖
WORKDIR /app/plugins
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# 最终运行镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    nginx \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

# 复制构建好的文件
COPY --from=builder /app/core/ ./core/
COPY --from=builder /app/frontend/dist/ ./frontend/dist/
COPY --from=builder /app/plugins/ ./plugins/
COPY --from=builder /app/resources/ ./resources/
COPY --from=builder /app/deploy/ ./deploy/

# 配置nginx
COPY deploy/nginx.conf /etc/nginx/nginx.conf
COPY deploy/common.conf /etc/nginx/common.conf

# 创建非root用户
RUN useradd -m -u 1000 vabhub && \
    chown -R vabhub:vabhub /app && \
    chown -R vabhub:vabhub /var/lib/nginx /var/log/nginx
USER vabhub

# 暴露端口
EXPOSE 4000
EXPOSE 4001

# 设置环境变量
ENV PYTHONPATH=/app/core
ENV PYTHONUNBUFFERED=1

# 启动脚本权限设置
RUN chmod +x /app/start.sh

# 启动命令
CMD ["/app/start.sh"]