# VabHub 1.3.0 GitHub 推送指南

## 📋 推送概览

VabHub 1.3.0 版本已准备就绪，需要将各仓库推送到对应的 GitHub 仓库。

### 🎯 推送目标
- **VabHub-Core**: https://github.com/vabhub/vabhub-core
- **VabHub-Frontend**: https://github.com/vabhub/vabhub-frontend
- **VabHub-Deploy**: https://github.com/vabhub/vabhub-deploy
- **VabHub-Plugins**: https://github.com/vabhub/vabhub-plugins

## 🚀 推送步骤

### 步骤一：准备各仓库

#### 1. VabHub-Core 仓库
```bash
# 进入 Core 仓库
cd f:\VabHub\VabHub-Core

# 初始化 Git 仓库
git init
git config user.name "VabHub Team"
git config user.email "team@vabhub.org"

# 添加文件
git add .

# 提交更改
git commit -m "release: v1.3.0 - 智能搜索系统升级"

# 连接到 GitHub 远程仓库
git remote add origin https://github.com/vabhub/vabhub-core.git

# 推送代码
git push -u origin main

# 创建版本标签
git tag -a v1.3.0 -m "Release VabHub-Core 1.3.0"
git push origin v1.3.0
```

#### 2. VabHub-Frontend 仓库
```bash
# 进入 Frontend 仓库
cd f:\VabHub\VabHub-Frontend

# 初始化 Git 仓库
git init
git config user.name "VabHub Team"
git config user.email "team@vabhub.org"

# 添加文件
git add .

# 提交更改
git commit -m "release: v1.3.0 - 现代化前端界面"

# 连接到 GitHub 远程仓库
git remote add origin https://github.com/vabhub/vabhub-frontend.git

# 推送代码
git push -u origin main

# 创建版本标签
git tag -a v1.3.0 -m "Release VabHub-Frontend 1.3.0"
git push origin v1.3.0
```

#### 3. VabHub-Deploy 仓库
```bash
# 进入 Deploy 仓库
cd f:\VabHub\VabHub-Deploy

# 初始化 Git 仓库
git init
git config user.name "VabHub Team"
git config user.email "team@vabhub.org"

# 添加文件
git add .

# 提交更改
git commit -m "release: v1.3.0 - 专业部署解决方案"

# 连接到 GitHub 远程仓库
git remote add origin https://github.com/vabhub/vabhub-deploy.git

# 推送代码
git push -u origin main

# 创建版本标签
git tag -a v1.3.0 -m "Release VabHub-Deploy 1.3.0"
git push origin v1.3.0
```

#### 4. VabHub-Plugins 仓库
```bash
# 进入 Plugins 仓库
cd f:\VabHub\VabHub-Plugins

# 初始化 Git 仓库
git init
git config user.name "VabHub Team"
git config user.email "team@vabhub.org"

# 添加文件
git add .

# 提交更改
git commit -m "release: v1.3.0 - 增强插件系统"

# 连接到 GitHub 远程仓库
git remote add origin https://github.com/vabhub/vabhub-plugins.git

# 推送代码
git push -u origin main

# 创建版本标签
git tag -a v1.3.0 -m "Release VabHub-Plugins 1.3.0"
git push origin v1.3.0
```

### 步骤二：使用 GitHub Desktop 推送

如果您更倾向于使用 GitHub Desktop，可以按照以下步骤操作：

#### 1. 打开 GitHub Desktop
```
C:\Users\56214\AppData\Local\GitHubDesktop\GitHubDesktop.exe
```

#### 2. 添加各仓库
1. 点击 "File" → "Add Local Repository"
2. 选择每个仓库的路径：
   - `f:\VabHub\VabHub-Core`
   - `f:\VabHub\VabHub-Frontend`
   - `f:\VabHub\VabHub-Deploy`
   - `f:\VabHub\VabHub-Plugins`

#### 3. 提交更改
1. 在 GitHub Desktop 中选择每个仓库
2. 查看更改的文件
3. 填写提交信息
4. 点击 "Commit to main"

#### 4. 推送到 GitHub
1. 点击 "Push origin" 按钮
2. 等待推送完成
3. 验证推送结果

#### 5. 创建 Release
1. 访问各仓库的 GitHub 页面
2. 点击 "Releases"
3. 点击 "Draft a new release"
4. 选择标签 `v1.3.0`
5. 填写发布标题和说明
6. 上传发布包（如果有）
7. 发布

