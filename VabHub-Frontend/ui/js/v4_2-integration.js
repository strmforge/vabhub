// v4.2 功能增强集成脚本
// 连接前端组件和后端API

class V4_2Integration {
    constructor() {
        this.apiBase = '/api/v4.2';
        this.init();
    }

    init() {
        console.log('🚀 v4.2 功能增强集成已初始化');
        this.setupEventListeners();
    }

    setupEventListeners() {
        // 智能搜索增强事件
        document.addEventListener('click', (e) => {
            if (e.target.matches('[onclick*="showEnhancedSearch"]')) {
                this.showEnhancedSearch();
            }
            if (e.target.matches('[onclick*="showBatchProcessor"]')) {
                this.showBatchProcessor();
            }
            if (e.target.matches('[onclick*="showPluginManager"]')) {
                this.showPluginManager();
            }
            if (e.target.matches('[onclick*="showBackupManager"]')) {
                this.showBackupManager();
            }
        });
    }

    // 智能搜索增强
    async showEnhancedSearch() {
        try {
            // 创建搜索界面
            this.createModal('智能搜索增强', this.getSearchTemplate());
            
            // 绑定搜索事件
            this.bindSearchEvents();
            
        } catch (error) {
            console.error('智能搜索增强初始化失败:', error);
            this.showError('智能搜索功能暂时不可用');
        }
    }

    // 批量操作优化
    async showBatchProcessor() {
        try {
            // 创建批量处理界面
            this.createModal('批量操作优化', this.getBatchTemplate());
            
            // 绑定批量操作事件
            this.bindBatchEvents();
            
        } catch (error) {
            console.error('批量操作优化初始化失败:', error);
            this.showError('批量操作功能暂时不可用');
        }
    }

    // 插件系统
    async showPluginManager() {
        try {
            // 创建插件管理界面
            this.createModal('插件管理系统', this.getPluginTemplate());
            
            // 加载插件列表
            await this.loadPlugins();
            
        } catch (error) {
            console.error('插件系统初始化失败:', error);
            this.showError('插件管理功能暂时不可用');
        }
    }

    // 数据备份恢复
    async showBackupManager() {
        try {
            // 创建备份管理界面
            this.createModal('数据备份恢复', this.getBackupTemplate());
            
            // 加载备份列表
            await this.loadBackups();
            
        } catch (error) {
            console.error('数据备份恢复初始化失败:', error);
            this.showError('备份管理功能暂时不可用');
        }
    }

