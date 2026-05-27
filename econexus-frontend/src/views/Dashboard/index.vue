<template>
  <div class="min-h-screen bg-gradient-to-br from-eco-dark via-[#064e3b] to-[#0f172a] p-6 grid grid-cols-12 gap-6 content-start relative overflow-hidden">

    <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-eco-primary opacity-10 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-[#fbbf24] opacity-5 rounded-full blur-[150px] pointer-events-none"></div>

    <header class="col-span-12 flex justify-between items-center border-b border-eco-border/50 pb-4 relative z-10">
     <div class="flex items-center gap-3 select-none z-10">
        <div class="flex items-baseline text-4xl font-black tracking-tighter" style="font-family: 'Arial Black', Impact, sans-serif;">
          <span class="text-white drop-shadow-sm">Eco</span>

          <div class="relative inline-flex items-center mx-[1px]">
            <span class="text-[#10b981] z-10 drop-shadow-sm">N</span>
            <svg class="absolute -top-1.5 -right-3 w-5 h-5 text-[#10b981] fill-current transform rotate-12 z-0 drop-shadow-sm" viewBox="0 0 24 24">
               <path d="M12 22C12 22 4 16 4 10C4 5.6 7.6 2 12 2C16.4 2 20 5.6 20 10C20 16 12 22 12 22ZM12 4.5C9.5 4.5 7.5 6.5 7.5 9C7.5 10.4 8.2 11.6 9.2 12.4L12 16L14.8 12.4C15.8 11.6 16.5 10.4 16.5 9C16.5 6.5 14.5 4.5 12 4.5Z" />
            </svg>
          </div>

          <span class="text-[#cbd5e1] drop-shadow-[1px_2px_1px_rgba(0,0,0,0.5)]">exus</span>
        </div>

        <h1 class="text-2xl font-semibold tracking-widest text-white border-l-2 border-[#10b981]/40 pl-4 ml-2">
          天衍·生境
        </h1>
      </div>
      <div class="flex space-x-6 text-sm text-eco-text items-center bg-eco-panel backdrop-blur-md px-4 py-2 rounded-full border border-eco-border">
        <span class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-eco-primary animate-pulse shadow-[0_0_8px_#34d399]"></span>
          边缘节点在线
        </span>
        <span class="text-eco-border">|</span>
        <span>系统负荷: <span class="text-white font-mono">{{ systemLoad }}%</span></span>
      </div>
    </header>

    <div class="col-span-12 grid grid-cols-1 md:grid-cols-4 gap-6 relative z-10">
      <div v-for="kpi in kpiData" :key="kpi.title" class="bg-eco-panel backdrop-blur-md border border-eco-border rounded-xl p-5 flex flex-col justify-between shadow-lg transition duration-300 hover:border-eco-primary/50 hover:bg-eco-dark/40">
        <div class="flex justify-between items-start">
          <span class="text-eco-text text-xs uppercase tracking-widest">{{ kpi.title }}</span>
          <span class="text-xl opacity-60">{{ kpi.icon }}</span>
        </div>
        <div class="flex items-end justify-between mt-4">
          <span class="text-3xl font-light text-white">{{ kpi.value }}</span>
          <span class="text-xs mb-1 font-medium bg-black/20 px-2 py-1 rounded" :class="kpi.trend > 0 ? 'text-eco-alert' : 'text-eco-primary'">
            {{ kpi.trend > 0 ? '↑' : '↓' }} {{ Math.abs(kpi.trend) }}%
          </span>
        </div>
      </div>
    </div>

    <main class="col-span-12 lg:col-span-8 bg-eco-panel backdrop-blur-md border border-eco-border rounded-xl p-6 flex flex-col relative z-10 shadow-lg">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-sm text-eco-text uppercase tracking-widest font-medium flex items-center gap-2">
          <span class="w-1 h-4 bg-eco-primary rounded-full"></span> 农田微气候与土壤墒情趋势
        </h2>
        <span class="text-[10px] text-eco-primary border border-eco-primary/30 px-2 py-1 rounded-full bg-eco-primary/10 tracking-wider">实时孪生同步</span>
      </div>
      <div ref="chartRef" class="w-full flex-1 min-h-[350px]"></div>
    </main>

    <aside class="col-span-12 lg:col-span-4 flex flex-col relative z-10">
      <div class="bg-eco-panel backdrop-blur-md border border-eco-border rounded-xl p-6 flex-1 flex flex-col overflow-hidden shadow-lg">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-sm text-eco-alert uppercase tracking-widest font-medium flex items-center gap-2">
            <span class="w-1 h-4 bg-eco-alert rounded-full"></span> 边缘视觉防线 (YOLOv8)
          </h2>
        </div>

        <div class="flex-1 overflow-hidden">
          <transition-group name="list" tag="div" class="space-y-4">
            <div
              v-for="alert in alertLogs"
              :key="alert.id"
              class="flex justify-between items-center text-sm border-b border-eco-border/50 pb-3 hover:bg-white/5 p-2 rounded transition-colors"
            >
              <div class="flex flex-col">
                <span class="text-white font-medium flex items-center gap-2">
                  <span class="text-xs bg-eco-alert/20 text-eco-alert px-1.5 py-0.5 rounded border border-eco-alert/30">{{ alert.node }}</span>
                  {{ alert.species }}
                </span>
                <span class="text-xs text-eco-text mt-1.5">拦截时间: {{ alert.time }}</span>
              </div>
              <div class="flex flex-col items-end">
                <span class="text-eco-primary font-mono bg-eco-primary/10 px-2 py-0.5 rounded">P={{ alert.confidence.toFixed(2) }}</span>
                <span class="text-[10px] text-eco-text mt-1.5 opacity-70">SAHI 切片检出</span>
              </div>
            </div>
          </transition-group>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// --- 模拟状态数据 (加入农学单位和 Emoji 装饰) ---
const systemLoad = ref(18)
const kpiData = ref([
  { title: '根系层土壤湿度', value: '42.5%', trend: -1.2, icon: '🌱' },
  { title: '日均蒸散发量', value: '18.4 mm', trend: 2.4, icon: '💧' },
  { title: '冠层微气候温度', value: '28.6 °C', trend: 0.5, icon: '☀️' },
  { title: '今日虫害拦截', value: '142 次', trend: 15.3, icon: '🦋' }
])

const alertLogs = ref([
  { id: 1, time: '10:42:01', node: 'Node-A', species: '稻飞虱', confidence: 0.92 },
  { id: 2, time: '10:38:15', node: 'Node-C', species: '蚜虫', confidence: 0.88 },
  { id: 3, time: '10:15:22', node: 'Node-B', species: '草地贪夜蛾', confidence: 0.95 },
  { id: 4, time: '09:55:10', node: 'Node-A', species: '稻飞虱', confidence: 0.89 },
])

// --- ECharts 动态折线图配置 ---
const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null
let timer: any = null

const initAdvancedChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)

  let timeAxis = ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00']
  let soilData = [45, 43, 42, 40, 48, 50, 49]
  let etData = [1.2, 1.4, 1.8, 2.5, 2.1, 1.5, 1.3]

  const getOption = () => ({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(2, 44, 34, 0.8)', // 提示框毛玻璃
      borderColor: '#047857',
      textStyle: { color: '#f8fafc' },
      axisPointer: { type: 'line', lineStyle: { color: '#34d399', type: 'dashed' } }
    },
    legend: { textStyle: { color: '#a7f3d0' }, top: 0, right: 0, icon: 'circle' },
    grid: { left: '2%', right: '2%', bottom: '0%', top: '15%', containLabel: true },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: timeAxis,
      axisLine: { lineStyle: { color: '#047857' } },
      axisLabel: { color: '#a7f3d0' },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: 'rgba(16, 185, 129, 0.15)', type: 'dashed' } },
      axisLabel: { color: '#a7f3d0' }
    },
    series: [
      {
        name: '土壤含水率',
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { color: '#34d399', width: 3 }, // 生机绿
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(52, 211, 153, 0.3)' },
            { offset: 1, color: 'rgba(52, 211, 153, 0)' }
          ])
        },
        data: soilData
      },
      {
        name: '蒸散发量 (ET0)',
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { color: '#fbbf24', width: 3 }, // 暖阳金
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(251, 191, 36, 0.2)' },
            { offset: 1, color: 'rgba(251, 191, 36, 0)' }
          ])
        },
        data: etData
      }
    ]
  })

  chartInstance.setOption(getOption())

  timer = setInterval(() => {
    const now = new Date()
    timeAxis.shift()
    timeAxis.push(`${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`)
    soilData.shift()
    soilData.push(45 + Math.random() * 5 - 2.5)
    etData.shift()
    etData.push(1.5 + Math.random() * 1 - 0.5)
    chartInstance?.setOption({ xAxis: { data: timeAxis }, series: [{ data: soilData }, { data: etData }] })

    if (Math.random() > 0.6) {
      const nodes = ['Node-A', 'Node-B', 'Node-C', 'Node-D']
      const pests = ['稻飞虱', '蚜虫', '草地贪夜蛾', '黏虫']
      alertLogs.value.unshift({
        id: Date.now(),
        time: `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`,
        node: nodes[Math.floor(Math.random() * nodes.length)],
        species: pests[Math.floor(Math.random() * pests.length)],
        confidence: 0.85 + Math.random() * 0.14
      })
      if (alertLogs.value.length > 5) alertLogs.value.pop()
    }
  }, 3000)
}

onMounted(() => {
  initAdvancedChart()
  window.addEventListener('resize', () => chartInstance?.resize())
})

onUnmounted(() => {
  window.removeEventListener('resize', () => chartInstance?.resize())
  chartInstance?.dispose()
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.list-enter-from {
  opacity: 0;
  transform: translateX(40px) scale(0.95);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(-40px) scale(0.95);
}
</style>