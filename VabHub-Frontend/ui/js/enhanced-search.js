/**
 * v4.2 智能搜索增强模块
 * 实现语义搜索、智能推荐和搜索历史功能
 */

class EnhancedSearchEngine {
    constructor() {
        this.searchHistory = this.loadSearchHistory();
        this.searchIndex = new Map();
        this.isIndexing = false;
        this.searchTimeout = null;
        
        // 初始化搜索索引
        this.initSearchIndex();
    }

    /**
     * 初始化搜索索引
     */
    async initSearchIndex() {
        try {
            this.isIndexing = true;
            
            // 从API获取媒体数据并构建索引
            const mediaData = await this.fetchMediaData();
            this.buildSearchIndex(mediaData);
            
            console.log('搜索索引初始化完成，索引数量:', this.searchIndex.size);
        } catch (error) {
            console.error('搜索索引初始化失败:', error);
        } finally {
            this.isIndexing = false;
        }
    }

    /**
     * 获取媒体数据
     */
    async fetchMediaData() {
        try {
            const response = await fetch('/api/media/list');
            if (!response.ok) throw new Error('获取媒体数据失败');
            return await response.json();
        } catch (error) {
            // 返回模拟数据用于演示
            return this.getMockMediaData();
        }
    }

    /**
     * 构建搜索索引
     */
    buildSearchIndex(mediaData) {
        this.searchIndex.clear();
        
        mediaData.forEach(item => {
            // 索引标题
            this.addToIndex(item.title, item);
            
            // 索引别名
            if (item.aliases) {
                item.aliases.forEach(alias => this.addToIndex(alias, item));
            }
            
            // 索引演员
            if (item.cast) {
                item.cast.forEach(actor => this.addToIndex(actor, item));
            }
            
            // 索引导演
            if (item.director) {
                this.addToIndex(item.director, item);
            }
        });
    }

    /**
     * 添加项目到索引
     */
    addToIndex(keyword, item) {
        const normalized = this.normalizeText(keyword);
        if (!this.searchIndex.has(normalized)) {
            this.searchIndex.set(normalized, []);
        }
        this.searchIndex.get(normalized).push(item);
    }

    /**
     * 文本标准化
     */
    normalizeText(text) {
        return text.toLowerCase().replace(/[^\w\u4e00-\u9fa5]/g, '');
    }

    /**
     * 执行智能搜索
     */
    async search(query, options = {}) {
        if (!query.trim()) return [];
        
        // 保存搜索历史
        this.saveToHistory(query);
        
        // 等待索引完成
        if (this.isIndexing) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        const normalizedQuery = this.normalizeText(query);
        const results = new Set();
        
        // 精确匹配
        if (this.searchIndex.has(normalizedQuery)) {
            this.searchIndex.get(normalizedQuery).forEach(item => results.add(item));
        }
        
        // 模糊匹配
        for (const [keyword, items] of this.searchIndex) {
            if (keyword.includes(normalizedQuery) || normalizedQuery.includes(keyword)) {
                items.forEach(item => results.add(item));
            }
        }
        
        // 语义相似度匹配
        const semanticResults = await this.semanticSearch(query);
        semanticResults.forEach(item => results.add(item));
        
        return Array.from(results).slice(0, options.limit || 20);
    }

