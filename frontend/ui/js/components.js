/* 现代化UI组件系统 - 模块化组件设计 */

/**
 * 模态框组件
 */
class Modal {
    constructor(options = {}) {
        this.id = options.id || `modal-${Date.now()}`;
        this.title = options.title || '模态框';
        this.content = options.content || '';
        this.size = options.size || 'md'; // sm, md, lg, xl
        this.onClose = options.onClose || null;
        this.onConfirm = options.onConfirm || null;
        
        this.init();
    }

    init() {
        this.createModal();
        this.bindEvents();
    }

    createModal() {
        const modalHtml = `
            <div class="modal" id="${this.id}">
                <div class="modal-content modal-${this.size}">
                    <div class="modal-header">
                        <h3 class="modal-title">${this.title}</h3>
                        <button class="modal-close" type="button">
                            <svg width="16" height="16" viewBox="0 0 16 16">
                                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" fill="currentColor"/>
                            </svg>
                        </button>
                    </div>
                    <div class="modal-body">
                        ${this.content}
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary modal-cancel">取消</button>
                        <button class="btn btn-primary modal-confirm">确认</button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        this.modalElement = document.getElementById(this.id);
    }

    bindEvents() {
        const closeBtn = this.modalElement.querySelector('.modal-close');
        const cancelBtn = this.modalElement.querySelector('.modal-cancel');
        const confirmBtn = this.modalElement.querySelector('.modal-confirm');

        const closeModal = () => {
            this.hide();
            if (this.onClose) this.onClose();
        };

        closeBtn.addEventListener('click', closeModal);
        cancelBtn.addEventListener('click', closeModal);

        confirmBtn.addEventListener('click', () => {
            if (this.onConfirm) {
                this.onConfirm();
            }
            this.hide();
        });

        // 点击背景关闭
        this.modalElement.addEventListener('click', (e) => {
            if (e.target === this.modalElement) {
                closeModal();
            }
        });

        // ESC键关闭
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modalElement.classList.contains('active')) {
                closeModal();
            }
        });
    }

    show() {
        this.modalElement.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    hide() {
        this.modalElement.classList.remove('active');
        document.body.style.overflow = '';
        
        setTimeout(() => {
            if (this.modalElement.parentNode) {
                this.modalElement.parentNode.removeChild(this.modalElement);
            }
        }, 300);
    }

    updateContent(newContent) {
        const body = this.modalElement.querySelector('.modal-body');
        if (body) {
            body.innerHTML = newContent;
        }
    }
}

/**
 * 通知组件
 */
class Notification {
    static show(message, type = 'info', duration = 5000) {
        const notification = new Notification(message, type, duration);
        return notification;
    }

    constructor(message, type = 'info', duration = 5000) {
        this.message = message;
        this.type = type;
        this.duration = duration;
        this.id = `notification-${Date.now()}`;
        
        this.create();
        this.show();
    }

    create() {
        const icon = this.getIcon();
        const notificationHtml = `
            <div class="notification ${this.type}" id="${this.id}">
                <div class="notification-icon">${icon}</div>
                <div class="notification-content">
                    <div class="notification-message">${this.message}</div>
                </div>
                <button class="notification-close">
                    <svg width="16" height="16" viewBox="0 0 16 16">
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" fill="currentColor"/>
                    </svg>
                </button>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', notificationHtml);
        this.element = document.getElementById(this.id);
        this.bindEvents();
    }

    getIcon() {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[this.type] || icons.info;
    }

    bindEvents() {
        const closeBtn = this.element.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => this.hide());

        if (this.duration > 0) {
            setTimeout(() => this.hide(), this.duration);
        }
    }

    show() {
        setTimeout(() => {
            this.element.classList.add('show');
        }, 10);
    }

    hide() {
        this.element.classList.remove('show');
        setTimeout(() => {
            if (this.element.parentNode) {
                this.element.parentNode.removeChild(this.element);
            }
        }, 300);
    }
}

/**
 * 加载器组件
 */
class Loader {
    static show(target, message = '加载中...') {
        const loader = new Loader(target, message);
        return loader;
    }

    constructor(target, message = '加载中...') {
        this.target = typeof target === 'string' ? document.querySelector(target) : target;
        this.message = message;
        this.originalContent = '';
        
        if (this.target) {
            this.show();
        }
    }

    show() {
        this.originalContent = this.target.innerHTML;
        this.target.innerHTML = `
            <div class="loading-overlay">
                <div class="loading-spinner"></div>
                <div class="loading-message">${this.message}</div>
            </div>
        `;
        this.target.style.position = 'relative';
    }

    hide() {
        if (this.target && this.originalContent) {
            this.target.innerHTML = this.originalContent;
        }
    }
}

/**
 * 标签页组件
 */
class Tabs {
    constructor(container) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.tabs = [];
        this.activeTab = null;
        
