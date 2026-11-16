// src/store/alert.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface PestAlert {
  id: number
  time: string
  node: string
  species: string
  confidence: number
}

export const useAlertStore = defineStore('alert', () => {
  // 1. 系统底层状态
  const isEdgeOnline = ref(true)
  const systemLoad = ref(18)

  // 2. YOLOv8 边缘拦截日志流
  const alertLogs = ref<PestAlert[]>([
    { id: 1, time: '10:42:01', node: 'Node-A', species: '稻飞虱', confidence: 0.92 },
    { id: 2, time: '10:38:15', node: 'Node-C', species: '蚜虫', confidence: 0.88 },
    { id: 3, time: '10:15:22', node: 'Node-B', species: '草地贪夜蛾', confidence: 0.95 },
    { id: 4, time: '09:55:10', node: 'Node-A', species: '稻飞虱', confidence: 0.89 },
  ])

  // 3. 接收新的 AI 预警 (维护固定队列长度，保持极简性能)
  const receiveAlert = (alert: PestAlert) => {
    alertLogs.value.unshift(alert)
    if (alertLogs.value.length > 5) {
      alertLogs.value.pop()
    }
    // 同步更新系统负荷与拦截次数
    systemLoad.value = Math.floor(15 + Math.random() * 10)
  }

  return { isEdgeOnline, systemLoad, alertLogs, receiveAlert }
})