    /**
     * 语义搜索
     */
    async semanticSearch(query) {
        try {
            // 模拟语义搜索API调用
            const response = await fetch('/api/search/semantic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.warn('语义搜索不可用，使用本地算法:', error);
        }
        
        // 本地语义搜索算法
        return this.localSemanticSearch(query);
    }

    /**
     * 本地语义搜索算法
     */
    localSemanticSearch(query) {
        const results = [];
        const queryWords = query.toLowerCase().split(/\s+/);
        
        for (const [keyword, items] of this.searchIndex) {
            let score = 0;
            
            queryWords.forEach(word => {
                if (keyword.includes(word)) {
                    score += word.length;
                }
            });
            
            if (score > 0) {
                items.forEach(item => {
                    results.push({ ...item, relevance: score });
                });
            }
        }
        
        return results.sort((a, b) => b.relevance - a.relevance).slice(0, 10);
    }

    /**
     * 获取搜索建议
     */
    getSuggestions(query) {
        if (!query.trim()) return this.getPopularSearches();
        
        const suggestions = new Set();
        const normalizedQuery = this.normalizeText(query);
        
        // 从搜索历史中获取建议
        this.searchHistory.forEach(history => {
            if (history.toLowerCase().includes(normalizedQuery)) {
                suggestions.add(history);
            }
        });
        
        // 从索引中获取建议
        for (const keyword of this.searchIndex.keys()) {
            if (keyword.includes(normalizedQuery)) {
                suggestions.add(keyword);
            }
        }
        
        return Array.from(suggestions).slice(0, 5);
    }

    /**
     * 获取热门搜索
     */
    getPopularSearches() {
        return [
            '复仇者联盟',
            '权力的游戏',
            '星际穿越',
            '黑镜',
            '西部世界'
        ];
    }

    /**
     * 保存搜索历史
     */
    saveToHistory(query) {
        if (!query.trim()) return;
        
        // 移除重复项
        this.searchHistory = this.searchHistory.filter(item => item !== query);
        
        // 添加到历史记录开头
        this.searchHistory.unshift(query);
        
        // 限制历史记录数量
        if (this.searchHistory.length > 50) {
            this.searchHistory = this.searchHistory.slice(0, 50);
        }
        
        this.saveSearchHistory();
    }

    /**
     * 加载搜索历史
     */
    loadSearchHistory() {
        try {
            const history = localStorage.getItem('searchHistory');
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('加载搜索历史失败:', error);
            return [];
        }
    }

    /**
     * 保存搜索历史
     */
    saveSearchHistory() {
        try {
            localStorage.setItem('searchHistory', JSON.stringify(this.searchHistory));
        } catch (error) {
            console.error('保存搜索历史失败:', error);
        }
    }

    /**
     * 获取模拟媒体数据
     */
    getMockMediaData() {
        return [
            {
                id: 1,
                title: '复仇者联盟：终局之战',
                type: 'movie',
                year: 2019,
                rating: 8.4,
                poster: '/api/media/poster/avengers-endgame.jpg',
                aliases: ['Avengers: Endgame', '复仇者联盟4'],
                cast: ['小罗伯特·唐尼', '克里斯·埃文斯', '斯嘉丽·约翰逊'],
                director: '安东尼·罗素'
            },
            {
                id: 2,
                title: '权力的游戏',
                type: 'tv',
                year: 2011,
                rating: 9.3,
                poster: '/api/media/poster/game-of-thrones.jpg',
                aliases: ['Game of Thrones', '冰与火之歌'],
                cast: ['艾米莉亚·克拉克', '基特·哈灵顿', '彼特·丁拉基'],
                director: '大卫·贝尼奥夫'
            }
        ];
    }
}

/**
 * 智能搜索UI组件
 */
class EnhancedSearchUI {
    constructor() {
        this.engine = new EnhancedSearchEngine();
        this.searchInput = null;
        this.suggestionsContainer = null;
        this.resultsContainer = null;
        this.isOpen = false;
        
        this.init();
    }

    init() {
        this.createUI();
        this.bindEvents();
    }

    createUI() {
        // 创建搜索建议容器
        this.suggestionsContainer = document.createElement('div');
        this.suggestionsContainer.className = 'search-suggestions';
        
        // 创建搜索结果容器
        this.resultsContainer = document.createElement('div');
        this.resultsContainer.className = 'search-results-enhanced';
        
        // 获取搜索输入框
        this.searchInput = document.querySelector('.search-input');
        
        if (this.searchInput) {
            this.searchInput.parentNode.appendChild(this.suggestionsContainer);
            this.searchInput.parentNode.appendChild(this.resultsContainer);
        }
    }

