/**
 * v4.2 插件系统增强模块
 * 实现插件管理器、热加载和插件市场功能
 */

class PluginManager {
    constructor() {
        this.plugins = new Map();
        this.installedPlugins = new Map();
        this.pluginEvents = new Map();
        this.isInitialized = false;
        
        // 插件事件类型
        this.eventTypes = {
            FILE_PROCESSING_STARTED: 'file.processing.started',
            FILE_PROCESSING_COMPLETED: 'file.processing.completed',
            FILE_RENAMED: 'file.renamed',
            ERROR_OCCURRED: 'error.occurred',
            MEDIA_ANALYZED: 'media.analyzed',
            DOWNLOAD_STARTED: 'download.started',
            DOWNLOAD_COMPLETED: 'download.completed'
        };
        
        this.initialize();
    }

    /**
     * 初始化插件管理器
     */
    async initialize() {
        try {
            // 加载已安装的插件
            await this.loadInstalledPlugins();
            
            // 初始化事件系统
            this.initializeEventSystem();
            
            this.isInitialized = true;
            console.log('插件管理器初始化完成');
        } catch (error) {
            console.error('插件管理器初始化失败:', error);
        }
    }

    /**
     * 加载已安装的插件
     */
    async loadInstalledPlugins() {
        try {
            // 从本地存储或API加载插件列表
            const installedPlugins = await this.fetchInstalledPlugins();
            
            for (const pluginData of installedPlugins) {
                await this.loadPlugin(pluginData);
            }
            
            console.log(`加载了 ${installedPlugins.length} 个已安装插件`);
        } catch (error) {
            console.error('加载已安装插件失败:', error);
        }
    }

    /**
     * 获取已安装插件列表
     */
    async fetchInstalledPlugins() {
        try {
            // 模拟API调用
            const response = await fetch('/api/plugins/installed');
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.warn('无法获取已安装插件列表，使用默认插件');
        }
        
        // 返回默认插件列表
        return this.getDefaultPlugins();
    }

    /**
     * 获取默认插件
     */
    getDefaultPlugins() {
        return [
            {
                id: 'file-analyzer',
                name: '文件分析器',
                version: '1.0.0',
                description: '智能分析媒体文件元数据',
                author: 'MediaRenamer Team',
                enabled: true,
                type: 'analyzer'
            },
            {
                id: 'metadata-scraper',
                name: '元数据刮削器',
                version: '1.0.0',
                description: '从在线数据库获取媒体元数据',
                author: 'MediaRenamer Team',
                enabled: true,
                type: 'scraper'
            },
            {
                id: 'file-organizer',
                name: '文件整理器',
                version: '1.0.0',
                description: '自动整理媒体文件到指定目录',
                author: 'MediaRenamer Team',
                enabled: true,
                type: 'organizer'
            }
        ];
    }

    /**
     * 加载插件
     */
    async loadPlugin(pluginData) {
        try {
            const plugin = new Plugin(pluginData);
            
            // 注册插件
            this.plugins.set(pluginData.id, plugin);
            this.installedPlugins.set(pluginData.id, pluginData);
            
            // 初始化插件
            await plugin.initialize();
            
            console.log(`插件加载成功: ${pluginData.name} v${pluginData.version}`);
            
            return plugin;
        } catch (error) {
            console.error(`加载插件失败 (${pluginData.name}):`, error);
            throw error;
        }
    }

    /**
     * 初始化事件系统
     */
    initializeEventSystem() {
        // 为每种事件类型创建监听器数组
        Object.values(this.eventTypes).forEach(eventType => {
            this.pluginEvents.set(eventType, []);
        });
    }

    /**
     * 注册事件监听器
     */
    subscribe(eventType, handler) {
        if (!this.pluginEvents.has(eventType)) {
            console.warn(`未知的事件类型: ${eventType}`);
            return;
        }
        
        this.pluginEvents.get(eventType).push(handler);
    }

    /**
     * 触发事件
     */
    emit(eventType, data) {
        if (!this.pluginEvents.has(eventType)) {
            console.warn(`未知的事件类型: ${eventType}`);
            return;
        }
        
        const handlers = this.pluginEvents.get(eventType);
        handlers.forEach(handler => {
            try {
                handler(data);
            } catch (error) {
                console.error(`事件处理器错误 (${eventType}):`, error);
            }
        });
    }

