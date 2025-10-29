/**
 * v4.2 批量操作优化模块
 * 实现异步批量处理队列、进度监控和暂停/恢复功能
 */

class BatchProcessor {
    constructor() {
        this.queue = [];
        this.isProcessing = false;
        this.isPaused = false;
        this.currentIndex = 0;
        this.progress = 0;
        this.totalItems = 0;
        this.successCount = 0;
        this.failedCount = 0;
        this.batchSize = 5; // 并发处理数量
        
        this.eventHandlers = new Map();
        this.initializeEvents();
    }

    /**
     * 初始化事件系统
     */
    initializeEvents() {
        this.eventHandlers.set('progress', []);
        this.eventHandlers.set('complete', []);
        this.eventHandlers.set('error', []);
        this.eventHandlers.set('pause', []);
        this.eventHandlers.set('resume', []);
        this.eventHandlers.set('itemComplete', []);
    }

    /**
     * 添加事件监听器
     */
    on(event, handler) {
        if (this.eventHandlers.has(event)) {
            this.eventHandlers.get(event).push(handler);
        }
    }

    /**
     * 触发事件
     */
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

    /**
     * 添加批量任务
     */
    addTasks(tasks) {
        if (!Array.isArray(tasks)) {
            tasks = [tasks];
        }

        tasks.forEach((task, index) => {
            this.queue.push({
                id: this.generateTaskId(),
                data: task,
                status: 'pending',
                index: this.queue.length + index,
                retryCount: 0
            });
        });

        this.totalItems = this.queue.length;
        this.updateProgress();
        
        console.log(`添加了 ${tasks.length} 个任务，队列总数: ${this.queue.length}`);
    }

