// src/store/sensor.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSensorStore = defineStore('sensor', () => {
  // 1. 顶部 KPI 核心指标
  const kpiData = ref([
    { title: '根系层土壤湿度', value: '42.5%', trend: -1.2, icon: '🌱' },
    { title: '日均蒸散发量', value: '18.4 mm', trend: 2.4, icon: '💧' },
    { title: '冠层微气候温度', value: '28.6 °C', trend: 0.5, icon: '☀️' },
    { title: '今日虫害拦截', value: '142 次', trend: 15.3, icon: '🦋' }
  ])

  // 2. ECharts 孪生图表数据流
  const chartData = ref({
    timeAxis: ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00'],
    soilData: [45, 43, 42, 40, 48, 50, 49],
    etData: [1.2, 1.4, 1.8, 2.5, 2.1, 1.5, 1.3]
  })

  // 3. 更新图表数据的 Action (后续对接 FastAPI WebSocket/轮询将在此触发)
  const pushNewSensorData = (time: string, soil: number, et: number) => {
    chartData.value.timeAxis.shift()
    chartData.value.timeAxis.push(time)

    chartData.value.soilData.shift()
    chartData.value.soilData.push(soil)

    chartData.value.etData.shift()
    chartData.value.etData.push(et)
  }

  return { kpiData, chartData, pushNewSensorData }
})