    /**
     * 安装插件
     */
    async installPlugin(pluginId) {
        try {
            if (this.installedPlugins.has(pluginId)) {
                console.warn(`插件已安装: ${pluginId}`);
                return this.plugins.get(pluginId);
            }
            
            // 从插件市场获取插件信息
            const pluginData = await this.fetchPluginInfo(pluginId);
            
            // 下载插件文件
            await this.downloadPlugin(pluginId);
            
            // 加载插件
            const plugin = await this.loadPlugin(pluginData);
            
            // 保存安装状态
            await this.savePluginInstallation(pluginData);
            
            console.log(`插件安装成功: ${pluginData.name}`);
            return plugin;
        } catch (error) {
            console.error(`安装插件失败 (${pluginId}):`, error);
            throw error;
        }
    }

    /**
     * 卸载插件
     */
    async uninstallPlugin(pluginId) {
        try {
            if (!this.installedPlugins.has(pluginId)) {
                console.warn(`插件未安装: ${pluginId}`);
                return;
            }
            
            const plugin = this.plugins.get(pluginId);
            
            // 禁用插件
            await this.disablePlugin(pluginId);
            
            // 清理插件资源
            if (plugin && typeof plugin.cleanup === 'function') {
                await plugin.cleanup();
            }
            
            // 移除插件
            this.plugins.delete(pluginId);
            this.installedPlugins.delete(pluginId);
            
            // 保存卸载状态
            await this.removePluginInstallation(pluginId);
            
            console.log(`插件卸载成功: ${pluginId}`);
        } catch (error) {
            console.error(`卸载插件失败 (${pluginId}):`, error);
            throw error;
        }
    }

    /**
     * 启用插件
     */
    async enablePlugin(pluginId) {
        try {
            const plugin = this.plugins.get(pluginId);
            if (!plugin) {
                throw new Error(`插件不存在: ${pluginId}`);
            }
            
            plugin.enabled = true;
            
            // 更新插件状态
            await this.updatePluginStatus(pluginId, true);
            
            console.log(`插件已启用: ${pluginId}`);
        } catch (error) {
            console.error(`启用插件失败 (${pluginId}):`, error);
            throw error;
        }
    }

    /**
     * 禁用插件
     */
    async disablePlugin(pluginId) {
        try {
            const plugin = this.plugins.get(pluginId);
            if (!plugin) {
                throw new Error(`插件不存在: ${pluginId}`);
            }
            
            plugin.enabled = false;
            
            // 更新插件状态
            await this.updatePluginStatus(pluginId, false);
            
            console.log(`插件已禁用: ${pluginId}`);
        } catch (error) {
            console.error(`禁用插件失败 (${pluginId}):`, error);
            throw error;
        }
    }

    /**
     * 获取插件信息
     */
    async fetchPluginInfo(pluginId) {
        try {
            const response = await fetch(`/api/plugins/market/${pluginId}`);
            if (response.ok) {
                return await response.json();
            }
            throw new Error(`获取插件信息失败: ${response.status}`);
        } catch (error) {
            console.error('获取插件信息失败:', error);
            throw error;
        }
    }

    /**
     * 下载插件
     */
    async downloadPlugin(pluginId) {
        try {
            const response = await fetch(`/api/plugins/download/${pluginId}`);
            if (!response.ok) {
                throw new Error(`下载插件失败: ${response.status}`);
            }
            
            // 模拟下载过程
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            console.log(`插件下载完成: ${pluginId}`);
        } catch (error) {
            console.error('下载插件失败:', error);
            throw error;
        }
    }

    /**
     * 保存插件安装状态
     */
    async savePluginInstallation(pluginData) {
        try {
            // 保存到本地存储或API
            localStorage.setItem(`plugin_${pluginData.id}`, JSON.stringify(pluginData));
        } catch (error) {
            console.error('保存插件安装状态失败:', error);
        }
    }

    /**
     * 移除插件安装状态
     */
    async removePluginInstallation(pluginId) {
        try {
            localStorage.removeItem(`plugin_${pluginId}`);
        } catch (error) {
            console.error('移除插件安装状态失败:', error);
        }
    }

