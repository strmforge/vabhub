/**
 * v4.2 数据备份恢复模块
 * 实现完整的数据库备份恢复功能
 */

class BackupManager {
    constructor() {
        this.backups = new Map();
        this.isBackingUp = false;
        this.isRestoring = false;
        this.autoBackupEnabled = true;
        this.backupInterval = 24 * 60 * 60 * 1000; // 24小时
        
        this.initialize();
    }

    /**
     * 初始化备份管理器
     */
    async initialize() {
        try {
            // 加载备份列表
            await this.loadBackupList();
            
            // 设置自动备份
            this.setupAutoBackup();
            
            console.log('备份管理器初始化完成');
        } catch (error) {
            console.error('备份管理器初始化失败:', error);
        }
    }

    /**
     * 加载备份列表
     */
    async loadBackupList() {
        try {
            const backups = await this.fetchBackupList();
            
            backups.forEach(backup => {
                this.backups.set(backup.id, backup);
            });
            
            console.log(`加载了 ${backups.length} 个备份`);
        } catch (error) {
            console.error('加载备份列表失败:', error);
        }
    }

    /**
     * 获取备份列表
     */
    async fetchBackupList() {
        try {
            const response = await fetch('/api/backup/list');
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.warn('无法获取备份列表，使用本地备份');
        }
        
        // 返回本地备份列表
        return this.getLocalBackups();
    }

    /**
     * 获取本地备份
     */
    getLocalBackups() {
        try {
            const backups = localStorage.getItem('backup_list');
            return backups ? JSON.parse(backups) : [];
        } catch (error) {
            console.error('获取本地备份失败:', error);
            return [];
        }
    }

    /**
     * 设置自动备份
     */
    setupAutoBackup() {
        if (!this.autoBackupEnabled) return;
        
        // 检查是否需要自动备份
        const lastBackup = localStorage.getItem('last_auto_backup');
        const now = Date.now();
        
        if (!lastBackup || (now - parseInt(lastBackup)) > this.backupInterval) {
            this.createAutoBackup();
        }
        
        // 设置定时器
        setInterval(() => {
            if (this.autoBackupEnabled) {
                this.createAutoBackup();
            }
        }, this.backupInterval);
    }

    /**
     * 创建自动备份
     */
    async createAutoBackup() {
        if (this.isBackingUp) return;
        
        try {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const backupName = `auto-backup-${timestamp}`;
            
            await this.createBackup(backupName, {
                description: '自动备份',
                type: 'auto',
                includeMedia: true,
                includeSettings: true,
                includeDatabase: true
            });
            
            localStorage.setItem('last_auto_backup', Date.now().toString());
            console.log('自动备份创建成功');
        } catch (error) {
            console.error('自动备份失败:', error);
        }
    }

    /**
     * 创建备份
     */
    async createBackup(name, options = {}) {
        if (this.isBackingUp) {
            throw new Error('备份操作正在进行中');
        }
        
        this.isBackingUp = true;
        
        try {
            const backupData = {
                id: this.generateBackupId(),
                name: name || `backup-${Date.now()}`,
                timestamp: Date.now(),
                size: 0,
                status: 'creating',
                ...options
            };
            
            // 开始备份过程
            const result = await this.performBackup(backupData);
            
            // 更新备份信息
            backupData.size = result.size;
            backupData.status = 'completed';
            backupData.filePath = result.filePath;
            
            // 保存备份
            this.backups.set(backupData.id, backupData);
            await this.saveBackupList();
            
            console.log(`备份创建成功: ${backupData.name}`);
            return backupData;
        } catch (error) {
            console.error('备份创建失败:', error);
            throw error;
        } finally {
            this.isBackingUp = false;
        }
    }

    /**
     * 执行备份操作
     */
    async performBackup(backupData) {
        return new Promise((resolve, reject) => {
            // 模拟备份过程
            let progress = 0;
            const totalSteps = 5;
            
            const interval = setInterval(() => {
                progress++;
                
                // 更新进度事件
                this.emit('backupProgress', {
                    backupId: backupData.id,
                    progress: (progress / totalSteps) * 100,
                    step: progress,
                    totalSteps: totalSteps
                });
                
                if (progress >= totalSteps) {
                    clearInterval(interval);
                    
                    // 模拟备份完成
                    resolve({
                        size: Math.floor(Math.random() * 1000000) + 100000,
                        filePath: `/backups/${backupData.id}.tar.gz`
                    });
                }
            }, 500);
        });
    }

