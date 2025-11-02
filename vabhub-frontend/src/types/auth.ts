// 用户信息接口
export interface UserInfo {
  id: number
  username: string
  email: string
  avatar?: string
  role: 'admin' | 'user'
  createdAt: string
  updatedAt: string
}

// 登录请求参数
export interface LoginRequest {
  username: string
  password: string
}

// 登录响应数据
export interface LoginResponse {
  token: string
  user: UserInfo
}

// 注册请求参数
export interface RegisterRequest {
  username: string
  email: string
  password: string
  confirmPassword: string
}

// 注册响应数据
export interface RegisterResponse {
  user: UserInfo
  message: string
}

// 验证token响应数据
export interface VerifyTokenResponse {
  valid: boolean
  user?: UserInfo
  message?: string
}