    /**
     * 更新插件状态
     */
    async updatePluginStatus(pluginId, enabled) {
        try {
            const pluginData = this.installedPlugins.get(pluginId);
            if (pluginData) {
                pluginData.enabled = enabled;
                await this.savePluginInstallation(pluginData);
            }
        } catch (error) {
            console.error('更新插件状态失败:', error);
        }
    }

    /**
     * 获取插件列表
     */
    getPlugins() {
        return Array.from(this.plugins.values());
    }

    /**
     * 获取已安装插件列表
     */
    getInstalledPlugins() {
        return Array.from(this.installedPlugins.values());
    }

    /**
     * 获取可用插件列表
     */
    async getAvailablePlugins() {
        try {
            const response = await fetch('/api/plugins/market');
            if (response.ok) {
                return await response.json();
            }
            throw new Error(`获取可用插件列表失败: ${response.status}`);
        } catch (error) {
            console.error('获取可用插件列表失败:', error);
            return this.getDefaultMarketPlugins();
        }
    }

    /**
     * 获取默认市场插件
     */
    getDefaultMarketPlugins() {
        return [
            {
                id: 'douban-scraper',
                name: '豆瓣数据源',
                version: '1.0.0',
                description: '从豆瓣获取电影、音乐、图书元数据',
                author: '豆瓣官方',
                rating: 4.8,
                downloads: 15000,
                price: 0,
                type: 'scraper'
            },
            {
                id: 'tmdb-scraper',
                name: 'TMDB数据源',
                version: '1.0.0',
                description: '从The Movie Database获取电影和电视剧元数据',
                author: 'TMDB官方',
                rating: 4.9,
                downloads: 25000,
                price: 0,
                type: 'scraper'
            },
            {
                id: 'ai-enhancer',
                name: 'AI增强器',
                version: '1.0.0',
                description: '使用AI技术增强媒体识别和分析能力',
                author: 'AI Labs',
                rating: 4.7,
                downloads: 8000,
                price: 9.99,
                type: 'enhancer'
            }
        ];
    }

    /**
     * 搜索插件
     */
    async searchPlugins(query) {
        try {
            const response = await fetch(`/api/plugins/search?q=${encodeURIComponent(query)}`);
            if (response.ok) {
                return await response.json();
            }
            throw new Error(`搜索插件失败: ${response.status}`);
        } catch (error) {
            console.error('搜索插件失败:', error);
            
            // 本地搜索
            const plugins = await this.getAvailablePlugins();
            return plugins.filter(plugin => 
                plugin.name.toLowerCase().includes(query.toLowerCase()) ||
                plugin.description.toLowerCase().includes(query.toLowerCase())
            );
        }
    }
}

/**
 * 插件基类
 */
class Plugin {
    constructor(pluginData) {
        this.id = pluginData.id;
        this.name = pluginData.name;
        this.version = pluginData.version;
        this.description = pluginData.description;
        this.author = pluginData.author;
        this.enabled = pluginData.enabled !== false;
        this.type = pluginData.type;
        
        this.eventHandlers = new Map();
    }

    /**
     * 初始化插件
     */
    async initialize() {
        // 子类应该重写此方法
        console.log(`初始化插件: ${this.name}`);
    }

    /**
     * 清理插件资源
     */
    async cleanup() {
        // 子类应该重写此方法
        console.log(`清理插件资源: ${this.name}`);
    }

    /**
     * 注册事件处理器
     */
    on(eventType, handler) {
        if (!this.eventHandlers.has(eventType)) {
            this.eventHandlers.set(eventType, []);
        }
        this.eventHandlers.get(eventType).push(handler);
    }

    /**
     * 触发事件
     */
    emit(eventType, data) {
        if (this.eventHandlers.has(eventType)) {
            this.eventHandlers.get(eventType).forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`插件事件处理器错误 (${this.name}):`, error);
                }
            });
        }
    }

    /**
     * 执行插件功能
     */
    async execute(data) {
        if (!this.enabled) {
            throw new Error(`插件未启用: ${this.name}`);
        }
        
        // 子类应该重写此方法
        return data;
    }

    /**
     * 获取插件信息
     */
    getInfo() {
        return {
            id: this.id,
            name: this.name,
            version: this.version,
            description: this.description,
            author: this.author,
            enabled: this.enabled,
            type: this.type
        };
    }
}

/**
 * 插件UI管理器
 */