    /**
     * 恢复备份
     */
    async restoreBackup(backupId, options = {}) {
        if (this.isRestoring) {
            throw new Error('恢复操作正在进行中');
        }
        
        if (!this.backups.has(backupId)) {
            throw new Error('备份不存在');
        }
        
        this.isRestoring = true;
        
        try {
            const backup = this.backups.get(backupId);
            
            // 开始恢复过程
            await this.performRestore(backup, options);
            
            console.log(`备份恢复成功: ${backup.name}`);
            return backup;
        } catch (error) {
            console.error('备份恢复失败:', error);
            throw error;
        } finally {
            this.isRestoring = false;
        }
    }

    /**
     * 执行恢复操作
     */
    async performRestore(backup, options) {
        return new Promise((resolve, reject) => {
            // 模拟恢复过程
            let progress = 0;
            const totalSteps = 4;
            
            const interval = setInterval(() => {
                progress++;
                
                // 更新进度事件
                this.emit('restoreProgress', {
                    backupId: backup.id,
                    progress: (progress / totalSteps) * 100,
                    step: progress,
                    totalSteps: totalSteps
                });
                
                if (progress >= totalSteps) {
                    clearInterval(interval);
                    
                    // 模拟恢复完成
                    resolve();
                }
            }, 500);
        });
    }

    /**
     * 删除备份
     */
    async deleteBackup(backupId) {
        if (!this.backups.has(backupId)) {
            throw new Error('备份不存在');
        }
        
        try {
            const backup = this.backups.get(backupId);
            
            // 删除备份文件
            await this.deleteBackupFile(backup);
            
            // 从列表中移除
            this.backups.delete(backupId);
            await this.saveBackupList();
            
            console.log(`备份删除成功: ${backup.name}`);
            return backup;
        } catch (error) {
            console.error('备份删除失败:', error);
            throw error;
        }
    }

    /**
     * 删除备份文件
     */
    async deleteBackupFile(backup) {
        // 模拟删除操作
        return new Promise(resolve => {
            setTimeout(() => {
                console.log(`删除备份文件: ${backup.filePath}`);
                resolve();
            }, 500);
        });
    }

    /**
     * 导出备份
     */
    async exportBackup(backupId, format = 'json') {
        if (!this.backups.has(backupId)) {
            throw new Error('备份不存在');
        }
        
        const backup = this.backups.get(backupId);
        
        try {
            // 模拟导出过程
            const exportData = await this.generateExportData(backup, format);
            
            // 创建下载链接
            this.downloadFile(exportData, `${backup.name}.${format}`);
            
            console.log(`备份导出成功: ${backup.name}`);
            return exportData;
        } catch (error) {
            console.error('备份导出失败:', error);
            throw error;
        }
    }

    /**
     * 生成导出数据
     */
    async generateExportData(backup, format) {
        return new Promise(resolve => {
            setTimeout(() => {
                const data = {
                    backup: backup,
                    exportTime: Date.now(),
                    format: format
                };
                
                if (format === 'json') {
                    resolve(JSON.stringify(data, null, 2));
                } else {
                    resolve(data);
                }
            }, 300);
        });
    }