    // API调用方法
    async apiCall(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API调用失败 ${endpoint}:`, error);
            throw error;
        }
    }

    // 智能搜索API
    async enhancedSearch(query, filters = {}) {
        return await this.apiCall('/search/enhanced', {
            method: 'POST',
            body: JSON.stringify({ query, filters, limit: 20 })
        });
    }

    // 批量操作API
    async startBatchOperation(operation, files, options = {}) {
        return await this.apiCall('/batch/start', {
            method: 'POST',
            body: JSON.stringify({ operation, files, options })
        });
    }

    async getBatchProgress(taskId) {
        return await this.apiCall(`/batch/progress/${taskId}`);
    }

    // 插件管理API
    async getPlugins() {
        return await this.apiCall('/plugins');
    }

    async installPlugin(pluginUrl, version) {
        return await this.apiCall('/plugins/install', {
            method: 'POST',
            body: JSON.stringify({ plugin_url: pluginUrl, version })
        });
    }

    async togglePlugin(pluginId, enabled) {
        return await this.apiCall(`/plugins/${pluginId}/toggle`, {
            method: 'POST',
            body: JSON.stringify({ enabled })
        });
    }

    // 备份管理API
    async createBackup(name, description, options = {}) {
        return await this.apiCall('/backup/create', {
            method: 'POST',
            body: JSON.stringify({ 
                name, 
                description, 
                include_database: true,
                include_config: true,
                include_media: false,
                ...options 
            })
        });
    }

    async listBackups() {
        return await this.apiCall('/backups');
    }

    async restoreBackup(backupId) {
        return await this.apiCall(`/backup/restore/${backupId}`, {
            method: 'POST'
        });
    }

    async deleteBackup(backupId) {
        return await this.apiCall(`/backup/${backupId}`, {
            method: 'DELETE'
        });
    }

    // 界面模板方法
    getSearchTemplate() {
        return `
            <div class="enhanced-search-container">
                <div class="search-input-group">
                    <input type="text" id="searchQuery" placeholder="输入搜索关键词..." class="search-input">
                    <button onclick="v4_2Integration.performSearch()" class="search-btn">搜索</button>
                </div>
                
                <div class="search-filters">
                    <label><input type="checkbox" name="filter" value="movie"> 电影</label>
                    <label><input type="checkbox" name="filter" value="tv"> 电视剧</label>
                    <label><input type="checkbox" name="filter" value="music"> 音乐</label>
                </div>
                
                <div id="searchResults" class="search-results"></div>
                <div id="searchSuggestions" class="search-suggestions"></div>
            </div>
        `;
    }

    getBatchTemplate() {
        return `
            <div class="batch-processor-container">
                <div class="batch-upload-area" id="batchUploadArea">
                    <p>拖放文件到这里或点击选择文件</p>
                    <input type="file" id="batchFileInput" multiple style="display: none;">
                    <button onclick="document.getElementById('batchFileInput').click()">选择文件</button>
                </div>
                
                <div class="batch-options">
                    <select id="batchOperation">
                        <option value="rename">重命名</option>
                        <option value="move">移动</option>
                        <option value="delete">删除</option>
                    </select>
                    
                    <button onclick="v4_2Integration.startBatch()" class="start-btn">开始批量处理</button>
                </div>
                
                <div id="batchProgress" class="batch-progress"></div>
                <div id="batchFileList" class="batch-file-list"></div>
            </div>
        `;
    }

    getPluginTemplate() {
        return `
            <div class="plugin-manager-container">
                <div class="plugin-install-section">
                    <h4>安装新插件</h4>
                    <input type="text" id="pluginUrl" placeholder="插件URL或GitHub地址">
                    <button onclick="v4_2Integration.installNewPlugin()">安装</button>
                </div>
                
                <div id="pluginList" class="plugin-list">
                    <p>加载中...</p>
                </div>
            </div>
        `;
    }

    getBackupTemplate() {
        return `
            <div class="backup-manager-container">
                <div class="backup-create-section">
                    <h4>创建新备份</h4>
                    <input type="text" id="backupName" placeholder="备份名称">
                    <textarea id="backupDescription" placeholder="备份描述"></textarea>
                    <button onclick="v4_2Integration.createNewBackup()">创建备份</button>
                </div>
                
                <div id="backupList" class="backup-list">
                    <p>加载中...</p>
                </div>
            </div>
        `;
    }

    // 模态框创建
    createModal(title, content) {
        // 移除现有模态框
        const existingModal = document.getElementById('v4_2Modal');
        if (existingModal) {
            existingModal.remove();
        }

        const modal = document.createElement('div');
        modal.id = 'v4_2Modal';
        modal.className = 'v4_2-modal';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close" onclick="v4_2Integration.closeModal()">×</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        
        // 添加样式
        this.addModalStyles();
    }

    closeModal() {
        const modal = document.getElementById('v4_2Modal');
        if (modal) {
            modal.remove();
        }
    }

    addModalStyles() {
        if (!document.getElementById('v4_2ModalStyles')) {
            const styles = document.createElement('style');
            styles.id = 'v4_2ModalStyles';
            styles.textContent = `
                .v4_2-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 1000;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .modal-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                }
                
                .modal-content {
                    background: var(--card-bg);
                    border-radius: 12px;
                    padding: 0;
                    max-width: 800px;
                    width: 90%;
                    max-height: 80vh;
                    overflow-y: auto;
                    z-index: 1001;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                }
                
