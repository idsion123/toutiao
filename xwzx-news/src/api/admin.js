/**
 * 后台管理 API 模块
 */
import axios from 'axios'
import { apiConfig } from '../config/api'
import { useUserStore } from '../store/user'

// 创建 axios 实例
const adminApi = axios.create({
  baseURL: `${apiConfig.baseURL}/api/admin`,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 添加请求拦截器，自动添加 token
adminApi.interceptors.request.use(config => {
  // 从 Pinia store 获取 token
  const userStore = useUserStore()
  const token = userStore.token
  
  if (token) {
    // 后端期望的格式是 "Bearer xxx"
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 添加响应拦截器
adminApi.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('Admin API Error:', error)
    return Promise.reject(error)
  }
)

/**
 * 仪表盘统计
 */
export const dashboardApi = {
  // 获取统计数据
  getStats() {
    return adminApi.get('/dashboard/stats')
  }
}

/**
 * 用户管理
 */
export const userApi = {
  // 获取用户列表
  getList(page = 1, limit = 20, keyword = null) {
    return adminApi.get('/users', {
      params: { page, limit, keyword }
    })
  },

  // 获取用户详情
  getDetail(userId) {
    return adminApi.get(`/users/${userId}`)
  },

  // 删除用户
  delete(userId) {
    return adminApi.delete(`/users/${userId}`)
  }
}

/**
 * 新闻管理
 */
export const newsApi = {
  // 获取新闻列表
  getList(page = 1, limit = 20, keyword = null, categoryId = null) {
    return adminApi.get('/news', {
      params: { page, limit, keyword, category_id: categoryId }
    })
  },

  // 获取新闻详情
  getDetail(newsId) {
    return adminApi.get(`/news/${newsId}`)
  },

  // 创建新闻
  create(newsData) {
    return adminApi.post('/news', newsData)
  },

  // 更新新闻
  update(newsId, newsData) {
    return adminApi.put(`/news/${newsId}`, newsData)
  },

  // 删除新闻
  delete(newsId) {
    return adminApi.delete(`/news/${newsId}`)
  }
}

/**
 * 分类管理
 */
export const categoryApi = {
  // 获取分类列表
  getList() {
    return adminApi.get('/categories')
  },

  // 获取分类详情
  getDetail(categoryId) {
    return adminApi.get(`/categories/${categoryId}`)
  },

  // 创建分类
  create(name, sortOrder = 0) {
    return adminApi.post('/categories', null, {
      params: { name, sort_order: sortOrder }
    })
  },

  // 更新分类
  update(categoryId, name = null, sortOrder = null) {
    return adminApi.put(`/categories/${categoryId}`, null, {
      params: { name, sort_order: sortOrder }
    })
  },

  // 删除分类
  delete(categoryId) {
    return adminApi.delete(`/categories/${categoryId}`)
  }
}

export default {
  dashboard: dashboardApi,
  user: userApi,
  news: newsApi,
  category: categoryApi
}
