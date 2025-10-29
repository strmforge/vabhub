/**
 * SmartMedia Hub v4.1 - 主题管理系统
 * 支持亮色/深色主题切换和多语言支持
 */

class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'auto';
        this.currentLanguage = localStorage.getItem('language') || 'zh-CN';
        this.translations = this.loadTranslations();
        
        this.init();
    }

    /**
     * 初始化主题管理器
     */
    init() {
        this.applyTheme(this.currentTheme);
        this.applyLanguage(this.currentLanguage);
        this.addThemeToggleButton();
        this.addLanguageToggleButton();
        
        console.log('主题管理器已初始化');
    }

    /**
     * 应用主题
     */
    applyTheme(theme) {
        const html = document.documentElement;
        
        // 移除现有主题属性
        html.removeAttribute('data-theme');
        
        if (theme === 'light') {
            html.setAttribute('data-theme', 'light');
        } else if (theme === 'dark') {
            html.removeAttribute('data-theme');
        }
        // auto模式不设置属性，让CSS媒体查询处理
        
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;
        
        // 更新主题切换按钮图标
        this.updateThemeButtonIcon();
    }

    /**
     * 添加主题切换按钮
     */
    addThemeToggleButton() {
        const themeToggle = document.createElement('div');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = `
            <button class="theme-btn" title="切换主题">
                <i class="fas fa-sun"></i>
                <span class="theme-label">主题</span>
            </button>
            <div class="theme-menu">
                <button class="theme-option" data-theme="auto">
                    <i class="fas fa-desktop"></i> 跟随系统
                </button>
                <button class="theme-option" data-theme="light">
                    <i class="fas fa-sun"></i> 亮色主题
                </button>
                <button class="theme-option" data-theme="dark">
                    <i class="fas fa-moon"></i> 深色主题
                </button>
            </div>
        `;
        
        const headerRight = document.querySelector('.header-right');
        if (headerRight) {
            headerRight.appendChild(themeToggle);
            this.bindThemeEvents();
        }
    }

    /**
     * 绑定主题事件
     */
    bindThemeEvents() {
        const themeBtn = document.querySelector('.theme-btn');
        const themeOptions = document.querySelectorAll('.theme-option');
        
        if (themeBtn) {
            themeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const menu = document.querySelector('.theme-menu');
                menu.classList.toggle('show');
            });
        }
        
        themeOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const theme = option.getAttribute('data-theme');
                this.applyTheme(theme);
                document.querySelector('.theme-menu').classList.remove('show');
            });
        });
        
        // 点击外部关闭菜单
        document.addEventListener('click', () => {
            document.querySelector('.theme-menu')?.classList.remove('show');
        });
    }

    /**
     * 更新主题按钮图标
     */
    updateThemeButtonIcon() {
        const themeBtn = document.querySelector('.theme-btn i');
        if (themeBtn) {
            if (this.currentTheme === 'light') {
                themeBtn.className = 'fas fa-sun';
            } else if (this.currentTheme === 'dark') {
                themeBtn.className = 'fas fa-moon';
            } else {
                themeBtn.className = 'fas fa-desktop';
            }
        }
    }

    /**
     * 应用语言
     */
    applyLanguage(lang) {
        document.documentElement.lang = lang;
        localStorage.setItem('language', lang);
        this.currentLanguage = lang;
        
        // 更新界面文本
        this.updateInterfaceText();
        
        // 更新语言按钮文本
        this.updateLanguageButtonText();
    }

    /**
     * 添加语言切换按钮
     */
    addLanguageToggleButton() {
        const langToggle = document.createElement('div');
        langToggle.className = 'language-toggle';
        langToggle.innerHTML = `
            <button class="lang-btn" title="切换语言">
                <i class="fas fa-globe"></i>
                <span class="lang-label">中文</span>
            </button>
            <div class="lang-menu">
                <button class="lang-option" data-lang="zh-CN">
                    <i class="fas fa-language"></i> 简体中文
                </button>
                <button class="lang-option" data-lang="en-US">
                    <i class="fas fa-language"></i> English
                </button>
            </div>
        `;
        
        const headerRight = document.querySelector('.header-right');
        if (headerRight) {
            headerRight.appendChild(langToggle);
            this.bindLanguageEvents();
        }
    }

    /**
     * 绑定语言事件
     */
    bindLanguageEvents() {
        const langBtn = document.querySelector('.lang-btn');
        const langOptions = document.querySelectorAll('.lang-option');
        
        if (langBtn) {
            langBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const menu = document.querySelector('.lang-menu');
                menu.classList.toggle('show');
            });
        }
        
        langOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const lang = option.getAttribute('data-lang');
                this.applyLanguage(lang);
                document.querySelector('.lang-menu').classList.remove('show');
            });
        });
        
        // 点击外部关闭菜单
        document.addEventListener('click', () => {
            document.querySelector('.lang-menu')?.classList.remove('show');
        });
    }

    /**
     * 更新语言按钮文本
     */
    updateLanguageButtonText() {
        const langLabel = document.querySelector('.lang-label');
        if (langLabel) {
            langLabel.textContent = this.currentLanguage === 'zh-CN' ? '中文' : 'English';
        }
    }

    /**
     * 加载翻译文本
     */
    loadTranslations() {
        return {
            'zh-CN': {
                searchPlaceholder: '搜索媒体、订阅源、设备...',
                dashboard: '仪表板',
                mediaLibrary: '媒体库',
                subscription: '订阅管理',
                recognition: '智能识别',
                metadata: '元数据刮削',
                recommendation: '智能推荐',
                sync: '设备同步',
                users: '用户管理',
                downloaders: '下载器',
                settings: '系统设置',
                welcomeTitle: '欢迎使用 SmartMedia Hub v4.0',
                welcomeDescription: '融合 MoviePilot、NASTool、MediaMaster 精华功能的现代化媒体管理平台',
                mediaFiles: '媒体文件',
                recognitionAccuracy: '识别准确率',
                onlineDevices: '在线设备',
                recentActivities: '实时活动',
                filter: '筛选'
            },
            'en-US': {
                searchPlaceholder: 'Search media, subscriptions, devices...',
                dashboard: 'Dashboard',
                mediaLibrary: 'Media Library',
                subscription: 'Subscription',
                recognition: 'Recognition',
                metadata: 'Metadata',
                recommendation: 'Recommendation',
                sync: 'Sync',
                users: 'Users',
                downloaders: 'Downloaders',
                settings: 'Settings',
                welcomeTitle: 'Welcome to SmartMedia Hub v4.0',
                welcomeDescription: 'Modern media management platform integrating MoviePilot, NASTool, and MediaMaster',
                mediaFiles: 'Media Files',
                recognitionAccuracy: 'Recognition Accuracy',
                onlineDevices: 'Online Devices',
                recentActivities: 'Recent Activities',
                filter: 'Filter'
            }
        };
    }

    /**
     * 更新界面文本
     */
    updateInterfaceText() {
        const texts = this.translations[this.currentLanguage] || this.translations['zh-CN'];
        
        // 更新搜索框占位符
        const searchInput = document.querySelector('.search-input');
        if (searchInput) searchInput.placeholder = texts.searchPlaceholder;
        
        // 更新导航菜单
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            const viewName = href.substring(1);
            if (texts[viewName]) {
                link.textContent = texts[viewName];
            }
        });
        
        // 更新欢迎横幅
        const welcomeTitle = document.querySelector('.welcome-content h1');
        const welcomeDesc = document.querySelector('.welcome-content p');
        if (welcomeTitle) welcomeTitle.textContent = texts.welcomeTitle;
        if (welcomeDesc) welcomeDesc.textContent = texts.welcomeDescription;
        
        // 更新统计标签
        const statLabels = document.querySelectorAll('.stat-label');
        if (statLabels.length >= 3) {
            statLabels[0].textContent = texts.mediaFiles;
            statLabels[1].textContent = texts.recognitionAccuracy;
            statLabels[2].textContent = texts.onlineDevices;
        }
        
        // 更新活动面板标题
        const activityTitle = document.querySelector('.activity-panel h3');
        if (activityTitle) {
            activityTitle.innerHTML = `<i class="fas fa-history"></i> ${texts.recentActivities}`;
        }
        
        // 更新筛选按钮
        const filterBtn = document.querySelector('.panel-actions .btn');
        if (filterBtn) {
            filterBtn.innerHTML = `<i class="fas fa-filter"></i> ${texts.filter}`;
        }
    }

    /**
     * 获取翻译文本
     */
    getText(key) {
        const texts = this.translations[this.currentLanguage] || this.translations['zh-CN'];
        return texts[key] || key;
    }
}

// 导出主题管理器
window.ThemeManager = ThemeManager;