    bindEvents() {
        if (!this.searchInput) return;
        
        this.searchInput.addEventListener('input', this.debounce(this.handleInput.bind(this), 300));
        this.searchInput.addEventListener('focus', this.handleFocus.bind(this));
        this.searchInput.addEventListener('blur', this.handleBlur.bind(this));
        
        // 键盘事件
        this.searchInput.addEventListener('keydown', this.handleKeydown.bind(this));
    }

    handleInput(event) {
        const query = event.target.value.trim();
        
        if (query) {
            this.showSuggestions(query);
        } else {
            this.hideSuggestions();
            this.hideResults();
        }
    }

    async handleFocus() {
        this.isOpen = true;
        this.showSuggestions('');
    }

    handleBlur() {
        setTimeout(() => {
            this.isOpen = false;
            this.hideSuggestions();
            this.hideResults();
        }, 200);
    }

    async showSuggestions(query) {
        const suggestions = this.engine.getSuggestions(query);
        
        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        const suggestionsHTML = suggestions.map(suggestion => `
            <div class="suggestion-item" data-suggestion="${suggestion}">
                <i class="fas fa-search"></i>
                <span>${suggestion}</span>
            </div>
        `).join('');
        
        this.suggestionsContainer.innerHTML = suggestionsHTML;
        this.suggestionsContainer.style.display = 'block';
        
        // 绑定建议项点击事件
        this.bindSuggestionEvents();
    }

    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
    }

    async performSearch(query) {
        try {
            const results = await this.engine.search(query);
            this.displayResults(results);
        } catch (error) {
            console.error('搜索失败:', error);
            this.showError('搜索失败，请重试');
        }
    }

    displayResults(results) {
        if (results.length === 0) {
            this.resultsContainer.innerHTML = '<div class="no-results">未找到相关结果</div>';
            this.resultsContainer.style.display = 'block';
            return;
        }
        
        const resultsHTML = results.map(result => `
            <div class="search-result-item" data-id="${result.id}">
                <div class="result-poster">
                    <img src="${result.poster}" alt="${result.title}" onerror="this.src='/api/media/placeholder.jpg'">
                </div>
                <div class="result-content">
                    <div class="result-title">${result.title}</div>
                    <div class="result-meta">
                        <span class="result-type">${result.type === 'movie' ? '电影' : '电视剧'}</span>
                        <span class="result-year">${result.year}</span>
                        <span class="result-rating">⭐ ${result.rating}</span>
                    </div>
                    <div class="result-cast">主演: ${result.cast ? result.cast.slice(0, 3).join(', ') : '未知'}</div>
                </div>
            </div>
        `).join('');
        
        this.resultsContainer.innerHTML = resultsHTML;
        this.resultsContainer.style.display = 'block';
    }

    hideResults() {
        this.resultsContainer.style.display = 'none';
    }

    bindSuggestionEvents() {
        const suggestionItems = this.suggestionsContainer.querySelectorAll('.suggestion-item');
        
        suggestionItems.forEach(item => {
            item.addEventListener('click', () => {
                const suggestion = item.getAttribute('data-suggestion');
                this.searchInput.value = suggestion;
                this.performSearch(suggestion);
                this.hideSuggestions();
            });
        });
    }

    handleKeydown(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            this.performSearch(this.searchInput.value);
            this.hideSuggestions();
        } else if (event.key === 'Escape') {
            this.hideSuggestions();
            this.hideResults();
        }
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

    showError(message) {
        this.resultsContainer.innerHTML = `<div class="search-error">${message}</div>`;
        this.resultsContainer.style.display = 'block';
    }
}

// 导出模块
window.EnhancedSearchEngine = EnhancedSearchEngine;
window.EnhancedSearchUI = EnhancedSearchUI;