class PluginManagerUI {
    constructor() {
        this.pluginManager = new PluginManager();
        this.container = null;
        this.currentView = 'installed'; // installed, market, settings
        
        this.init();
    }

    async init() {
        await this.pluginManager.initialize();
        this.createUI();
        this.bindEvents();
        this.showInstalledPlugins();
    }

    createUI() {
        this.container = document.createElement('div');
        this.container.className = 'plugin-manager-container';
        this.container.innerHTML = this.getTemplate();
        
        // 添加到页面
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.appendChild(this.container);
        }
    }

    getTemplate() {
        return `
            <div class="plugin-manager-panel">
                <div class="plugin-header">
                    <h2>插件管理器</h2>
                    <div class="plugin-stats">
                        <span class="stat">
                            <i class="fas fa-plug"></i>
                            <span id="plugin-count">0</span> 个插件
                        </span>
                        <span class="stat">
                            <i class="fas fa-check-circle"></i>
                            <span id="enabled-count">0</span> 个启用
                        </span>
                    </div>
                </div>
                
                <div class="plugin-navigation">
                    <button class="nav-btn active" data-view="installed">
                        <i class="fas fa-box"></i> 已安装
                    </button>
                    <button class="nav-btn" data-view="market">
                        <i class="fas fa-store"></i> 插件市场
                    </button>
                    <button class="nav-btn" data-view="settings">
                        <i class="fas fa-cog"></i> 设置
                    </button>
                </div>
                
                <div class="plugin-search">
                    <div class="search-container">
                        <i class="fas fa-search"></i>
                        <input type="text" placeholder="搜索插件..." id="plugin-search-input">
                    </div>
                </div>
                
                <div class="plugin-content">
                    <div id="installed-view" class="view active">
                        <div class="plugin-list" id="installed-plugin-list"></div>
                    </div>
                    <div id="market-view" class="view">
                        <div class="plugin-list" id="market-plugin-list"></div>
                    </div>
                    <div id="settings-view" class="view">
                        <div class="settings-panel">
                            <h3>插件设置</h3>
                            <div class="setting-item">
                                <label>
                                    <input type="checkbox" id="auto-update-plugins" checked>
                                    自动更新插件
                                </label>
                            </div>
                            <div class="setting-item">
                                <label>
                                    <input type="checkbox" id="enable-hot-reload" checked>
                                    启用热重载
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        // 导航按钮
        this.container.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const view = e.target.getAttribute('data-view');
                this.switchView(view);
            });
        });
        
        // 搜索功能
        const searchInput = this.container.querySelector('#plugin-search-input');
        searchInput.addEventListener('input', this.debounce(() => {
            this.searchPlugins(searchInput.value);
        }, 300));
    }

    switchView(view) {
        // 更新导航按钮
        this.container.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        this.container.querySelector(`[data-view="${view}"]`).classList.add('active');
        
        // 更新内容视图
        this.container.querySelectorAll('.view').forEach(viewEl => {
            viewEl.classList.remove('active');
        });
        this.container.querySelector(`#${view}-view`).classList.add('active');
        
        this.currentView = view;
        
        // 加载对应视图的内容
        switch (view) {
            case 'installed':
                this.showInstalledPlugins();
                break;
            case 'market':
                this.showPluginMarket();
                break;
            case 'settings':
                // 设置视图不需要额外加载
                break;
        }
    }

    async showInstalledPlugins() {
        const plugins = this.pluginManager.getInstalledPlugins();
        const container = this.container.querySelector('#installed-plugin-list');
        
        container.innerHTML = plugins.map(plugin => this.getPluginCardHTML(plugin, true)).join('') || 
            '<div class="empty-state">没有安装任何插件</div>';
        
        this.updateStats();
        this.bindPluginActions();
    }

    async showPluginMarket() {
        try {
            const plugins = await this.pluginManager.getAvailablePlugins();
            const container = this.container.querySelector('#market-plugin-list');
            
            container.innerHTML = plugins.map(plugin => this.getPluginCardHTML(plugin, false)).join('');
            
            this.bindPluginActions();
        } catch (error) {
            console.error('加载插件市场失败:', error);
        }
    }

    getPluginCardHTML(plugin, isInstalled) {
        const installed = this.pluginManager.installedPlugins.has(plugin.id);
        const enabled = installed && this.pluginManager.plugins.get(plugin.id)?.enabled;
        
        return `
            <div class="plugin-card" data-plugin-id="${plugin.id}">
                <div class="plugin-header">
                    <div class="plugin-icon">
                        <i class="fas fa-plug"></i>
                    </div>
                    <div class="plugin-info">
                        <h4 class="plugin-name">${plugin.name}</h4>
                        <span class="plugin-version">v${plugin.version}</span>
                        <span class="plugin-author">by ${plugin.author}</span>
                    </div>
                    <div class="plugin-actions">
                        ${isInstalled ? `
                            <button class="btn btn-sm ${enabled ? 'btn-danger' : 'btn-success'}" data-action="${enabled ? 'disable' : 'enable'}">
                                ${enabled ? '禁用' : '启用'}
                            </button>
                            <button class="btn btn-sm btn-outline" data-action="uninstall">卸载</button>
                        ` : `
                            <button class="btn btn-sm btn-primary" data-action="install">安装</button>
                        `}
                    </div>
                </div>
                <div class="plugin-description">
                    ${plugin.description}
                </div>
                <div class="plugin-meta">
                    ${plugin.rating ? `<span class="plugin-rating">⭐ ${plugin.rating}</span>` : ''}
                    ${plugin.downloads ? `<span class="plugin-downloads">📥 ${plugin.downloads}</span>` : ''}
                    ${plugin.price !== undefined ? `<span class="plugin-price">${plugin.price === 0 ? '免费' : `$${plugin.price}`}</span>` : ''}
                </div>
            </div>
        `;
    }

    bindPluginActions() {
        this.container.querySelectorAll('.plugin-card').forEach(card => {
            const pluginId = card.getAttribute('data-plugin-id');
            
            card.querySelectorAll('[data-action]').forEach(btn => {
                const action = btn.getAttribute('data-action');
                
                btn.addEventListener('click', async () => {
                    try {
                        await this.handlePluginAction(pluginId, action);
                    } catch (error) {
                        console.error(`插件操作失败 (${action}):`, error);
                        this.showNotification(`操作失败: ${error.message}`, 'error');
                    }
                });
            });
        });
    }

    async handlePluginAction(pluginId, action) {
        switch (action) {
            case 'install':
                await this.pluginManager.installPlugin(pluginId);
                this.showNotification('插件安装成功', 'success');
                this.showInstalledPlugins();
                break;
            case 'uninstall':
                if (confirm('确定要卸载这个插件吗？')) {
                    await this.pluginManager.uninstallPlugin(pluginId);
                    this.showNotification('插件卸载成功', 'success');
                    this.showInstalledPlugins();
                }
                break;
            case 'enable':
                await this.pluginManager.enablePlugin(pluginId);
                this.showNotification('插件已启用', 'success');
                this.showInstalledPlugins();
                break;
            case 'disable':
                await this.pluginManager.disablePlugin(pluginId);
                this.showNotification('插件已禁用', 'success');
                this.showInstalledPlugins();
                break;
        }
    }

    updateStats() {
        const plugins = this.pluginManager.getInstalledPlugins();
        const enabledCount = plugins.filter(p => p.enabled).length;
        
        this.container.querySelector('#plugin-count').textContent = plugins.length;
        this.container.querySelector('#enabled-count').textContent = enabledCount;
    }

    async searchPlugins(query) {
        if (!query.trim()) {
            if (this.currentView === 'installed') {
                this.showInstalledPlugins();
            } else {
                this.showPluginMarket();
            }
            return;
        }
        
        try {
            const results = await this.pluginManager.searchPlugins(query);
            const container = this.container.querySelector(`#${this.currentView}-view .plugin-list`);
            
            container.innerHTML = results.map(plugin => this.getPluginCardHTML(plugin, this.currentView === 'installed')).join('') || 
                '<div class="empty-state">没有找到相关插件</div>';
            
            this.bindPluginActions();
        } catch (error) {
            console.error('搜索插件失败:', error);
        }
    }

    showNotification(message, type = 'info') {
        // 简单的通知实现
        const notification = document.createElement('div');
        notification.className = `plugin-notification ${type}`;
        notification.textContent = message;
        
        this.container.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

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
}

// 导出模块
window.PluginManager = PluginManager;
window.Plugin = Plugin;
window.PluginManagerUI = PluginManagerUI;