    /**
     * 生成任务ID
     */
    generateTaskId() {
        return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * 开始处理
     */
    async start() {
        if (this.isProcessing) {
            console.warn('批量处理已在进行中');
            return;
        }

        if (this.queue.length === 0) {
            console.warn('队列为空，无法开始处理');
            return;
        }

        this.isProcessing = true;
        this.isPaused = false;
        this.currentIndex = 0;
        this.successCount = 0;
        this.failedCount = 0;

        console.log('开始批量处理，队列大小:', this.queue.length);

        await this.processBatch();
    }

    /**
     * 批量处理
     */
    async processBatch() {
        while (this.currentIndex < this.queue.length && this.isProcessing && !this.isPaused) {
            const batchTasks = this.queue.slice(this.currentIndex, this.currentIndex + this.batchSize);
            
            try {
                await Promise.allSettled(
                    batchTasks.map(task => this.processTask(task))
                );
                
                this.currentIndex += batchTasks.length;
                this.updateProgress();
                
                // 添加延迟以避免过度占用资源
                await this.delay(100);
                
            } catch (error) {
                console.error('批量处理错误:', error);
                this.emit('error', { error, batchIndex: this.currentIndex });
            }
        }

        if (this.currentIndex >= this.queue.length) {
            this.completeProcessing();
        }
    }

    /**
     * 处理单个任务
     */
    async processTask(task) {
        if (task.status === 'completed' || task.status === 'failed') {
            return;
        }

        task.status = 'processing';
        
        try {
            // 模拟API调用
            const result = await this.executeTask(task.data);
            
            task.status = 'completed';
            task.result = result;
            this.successCount++;
            
            this.emit('itemComplete', {
                taskId: task.id,
                result,
                success: true
            });
            
        } catch (error) {
            task.status = 'failed';
            task.error = error;
            this.failedCount++;
            
            this.emit('itemComplete', {
                taskId: task.id,
                error,
                success: false
            });
            
            // 重试逻辑
            if (task.retryCount < 3) {
                task.retryCount++;
                console.log(`任务 ${task.id} 重试 (${task.retryCount}/3)`);
                await this.delay(1000 * task.retryCount); // 指数退避
                return this.processTask(task);
            }
        }
    }

    /**
     * 执行任务
     */
    async executeTask(taskData) {
        // 模拟不同类型的任务处理
        if (taskData.type === 'rename') {
            return await this.renameFile(taskData);
        } else if (taskData.type === 'analyze') {
            return await this.analyzeMedia(taskData);
        } else if (taskData.type === 'download') {
            return await this.downloadMedia(taskData);
        } else {
            throw new Error(`未知的任务类型: ${taskData.type}`);
        }
    }

    /**
     * 重命名文件
     */
    async renameFile(taskData) {
        // 模拟API调用
        await this.delay(Math.random() * 500 + 200);
        
        if (Math.random() < 0.05) { // 5%失败率
            throw new Error('重命名失败: 文件不存在');
        }
        
        return {
            originalName: taskData.fileName,
            newName: `${taskData.prefix || ''}${taskData.fileName}`,
            success: true
        };
    }

    /**
     * 分析媒体文件
     */
    async analyzeMedia(taskData) {
        await this.delay(Math.random() * 1000 + 500);
        
        if (Math.random() < 0.03) { // 3%失败率
            throw new Error('分析失败: 文件格式不支持');
        }
        
        return {
            fileName: taskData.fileName,
            mediaType: ['movie', 'tv', 'music'][Math.floor(Math.random() * 3)],
            duration: Math.floor(Math.random() * 7200),
            size: Math.floor(Math.random() * 1000000000),
            success: true
        };
    }

    /**
     * 下载媒体
     */
    async downloadMedia(taskData) {
        await this.delay(Math.random() * 2000 + 1000);
        
        if (Math.random() < 0.08) { // 8%失败率
            throw new Error('下载失败: 网络连接错误');
        }
        
        return {
            url: taskData.url,
            destination: taskData.destination,
            size: Math.floor(Math.random() * 500000000),
            success: true
        };
    }

    /**
     * 暂停处理
     */
    pause() {
        if (!this.isProcessing) {
            console.warn('处理未开始，无法暂停');
            return;
        }
        
        if (this.isPaused) {
            console.warn('处理已暂停');
            return;
        }
        
        this.isPaused = true;
        this.emit('pause', { progress: this.progress });
        console.log('批量处理已暂停');
    }

    /**
     * 恢复处理
     */
    resume() {
        if (!this.isProcessing) {
            console.warn('处理未开始，无法恢复');
            return;
        }
        
        if (!this.isPaused) {
            console.warn('处理未暂停，无需恢复');
            return;
        }
        
        this.isPaused = false;
        this.emit('resume', { progress: this.progress });
        console.log('批量处理已恢复');
        
        this.processBatch();
    }

    /**
     * 停止处理
     */
    stop() {
        this.isProcessing = false;
        this.isPaused = false;
        console.log('批量处理已停止');
    }

    /**
     * 完成处理
     */
    completeProcessing() {
        this.isProcessing = false;
        this.progress = 100;
        
        const summary = {
            total: this.totalItems,
            success: this.successCount,
            failed: this.failedCount,
            duration: Date.now() - this.startTime
        };
        
        this.emit('complete', summary);
        console.log('批量处理完成:', summary);
    }

    /**
     * 更新进度
     */
    updateProgress() {
        if (this.totalItems === 0) {
            this.progress = 0;
        } else {
            this.progress = Math.round((this.currentIndex / this.totalItems) * 100);
        }
        
        this.emit('progress', {
            progress: this.progress,
            current: this.currentIndex,
            total: this.totalItems,
            success: this.successCount,
            failed: this.failedCount
        });
    }

    /**
     * 获取队列状态
     */
    getStatus() {
        return {
            isProcessing: this.isProcessing,
            isPaused: this.isPaused,
            progress: this.progress,
            currentIndex: this.currentIndex,
            totalItems: this.totalItems,
            successCount: this.successCount,
            failedCount: this.failedCount,
            queueLength: this.queue.length
        };
    }

    /**
     * 清空队列
     */
    clearQueue() {
        this.queue = [];
        this.totalItems = 0;
        this.progress = 0;
        this.successCount = 0;
        this.failedCount = 0;
        console.log('队列已清空');
    }

    /**
     * 延迟函数
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * 获取任务统计
     */
    getStatistics() {
        const statusCounts = {};
        this.queue.forEach(task => {
            statusCounts[task.status] = (statusCounts[task.status] || 0) + 1;
        });
        
        return {
            total: this.queue.length,
            statusCounts,
            successRate: this.totalItems > 0 ? (this.successCount / this.totalItems * 100).toFixed(2) : 0
        };
    }
}

/**
 * 批量操作UI组件
 */
class BatchProcessorUI {
    constructor() {
        this.processor = new BatchProcessor();
        this.container = null;
        this.progressBar = null;
        this.statusText = null;
        this.controlButtons = null;
        this.taskList = null;
        
        this.init();
    }

