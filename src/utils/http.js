// http.js
// axios基础的封装
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/userStore'
// 后端接口网址
const httpInstance = axios.create({
  // baseURL: 'https://pcapi-xiaotuxian-front-devtest.itheima.net',
  // baseURL: 'http://127.0.0.1:4523/m1/5240263-4907578-default',
  baseURL: 'https://apifoxmock.com/m1/5240263-4907578-default',
  // baseURL: 'http://127.0.0.1:8000/',
  timeout: 5000
})

// axios请求拦截器
httpInstance.interceptors.request.use(config => {
  // 1. 从pinia获取token数据
  const userStore = useUserStore()
  // 2. 按照后端的要求拼接token数据
  const token = userStore.userInfo.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, e => Promise.reject(e))

// axios响应式拦截器
httpInstance.interceptors.response.use(res => res.data, e => {
  // 统一错误提示
  ElMessage({
    type: 'warning',
    message: e.response.data.message
  })
  return Promise.reject(e)
})


export default httpInstance