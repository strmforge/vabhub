/**
 * 微前端模块间通信服务
 * 提供模块联邦应用间的通信机制
 */

import { ref, reactive, watch, onUnmounted } from 'vue'

// 事件类型定义
export interface MicroFrontendEvent {
  type: string
  payload?: any
  source: string
  timestamp: number
}

// 事件监听器类型
export type EventListener = (event: MicroFrontendEvent) => void

// 微前端通信管理器
class MicroFrontendCommunication {
  private eventListeners: Map<string, EventListener[]> = new Map()
  private sharedState: Map<string, any> = new Map()
  private stateListeners: Map<string, Function[]> = new Map()
  
  // 应用标识
  private appId: string = 'vabhub-main'
  
  constructor() {
    // 监听来自其他应用的事件
    this.setupGlobalEventListener()
  }
  
  /**
   * 设置全局事件监听器
   */
  private setupGlobalEventListener() {
    if (typeof window !== 'undefined') {
      // 监听来自其他应用的消息
      window.addEventListener('microfrontend-event', (event: any) => {
        this.handleIncomingEvent(event.detail)
      })
    }
  }
  
  /**
   * 处理传入事件
   */
  private handleIncomingEvent(event: MicroFrontendEvent) {
    // 忽略来自自身的事件
    if (event.source === this.appId) return
    
    const listeners = this.eventListeners.get(event.type) || []
    listeners.forEach(listener => {
      try {
        listener(event)
      } catch (error) {
        console.error(`Error handling microfrontend event ${event.type}:`, error)
      }
    })
  }
  
