/**
 * 全局加载状态管理器
 * 管理应用各个组件的加载状态，确保所有关键资源加载完成后再移除加载界面
 */

class LoadingStateManager {
  constructor() {
    this.states = new Map()
    this.completionCallbacks = []
  }

  /**
   * 设置加载状态
   * @param {string} key 状态标识
   * @param {boolean} loading 是否正在加载
   */
  setLoadingState(key, loading) {
    this.states.set(key, loading)
    this.checkCompletion()
  }

  /**
   * 获取加载状态
   * @param {string} key 状态标识
   * @returns {boolean} 是否正在加载
   */
  getLoadingState(key) {
    return this.states.get(key) || false
  }

  /**
   * 检查所有加载是否完成
   * @returns {boolean} 是否所有加载都已完成
   */
  isAllComplete() {
    for (const loading of this.states.values()) {
      if (loading) {
        return false
      }
    }
    return true
  }

  /**
   * 检查完成状态并触发回调
   */
  checkCompletion() {
    if (this.isAllComplete()) {
      this.completionCallbacks.forEach(callback => {
        try {
          callback()
        } catch (error) {
          console.warn('加载完成回调执行失败:', error)
        }
      })
      this.completionCallbacks = []
    }
  }

  /**
   * 等待所有加载完成
   * @returns {Promise<void>}
   */
  waitForAllComplete() {
    return new Promise((resolve) => {
      if (this.isAllComplete()) {
        resolve()
      } else {
        this.completionCallbacks.push(resolve)
      }
    })
  }

  /**
   * 重置所有状态
   */
  reset() {
    this.states.clear()
    this.completionCallbacks = []
  }

  /**
   * 获取当前加载状态统计
   * @returns {Object} 加载状态统计
   */
  getStats() {
    const total = this.states.size
    const loading = Array.from(this.states.values()).filter(Boolean).length
    const completed = total - loading

    return {
      total,
      loading,
      completed,
      allComplete: loading === 0 && total > 0
    }
  }
}

// 创建全局实例
export const globalLoadingStateManager = new LoadingStateManager()

export default globalLoadingStateManager