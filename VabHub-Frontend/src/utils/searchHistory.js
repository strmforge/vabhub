// 搜索历史管理工具
class SearchHistoryManager {
    constructor() {
        this.storageKey = 'vabhub_search_history'
        this.maxHistoryItems = 100
        this.history = this.loadHistory()
    }

    // 加载搜索历史
    loadHistory() {
        try {
            const stored = localStorage.getItem(this.storageKey)
            if (stored) {
                return JSON.parse(stored)
            }
        } catch (error) {
            console.error('加载搜索历史失败:', error)
        }
        return []
    }

    // 保存搜索历史
    saveHistory() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.history))
        } catch (error) {
            console.error('保存搜索历史失败:', error)
        }
    }

    // 添加搜索记录
    addSearch(query, searchMode = 'combined', contentType = 'all', sources = []) {
        const searchRecord = {
            id: this.generateId(),
            query: query.trim(),
            searchMode,
            contentType,
            sources,
            timestamp: new Date().toISOString(),
            resultCount: 0
        }

        // 移除重复的搜索记录
        this.history = this.history.filter(
            record => record.query.toLowerCase() !== query.toLowerCase()
        )

        // 添加到历史记录开头
        this.history.unshift(searchRecord)

        // 限制历史记录数量
        if (this.history.length > this.maxHistoryItems) {
            this.history = this.history.slice(0, this.maxHistoryItems)
        }

        this.saveHistory()
        return searchRecord
    }

    // 更新搜索结果数量
    updateResultCount(searchId, resultCount) {
        const record = this.history.find(item => item.id === searchId)
        if (record) {
            record.resultCount = resultCount
            this.saveHistory()
        }
    }

    // 获取搜索历史
    getHistory(limit = 20, offset = 0) {
        return this.history.slice(offset, offset + limit)
    }

    // 获取热门搜索（基于搜索频率）
    getPopularSearches(limit = 10) {
        const frequencyMap = {}
        
        this.history.forEach(record => {
            if (frequencyMap[record.query]) {
                frequencyMap[record.query]++
            } else {
                frequencyMap[record.query] = 1
            }
        })

        return Object.entries(frequencyMap)
            .sort(([, a], [, b]) => b - a)
            .slice(0, limit)
            .map(([query, count]) => ({ query, count }))
    }

    // 搜索建议
    getSuggestions(query, limit = 10) {
        if (!query.trim()) {
            return this.getHistory(limit).map(record => record.query)
        }

        const suggestions = []
        const queryLower = query.toLowerCase()

        // 从历史记录中匹配
        this.history.forEach(record => {
            if (record.query.toLowerCase().includes(queryLower)) {
                suggestions.push(record.query)
            }
        })

        // 去重并限制数量
        return [...new Set(suggestions)].slice(0, limit)
    }

    // 删除搜索记录
    deleteSearch(searchId) {
        this.history = this.history.filter(record => record.id !== searchId)
        this.saveHistory()
    }

    // 清空搜索历史
    clearHistory() {
        this.history = []
        this.saveHistory()
    }

    // 生成唯一ID
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2)
    }

    // 获取搜索统计
    getSearchStats() {
        const totalSearches = this.history.length
        const uniqueQueries = new Set(this.history.map(record => record.query)).size
        const today = new Date().toISOString().split('T')[0]
        const todaySearches = this.history.filter(
            record => record.timestamp.startsWith(today)
        ).length

        return {
            totalSearches,
            uniqueQueries,
            todaySearches
        }
    }
}

// 创建全局实例
export const searchHistoryManager = new SearchHistoryManager()

export default SearchHistoryManager