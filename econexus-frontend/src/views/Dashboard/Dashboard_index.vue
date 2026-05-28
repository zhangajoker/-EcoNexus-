<template>
  <div class="relative min-h-screen text-white p-8 overflow-hidden"
       style="background-image: url('https://images.unsplash.com/photo-1541427468627-c14b4869614f?q=80&w=2000&auto=format&fit=crop'); background-size: cover; background-position: center;">

    <div class="absolute inset-0 bg-[#0a0c0a]/90 backdrop-blur-md z-0"></div>

    <div class="relative z-10">
      <div class="flex justify-between items-center mb-8 border-b border-white/10 pb-6">
        <div class="flex items-center gap-4">
          <div class="scale-75 origin-left">
            <EcoLogo />
          </div>
          <div>
            <h2 class="text-2xl font-bold tracking-widest text-white">天衍·智慧农业</h2>
            <p class="text-xs text-eco-primary font-mono tracking-wider uppercase">EcoNexus Intelligence Command</p>
          </div>
        </div>

        <div class="text-right">
          <span class="text-gray-400 text-xs uppercase">全域生产健康指数</span>
          <div class="text-3xl font-mono mt-1" :class="apiData.efficiency_score >= 90 ? 'text-white' : 'text-yellow-400'">
            <span v-if="isLoading" class="animate-pulse">--.-</span>
            <span v-else>{{ apiData.efficiency_score }}</span>
            <span class="text-sm text-eco-primary">/ 100</span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div class="lg:col-span-3 bg-black/40 p-6 rounded-2xl border border-white/5 shadow-2xl">
          <h3 class="text-sm font-bold text-gray-300 mb-6 flex items-center gap-2">
            <span class="w-1.5 h-4 bg-eco-primary rounded-full animate-pulse shadow-[0_0_8px_#34d399]"></span> AI 自动研判与调度建议
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="space-y-2 border-l border-emerald-500/20 pl-4">
              <p class="text-xs text-gray-500 flex justify-between">
                <span>氮肥利用率决策</span>
                <span class="text-emerald-400">{{ apiData.nitrogen_efficiency?.status_tag }}</span>
              </p>
              <p class="text-sm text-gray-200 leading-relaxed min-h-[40px]">
                {{ apiData.nitrogen_efficiency?.ai_analysis || 'AI 模型数据同步中...' }}
              </p>
            </div>
            <div class="space-y-2 border-l border-yellow-500/20 pl-4">
              <p class="text-xs text-gray-500 flex justify-between">
                <span>病虫害干预预警</span>
                <span class="text-yellow-500">{{ apiData.pest_risk?.status_tag }}</span>
              </p>
              <p class="text-sm text-gray-200 leading-relaxed min-h-[40px]">
                 {{ apiData.pest_risk?.ai_analysis || 'AI 模型数据同步中...' }}
              </p>
            </div>
            <div class="space-y-2 border-l border-blue-500/20 pl-4">
              <p class="text-xs text-gray-500 flex justify-between">
                <span>土壤墒情动态调控</span>
                <span class="text-blue-400">{{ apiData.soil_moisture?.status_tag }}</span>
              </p>
              <p class="text-sm text-gray-200 leading-relaxed min-h-[40px]">
                 {{ apiData.soil_moisture?.ai_analysis || 'AI 模型数据同步中...' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div @click="openDrillDown('nitrogen')" class="bg-black/40 border border-white/5 p-6 rounded-2xl cursor-pointer group hover:border-emerald-500/50 hover:-translate-y-1 transition-all relative overflow-hidden">
          <div class="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
            <span class="text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded">点击钻取详情</span>
          </div>
          <h4 class="text-gray-400 text-xs mb-2">氮肥利用率 (NUE)</h4>
          <div class="text-4xl font-mono mb-4 text-white">
             <span v-if="isLoading" class="animate-pulse">--</span>
             <span v-else>{{ apiData.nitrogen_efficiency?.current_value }}</span>
             <span class="text-base text-gray-600">%</span>
          </div>
          <div class="h-1.5 bg-black rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 transition-all duration-1000" :style="`width: ${apiData.nitrogen_efficiency?.current_value || 0}%`"></div>
          </div>
        </div>

        <div @click="openDrillDown('pest')" class="bg-black/40 border border-white/5 p-6 rounded-2xl cursor-pointer group hover:border-yellow-500/50 hover:-translate-y-1 transition-all relative overflow-hidden">
          <div class="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
            <span class="text-[10px] text-yellow-500 bg-yellow-500/10 px-2 py-1 rounded">点击钻取详情</span>
          </div>
          <h4 class="text-gray-400 text-xs mb-2">病虫害等级预警</h4>
          <div class="text-3xl font-bold mb-4" :class="apiData.pest_risk?.current_value === 'MEDIUM' ? 'text-yellow-500' : 'text-emerald-500'">
            <span v-if="isLoading" class="animate-pulse">LOADING</span>
            <span v-else>{{ apiData.pest_risk?.current_value }}</span>
          </div>
          <p class="text-xs text-gray-500 font-mono">Vision Inferencing ACTIVE</p>
        </div>

        <div @click="openDrillDown('moisture')" class="bg-black/40 border border-white/5 p-6 rounded-2xl cursor-pointer group hover:border-blue-500/50 hover:-translate-y-1 transition-all relative overflow-hidden">
           <div class="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
            <span class="text-[10px] text-blue-400 bg-blue-500/10 px-2 py-1 rounded">点击钻取详情</span>
          </div>
          <h4 class="text-gray-400 text-xs mb-2">土壤墒情监测</h4>
          <div class="text-4xl font-mono text-blue-400 mb-4">
            <span v-if="isLoading" class="animate-pulse">--</span>
            <span v-else>{{ apiData.soil_moisture?.current_value }}</span>
            <span class="text-base text-blue-400/50">%</span>
          </div>
          <p class="text-xs text-gray-500 font-mono">PM Model Running</p>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="closeModal"></div>

        <div class="bg-[#0a0c0a]/95 border border-eco-primary/30 rounded-2xl w-full max-w-4xl p-6 md:p-8 relative z-10 shadow-[0_0_50px_rgba(0,0,0,0.8)]">
          <button @click="closeModal" class="absolute top-5 right-5 text-gray-500 hover:text-eco-primary transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>

          <div v-if="isDrilling" class="h-[400px] flex flex-col items-center justify-center text-eco-primary">
            <svg class="animate-spin h-10 w-10 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            <span class="tracking-widest font-mono">云端时序溯源中...</span>
          </div>

          <div v-else>
            <div class="border-b border-white/10 pb-4 mb-6">
              <h3 class="text-xl md:text-2xl font-bold text-white flex items-center gap-3">
                <span class="w-1.5 h-6 bg-eco-primary rounded shadow-[0_0_8px_#34d399]"></span>
                {{ drillData?.metric_name }}
              </h3>
            </div>

            <div class="bg-white/5 border border-white/10 p-4 rounded-lg mb-6 flex gap-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-eco-primary shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <div>
                <h4 class="text-white font-bold text-sm mb-1">AI 溯源诊断</h4>
                <p class="text-sm text-gray-400 leading-relaxed">{{ drillData?.summary_analysis }}</p>
              </div>
            </div>

            <div ref="chartRef" class="w-full h-[300px] bg-black/40 rounded-lg border border-white/5 mb-6"></div>

            <div class="flex gap-4">
              <div v-for="(dev, idx) in drillData?.device_status" :key="idx" class="bg-black/60 px-3 py-2 rounded border border-white/5 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_5px_#10b981]"></span>
                <span class="text-xs text-gray-400">{{ dev.name }}: <span class="text-white font-mono">{{ dev.status }}</span></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';
import EcoLogo from '../../components/EcoLogo.vue';

const isLoading = ref(true);
const apiData = ref({});

// 弹窗与图表状态
const isModalOpen = ref(false);
const isDrilling = ref(false);
const drillData = ref(null);
const chartRef = ref(null);
let myChart = null;

// 组件挂载时获取总览数据
onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/dashboard/overview');
    apiData.value = response.data;
  } catch (error) {
    console.error('获取决策数据失败:', error);
  } finally {
    isLoading.value = false;
  }
});

