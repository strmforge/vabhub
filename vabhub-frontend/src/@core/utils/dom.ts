/**
 * DOM 工具函数
 */

/**
 * 确保渲染完成的工具函数
 * @param callback 渲染完成后的回调函数
 */
export function ensureRenderComplete(callback: () => void): void {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', callback)
  } else {
    // 使用 setTimeout 确保在下一个事件循环中执行
    setTimeout(callback, 0)
  }
}

/**
 * 移除 DOM 元素的工具函数
 * @param selector 选择器或 DOM 元素
 */
export function removeEl(selector: string | Element): void {
  let element: Element | null
  
  if (typeof selector === 'string') {
    element = document.querySelector(selector)
  } else {
    element = selector
  }
  
  if (element && element.parentNode) {
    element.parentNode.removeChild(element)
  }
}

/**
 * 检查元素是否存在
 * @param selector 选择器
 */
export function elementExists(selector: string): boolean {
  return !!document.querySelector(selector)
}

/**
 * 添加 CSS 类
 * @param selector 选择器
 * @param className CSS 类名
 */
export function addClass(selector: string, className: string): void {
  const element = document.querySelector(selector)
  if (element) {
    element.classList.add(className)
  }
}

/**
 * 移除 CSS 类
 * @param selector 选择器
 * @param className CSS 类名
 */
export function removeClass(selector: string, className: string): void {
  const element = document.querySelector(selector)
  if (element) {
    element.classList.remove(className)
  }
}

/**
 * 切换 CSS 类
 * @param selector 选择器
 * @param className CSS 类名
 */
export function toggleClass(selector: string, className: string): void {
  const element = document.querySelector(selector)
  if (element) {
    element.classList.toggle(className)
  }
}