  /**
   * 发送事件到其他应用
   */
  sendEvent(type: string, payload?: any) {
    const event: MicroFrontendEvent = {
      type,
      payload,
      source: this.appId,
      timestamp: Date.now()
    }
    
    // 发送到全局事件系统
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('microfrontend-event', {
        detail: event
      }))
    }
    
    // 同时触发本地监听器
    this.triggerLocalEvent(event)
  }
  
  /**
   * 触发本地事件
   */
  private triggerLocalEvent(event: MicroFrontendEvent) {
    const listeners = this.eventListeners.get(event.type) || []
    listeners.forEach(listener => {
      try {
        listener(event)
      } catch (error) {
        console.error(`Error handling local event ${event.type}:`, error)
      }
    })
  }
  
  /**
   * 监听事件
   */
  onEvent(type: string, listener: EventListener) {
    if (!this.eventListeners.has(type)) {
      this.eventListeners.set(type, [])
    }
    this.eventListeners.get(type)!.push(listener)
    
    // 返回取消监听函数
    return () => {
      this.offEvent(type, listener)
    }
  }
  
  /**
   * 取消事件监听
   */
  offEvent(type: string, listener: EventListener) {
    const listeners = this.eventListeners.get(type)
    if (listeners) {
      const index = listeners.indexOf(listener)
      if (index > -1) {
        listeners.splice(index, 1)
      }
    }
  }
  
  /**
   * 设置共享状态
   */
  setSharedState(key: string, value: any) {
    this.sharedState.set(key, value)
    this.notifyStateChange(key, value)
  }
  
  /**
   * 获取共享状态
   */
  getSharedState(key: string) {
    return this.sharedState.get(key)
  }
  
  /**
   * 监听共享状态变化
   */
  watchSharedState(key: string, callback: (value: any) => void) {
    if (!this.stateListeners.has(key)) {
      this.stateListeners.set(key, [])
    }
    this.stateListeners.get(key)!.push(callback)
    
    // 返回取消监听函数
    return () => {
      this.unwatchSharedState(key, callback)
    }
  }
  
  /**
   * 取消共享状态监听
   */
  unwatchSharedState(key: string, callback: Function) {
    const listeners = this.stateListeners.get(key)
    if (listeners) {
      const index = listeners.indexOf(callback)
      if (index > -1) {
        listeners.splice(index, 1)
      }
    }
  }
  
  /**
   * 通知状态变化
   */
  private notifyStateChange(key: string, value: any) {
    const listeners = this.stateListeners.get(key) || []
    listeners.forEach(listener => {
      try {
        listener(value)
      } catch (error) {
        console.error(`Error notifying state change for ${key}:`, error)
      }
    })
  }
  
  /**
   * 远程调用其他应用的方法
   */
  async remoteCall(appName: string, method: string, ...args: any[]): Promise<any> {
    const callId = this.generateCallId()
    
    return new Promise((resolve, reject) => {
      // 设置超时
      const timeout = setTimeout(() => {
        reject(new Error(`Remote call timeout: ${appName}.${method}`))
        this.offEvent(`remote-response-${callId}`, responseHandler)
      }, 10000) // 10秒超时
      
      // 响应处理器
      const responseHandler = (event: MicroFrontendEvent) => {
        clearTimeout(timeout)
        this.offEvent(`remote-response-${callId}`, responseHandler)
        
        if (event.payload.error) {
          reject(new Error(event.payload.error))
        } else {
          resolve(event.payload.result)
        }
      }
      
      // 监听响应
      this.onEvent(`remote-response-${callId}`, responseHandler)
      
      // 发送调用请求
      this.sendEvent('remote-call', {
        appName,
        method,
        args,
        callId
      })
    })
  }
  
  /**
   * 处理远程调用请求
   */
  handleRemoteCall(callback: (appName: string, method: string, args: any[]) => Promise<any>) {
    return this.onEvent('remote-call', async (event) => {
      const { appName, method, args, callId } = event.payload
      
      try {
        const result = await callback(appName, method, args)
        
        // 发送响应
        this.sendEvent(`remote-response-${callId}`, {
          result,
          callId
        })
      } catch (error) {
        // 发送错误响应
        this.sendEvent(`remote-response-${callId}`, {
          error: error instanceof Error ? error.message : 'Unknown error',
          callId
        })
      }
    })
  }
  
  /**
   * 生成调用ID
   */
  private generateCallId(): string {
    return `${this.appId}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  }
  
  /**
   * 销毁通信实例
   */
  destroy() {
    this.eventListeners.clear()
    this.sharedState.clear()
    this.stateListeners.clear()
    
    if (typeof window !== 'undefined') {
      window.removeEventListener('microfrontend-event', this.handleIncomingEvent as any)
    }
  }
}

// 创建全局通信实例
const microfrontendComm = new MicroFrontendCommunication()

// Vue Composition API 封装

export function useMicroFrontendCommunication() {
  // 响应式共享状态
  const sharedStates = reactive(new Map())
  
  // 监听共享状态变化
  const watchSharedState = (key: string, callback: (value: any) => void) => {
    return microfrontendComm.watchSharedState(key, (value) => {
      sharedStates.set(key, value)
      callback(value)
    })
  }
  
  // 响应式共享状态引用
  const useSharedState = (key: string, defaultValue?: any) => {
    const state = ref(defaultValue)
    
    // 初始值
    const initialValue = microfrontendComm.getSharedState(key)
    if (initialValue !== undefined) {
      state.value = initialValue
    }
    
    // 监听变化
    const unwatch = microfrontendComm.watchSharedState(key, (value) => {
      state.value = value
    })
    
    // 组件卸载时取消监听
    onUnmounted(() => {
      unwatch()
    })
    
    // 设置状态的方法
    const setState = (value: any) => {
      microfrontendComm.setSharedState(key, value)
    }
    
    return {
      state,
      setState
    }
  }
  
  // 事件监听
  const useEvent = (type: string, listener: EventListener) => {
    const unwatch = microfrontendComm.onEvent(type, listener)
    
    // 组件卸载时取消监听
    onUnmounted(() => {
      unwatch()
    })
    
    return unwatch
  }
  
  return {
    // 原始通信实例
    comm: microfrontendComm,
    
    // 响应式工具
    useSharedState,
    useEvent,
    watchSharedState,
    
    // 直接方法
    sendEvent: microfrontendComm.sendEvent.bind(microfrontendComm),
    onEvent: microfrontendComm.onEvent.bind(microfrontendComm),
    setSharedState: microfrontendComm.setSharedState.bind(microfrontendComm),
    getSharedState: microfrontendComm.getSharedState.bind(microfrontendComm),
    remoteCall: microfrontendComm.remoteCall.bind(microfrontendComm),
    handleRemoteCall: microfrontendComm.handleRemoteCall.bind(microfrontendComm)
  }
}

// 导出默认实例
export default microfrontendComm

// 预定义事件类型
export const MicroFrontendEvents = {
  // 用户相关
  USER_LOGIN: 'user-login',
  USER_LOGOUT: 'user-logout',
  USER_PROFILE_UPDATE: 'user-profile-update',
  
  // 主题相关
  THEME_CHANGE: 'theme-change',
  LANGUAGE_CHANGE: 'language-change',
  
  // 数据相关
  DATA_REFRESH: 'data-refresh',
  DATA_UPDATE: 'data-update',
  
  // 导航相关
  NAVIGATION_CHANGE: 'navigation-change',
  MODULE_LOADED: 'module-loaded',
  
  // 远程调用
  REMOTE_CALL: 'remote-call',
  REMOTE_CALL_RESPONSE: 'remote-call-response'
}