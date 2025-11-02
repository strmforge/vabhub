import { useAppStore } from '@/stores/app'

// WebSocket服务类
export class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectInterval = 3000
  private url: string
  private messageHandlers: Map<string, Function[]> = new Map()

  constructor(url: string) {
    this.url = url
    this.connect()
  }

  // 连接WebSocket
  connect() {
    try {
      this.ws = new WebSocket(this.url)
      
      this.ws.onopen = () => {
        console.log('WebSocket连接成功')
        this.reconnectAttempts = 0
        this.onConnected()
      }

      this.ws.onmessage = (event) => {
        this.handleMessage(event)
      }

      this.ws.onclose = (event) => {
        console.log('WebSocket连接关闭:', event.code, event.reason)
        this.onDisconnected()
        this.attemptReconnect()
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket错误:', error)
        this.onError(error)
      }
    } catch (error) {
      console.error('WebSocket连接失败:', error)
      this.attemptReconnect()
    }
  }

  // 处理消息
  private handleMessage(event: MessageEvent) {
    try {
      const data = JSON.parse(event.data)
      const { type, payload } = data
      
      // 调用对应的消息处理器
      const handlers = this.messageHandlers.get(type) || []
      handlers.forEach(handler => handler(payload))
      
      // 默认的消息处理
      this.handleDefaultMessage(type, payload)
    } catch (error) {
      console.error('消息处理错误:', error)
    }
  }

  // 默认消息处理
  private handleDefaultMessage(type: string, payload: any) {
    const appStore = useAppStore()
    
    switch (type) {
      case 'notification':
        appStore.addNotification({
          type: payload.level || 'info',
          title: payload.title || '系统通知',
          message: payload.message,
          duration: payload.duration || 5000
        })
        break
        
      case 'system_status':
        // 更新系统状态
        break
        
      case 'download_progress':
        // 下载进度更新
        break
        
      case 'plugin_update':
        // 插件更新通知
        break
        
      default:
        console.log('未知消息类型:', type, payload)
    }
  }

  // 发送消息
  send(type: string, payload?: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload }))
      return true
    }
    return false
  }

  // 订阅消息
  subscribe(type: string, handler: Function) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, [])
    }
    this.messageHandlers.get(type)!.push(handler)
    
    // 返回取消订阅的函数
    return () => {
      const handlers = this.messageHandlers.get(type) || []
      const index = handlers.indexOf(handler)
      if (index > -1) {
        handlers.splice(index, 1)
      }
    }
  }

  // 尝试重连
  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`尝试重连... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      
      setTimeout(() => {
        this.connect()
      }, this.reconnectInterval)
    } else {
      console.error('WebSocket重连失败，已达到最大重连次数')
    }
  }

  // 连接成功回调
  private onConnected() {
    console.log('WebSocket连接已建立')
    // 发送认证消息（如果需要）
    // this.send('auth', { token: localStorage.getItem('token') })
  }

  // 连接断开回调
  private onDisconnected() {
    console.log('WebSocket连接已断开')
  }

  // 错误处理回调
  private onError(error: any) {
    console.error('WebSocket错误:', error)
  }

  // 关闭连接
  close() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  // 获取连接状态
  getStatus() {
    if (!this.ws) return 'disconnected'
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING:
        return 'connecting'
      case WebSocket.OPEN:
        return 'connected'
      case WebSocket.CLOSING:
        return 'closing'
      case WebSocket.CLOSED:
        return 'disconnected'
      default:
        return 'unknown'
    }
  }
}

// 创建全局WebSocket实例
const wsUrl = import.meta.env.VITE_WS_URL || `ws://${window.location.host}/ws`
export const wsService = new WebSocketService(wsUrl)

export default WebSocketService