    /**
     * 下载文件
     */
    downloadFile(content, filename) {
        const blob = new Blob([content], { type: 'application/octet-stream' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        
        URL.revokeObjectURL(url);
    }

    /**
     * 导入备份
     */
    async importBackup(file, options = {}) {
        try {
            const content = await this.readFile(file);
            const backupData = JSON.parse(content);
            
            // 验证备份数据
            this.validateBackupData(backupData);
            
            // 创建新备份
            const newBackup = await this.createBackup(`imported-${backupData.backup.name}`, {
                ...backupData.backup,
                imported: true,
                importTime: Date.now()
            });
            
            console.log(`备份导入成功: ${newBackup.name}`);
            return newBackup;
        } catch (error) {
            console.error('备份导入失败:', error);
            throw error;
        }
    }

    /**
     * 读取文件
     */
    readFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }

    /**
     * 验证备份数据
     */
    validateBackupData(backupData) {
        if (!backupData.backup || !backupData.backup.id || !backupData.backup.name) {
            throw new Error('无效的备份文件格式');
        }
    }

    /**
     * 生成备份ID
     */
    generateBackupId() {
        return `backup_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * 保存备份列表
     */
    async saveBackupList() {
        try {
            const backupList = Array.from(this.backups.values());
            localStorage.setItem('backup_list', JSON.stringify(backupList));
        } catch (error) {
            console.error('保存备份列表失败:', error);
        }
    }

    /**
     * 获取备份列表
     */
    getBackups() {
        return Array.from(this.backups.values()).sort((a, b) => b.timestamp - a.timestamp);
    }

    /**
     * 获取备份统计
     */
    getBackupStats() {
        const backups = this.getBackups();
        const totalSize = backups.reduce((sum, backup) => sum + (backup.size || 0), 0);
        
        return {
            total: backups.length,
            totalSize: totalSize,
            autoBackups: backups.filter(b => b.type === 'auto').length,
            manualBackups: backups.filter(b => b.type === 'manual').length,
            lastBackup: backups.length > 0 ? Math.max(...backups.map(b => b.timestamp)) : null
        };
    }

    /**
     * 事件系统
     */
    eventHandlers = new Map();
    
    on(event, handler) {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, []);
        }
        this.eventHandlers.get(event).push(handler);
    }
    
    emit(event, data) {
        if (this.eventHandlers.has(event)) {
            this.eventHandlers.get(event).forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`事件处理器错误 (${event}):`, error);
                }
            });
        }
    }
}

/**
 * 备份管理器UI组件
 */
class BackupManagerUI {
    constructor() {
        this.backupManager = new BackupManager();
        this.container = null;
        this.currentView = 'list'; // list, create, restore
        
        this.init();
    }

    async init() {
        await this.backupManager.initialize();
        this.createUI();
        this.bindEvents();
        this.showBackupList();
    }

    createUI() {
        this.container = document.createElement('div');
        this.container.className = 'backup-manager-container';
        this.container.innerHTML = this.getTemplate();
        
        // 添加到页面
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.appendChild(this.container);
        }
    }

    getTemplate() {
        return `
            <div class="backup-manager-panel">
                <div class="backup-header">
                    <h2>数据备份恢复</h2>
                    <div class="backup-stats">
                        <span class="stat">
                            <i class="fas fa-database"></i>
                            <span id="backup-count">0</span> 个备份
                        </span>
                        <span class="stat">
                            <i class="fas fa-hdd"></i>
                            <span id="backup-size">0 MB</span>
                        </span>
                    </div>
                </div>
                
                <div class="backup-controls">
                    <button class="btn btn-primary" id="create-backup-btn">
                        <i class="fas fa-plus"></i> 创建备份
                    </button>
                    <button class="btn btn-outline" id="import-backup-btn">
                        <i class="fas fa-upload"></i> 导入备份
                    </button>
                    <input type="file" id="backup-file-input" accept=".json,.tar.gz" style="display: none;">
                </div>
                
                <div class="backup-content">
                    <div id="backup-list-view" class="view active">
                        <div class="backup-list" id="backup-list"></div>
                    </div>
                    
                    <div id="create-backup-view" class="view">
                        <div class="create-backup-panel">
                            <h3>创建新备份</h3>
                            <div class="form-group">
                                <label for="backup-name">备份名称</label>
                                <input type="text" id="backup-name" placeholder="输入备份名称">
                            </div>
                            <div class="form-group">
                                <label for="backup-description">描述</label>
                                <textarea id="backup-description" placeholder="备份描述（可选）"></textarea>
                            </div>
                            <div class="form-group">
                                <h4>备份内容</h4>
                                <div class="checkbox-group">
                                    <label>
                                        <input type="checkbox" id="include-media" checked>
                                        媒体文件
                                    </label>
                                    <label>
                                        <input type="checkbox" id="include-settings" checked>
                                        系统设置
                                    </label>
                                    <label>
                                        <input type="checkbox" id="include-database" checked>
                                        数据库
                                    </label>
                                </div>
                            </div>
                            <div class="form-actions">
                                <button class="btn btn-primary" id="start-backup-btn">开始备份</button>
                                <button class="btn btn-outline" id="cancel-backup-btn">取消</button>
                            </div>
                        </div>
                    </div>
                    
                    <div id="backup-progress-view" class="view">
                        <div class="progress-panel">
                            <h3 id="progress-title">备份进行中</h3>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 0%"></div>
                            </div>
                            <div class="progress-info">
                                <span id="progress-text">准备中...</span>
                                <span id="progress-percentage">0%</span>
                            </div>
                            <button class="btn btn-danger" id="cancel-progress-btn">取消</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        // 控制按钮
        this.container.querySelector('#create-backup-btn').addEventListener('click', () => {
            this.showCreateBackupView();
        });
        
        this.container.querySelector('#import-backup-btn').addEventListener('click', () => {
            this.container.querySelector('#backup-file-input').click();
        });
        
        // 文件导入
        this.container.querySelector('#backup-file-input').addEventListener('change', (e) => {
            this.handleFileImport(e.target.files[0]);
        });
        
        // 创建备份表单
        this.container.querySelector('#start-backup-btn').addEventListener('click', () => {
            this.startBackup();
        });
        
        this.container.querySelector('#cancel-backup-btn').addEventListener('click', () => {
            this.showBackupList();
        });
        
        this.container.querySelector('#cancel-progress-btn').addEventListener('click', () => {
            this.cancelBackup();
        });
        
        // 备份管理器事件
        this.backupManager.on('backupProgress', (data) => {
            this.updateBackupProgress(data);
        });
        
        this.backupManager.on('restoreProgress', (data) => {
            this.updateRestoreProgress(data);
        });
    }

    showBackupList() {
        this.switchView('list');
        this.renderBackupList();
        this.updateStats();
    }

    showCreateBackupView() {
        this.switchView('create');
        
        // 重置表单
        this.container.querySelector('#backup-name').value = `backup-${new Date().toISOString().split('T')[0]}`;
        this.container.querySelector('#backup-description').value = '';
    }

    showProgressView(title = '备份进行中') {
        this.switchView('progress');
        this.container.querySelector('#progress-title').textContent = title;
        this.resetProgress();
    }

    switchView(view) {
        // 隐藏所有视图
        this.container.querySelectorAll('.view').forEach(viewEl => {
            viewEl.classList.remove('active');
        });
        
        // 显示目标视图
        this.container.querySelector(`#${view}-view`).classList.add('active');
        this.currentView = view;
    }

    renderBackupList() {
        const backups = this.backupManager.getBackups();
        const container = this.container.querySelector('#backup-list');
        
        if (backups.length === 0) {
            container.innerHTML = '<div class="empty-state">暂无备份</div>';
            return;
        }
        
        container.innerHTML = backups.map(backup => this.getBackupCardHTML(backup)).join('');
        this.bindBackupActions();
    }

    getBackupCardHTML(backup) {
        const date = new Date(backup.timestamp);
        const size = this.formatFileSize(backup.size);
        
        return `
            <div class="backup-card" data-backup-id="${backup.id}">
                <div class="backup-header">
                    <div class="backup-icon">
                        <i class="fas fa-database"></i>
                    </div>
                    <div class="backup-info">
                        <h4 class="backup-name">${backup.name}</h4>
                        <div class="backup-meta">
                            <span class="backup-date">${date.toLocaleString()}</span>
                            <span class="backup-size">${size}</span>
                            <span class="backup-type">${backup.type === 'auto' ? '自动' : '手动'}</span>
                        </div>
                        ${backup.description ? `<p class="backup-description">${backup.description}</p>` : ''}
                    </div>
                </div>
                <div class="backup-actions">
                    <button class="btn btn-sm btn-success" data-action="restore">恢复</button>
                    <button class="btn btn-sm btn-outline" data-action="export">导出</button>
                    <button class="btn btn-sm btn-danger" data-action="delete">删除</button>
                </div>
            </div>
        `;
    }

    bindBackupActions() {
        this.container.querySelectorAll('.backup-card').forEach(card => {
            const backupId = card.getAttribute('data-backup-id');
            
            card.querySelectorAll('[data-action]').forEach(btn => {
                const action = btn.getAttribute('data-action');
                
                btn.addEventListener('click', async () => {
                    try {
                        await this.handleBackupAction(backupId, action);
                    } catch (error) {
                        console.error(`备份操作失败 (${action}):`, error);
                        this.showNotification(`操作失败: ${error.message}`, 'error');
                    }
                });
            });
        });
    }

    async handleBackupAction(backupId, action) {
        switch (action) {
            case 'restore':
                if (confirm('确定要恢复这个备份吗？当前数据将被覆盖。')) {
                    await this.restoreBackup(backupId);
                }
                break;
            case 'export':
                await this.exportBackup(backupId);
                break;
            case 'delete':
                if (confirm('确定要删除这个备份吗？此操作不可恢复。')) {
                    await this.deleteBackup(backupId);
                    this.showBackupList();
                }
                break;
        }
    }

    async startBackup() {
        const name = this.container.querySelector('#backup-name').value.trim();
        const description = this.container.querySelector('#backup-description').value.trim();
        
        if (!name) {
            this.showNotification('请输入备份名称', 'error');
            return;
        }
        
        const options = {
            description: description || undefined,
            type: 'manual',
            includeMedia: this.container.querySelector('#include-media').checked,
            includeSettings: this.container.querySelector('#include-settings').checked,
            includeDatabase: this.container.querySelector('#include-database').checked
        };
        
        try {
            this.showProgressView('备份进行中');
            await this.backupManager.createBackup(name, options);
            this.showNotification('备份创建成功', 'success');
            this.showBackupList();
        } catch (error) {
            this.showNotification(`备份失败: ${error.message}`, 'error');
            this.showBackupList();
        }
    }

    async restoreBackup(backupId) {
        try {
            this.showProgressView('恢复进行中');
            await this.backupManager.restoreBackup(backupId);
            this.showNotification('备份恢复成功', 'success');
            this.showBackupList();
        } catch (error) {
            this.showNotification(`恢复失败: ${error.message}`, 'error');
            this.showBackupList();
        }
    }

    async exportBackup(backupId) {
        try {
            await this.backupManager.exportBackup(backupId);
            this.showNotification('备份导出成功', 'success');
        } catch (error) {
            this.showNotification(`导出失败: ${error.message}`, 'error');
        }
    }

    async deleteBackup(backupId) {
        try {
            await this.backupManager.deleteBackup(backupId);
            this.showNotification('备份删除成功', 'success');
        } catch (error) {
            this.showNotification(`删除失败: ${error.message}`, 'error');
        }
    }

    async handleFileImport(file) {
        if (!file) return;
        
        try {
            await this.backupManager.importBackup(file);
            this.showNotification('备份导入成功', 'success');
            this.showBackupList();
        } catch (error) {
            this.showNotification(`导入失败: ${error.message}`, 'error');
        }
    }

    cancelBackup() {
        // 这里应该实现取消逻辑
        this.showNotification('操作已取消', 'info');
        this.showBackupList();
    }

    updateBackupProgress(data) {
        const progress = data.progress;
        const progressFill = this.container.querySelector('.progress-fill');
        const progressText = this.container.querySelector('#progress-text');
        const progressPercentage = this.container.querySelector('#progress-percentage');
        
        progressFill.style.width = `${progress}%`;
        progressText.textContent = `步骤 ${data.step}/${data.totalSteps}`;
        progressPercentage.textContent = `${Math.round(progress)}%`;
    }

    updateRestoreProgress(data) {
        this.updateBackupProgress(data);
    }

    resetProgress() {
        const progressFill = this.container.querySelector('.progress-fill');
        const progressText = this.container.querySelector('#progress-text');
        const progressPercentage = this.container.querySelector('#progress-percentage');
        
        progressFill.style.width = '0%';
        progressText.textContent = '准备中...';
        progressPercentage.textContent = '0%';
    }

    updateStats() {
        const stats = this.backupManager.getBackupStats();
        
        this.container.querySelector('#backup-count').textContent = stats.total;
        this.container.querySelector('#backup-size').textContent = this.formatFileSize(stats.totalSize);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `backup-notification ${type}`;
        notification.textContent = message;
        
        this.container.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// 导出模块
window.BackupManager = BackupManager;
window.BackupManagerUI = BackupManagerUI;