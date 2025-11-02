/**
 * 徽章管理工具
 * 处理未读消息徽章显示和更新
 */

/**
 * 检查并发送未读消息数量
 * 用于更新页面标题或显示徽章
 */
export function checkAndEmitUnreadMessages() {
  try {
    // 获取未读消息数量
    const unreadCount = getUnreadMessageCount()
    
    // 更新页面标题徽章
    updatePageTitleBadge(unreadCount)
    
    // 发送自定义事件通知其他组件
    emitUnreadMessageEvent(unreadCount)
    
    console.log(`未读消息检查完成: ${unreadCount} 条未读消息`)
  } catch (error) {
    console.warn('检查未读消息时出错:', error)
  }
}

/**
 * 获取未读消息数量
 * @returns {number} 未读消息数量
 */
function getUnreadMessageCount() {
  try {
    // 从本地存储获取未读消息数量
    const storedCount = localStorage.getItem('unread_message_count')
    
    if (storedCount) {
      const count = parseInt(storedCount, 10)
      return isNaN(count) ? 0 : Math.max(0, count)
    }
    
    // 如果没有存储数据，默认为0
    return 0
  } catch (error) {
    console.warn('获取未读消息数量失败:', error)
    return 0
  }
}

/**
 * 更新页面标题徽章
 * @param {number} count 未读消息数量
 */
function updatePageTitleBadge(count) {
  try {
    const originalTitle = document.title.replace(/^\(\d+\)\s*/, '')
    
    if (count > 0) {
      document.title = `(${count}) ${originalTitle}`
    } else {
      document.title = originalTitle
    }
  } catch (error) {
    console.warn('更新页面标题徽章失败:', error)
  }
}

/**
 * 发送未读消息事件
 * @param {number} count 未读消息数量
 */
function emitUnreadMessageEvent(count) {
  try {
    const event = new CustomEvent('unreadMessagesUpdated', {
      detail: { count }
    })
    window.dispatchEvent(event)
  } catch (error) {
    console.warn('发送未读消息事件失败:', error)
  }
}

/**
 * 设置未读消息数量
 * @param {number} count 未读消息数量
 */
export function setUnreadMessageCount(count) {
  try {
    const validCount = Math.max(0, parseInt(count, 10) || 0)
    
    // 存储到本地存储
    localStorage.setItem('unread_message_count', validCount.toString())
    
    // 立即更新徽章显示
    checkAndEmitUnreadMessages()
    
    return validCount
  } catch (error) {
    console.warn('设置未读消息数量失败:', error)
    return 0
  }
}

/**
 * 增加未读消息数量
 * @param {number} increment 增加的数量，默认为1
 */
export function incrementUnreadMessageCount(increment = 1) {
  try {
    const currentCount = getUnreadMessageCount()
    const newCount = Math.max(0, currentCount + (parseInt(increment, 10) || 1))
    
    return setUnreadMessageCount(newCount)
  } catch (error) {
    console.warn('增加未读消息数量失败:', error)
    return getUnreadMessageCount()
  }
}

/**
 * 减少未读消息数量
 * @param {number} decrement 减少的数量，默认为1
 */
export function decrementUnreadMessageCount(decrement = 1) {
  try {
    const currentCount = getUnreadMessageCount()
    const newCount = Math.max(0, currentCount - (parseInt(decrement, 10) || 1))
    
    return setUnreadMessageCount(newCount)
  } catch (error) {
    console.warn('减少未读消息数量失败:', error)
    return getUnreadMessageCount()
  }
}

/**
 * 清空未读消息数量
 */
export function clearUnreadMessageCount() {
  return setUnreadMessageCount(0)
}

/**
 * 获取当前未读消息数量
 * @returns {number} 当前未读消息数量
 */
export function getCurrentUnreadCount() {
  return getUnreadMessageCount()
}

/**
 * 监听未读消息变化
 * @param {Function} callback 回调函数
 * @returns {Function} 取消监听函数
 */
export function onUnreadMessagesChange(callback) {
  const handler = (event) => {
    if (callback && typeof callback === 'function') {
      callback(event.detail.count)
    }
  }
  
  window.addEventListener('unreadMessagesUpdated', handler)
  
  // 返回取消监听函数
  return () => {
    window.removeEventListener('unreadMessagesUpdated', handler)
  }
}