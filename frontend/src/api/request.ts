// src/api/request.ts
import axios, { InternalAxiosRequestConfig, AxiosResponse } from 'axios';

// 创建 axios 实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  timeout: 15000, // 物联网数据请求容易延迟，设置15秒超时
});

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 预留：如果以后有 Token，在这里统一添加
    // const token = localStorage.getItem('token');
    // if (token) { config.headers['Authorization'] = `Bearer ${token}`; }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 直接返回 data 部分，剥离 axios 的外层包装
    return response.data;
  },
  (error) => {
    console.error('天衍中枢通信异常:', error.message);
    // 这里可以接入 Element Plus 的 ElMessage 进行全局统一报错
    return Promise.reject(error);
  }
);

export default service;