        if (this.container) {
            this.init();
        }
    }

    init() {
        const tabElements = this.container.querySelectorAll('.tab');
        const contentElements = this.container.querySelectorAll('.tab-content');

        tabElements.forEach((tab, index) => {
            const tabId = tab.getAttribute('data-tab') || `tab-${index}`;
            const content = contentElements[index];
            
            this.tabs.push({
                id: tabId,
                tab: tab,
                content: content
            });

            tab.addEventListener('click', () => this.activate(tabId));

            if (tab.classList.contains('active')) {
                this.activeTab = tabId;
            }
        });

        if (!this.activeTab && this.tabs.length > 0) {
            this.activate(this.tabs[0].id);
        }
    }

    activate(tabId) {
        // 隐藏所有内容
        this.tabs.forEach(tab => {
            tab.tab.classList.remove('active');
            if (tab.content) {
                tab.content.classList.remove('active');
            }
        });

        // 显示激活的内容
        const activeTab = this.tabs.find(tab => tab.id === tabId);
        if (activeTab) {
            activeTab.tab.classList.add('active');
            if (activeTab.content) {
                activeTab.content.classList.add('active');
            }
            this.activeTab = tabId;
        }

        // 触发自定义事件
        this.container.dispatchEvent(new CustomEvent('tabChange', {
            detail: { tabId: tabId }
        }));
    }

    addTab(tabConfig) {
        // 动态添加标签页的功能
        const tabId = tabConfig.id || `tab-${this.tabs.length}`;
        
        // 创建标签元素
        const tabElement = document.createElement('button');
        tabElement.className = 'tab';
        tabElement.setAttribute('data-tab', tabId);
        tabElement.textContent = tabConfig.title;
        
        // 创建内容元素
        const contentElement = document.createElement('div');
        contentElement.className = 'tab-content';
        contentElement.innerHTML = tabConfig.content;
        
        // 添加到容器
        this.container.querySelector('.tabs').appendChild(tabElement);
        this.container.querySelector('.tab-contents').appendChild(contentElement);
        
        // 重新初始化
        this.tabs = [];
        this.init();
    }
}

/**
 * 数据表格组件
 */
class DataTable {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.options = {
            columns: [],
            data: [],
            pagination: true,
            pageSize: 10,
            search: true,
            ...options
        };
        
        this.currentPage = 1;
        this.filteredData = [];
        
        if (this.container) {
            this.init();
        }
    }

    init() {
        this.render();
        this.bindEvents();
    }

    render() {
        const { columns, data, pagination, search } = this.options;
        this.filteredData = [...data];

        let html = `
            <div class="data-table">
                ${search ? this.renderSearch() : ''}
                <div class="table-container">
                    <table class="table">
                        ${this.renderHeader()}
                        ${this.renderBody()}
                    </table>
                </div>
                ${pagination ? this.renderPagination() : ''}
            </div>
        `;

        this.container.innerHTML = html;
    }

    renderSearch() {
        return `
            <div class="table-search">
                <input type="text" class="form-input table-search-input" placeholder="搜索...">
            </div>
        `;
    }

    renderHeader() {
        const { columns } = this.options;
        return `
            <thead>
                <tr>
                    ${columns.map(col => `<th>${col.title}</th>`).join('')}
                </tr>
            </thead>
        `;
    }

    renderBody() {
        const { columns, pageSize } = this.options;
        const startIndex = (this.currentPage - 1) * pageSize;
        const pageData = this.filteredData.slice(startIndex, startIndex + pageSize);

        return `
            <tbody>
                ${pageData.map(row => `
                    <tr>
                        ${columns.map(col => `
                            <td>${row[col.key] || ''}</td>
                        `).join('')}
                    </tr>
                `).join('')}
            </tbody>
        `;
    }

    renderPagination() {
        const totalPages = Math.ceil(this.filteredData.length / this.options.pageSize);
        
        return `
            <div class="table-pagination">
                <button class="btn btn-secondary pagination-prev" ${this.currentPage === 1 ? 'disabled' : ''}>
                    上一页
                </button>
                <span class="pagination-info">
                    第 ${this.currentPage} 页，共 ${totalPages} 页
                </span>
                <button class="btn btn-secondary pagination-next" ${this.currentPage === totalPages ? 'disabled' : ''}>
                    下一页
                </button>
            </div>
        `;
    }

    bindEvents() {
        // 搜索功能
        const searchInput = this.container.querySelector('.table-search-input');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce(() => {
                this.filterData(searchInput.value);
            }, 300));
        }

        // 分页功能
        const prevBtn = this.container.querySelector('.pagination-prev');
        const nextBtn = this.container.querySelector('.pagination-next');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousPage());
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextPage());
        }
    }

    filterData(searchTerm) {
        const { columns, data } = this.options;
        
        if (!searchTerm.trim()) {
            this.filteredData = [...data];
        } else {
            this.filteredData = data.filter(row => 
                columns.some(col => {
                    const value = String(row[col.key] || '').toLowerCase();
                    return value.includes(searchTerm.toLowerCase());
                })
            );
        }
        
        this.currentPage = 1;
        this.renderBody();
        this.renderPagination();
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.renderBody();
            this.renderPagination();
        }
    }

    nextPage() {
        const totalPages = Math.ceil(this.filteredData.length / this.options.pageSize);
        if (this.currentPage < totalPages) {
            this.currentPage++;
            this.renderBody();
            this.renderPagination();
        }
    }

    updateData(newData) {
        this.options.data = newData;
        this.filteredData = [...newData];
        this.currentPage = 1;
        this.render();
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

/**
 * 图表组件（基础实现）
 */
class SimpleChart {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.options = {
            type: 'bar', // bar, line, pie
            data: [],
            labels: [],
            colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c'],
            ...options
        };
        
        if (this.container) {
            this.init();
        }
    }

    init() {
        this.render();
    }

    render() {
        const { type, data, labels, colors } = this.options;
        
        if (type === 'bar') {
            this.renderBarChart(data, labels, colors);
        } else if (type === 'pie') {
            this.renderPieChart(data, labels, colors);
        }
    }

    renderBarChart(data, labels, colors) {
        const maxValue = Math.max(...data);
        const chartHeight = 200;
        
        let html = '<div class="simple-chart bar-chart">';
        
        data.forEach((value, index) => {
            const height = (value / maxValue) * chartHeight;
            const color = colors[index % colors.length];
            
            html += `
                <div class="bar-container">
                    <div class="bar" style="height: ${height}px; background: ${color}"></div>
                    <div class="bar-label">${labels[index]}</div>
                    <div class="bar-value">${value}</div>
                </div>
            `;
        });
        
        html += '</div>';
        this.container.innerHTML = html;
    }

    renderPieChart(data, labels, colors) {
        const total = data.reduce((sum, value) => sum + value, 0);
        let cumulativePercent = 0;
        
        let html = '<div class="simple-chart pie-chart">';
        
        data.forEach((value, index) => {
            const percent = (value / total) * 100;
            const color = colors[index % colors.length];
            
            html += `
                <div class="pie-segment" style="
                    --percent: ${percent}%;
                    --color: ${color};
                    --start: ${cumulativePercent}%;
                ">
                    <div class="segment-label">${labels[index]} (${percent.toFixed(1)}%)</div>
                </div>
            `;
            
            cumulativePercent += percent;
        });
        
        html += '</div>';
        this.container.innerHTML = html;
    }

    update(newOptions) {
        this.options = { ...this.options, ...newOptions };
        this.render();
    }
}

