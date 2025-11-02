FROM node:20-alpine

WORKDIR /workspace

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 使用nginx服务静态文件
FROM nginx:alpine

# 复制构建文件到nginx目录
COPY --from=0 /workspace/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 8090

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]