    init() {
        this.createUI();
        this.bindEvents();
        this.setupProcessorEvents();
    }

    createUI() {
        // 创建批量处理容器
        this.container = document.createElement('div');
        this.container.className = 'batch-processor-container';
        this.container.innerHTML = this.getTemplate();
        
        // 获取DOM元素
        this.progressBar = this.container.querySelector('.batch-progress-bar');
        this.statusText = this.container.querySelector('.batch-status-text');
        this.controlButtons = this.container.querySelector('.batch-control-buttons');
        this.taskList = this.container.querySelector('.batch-task-list');
        
        // 添加到页面
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.appendChild(this.container);
        }
    }

    getTemplate() {
        return `
            <div class="batch-processor-panel">
                <div class="batch-header">
                    <h3>批量操作</h3>
                    <div class="batch-stats">
                        <span class="stat-item">
                            <i class="fas fa-tasks"></i>
                            <span class="stat-value" id="batch-total">0</span>
                        </span>
                        <span class="stat-item">
                            <i class="fas fa-check-circle"></i>
                            <span class="stat-value" id="batch-success">0</span>
                        </span>
                        <span class="stat-item">
                            <i class="fas fa-times-circle"></i>
                            <span class="stat-value" id="batch-failed">0</span>
                        </span>
                    </div>
                </div>
                
                <div class="batch-progress">
                    <div class="progress-bar-container">
                        <div class="batch-progress-bar">
                            <div class="progress-fill" style="width: 0%"></div>
                        </div>
                        <div class="progress-text">
                            <span class="batch-status-text">等待开始</span>
                            <span class="batch-percentage">0%</span>
                        </div>
                    </div>
                </div>
                
                <div class="batch-control-buttons">
                    <button class="btn btn-primary" id="batch-start">
                        <i class="fas fa-play"></i> 开始
                    </button>
                    <button class="btn btn-secondary" id="batch-pause" disabled>
                        <i class="fas fa-pause"></i> 暂停
                    </button>
                    <button class="btn btn-secondary" id="batch-resume" disabled>
                        <i class="fas fa-redo"></i> 恢复
                    </button>
                    <button class="btn btn-danger" id="batch-stop" disabled>
                        <i class="fas fa-stop"></i> 停止
                    </button>
                    <button class="btn btn-outline" id="batch-clear">
                        <i class="fas fa-trash"></i> 清空
                    </button>
                </div>
                
                <div class="batch-task-list">
                    <div class="task-list-header">
                        <span>任务列表</span>
                        <span class="task-count">0 个任务</span>
                    </div>
                    <div class="task-items"></div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        // 绑定按钮事件
        this.container.querySelector('#batch-start').addEventListener('click', () => this.startProcessing());
        this.container.querySelector('#batch-pause').addEventListener('click', () => this.pauseProcessing());
        this.container.querySelector('#batch-resume').addEventListener('click', () => this.resumeProcessing());
        this.container.querySelector('#batch-stop').addEventListener('click', () => this.stopProcessing());
        this.container.querySelector('#batch-clear').addEventListener('click', () => this.clearQueue());
        
        // 文件拖放支持
        this.setupDragAndDrop();
    }

    setupProcessorEvents() {
        this.processor.on('progress', (data) => this.updateProgress(data));
        this.processor.on('complete', (data) => this.handleComplete(data));
        this.processor.on('error', (data) => this.handleError(data));
        this.processor.on('itemComplete', (data) => this.updateTaskItem(data));
        this.processor.on('pause', () => this.updateButtonStates());
        this.processor.on('resume', () => this.updateButtonStates());
    }

    startProcessing() {
        // 添加示例任务
        const sampleTasks = this.generateSampleTasks(10);
        this.processor.addTasks(sampleTasks);
        this.processor.start();
        this.updateButtonStates();
        this.updateTaskList();
    }

    pauseProcessing() {
        this.processor.pause();
        this.updateButtonStates();
    }

    resumeProcessing() {
        this.processor.resume();
        this.updateButtonStates();
    }

    stopProcessing() {
        this.processor.stop();
        this.updateButtonStates();
    }

    clearQueue() {
        this.processor.clearQueue();
        this.updateProgress({ progress: 0, current: 0, total: 0, success: 0, failed: 0 });
        this.updateButtonStates();
        this.updateTaskList();
    }

    updateProgress(data) {
        // 更新进度条
        const progressFill = this.progressBar.querySelector('.progress-fill');
        progressFill.style.width = `${data.progress}%`;
        
        // 更新状态文本
        this.statusText.textContent = `处理中: ${data.current}/${data.total}`;
        this.container.querySelector('.batch-percentage').textContent = `${data.progress}%`;
        
        // 更新统计信息
        this.container.querySelector('#batch-total').textContent = data.total;
        this.container.querySelector('#batch-success').textContent = data.success;
        this.container.querySelector('#batch-failed').textContent = data.failed;
    }

    handleComplete(data) {
        this.statusText.textContent = `处理完成: ${data.success}/${data.total} 成功`;
        this.updateButtonStates();
        
        // 显示完成通知
        this.showNotification(`批量处理完成！成功: ${data.success}, 失败: ${data.failed}`);
    }

    handleError(data) {
        console.error('处理错误:', data.error);
        this.showNotification(`处理错误: ${data.error.message}`, 'error');
    }

    updateTaskItem(data) {
        const taskItem = this.taskList.querySelector(`[data-task-id="${data.taskId}"]`);
        if (taskItem) {
            taskItem.className = `task-item ${data.success ? 'success' : 'failed'}`;
            taskItem.querySelector('.task-status').textContent = data.success ? '✓' : '✗';
        }
    }

    updateButtonStates() {
        const status = this.processor.getStatus();
        
        const startBtn = this.container.querySelector('#batch-start');
        const pauseBtn = this.container.querySelector('#batch-pause');
        const resumeBtn = this.container.querySelector('#batch-resume');
        const stopBtn = this.container.querySelector('#batch-stop');
        
        startBtn.disabled = status.isProcessing;
        pauseBtn.disabled = !status.isProcessing || status.isPaused;
        resumeBtn.disabled = !status.isProcessing || !status.isPaused;
        stopBtn.disabled = !status.isProcessing;
    }

    updateTaskList() {
        const taskItems = this.taskList.querySelector('.task-items');
        taskItems.innerHTML = '';
        
        const tasks = this.processor.queue;
        tasks.forEach(task => {
            const taskElement = document.createElement('div');
            taskElement.className = `task-item ${task.status}`;
            taskElement.setAttribute('data-task-id', task.id);
            taskElement.innerHTML = `
                <div class="task-info">
                    <span class="task-name">${task.data.fileName || '任务'}</span>
                    <span class="task-type">${task.data.type}</span>
                </div>
                <div class="task-status">${this.getStatusIcon(task.status)}</div>
            `;
            taskItems.appendChild(taskElement);
        });
        
        this.container.querySelector('.task-count').textContent = `${tasks.length} 个任务`;
    }

    getStatusIcon(status) {
        switch (status) {
            case 'pending': return '○';
            case 'processing': return '⟳';
            case 'completed': return '✓';
            case 'failed': return '✗';
            default: return '?';
        }
    }

    generateSampleTasks(count) {
        const tasks = [];
        const types = ['rename', 'analyze', 'download'];
        
        for (let i = 0; i < count; i++) {
            const type = types[Math.floor(Math.random() * types.length)];
            tasks.push({
                type,
                fileName: `示例文件_${i + 1}.mp4`,
                prefix: `[重命名]_`,
                url: `https://example.com/media_${i + 1}.mp4`,
                destination: `/downloads/media_${i + 1}.mp4`
            });
        }
        
        return tasks;
    }

    setupDragAndDrop() {
        this.container.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.container.classList.add('drag-over');
        });
        
        this.container.addEventListener('dragleave', () => {
            this.container.classList.remove('drag-over');
        });
        
        this.container.addEventListener('drop', (e) => {
            e.preventDefault();
            this.container.classList.remove('drag-over');
            
            const files = Array.from(e.dataTransfer.files);
            this.handleDroppedFiles(files);
        });
    }

    handleDroppedFiles(files) {
        const tasks = files.map(file => ({
            type: 'analyze',
            fileName: file.name,
            file: file
        }));
        
        this.processor.addTasks(tasks);
        this.updateTaskList();
        this.showNotification(`添加了 ${files.length} 个文件到队列`);
    }

    showNotification(message, type = 'info') {
        // 简单的通知实现
        const notification = document.createElement('div');
        notification.className = `batch-notification ${type}`;
        notification.textContent = message;
        
        this.container.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// 导出模块
window.BatchProcessor = BatchProcessor;
window.BatchProcessorUI = BatchProcessorUI;