/**
 * 文件上传组件
 */
class FileUpload {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.options = {
            multiple: false,
            accept: '*',
            maxSize: 10 * 1024 * 1024, // 10MB
            onUpload: null,
            ...options
        };
        
        if (this.container) {
            this.init();
        }
    }

    init() {
        this.render();
        this.bindEvents();
    }

    render() {
        const { multiple, accept } = this.options;
        
        this.container.innerHTML = `
            <div class="file-upload">
                <input type="file" class="file-input" 
                       ${multiple ? 'multiple' : ''} 
                       accept="${accept}">
                <div class="upload-area">
                    <div class="upload-icon">📁</div>
                    <div class="upload-text">点击或拖拽文件到此处</div>
                    <div class="upload-hint">支持单个文件，最大10MB</div>
                </div>
                <div class="file-list"></div>
            </div>
        `;
    }

    bindEvents() {
        const fileInput = this.container.querySelector('.file-input');
        const uploadArea = this.container.querySelector('.upload-area');
        
        // 点击上传区域触发文件选择
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // 文件选择事件
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
        
        // 拖拽事件
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            this.handleFiles(e.dataTransfer.files);
        });
    }

    handleFiles(files) {
        const validFiles = [];
        
        Array.from(files).forEach(file => {
            if (file.size > this.options.maxSize) {
                Notification.show(`文件 ${file.name} 超过大小限制`, 'error');
                return;
            }
            
            validFiles.push(file);
        });
        
        if (validFiles.length > 0) {
            this.displayFiles(validFiles);
            
            if (this.options.onUpload) {
                this.options.onUpload(validFiles);
            }
        }
    }

    displayFiles(files) {
        const fileList = this.container.querySelector('.file-list');
        
        fileList.innerHTML = files.map(file => `
            <div class="file-item">
                <div class="file-info">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${this.formatFileSize(file.size)}</div>
                </div>
                <div class="file-progress">
                    <div class="progress-bar" style="width: 100%"></div>
                </div>
            </div>
        `).join('');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// 导出所有组件
window.Modal = Modal;
window.Notification = Notification;
window.Loader = Loader;
window.Tabs = Tabs;
window.DataTable = DataTable;
window.SimpleChart = SimpleChart;
window.FileUpload = FileUpload;

// 自动初始化组件
document.addEventListener('DOMContentLoaded', () => {
    // 自动初始化标签页
    document.querySelectorAll('.tabs').forEach(container => {
        new Tabs(container);
    });
    
    // 自动初始化数据表格
    document.querySelectorAll('[data-table]').forEach(container => {
        const options = JSON.parse(container.getAttribute('data-table-options') || '{}');
        new DataTable(container, options);
    });
});