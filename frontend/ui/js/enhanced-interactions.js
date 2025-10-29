// SmartMedia Hub v4.0 - 增强交互功能

class SmartMediaHub {
    constructor() {
        this.currentFeature = null;
        this.isLoading = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadInitialData();
        this.setupWebSocket();
    }

    bindEvents() {
        // 搜索功能
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performSearch(searchInput.value);
                }
            });
        }

        // 快速操作按钮
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const title = btn.getAttribute('title');
                this.showToast(`${title}功能已激活`, 'info');
            });
        });

        // 导航菜单
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = link.getAttribute('href').substring(1);
                this.navigateToFeature(target);
            });
        });
    }

    async loadInitialData() {
        try {
            const response = await fetch('/api/demo/stats');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.updateDashboardStats(data.data);
            }
        } catch (error) {
            console.error('加载初始数据失败:', error);
        }
    }

    updateDashboardStats(stats) {
        // 更新欢迎横幅统计
        const welcomeStats = document.querySelector('.welcome-stats');
        if (welcomeStats) {
            welcomeStats.innerHTML = `
                <div class="stat">
                    <span class="stat-value">${stats.total_media.toLocaleString()}</span>
                    <span class="stat-label">媒体文件</span>
                </div>
                <div class="stat">
                    <span class="stat-value">${stats.recognition_accuracy}%</span>
                    <span class="stat-label">识别准确率</span>
                </div>
                <div class="stat">
                    <span class="stat-value">${stats.online_devices}</span>
                    <span class="stat-label">在线设备</span>
                </div>
            `;
        }

        // 更新功能卡片统计
        this.updateFeatureCards(stats);
    }

    updateFeatureCards(stats) {
        // 更新智能识别卡片
        const recognitionStats = document.querySelector('.recognition-card .feature-stats');
        if (recognitionStats) {
            recognitionStats.innerHTML = `
                <span class="stat">
                    <i class="fas fa-check-circle"></i>
                    今日识别: ${Math.floor(Math.random() * 50) + 10}
                </span>
                <span class="stat">
                    <i class="fas fa-chart-line"></i>
                    准确率: ${stats.recognition_accuracy}%
                </span>
            `;
        }

        // 更新订阅管理卡片
        const subscriptionStats = document.querySelector('.subscription-card .feature-stats');
        if (subscriptionStats) {
            subscriptionStats.innerHTML = `
                <span class="stat">
                    <i class="fas fa-rss"></i>
                    活跃订阅: ${stats.active_subscriptions}
                </span>
                <span class="stat">
                    <i class="fas fa-download"></i>
                    今日下载: ${stats.today_downloads}
                </span>
            `;
        }

        // 更新设备同步卡片
        const syncStats = document.querySelector('.sync-card .feature-stats');
        if (syncStats) {
            syncStats.innerHTML = `
                <span class="stat">
                    <i class="fas fa-desktop"></i>
                    在线设备: ${stats.online_devices}
                </span>
                <span class="stat">
                    <i class="fas fa-check"></i>
                    同步状态: ${stats.sync_status}
                </span>
            `;
        }

        // 更新推荐系统卡片
        const recommendationStats = document.querySelector('.recommendation-card .feature-stats');
        if (recommendationStats) {
            recommendationStats.innerHTML = `
                <span class="stat">
                    <i class="fas fa-user"></i>
                    用户偏好: 已分析
                </span>
                <span class="stat">
                    <i class="fas fa-lightbulb"></i>
                    推荐精度: ${stats.recommendation_accuracy}%
                </span>
            `;
        }
    }

    setupWebSocket() {
        const ws = new WebSocket('ws://' + window.location.host + '/ws');
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'stats_update') {
                this.updateRealTimeStats(data.data);
            }
        };

        ws.onclose = () => {
            setTimeout(() => this.setupWebSocket(), 5000);
        };
    }

    updateRealTimeStats(stats) {
        // 更新CPU使用率
        const cpuElement = document.querySelector('.status-item:nth-child(2) span');
        if (cpuElement) {
            cpuElement.textContent = stats.cpu_usage;
        }

        // 更新系统状态
        this.updateSystemStatus(stats);
    }

    updateSystemStatus(stats) {
        // 这里可以添加更多的实时状态更新逻辑
        console.log('实时状态更新:', stats);
    }

    // 功能详情展示
    showFeatureDetails(feature) {
        this.currentFeature = feature;
        
        const features = {
            'recognition': {
                title: '智能识别引擎',
                description: '融合NASTool算法的智能识别系统',
                details: '支持复杂文件名解析、多算法并行识别、自动分类等功能'
            },
            'subscription': {
                title: '订阅管理系统', 
                description: 'MoviePilot精华功能集成',
                details: '自动化RSS订阅、智能下载、过滤规则配置'
            },
            'sync': {
                title: '多设备同步',
                description: 'MediaMaster技术实现',
                details: '跨设备实时同步、冲突解决、规则配置'
            },
            'recommendation': {
                title: '智能推荐系统',
                description: '个性化内容推荐',
                details: '基于用户偏好分析、相似内容发现、趋势分析'
            }
        };

        const featureInfo = features[feature];
        if (featureInfo) {
            this.showModal(featureInfo.title, featureInfo.details);
        }
    }

    showModal(title, content) {
        // 创建模态框
        const modal = document.createElement('div');
        modal.className = 'feature-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close" onclick="this.closest('.feature-modal').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <p>${content}</p>
                    <div class="modal-actions">
                        <button class="btn btn-primary" onclick="smartMediaHub.openFeature('${this.currentFeature}')">
                            打开功能
                        </button>
                        <button class="btn btn-outline" onclick="this.closest('.feature-modal').remove()">
                            关闭
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    openFeature(feature) {
        this.showToast(`正在打开${feature}功能...`, 'info');
        
        // 模拟打开功能
        setTimeout(() => {
            this.showToast(`${feature}功能已打开`, 'success');
            // 关闭模态框
            document.querySelector('.feature-modal')?.remove();
        }, 1000);
    }

    // 搜索功能
    performSearch(query) {
        if (!query.trim()) return;
        
        this.showToast(`搜索: ${query}`, 'info');
        
        // 模拟搜索过程
        this.showLoading('正在搜索...');
        
        setTimeout(() => {
            this.hideLoading();
            this.showSearchResults(query);
        }, 1500);
    }

    showSearchResults(query) {
        const results = [
            { type: 'media', title: 'The Matrix (1999)', match: '95%' },
            { type: 'subscription', title: '电影RSS订阅源', match: '88%' },
            { type: 'device', title: 'NAS-01设备', match: '76%' }
        ];

        const modal = document.createElement('div');
        modal.className = 'search-results-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>搜索结果: "${query}"</h3>
                    <button class="modal-close" onclick="this.closest('.search-results-modal').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    ${results.map(result => `
                        <div class="search-result-item">
                            <div class="result-type">${result.type}</div>
                            <div class="result-title">${result.title}</div>
                            <div class="result-match">匹配度: ${result.match}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    // 导航功能
    navigateToFeature(feature) {
        this.showToast(`正在切换到${feature}页面...`, 'info');
        
        // 更新活动导航项
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const targetItem = document.querySelector(`[href="#${feature}"]`).closest('.nav-item');
        if (targetItem) {
            targetItem.classList.add('active');
        }

        // 更新面包屑
        this.updateBreadcrumb(feature);
    }

    updateBreadcrumb(feature) {
        const breadcrumb = document.querySelector('.breadcrumb ol');
        if (breadcrumb) {
            const featureNames = {
                'dashboard': '仪表板',
                'media-library': '媒体库',
                'subscription': '订阅管理',
                'recognition': '智能识别',
                'sync': '设备同步',
                'recommendation': '智能推荐'
            };

            breadcrumb.innerHTML = `
                <li><a href="#dashboard"><i class="fas fa-home"></i> 首页</a></li>
                <li><i class="fas fa-chevron-right"></i></li>
                <li>${featureNames[feature] || feature}</li>
            `;
        }
    }

    // 工具方法
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${this.getToastIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    getToastIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'times-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    showLoading(message = '加载中...') {
        this.isLoading = true;
        
        const loading = document.createElement('div');
        loading.className = 'loading-overlay';
        loading.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <p>${message}</p>
            </div>
        `;

        document.body.appendChild(loading);
    }

    hideLoading() {
        this.isLoading = false;
        document.querySelector('.loading-overlay')?.remove();
    }

    // 功能按钮交互方法
    startRecognition() {
        this.showLoading('开始智能识别...');
        
        setTimeout(() => {
            this.hideLoading();
            this.showToast('智能识别完成！识别了24个新文件', 'success');
        }, 2000);
    }

    addSubscription() {
        this.showModal('添加订阅', '请输入RSS订阅源地址和配置信息');
    }

    startSync() {
        this.showLoading('开始设备同步...');
        
        setTimeout(() => {
            this.hideLoading();
            this.showToast('设备同步完成！8个设备已同步', 'success');
        }, 1500);
    }

    generateRecommendations() {
        this.showLoading('生成个性化推荐...');
        
        setTimeout(() => {
            this.hideLoading();
            this.showToast('推荐生成完成！发现15个您可能喜欢的内容', 'success');
        }, 2500);
    }
}

// 全局实例
const smartMediaHub = new SmartMediaHub();

// 导出到全局作用域
window.smartMediaHub = smartMediaHub;

// 功能按钮的全局函数
window.showFeatureDetails = (feature) => smartMediaHub.showFeatureDetails(feature);
window.startRecognition = () => smartMediaHub.startRecognition();
window.addSubscription = () => smartMediaHub.addSubscription();
window.startSync = () => smartMediaHub.startSync();
window.generateRecommendations = () => smartMediaHub.generateRecommendations();
window.openSettings = (feature) => smartMediaHub.showToast(`打开${feature}设置`, 'info');
window.monitorSubscriptions = () => smartMediaHub.showToast('打开订阅监控', 'info');
window.addDevice = () => smartMediaHub.showToast('添加新设备', 'info');
window.showAnalysisReport = () => smartMediaHub.showToast('打开分析报告', 'info');
window.scanMediaLibrary = () => smartMediaHub.showToast('开始扫描媒体库', 'info');
window.openMediaLibrary = () => smartMediaHub.showToast('打开媒体库', 'info');
window.configureScrapers = () => smartMediaHub.showToast('配置刮削器', 'info');
window.startScraping = () => smartMediaHub.showToast('开始元数据刮削', 'info');
window.manageUsers = () => smartMediaHub.showToast('管理用户', 'info');
window.addUser = () => smartMediaHub.showToast('添加用户', 'info');
window.viewDownloads = () => smartMediaHub.showToast('查看下载任务', 'info');
window.addDownload = () => smartMediaHub.showToast('添加下载任务', 'info');