                .modal-header {
                    padding: 20px;
                    border-bottom: 1px solid var(--border-color);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .modal-body {
                    padding: 20px;
                }
                
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    color: var(--text-secondary);
                }
                
                .modal-close:hover {
                    color: var(--text-primary);
                }
            `;
            document.head.appendChild(styles);
        }
    }

    showError(message) {
        alert(`错误: ${message}`);
    }

    // 具体功能实现方法
    async performSearch() {
        const query = document.getElementById('searchQuery').value;
        if (!query.trim()) return;

        try {
            const results = await this.enhancedSearch(query);
            this.displaySearchResults(results);
        } catch (error) {
            this.showError('搜索失败');
        }
    }

    displaySearchResults(results) {
        const container = document.getElementById('searchResults');
        if (!container) return;

        container.innerHTML = results.results.map(result => `
            <div class="search-result-item">
                <h4>${result.title}</h4>
                <p>类型: ${result.type} | 相关度: ${(result.relevance * 100).toFixed(1)}%</p>
                <p>${result.highlights.join(', ')}</p>
            </div>
        `).join('');
    }

    async loadPlugins() {
        try {
            const plugins = await this.getPlugins();
            this.displayPlugins(plugins);
        } catch (error) {
            this.showError('加载插件失败');
        }
    }

    displayPlugins(plugins) {
        const container = document.getElementById('pluginList');
        if (!container) return;

        container.innerHTML = plugins.map(plugin => `
            <div class="plugin-item">
                <h4>${plugin.name} v${plugin.version}</h4>
                <p>${plugin.description}</p>
                <p>作者: ${plugin.author}</p>
                <button onclick="v4_2Integration.togglePlugin('${plugin.id}', ${!plugin.enabled})">
                    ${plugin.enabled ? '禁用' : '启用'}
                </button>
            </div>
        `).join('');
    }

    async loadBackups() {
        try {
            const backups = await this.listBackups();
            this.displayBackups(backups);
        } catch (error) {
            this.showError('加载备份列表失败');
        }
    }

    displayBackups(backups) {
        const container = document.getElementById('backupList');
        if (!container) return;

        container.innerHTML = backups.map(backup => `
            <div class="backup-item">
                <h4>${backup.name}</h4>
                <p>创建时间: ${new Date(backup.timestamp).toLocaleString()}</p>
                <p>大小: ${(backup.size / 1024 / 1024).toFixed(2)} MB</p>
                <button onclick="v4_2Integration.restoreBackup('${backup.id}')">恢复</button>
                <button onclick="v4_2Integration.deleteBackup('${backup.id}')">删除</button>
            </div>
        `).join('');
    }

    // 其他具体方法实现...
    async installNewPlugin() {
        const url = document.getElementById('pluginUrl').value;
        if (!url.trim()) return;

        try {
            await this.installPlugin(url);
            this.showSuccess('插件安装成功');
            await this.loadPlugins();
        } catch (error) {
            this.showError('插件安装失败');
        }
    }

    async createNewBackup() {
        const name = document.getElementById('backupName').value;
        const description = document.getElementById('backupDescription').value;
        
        if (!name.trim()) return;

        try {
            await this.createBackup(name, description);
            this.showSuccess('备份创建成功');
            await this.loadBackups();
        } catch (error) {
            this.showError('备份创建失败');
        }
    }

    showSuccess(message) {
        alert(`成功: ${message}`);
    }
}

// 全局实例
window.v4_2Integration = new V4_2Integration();

// 全局函数供HTML调用
window.showEnhancedSearch = () => v4_2Integration.showEnhancedSearch();
window.showBatchProcessor = () => v4_2Integration.showBatchProcessor();
window.showPluginManager = () => v4_2Integration.showPluginManager();
window.showBackupManager = () => v4_2Integration.showBackupManager();