## 📊 推送验证

### 验证各仓库
推送完成后，请验证以下内容：

#### VabHub-Core
- [ ] 代码已推送到 https://github.com/vabhub/vabhub-core
- [ ] 版本标签 `v1.3.0` 已创建
- [ ] GitHub Actions 已触发
- [ ] Docker 镜像已构建
- [ ] 发布页面已创建

#### VabHub-Frontend
- [ ] 代码已推送到 https://github.com/vabhub/vabhub-frontend
- [ ] 版本标签 `v1.3.0` 已创建
- [ ] GitHub Actions 已触发
- [ ] 前端构建已完成
- [ ] 发布页面已创建

#### VabHub-Deploy
- [ ] 代码已推送到 https://github.com/vabhub/vabhub-deploy
- [ ] 版本标签 `v1.3.0` 已创建
- [ ] 发布包已生成
- [ ] 发布页面已创建

#### VabHub-Plugins
- [ ] 代码已推送到 https://github.com/vabhub/vabhub-plugins
- [ ] 版本标签 `v1.3.0` 已创建
- [ ] 发布页面已创建

## 🔧 故障排除

### 常见问题

#### 问题1：远程仓库不存在
```bash
# 如果远程仓库不存在，需要先创建
# 访问 GitHub 创建对应的仓库
# 然后添加远程仓库
git remote add origin https://github.com/vabhub/vabhub-core.git
```

#### 问题2：推送权限不足
```bash
# 检查 GitHub 账户权限
# 确保有推送权限
# 或者使用 Personal Access Token
git remote set-url origin https://token@github.com/vabhub/vabhub-core.git
```

#### 问题3：标签已存在
```bash
# 删除本地标签
git tag -d v1.3.0

# 删除远程标签
git push --delete origin v1.3.0

# 重新创建标签
git tag -a v1.3.0 -m "Release VabHub-Core 1.3.0"
git push origin v1.3.0
```

### GitHub Desktop 问题

#### 问题1：仓库未识别
- 确保仓库路径正确
- 检查 `.git` 目录是否存在
- 重新添加仓库

#### 问题2：推送失败
- 检查网络连接
- 验证 GitHub 账户权限
- 查看错误信息并解决

## 📈 发布后验证

### 功能验证
推送完成后，请验证以下功能：

#### 后端功能
- [ ] API 服务正常启动
- [ ] 数据库连接正常
- [ ] 搜索功能正常工作
- [ ] 插件系统正常加载

#### 前端功能
- [ ] 界面正常显示
- [ ] 路由导航正常
- [ ] 实时数据更新正常
- [ ] 响应式设计正常

#### 部署功能
- [ ] Docker 容器正常启动
- [ ] 服务健康检查通过
- [ ] 监控系统正常工作
- [ ] 备份恢复功能正常

## 🔗 相关资源

### GitHub 仓库链接
- **VabHub-Core**: https://github.com/vabhub/vabhub-core
- **VabHub-Frontend**: https://github.com/vabhub/vabhub-frontend
- **VabHub-Deploy**: https://github.com/vabhub/vabhub-deploy
- **VabHub-Plugins**: https://github.com/vabhub/vabhub-plugins

### 发布页面
- **VabHub-Core Releases**: https://github.com/vabhub/vabhub-core/releases
- **VabHub-Frontend Releases**: https://github.com/vabhub/vabhub-frontend/releases
- **VabHub-Deploy Releases**: https://github.com/vabhub/vabhub-deploy/releases
- **VabHub-Plugins Releases**: https://github.com/vabhub/vabhub-plugins/releases

### 文档资源
- **项目文档**: https://docs.vabhub.org
- **API文档**: 各仓库的 README.md
- **部署指南**: VabHub-Deploy/README.md

## 🤝 支持信息

### 技术支持
如果在推送过程中遇到问题，请：

1. 查看错误信息
2. 参考故障排除部分
3. 查看 GitHub 文档
4. 在社区论坛寻求帮助

### 联系方式
- **GitHub Issues**: 各仓库的 Issues 页面
- **社区论坛**: https://community.vabhub.org
- **Discord**: https://discord.gg/vabhub

---

**VabHub Team**  
*多仓库协调发布指南*  
2025年10月28日