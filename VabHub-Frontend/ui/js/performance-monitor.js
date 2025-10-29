/* 性能监控模块 */

class PerformanceMonitor {
    constructor() {
        this.metrics = {
            cpu: 0,
            memory: 0,
            disk: 0,
            network: 0,
            responseTime: 0
        };
        this.history = {
            cpu: [],
            memory: [],
            disk: [],
            network: [],
            responseTime: []
        };
        this.alerts = [];
        this.updateInterval = null;
        this.maxHistoryPoints = 60; // 保留最近60个数据点
    }

    /**
     * 初始化性能监控
     */
    init() {
        this.startMonitoring();
        this.setupEventListeners();
        this.renderPerformanceDashboard();
        
        console.log('性能监控模块已初始化');
    }

    /**
     * 开始监控
     */
    startMonitoring() {
        // 立即获取一次数据
        this.updateMetrics();
        
        // 设置定时更新
        this.updateInterval = setInterval(() => {
            this.updateMetrics();
            this.checkAlerts();
            this.updateCharts();
        }, 5000); // 每5秒更新一次
    }

    /**
     * 停止监控
     */
    stopMonitoring() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    /**
     * 更新性能指标
     */
    async updateMetrics() {
        try {
            // 模拟获取性能数据
            const newMetrics = await this.fetchPerformanceData();
            
            // 更新当前指标
            Object.assign(this.metrics, newMetrics);
            
            // 添加到历史记录
            this.addToHistory(newMetrics);
            
            // 更新UI
            this.updateMetricsDisplay();
            
        } catch (error) {
            console.error('获取性能数据失败:', error);
            this.addAlert('error', '性能监控', '无法获取系统性能数据');
        }
    }

