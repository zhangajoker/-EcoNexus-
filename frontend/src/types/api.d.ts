// src/types/api.d.ts

// 1. 定义全局通用的 API 返回结构
export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

// 2. 定义气象数据接口 (结合大屏右侧面板需求)
export interface WeatherData {
  temperature_2m: number;
  relative_humidity_2m: number;
  weather_code: number;
  wind_speed?: number;
  precipitation?: number; // 降水量
}

// 3. 定义大屏左侧实时传感器环形图数据
export interface SensorGaugeData {
  airTemp: number;     // 空气温度
  airHumidity: number; // 空气湿度
  soilMoisture: number;// 土壤水分
  soilTemp: number;    // 土壤温度
}

// 4. 定义趋势折线图数据
export interface TrendDataPoint {
  time: string;
  value: number;
}