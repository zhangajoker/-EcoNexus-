// src/api/dashboard.ts
import request from './request';
import type { WeatherData, SensorGaugeData, TrendDataPoint, ApiResponse } from '../types/api';

export const dashboardApi = {
  // 获取气象数据
  getWeather() {
    return request.get<any, ApiResponse<WeatherData>>('/api/weather');
  },
  // 获取大屏左侧实时传感器数据
  getRealtimeSensors() {
    return request.get<any, ApiResponse<SensorGaugeData>>('/api/dashboard/sensors');
  },
  // 获取历史趋势数据 (按类型: 'soil' | 'air')
  getTrendData(type: string) {
    return request.get<any, ApiResponse<TrendDataPoint[]>>(`/api/dashboard/trend/${type}`);
  }
};