    /**
     * 模拟获取性能数据
     */
    async fetchPerformanceData() {
        // 在实际应用中，这里会调用真实的API
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    cpu: Math.random() * 100,
                    memory: 30 + Math.random() * 50,
                    disk: 20 + Math.random() * 60,
                    network: Math.random() * 100,
                    responseTime: Math.random() * 200
                });
            }, 100);
        });
    }

    /**
     * 添加到历史记录
     */
    addToHistory(metrics) {
        const timestamp = Date.now();
        
        Object.keys(metrics).forEach(key => {
            this.history[key].push({
                value: metrics[key],
                timestamp: timestamp
            });
            
            // 保持历史记录长度
            if (this.history[key].length > this.maxHistoryPoints) {
                this.history[key].shift();
            }
        });
    }

    /**
     * 检查告警
     */
    checkAlerts() {
        const thresholds = {
            cpu: { critical: 90, warning: 80 },
            memory: { critical: 90, warning: 80 },
            disk: { critical: 95, warning: 85 },
            responseTime: { critical: 1000, warning: 500 }
        };

        Object.keys(thresholds).forEach(metric => {
            const value = this.metrics[metric];
            const threshold = thresholds[metric];
            
            if (value >= threshold.critical) {
                this.addAlert('critical', metric.toUpperCase(), `${metric}使用率过高: ${value.toFixed(1)}%`);
            } else if (value >= threshold.warning) {
                this.addAlert('warning', metric.toUpperCase(), `${metric}使用率较高: ${value.toFixed(1)}%`);
            }
        });
    }

    /**
     * 添加告警
     */
    addAlert(level, title, description) {
        const alert = {
            id: Date.now(),
            level: level,
            title: title,
            description: description,
            timestamp: new Date().toLocaleTimeString(),
            acknowledged: false
        };
        
        this.alerts.unshift(alert);
        
        // 保持最多20个告警
        if (this.alerts.length > 20) {
            this.alerts.pop();
        }
        
        // 更新告警显示
        this.updateAlertsDisplay();
        
        // 发送通知
        this.sendNotification(alert);
    }

    /**
     * 发送通知
     */
    sendNotification(alert) {
        if (window.smartMediaHub && window.smartMediaHub.sendNotification) {
            window.smartMediaHub.sendNotification(
                `性能告警: ${alert.title}`,
                alert.description
            );
        }
    }

    /**
     * 设置事件监听器
     */
    setupEventListeners() {
        // 监听窗口焦点变化
        window.addEventListener('focus', () => {
            this.updateMetrics();
        });

        // 监听网络状态变化
        window.addEventListener('online', () => {
            this.addAlert('info', '网络状态', '网络连接已恢复');
        });

        window.addEventListener('offline', () => {
            this.addAlert('warning', '网络状态', '网络连接已断开');
        });
    }

    /**
     * 渲染性能监控面板
     */
    renderPerformanceDashboard() {
        const dashboard = document.getElementById('performance-dashboard');
        if (!dashboard) return;

        dashboard.innerHTML = `
            <div class="performance-dashboard">
                <!-- 性能指标卡片 -->
                <div class="performance-metrics">
                    <div class="metric-card" id="metric-cpu">
                        <div class="metric-header">
                            <span class="metric-title">CPU使用率</span>
                            <div class="metric-gauge">
                                <div class="gauge-inner">0%</div>
                            </div>
                        </div>
                        <div class="metric-value">0%</div>
                        <div class="metric-trend trend-stable">
                            <i class="fas fa-minus"></i>
                            <span>稳定</span>
                        </div>
                    </div>
                    
                    <div class="metric-card" id="metric-memory">
                        <div class="metric-header">
                            <span class="metric-title">内存使用</span>
                            <div class="metric-gauge">
                                <div class="gauge-inner">0%</div>
                            </div>
                        </div>
                        <div class="metric-value">0%</div>
                        <div class="metric-trend trend-stable">
                            <i class="fas fa-minus"></i>
                            <span>稳定</span>
                        </div>
                    </div>
                    
                    <div class="metric-card" id="metric-disk">
                        <div class="metric-header">
                            <span class="metric-title">磁盘使用</span>
                            <div class="metric-gauge">
                                <div class="gauge-inner">0%</div>
                            </div>
                        </div>
                        <div class="metric-value">0%</div>
                        <div class="metric-trend trend-stable">
                            <i class="fas fa-minus"></i>
                            <span>稳定</span>
                        </div>
                    </div>
                    
                    <div class="metric-card" id="metric-response">
                        <div class="metric-header">
                            <span class="metric-title">响应时间</span>
                            <i class="fas fa-clock"></i>
                        </div>
                        <div class="metric-value">0ms</div>
                        <div class="metric-trend trend-stable">
                            <i class="fas fa-minus"></i>
                            <span>稳定</span>
                        </div>
                    </div>
                </div>
                
                <!-- 实时图表 -->
                <div class="realtime-charts">
                    <div class="chart-container">
                        <div class="chart-header">
                            <h3 class="chart-title">CPU & 内存使用趋势</h3>
                            <div class="chart-actions">
                                <button class="chart-action-btn" title="刷新">
                                    <i class="fas fa-sync-alt"></i>
                                </button>
                                <button class="chart-action-btn" title="导出">
                                    <i class="fas fa-download"></i>
                                </button>
                            </div>
                        </div>
                        <canvas class="chart-canvas" id="cpu-memory-chart"></canvas>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-header">
                            <h3 class="chart-title">系统状态</h3>
                        </div>
                        <div class="system-status">
                            <div class="status-item">
                                <div class="status-icon online">
                                    <i class="fas fa-server"></i>
                                </div>
                                <div class="status-info">
                                    <div class="status-label">应用服务</div>
                                    <div class="status-value">运行中</div>
                                </div>
                            </div>
                            <div class="status-item">
                                <div class="status-icon online">
                                    <i class="fas fa-database"></i>
                                </div>
                                <div class="status-info">
                                    <div class="status-label">数据库</div>
                                    <div class="status-value">正常</div>
                                </div>
                            </div>
                            <div class="status-item">
                                <div class="status-icon online">
                                    <i class="fas fa-network-wired"></i>
                                </div>
                                <div class="status-info">
                                    <div class="status-label">网络连接</div>
                                    <div class="status-value">稳定</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 告警面板 -->
                <div class="alerts-panel">
                    <div class="alerts-header">
                        <h3 class="alerts-title">系统告警</h3>
                        <span class="alerts-count" id="alerts-count">0</span>
                    </div>
                    <div class="alerts-list" id="alerts-list">
                        <div class="alert-item">
                            <div class="alert-icon info">
                                <i class="fas fa-info-circle"></i>
                            </div>
                            <div class="alert-content">
                                <div class="alert-title">系统监控已启动</div>
                                <div class="alert-description">性能监控模块正常运行中</div>
                            </div>
                            <div class="alert-time">${new Date().toLocaleTimeString()}</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.initializeCharts();
    }

    /**
     * 初始化图表
     */
    initializeCharts() {
        // 这里可以集成Chart.js或其他图表库
        // 暂时使用简单的Canvas绘制
        this.drawSimpleChart('cpu-memory-chart');
    }

    /**
     * 绘制简单图表
     */
    drawSimpleChart(canvasId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        // 清空画布
        ctx.clearRect(0, 0, width, height);
        
        // 绘制网格
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;
        
        // 水平网格线
        for (let i = 0; i <= 5; i++) {
            const y = (height / 5) * i;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        
        // 垂直网格线
        for (let i = 0; i <= 10; i++) {
            const x = (width / 10) * i;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
        
        // 绘制提示文本
        ctx.fillStyle = 'var(--text-secondary)';
        ctx.font = '14px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('实时监控图表', width / 2, height / 2);
        ctx.fillText('(集成Chart.js后可显示详细数据)', width / 2, height / 2 + 20);
    }

    /**
     * 更新指标显示
     */
    updateMetricsDisplay() {
        // 更新CPU指标
        this.updateMetricCard('cpu', this.metrics.cpu, '%');
        this.updateMetricCard('memory', this.metrics.memory, '%');
        this.updateMetricCard('disk', this.metrics.disk, '%');
        this.updateMetricCard('response', this.metrics.responseTime, 'ms');
    }

    /**
     * 更新单个指标卡片
     */
    updateMetricCard(metric, value, unit) {
        const card = document.getElementById(`metric-${metric}`);
        if (!card) return;
        
        const valueElement = card.querySelector('.metric-value');
        const gaugeElement = card.querySelector('.gauge-inner');
        const trendElement = card.querySelector('.metric-trend');
        
        if (valueElement) {
            valueElement.textContent = `${value.toFixed(1)}${unit}`;
        }
        
        if (gaugeElement) {
            gaugeElement.textContent = `${value.toFixed(0)}%`;
        }
        
        // 根据值设置卡片状态
        card.className = `metric-card ${this.getMetricStatus(metric, value)}`;
        
        // 更新趋势指示器
        this.updateTrendIndicator(trendElement, metric, value);
    }

    /**
     * 获取指标状态
     */
    getMetricStatus(metric, value) {
        const thresholds = {
            cpu: { critical: 90, warning: 80 },
            memory: { critical: 90, warning: 80 },
            disk: { critical: 95, warning: 85 },
            response: { critical: 1000, warning: 500 }
        };
        
        const threshold = thresholds[metric];
        if (!threshold) return 'normal';
        
        if (value >= threshold.critical) return 'critical';
        if (value >= threshold.warning) return 'warning';
        return 'normal';
    }

    /**
     * 更新趋势指示器
     */
    updateTrendIndicator(trendElement, metric, currentValue) {
        if (!trendElement || this.history[metric].length < 2) return;
        
        const previousValue = this.history[metric][this.history[metric].length - 2].value;
        const diff = currentValue - previousValue;
        
        let trendClass, trendIcon, trendText;
        
        if (Math.abs(diff) < 0.1) {
            trendClass = 'trend-stable';
            trendIcon = 'fa-minus';
            trendText = '稳定';
        } else if (diff > 0) {
            trendClass = 'trend-up';
            trendIcon = 'fa-arrow-up';
            trendText = '上升';
        } else {
            trendClass = 'trend-down';
            trendIcon = 'fa-arrow-down';
            trendText = '下降';
        }
        
        trendElement.className = `metric-trend ${trendClass}`;
        trendElement.innerHTML = `<i class="fas ${trendIcon}"></i><span>${trendText}</span>`;
    }

    /**
     * 更新图表
     */
    updateCharts() {
        this.drawSimpleChart('cpu-memory-chart');
    }

    /**
     * 更新告警显示
     */
    updateAlertsDisplay() {
        const alertsList = document.getElementById('alerts-list');
        const alertsCount = document.getElementById('alerts-count');
        
        if (!alertsList || !alertsCount) return;
        
        // 更新告警数量
        const criticalAlerts = this.alerts.filter(alert => alert.level === 'critical' && !alert.acknowledged);
        alertsCount.textContent = criticalAlerts.length;
        
        // 更新告警列表
        alertsList.innerHTML = this.alerts.map(alert => `
            <div class="alert-item ${alert.level} ${alert.acknowledged ? 'acknowledged' : ''}">
                <div class="alert-icon ${alert.level}">
                    <i class="fas ${
                        alert.level === 'critical' ? 'fa-exclamation-triangle' :
                        alert.level === 'warning' ? 'fa-exclamation-circle' : 'fa-info-circle'
                    }"></i>
                </div>
                <div class="alert-content">
                    <div class="alert-title">${alert.title}</div>
                    <div class="alert-description">${alert.description}</div>
                </div>
                <div class="alert-time">${alert.timestamp}</div>
            </div>
        `).join('');
        
        if (this.alerts.length === 0) {
            alertsList.innerHTML = `
                <div class="alert-item">
                    <div class="alert-icon info">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <div class="alert-content">
                        <div class="alert-title">系统正常</div>
                        <div class="alert-description">暂无告警信息</div>
                    </div>
                    <div class="alert-time">${new Date().toLocaleTimeString()}</div>
                </div>
            `;
        }
    }

    /**
     * 导出性能数据
     */
    exportData() {
        const data = {
            metrics: this.metrics,
            history: this.history,
            alerts: this.alerts,
            exportTime: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `performance-data-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * 获取性能摘要
     */
    getPerformanceSummary() {
        return {
            overallHealth: this.calculateOverallHealth(),
            criticalAlerts: this.alerts.filter(alert => alert.level === 'critical').length,
            warningAlerts: this.alerts.filter(alert => alert.level === 'warning').length,
            uptime: this.calculateUptime(),
            lastUpdate: new Date().toISOString()
        };
    }

    /**
     * 计算整体健康度
     */
    calculateOverallHealth() {
        const weights = { cpu: 0.3, memory: 0.3, disk: 0.2, responseTime: 0.2 };
        let health = 100;
        
        Object.keys(weights).forEach(metric => {
            const value = this.metrics[metric];
            const threshold = metric === 'responseTime' ? 500 : 80;
            const penalty = Math.max(0, (value - threshold) / (100 - threshold)) * 100;
            health -= penalty * weights[metric];
        });
        
        return Math.max(0, Math.min(100, health));
    }

    /**
     * 计算运行时间
     */
    calculateUptime() {
        // 这里应该从系统启动时间计算
        return '24小时15分钟';
    }
}

// 全局性能监控实例
window.performanceMonitor = new PerformanceMonitor();

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('performance-dashboard')) {
        window.performanceMonitor.init();
    }
});