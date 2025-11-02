/**
 * 后台任务管理器
 * 管理后台运行的定时任务，优化性能，在页面不可见时自动暂停任务
 */

class BackgroundManager {
  constructor() {
    this.timers = new Map()
    this.isVisible = true
    
    // 监听页面可见性变化
    this.setupVisibilityListener()
  }

  /**
   * 设置页面可见性监听器
   */
  setupVisibilityListener() {
    if (typeof document !== 'undefined') {
      document.addEventListener('visibilitychange', () => {
        this.isVisible = !document.hidden
        this.handleVisibilityChange()
      })
    }
  }

  /**
   * 处理页面可见性变化
   */
  handleVisibilityChange() {
    if (this.isVisible) {
      // 页面变为可见，恢复所有定时器
      this.resumeAllTimers()
    } else {
      // 页面变为不可见，暂停所有定时器
      this.pauseAllTimers()
    }
  }

  /**
   * 添加后台定时器
   * @param {string} id 定时器标识
   * @param {Function} callback 回调函数
   * @param {number} interval 执行间隔（毫秒）
   * @param {Object} options 配置选项
   * @param {boolean} options.runInBackground 是否在后台运行
   * @param {boolean} options.skipInitialRun 是否跳过首次立即执行
   */
  addBackgroundTimer(id, callback, interval, options = {}) {
    const {
      runInBackground = true,
      skipInitialRun = false
    } = options

    // 清除已存在的定时器
    this.removeBackgroundTimer(id)

    let timerId = null
    let isPaused = false

    const executeCallback = () => {
      if (isPaused) return
      
      try {
        callback()
      } catch (error) {
        console.warn(`后台定时器 ${id} 执行失败:`, error)
      }
    }

    const startTimer = () => {
      if (!skipInitialRun) {
        executeCallback()
      }
      
      timerId = setInterval(executeCallback, interval)
    }

    const timer = {
      id,
      callback,
      interval,
      runInBackground,
      timerId,
      isPaused,
      startTimer,
      stopTimer: () => {
        if (timerId) {
          clearInterval(timerId)
          timerId = null
        }
      },
      pause: () => {
        isPaused = true
        this.stopTimer()
      },
      resume: () => {
        isPaused = false
        startTimer()
      }
    }

    this.timers.set(id, timer)

    // 根据当前可见性状态决定是否启动
    if (this.isVisible || runInBackground) {
      startTimer()
    }

    return timer
  }

  /**
   * 移除后台定时器
   * @param {string} id 定时器标识
   */
  removeBackgroundTimer(id) {
    const timer = this.timers.get(id)
    if (timer) {
      timer.stopTimer()
      this.timers.delete(id)
    }
  }

  /**
   * 暂停所有定时器
   */
  pauseAllTimers() {
    for (const timer of this.timers.values()) {
      if (!timer.runInBackground) {
        timer.pause()
      }
    }
  }

  /**
   * 恢复所有定时器
   */
  resumeAllTimers() {
    for (const timer of this.timers.values()) {
      if (!timer.runInBackground || this.isVisible) {
        timer.resume()
      }
    }
  }

  /**
   * 获取定时器状态
   * @param {string} id 定时器标识
   * @returns {Object|null} 定时器状态
   */
  getTimerStatus(id) {
    const timer = this.timers.get(id)
    if (!timer) return null

    return {
      id: timer.id,
      isRunning: !!timer.timerId,
      isPaused: timer.isPaused,
      runInBackground: timer.runInBackground,
      interval: timer.interval
    }
  }

  /**
   * 获取所有定时器状态
   * @returns {Array} 所有定时器状态
   */
  getAllTimerStatus() {
    return Array.from(this.timers.values()).map(timer => this.getTimerStatus(timer.id))
  }

  /**
   * 清空所有定时器
   */
  clearAllTimers() {
    for (const timer of this.timers.values()) {
      timer.stopTimer()
    }
    this.timers.clear()
  }
}

// 创建全局实例
const backgroundManager = new BackgroundManager()

// 导出便捷函数
export function addBackgroundTimer(id, callback, interval, options) {
  return backgroundManager.addBackgroundTimer(id, callback, interval, options)
}

export function removeBackgroundTimer(id) {
  return backgroundManager.removeBackgroundTimer(id)
}

export function getBackgroundTimerStatus(id) {
  return backgroundManager.getTimerStatus(id)
}

export function getAllBackgroundTimerStatus() {
  return backgroundManager.getAllTimerStatus()
}

export function clearAllBackgroundTimers() {
  return backgroundManager.clearAllTimers()
}

export default backgroundManager