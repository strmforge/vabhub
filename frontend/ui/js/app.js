/* 现代化UI应用控制器 - 参考MoviePilot架构设计 */

class MediaManagerApp {
    constructor() {
        this.currentView = 'dashboard';
        this.isMobileMenuOpen = false;
        this.apiBaseUrl = '/api';
        this.cache = new Map();
        
        this.init();
    }

    /**
     * 初始化应用
     */
    init() {
        this.bindEvents();
        this.loadInitialData();
        this.setupServiceWorker();
        this.setupTheme();
        
        console.log('智能媒体管理平台 UI 已初始化');
    }

    /**
     * 绑定事件监听器
     */
    bindEvents() {
        // 导航菜单点击事件
        this.bindNavigationEvents();
        
        // 搜索功能
        this.bindSearchEvents();
        
        // 移动端菜单
        this.bindMobileEvents();
        
        // 窗口调整事件
        this.bindResizeEvents();
        
        // 键盘快捷键
        this.bindKeyboardEvents();
    }

    /**
     * 导航事件绑定
     */
    bindNavigationEvents() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetView = link.getAttribute('href').substring(1);
                this.navigateTo(targetView);
            });
        });

        // 面包屑导航
        const breadcrumbLinks = document.querySelectorAll('.breadcrumb a');
        breadcrumbLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetView = link.getAttribute('href').substring(1);
                this.navigateTo(targetView);
            });
        });
    }

    /**
     * 搜索事件绑定
     */
    bindSearchEvents() {
        const searchInput = document.querySelector('.search-input');
        const searchBtn = document.querySelector('.search-btn');

        if (searchInput) {
            searchInput.addEventListener('input', this.debounce(() => {
                this.performSearch(searchInput.value);
            }, 300));

            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performSearch(searchInput.value);
                }
            });
        }

        if (searchBtn) {
            searchBtn.addEventListener('click', () => {
                this.performSearch(searchInput.value);
            });
        }
    }

    /**
     * 移动端事件绑定
     */
    bindMobileEvents() {
        // 创建移动端菜单按钮
        this.createMobileMenuButton();
        
        // 点击外部关闭移动菜单
        document.addEventListener('click', (e) => {
            if (this.isMobileMenuOpen && !e.target.closest('.app-sidebar') && !e.target.closest('.mobile-menu-btn')) {
                this.toggleMobileMenu(false);
            }
        });
    }

    /**
     * 创建移动端菜单按钮
     */
    createMobileMenuButton() {
        const headerLeft = document.querySelector('.header-left');
        if (headerLeft && window.innerWidth <= 767) {
            const menuBtn = document.createElement('button');
            menuBtn.className = 'mobile-menu-btn';
            menuBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 20 20">
                    <path d="M2 4h16v2H2V4zm0 5h16v2H2V9zm0 5h16v2H2v-2z" fill="currentColor"/>
                </svg>
            `;
            menuBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleMobileMenu();
            });
            headerLeft.prepend(menuBtn);
        }
    }

    /**
     * 窗口调整事件
     */
    bindResizeEvents() {
        window.addEventListener('resize', this.debounce(() => {
            this.handleResize();
        }, 250));
    }

    /**
     * 键盘快捷键
     */
    bindKeyboardEvents() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K 聚焦搜索
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('.search-input');
                if (searchInput) {
                    searchInput.focus();
                }
            }
            
            // ESC 键关闭移动菜单
            if (e.key === 'Escape' && this.isMobileMenuOpen) {
                this.toggleMobileMenu(false);
            }
            
            // 数字键快速导航
            if (e.key >= '1' && e.key <= '9' && e.altKey) {
                e.preventDefault();
                this.quickNavigate(parseInt(e.key));
            }
        });
    }

    /**
     * 处理窗口调整
     */
    handleResize() {
        const sidebar = document.querySelector('.app-sidebar');
        
        if (window.innerWidth > 767) {
            // 桌面端显示侧边栏
            sidebar.style.display = 'block';
            sidebar.classList.remove('mobile-open');
            this.isMobileMenuOpen = false;
        } else {
            // 移动端隐藏侧边栏
            sidebar.style.display = 'none';
        }
        
        // 重新创建移动菜单按钮
        this.createMobileMenuButton();
    }

    /**
     * 切换移动端菜单
     */
    toggleMobileMenu(force) {
        const sidebar = document.querySelector('.app-sidebar');
        if (!sidebar) return;

        this.isMobileMenuOpen = force !== undefined ? force : !this.isMobileMenuOpen;
        
        if (this.isMobileMenuOpen) {
            sidebar.style.display = 'block';
            setTimeout(() => {
                sidebar.classList.add('mobile-open');
            }, 10);
        } else {
            sidebar.classList.remove('mobile-open');
            setTimeout(() => {
                sidebar.style.display = 'none';
            }, 300);
        }
    }

    /**
     * 导航到指定视图
     */
    async navigateTo(view) {
        if (this.currentView === view) return;

        // 更新活动状态
        this.updateActiveNav(view);
        
        // 更新面包屑
        this.updateBreadcrumb(view);
        
        // 加载视图内容
        await this.loadViewContent(view);
        
        this.currentView = view;
        
        // 移动端自动关闭菜单
        if (window.innerWidth <= 767) {
            this.toggleMobileMenu(false);
        }
        
        // 滚动到顶部
        window.scrollTo(0, 0);
    }

    /**
     * 更新导航活动状态
     */
    updateActiveNav(view) {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.classList.remove('active');
            const link = item.querySelector('.nav-link');
            if (link && link.getAttribute('href') === `#${view}`) {
                item.classList.add('active');
            }
        });
    }

    /**
     * 更新面包屑导航
     */
    updateBreadcrumb(view) {
        const breadcrumb = document.querySelector('.breadcrumb ol');
        if (!breadcrumb) return;

        const breadcrumbMap = {
            'dashboard': ['仪表板', '概览'],
            'media-library': ['媒体库', '文件管理'],
            'ai-analysis': ['AI分析', '智能识别'],
            'smart-home': ['智能家居', '设备管理'],
            'cloud-native': ['云原生', '部署状态'],
            'community': ['社区生态', '插件管理'],
            'settings': ['系统设置', '配置'],
            'logs': ['日志查看', '系统日志']
        };

        const items = breadcrumbMap[view] || ['仪表板', '未知页面'];
        
        breadcrumb.innerHTML = `
            <li><a href="#dashboard">${items[0]}</a></li>
            <li>${items[1]}</li>
        `;
    }

    /**
     * 加载视图内容
     */
    async loadViewContent(view) {
        const mainContent = document.querySelector('.app-main');
        if (!mainContent) return;

        // 显示加载状态
        mainContent.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>加载中...</p>
            </div>
        `;

        try {
            const content = await this.fetchViewContent(view);
            mainContent.innerHTML = content;
            
            // 重新绑定新内容的事件
            this.bindDynamicEvents();
            
        } catch (error) {
            console.error('加载视图失败:', error);
            mainContent.innerHTML = `
                <div class="error-state">
                    <h3>加载失败</h3>
                    <p>无法加载页面内容，请检查网络连接或刷新页面。</p>
                    <button class="btn btn-primary" onclick="app.retryLoad()">重试</button>
                </div>
            `;
        }
    }

    /**
     * 获取视图内容
     */
    async fetchViewContent(view) {
        // 检查缓存
        if (this.cache.has(view)) {
            return this.cache.get(view);
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/ui/views/${view}`);
            if (!response.ok) throw new Error('HTTP error');
            
            const content = await response.text();
            this.cache.set(view, content);
            return content;
            
        } catch (error) {
            // 如果API不可用，返回静态内容
            return this.getStaticViewContent(view);
        }
    }

    /**
     * 获取静态视图内容
     */
    getStaticViewContent(view) {
        const viewTemplates = {
            'dashboard': `
                <nav class="breadcrumb">
                    <ol>
                        <li><a href="#dashboard">仪表板</a></li>
                        <li>概览</li>
                    </ol>
                </nav>
                <div class="dashboard-content">
                    ${this.getStatsGrid()}
                    ${this.getChartsGrid()}
                </div>
            `,
            'media-library': `
                <nav class="breadcrumb">
                    <ol>
                        <li><a href="#dashboard">仪表板</a></li>
                        <li>媒体库</li>
                    </ol>
                </nav>
                <div class="media-library-content">
                    <h2>媒体库管理</h2>
                    <p>媒体文件管理和浏览功能</p>
                </div>
            `
            // 其他视图模板...
        };

        return viewTemplates[view] || '<p>页面不存在</p>';
    }

    /**
     * 绑定动态内容事件
     */
    bindDynamicEvents() {
        // 绑定新创建的元素事件
        const buttons = document.querySelectorAll('.btn, .action-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', this.handleButtonClick.bind(this));
        });
    }

    /**
     * 处理按钮点击
     */
    handleButtonClick(e) {
        const button = e.target.closest('button');
        if (!button) return;

        // 添加点击反馈
        button.style.transform = 'scale(0.98)';
        setTimeout(() => {
            button.style.transform = '';
        }, 150);
    }

    /**
     * 执行搜索
     */
    async performSearch(query) {
        if (!query.trim()) return;

        console.log('搜索:', query);
        // 这里可以集成实际的搜索API
    }

    /**
     * 快速导航
     */
    quickNavigate(index) {
        const navItems = document.querySelectorAll('.nav-item');
        if (index <= navItems.length) {
            const link = navItems[index - 1].querySelector('.nav-link');
            if (link) {
                const view = link.getAttribute('href').substring(1);
                this.navigateTo(view);
            }
        }
    }

    /**
     * 加载初始数据
     */
    async loadInitialData() {
        try {
            await this.loadStatsData();
            await this.loadSystemStatus();
        } catch (error) {
            console.warn('初始数据加载失败:', error);
        }
    }

    /**
     * 加载统计数据
     */
    async loadStatsData() {
        // 模拟API调用
        const stats = await this.mockApiCall('/api/stats', {
            mediaCount: 1247,
            aiAccuracy: 98.5,
            onlineDevices: 8,
            storageUsed: 256
        });
        
        this.updateStatsDisplay(stats);
    }

    /**
     * 更新统计显示
     */
    updateStatsDisplay(stats) {
        const statCards = document.querySelectorAll('.stat-card');
        if (statCards.length === 0) return;

        // 实际项目中这里会更新具体的统计数值
    }

    /**
     * 加载系统状态
     */
    async loadSystemStatus() {
        // 系统状态检查
    }

    /**
     * 设置主题
     */
    setupTheme() {
        // 检测系统主题偏好
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
        }

        // 监听主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
        });
    }

    /**
     * 设置Service Worker
     */
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').catch(console.error);
        }
    }

    /**
     * 防抖函数
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * 模拟API调用
     */
    async mockApiCall(endpoint, data) {
        return new Promise((resolve) => {
            setTimeout(() => resolve(data), 500);
        });
    }

    /**
     * 获取统计网格HTML
     */
    getStatsGrid() {
        return `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24">
                            <path d="M4 4h16v16H4V4zm2 2v12h12V6H6z" fill="currentColor"/>
                        </svg>
                    </div>
                    <div class="stat-content">
                        <div class="stat-value">1,247</div>
                        <div class="stat-label">媒体文件</div>
                    </div>
                    <div class="stat-trend positive">+12%</div>
                </div>
                <!-- 其他统计卡片 -->
            </div>
        `;
    }

    /**
     * 获取图表网格HTML
     */
    getChartsGrid() {
        return `
            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>媒体类型分布</h3>
                        <div class="chart-actions">
                            <button class="btn-icon">
                                <svg width="16" height="16" viewBox="0 0 16 16">
                                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" fill="currentColor"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div class="chart-content">
                        <div class="placeholder-chart">图表区域</div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * 重试加载
     */
    retryLoad() {
        this.loadViewContent(this.currentView);
    }
}

// 全局应用实例
window.app = new MediaManagerApp();

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MediaManagerApp;
}