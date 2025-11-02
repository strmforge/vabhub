# VabHub 贡献指南

欢迎参与 VabHub 项目的开发！本指南将帮助您了解如何为项目做出贡献。

## 🚀 快速开始

### 开发环境设置

1. **克隆仓库**
```bash
git clone https://github.com/strmforge/vabhub.git
cd vabhub
```

2. **安装依赖**
```bash
# 前端依赖
cd frontend
npm install

# 后端依赖
cd ../core
pip install -r requirements.txt
```

3. **启动开发服务器**
```bash
# 后端服务
cd core
python start.py

# 前端服务 (新终端)
cd frontend
npm run dev
```

## 📝 代码规范

### 提交信息规范
使用约定式提交格式：
```bash
feat: 添加新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 添加测试
chore: 构建过程或辅助工具变动
```

### 代码风格
- **Python**: 遵循 PEP 8，使用 Black 格式化
- **TypeScript**: 使用 ESLint + Prettier
- **Vue**: 遵循 Vue 风格指南

## 🔧 开发流程

### 1. 创建分支
```bash
git checkout -b feature/your-feature-name
```

### 2. 开发代码
- 遵循项目代码规范
- 添加必要的测试
- 更新相关文档

### 3. 提交代码
```bash
git add .
git commit -m "feat: 添加新功能描述"
```

### 4. 创建 Pull Request
- 在 GitHub 上创建 Pull Request
- 填写详细的描述信息
- 关联相关 issue

## 🧪 测试要求

### 单元测试
- 核心功能必须包含单元测试
- 测试覆盖率不低于 80%

### 集成测试
- 重要流程需要集成测试
- 确保各组件协同工作正常

### 性能测试
- 关键接口需要性能测试
- 响应时间控制在合理范围内

## 📋 Issue 管理

### Issue 类型
- **bug**: 功能缺陷或错误
- **feature**: 新功能请求
- **enhancement**: 现有功能改进
- **documentation**: 文档相关
- **question**: 问题咨询

### 优先级
- **P0**: 紧急 - 影响核心功能
- **P1**: 高 - 重要功能缺陷
- **P2**: 中 - 一般功能改进
- **P3**: 低 - 优化或小改进

## 🔐 安全指南

### 敏感信息处理
- 不要将 API 密钥硬编码在代码中
- 使用环境变量管理敏感信息
- 遵循最小权限原则

### 代码审查
- 所有代码变更都需要审查
- 至少需要一名核心成员批准
- 关注安全漏洞和性能问题

## 📊 性能优化

### 前端优化
- 代码分割和懒加载
- 图片和资源优化
- 缓存策略优化

### 后端优化
- 数据库查询优化
- 缓存策略实施
- 异步处理优化

## 🤝 社区交流

### 沟通渠道
- **GitHub Issues**: 问题反馈和功能请求
- **GitHub Discussions**: 技术讨论和社区交流
- **邮件列表**: team@vabhub.org

### 行为准则
- 尊重所有社区成员
- 保持专业和建设性的讨论
- 遵守开源社区行为准则

## 🎯 发布流程

### 版本管理
- 使用语义化版本控制 (SemVer)
- 主版本: 不兼容的 API 修改
- 次版本: 向后兼容的功能性新增
- 修订版本: 向后兼容的问题修正

### 发布检查清单
- [ ] 所有测试通过
- [ ] 文档更新完成
- [ ] 版本号更新
- [ ] 变更日志更新
- [ ] 发布说明编写

## 📚 学习资源

### 技术文档
- [Vue 3 文档](https://v3.vuejs.org/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [TypeScript 文档](https://www.typescriptlang.org/)

### 开发工具
- [VS Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/)
- [Postman](https://www.postman.com/)

---

感谢您对 VabHub 项目的贡献！让我们一起打造更好的媒体管理系统。