// 打开数据钻取面板
const openDrillDown = async (metricId) => {
  isModalOpen.value = true;
  isDrilling.value = true;

  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/dashboard/drill-down/${metricId}`);
    drillData.value = response.data;

    isDrilling.value = false;
    await nextTick();

    // 根据不同指标应用不同的主题色
    const color = metricId === 'pest' ? '#eab308' : (metricId === 'moisture' ? '#60a5fa' : '#10b981');
    renderChart(drillData.value.timeline_data, color);

  } catch (error) {
    console.error('钻取时序数据失败:', error);
    isDrilling.value = false;
  }
};

const closeModal = () => {
  isModalOpen.value = false;
  if (myChart) {
    myChart.dispose();
    myChart = null;
  }
};

// 渲染 ECharts 折线图
const renderChart = (timelineData, themeColor) => {
  if (!chartRef.value) return;

  const times = timelineData.map(item => item.time);
  const values = timelineData.map(item => item.value);

  myChart = echarts.init(chartRef.value);

  const option = {
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(0,0,0,0.9)', borderColor: themeColor, textStyle: { color: '#fff' } },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: times, axisLine: { lineStyle: { color: '#333' } }, axisLabel: { color: '#9ca3af' } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }, axisLabel: { color: '#9ca3af' } },
    series: [
      {
        data: values,
        type: 'line',
        smooth: true,
        symbolSize: 6,
        itemStyle: { color: themeColor },
        lineStyle: { color: themeColor, width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: `${themeColor}66` }, // 40% opacity
            { offset: 1, color: `${themeColor}00` }  // 0% opacity
          ])
        }
      }
    ]
  };

  myChart.setOption(option);
  window.addEventListener('resize', () => myChart?.resize());
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>