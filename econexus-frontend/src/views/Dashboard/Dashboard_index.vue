<template>
  <div class="relative min-h-screen text-white p-8 overflow-hidden"
       style="background-image: url('https://images.unsplash.com/photo-1541427468627-c14b4869614f?q=80&w=2000&auto=format&fit=crop'); background-size: cover; background-position: center;">

    <div class="absolute inset-0 bg-[#0a0c0a]/90 backdrop-blur-md z-0 tech-grid"></div>

    <transition name="fade">
      <div v-if="isLoading" class="absolute inset-0 z-50 flex flex-col items-center justify-center bg-[#0a0c0a]/95 backdrop-blur-xl">
        <div class="relative w-32 h-32 mb-8">
          <div class="absolute inset-0 rounded-full border-t-2 border-l-2 border-emerald-500/80 animate-spin shadow-[0_0_15px_rgba(16,185,129,0.3)]"></div>
          <div class="absolute inset-3 rounded-full border-b-2 border-r-2 border-blue-400/80 animate-[spin_1.5s_linear_infinite_reverse]"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-12 h-12 bg-emerald-500/20 rounded-full flex items-center justify-center animate-pulse">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
              </svg>
            </div>
          </div>
        </div>
        <h2 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-blue-500 tracking-[0.2em] mb-4">天衍·生态监测引擎</h2>
        <div class="flex items-center gap-3 text-xs text-gray-400 font-mono tracking-widest">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          全域节点数据建立握手中...
        </div>
      </div>
    </transition>

    <div class="relative z-10">
      <div class="flex justify-between items-center mb-8 border-b border-white/10 pb-6">
        <div class="flex items-center gap-4">
          <div class="scale-75 origin-left"><EcoLogo /></div>
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

      <div v-if="errorMessage" class="bg-red-500/20 border border-red-500/50 text-red-400 px-4 py-2 rounded mb-6 text-sm flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        {{ errorMessage }}
      </div>

      <div class="glass-card p-6 rounded-2xl mb-8 relative overflow-hidden group">
        <div class="flex flex-col md:flex-row gap-6 relative z-10">
          <div class="flex items-center gap-6 min-w-max border-b md:border-b-0 md:border-r border-white/10 pb-4 md:pb-0 md:pr-8">
            <div class="text-blue-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 drop-shadow-[0_0_8px_rgba(96,165,250,0.5)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 18v2m-4-2v2m8-2v2" class="animate-pulse" />
              </svg>
            </div>
            <div>
              <div class="text-3xl font-mono text-white mb-1 flex items-baseline gap-2">
                {{ weatherInfo.temp }}
                <span class="text-xs text-eco-primary font-sans tracking-widest">LIVE</span>
              </div>
              <div class="text-xs text-gray-400 flex gap-3">
                <span>{{ weatherInfo.condition }}</span>
                <span class="text-blue-400/80">相对湿度 {{ weatherInfo.humidity }}</span>
              </div>
            </div>
          </div>
          <div class="flex-1 flex flex-col justify-center">
            <div v-if="weatherInfo.warning" class="flex items-center gap-3 mb-3">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold tracking-wider bg-orange-500/20 text-orange-400 border border-orange-500/40 animate-pulse">{{ weatherInfo.warning.level }}</span>
              <span class="text-sm font-bold text-gray-200">{{ weatherInfo.warning.title }}</span>
            </div>
            <div v-else class="flex items-center gap-3 mb-3">
               <span class="px-2 py-0.5 rounded text-[10px] font-bold tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">气象平稳</span>
              <span class="text-sm font-bold text-gray-400">当前无灾害性天气预警</span>
            </div>
            <div class="text-sm text-gray-300 leading-relaxed bg-gradient-to-r from-blue-900/30 to-transparent p-3 rounded-lg border-l-2 border-eco-primary backdrop-blur-sm">
              <span class="text-eco-primary font-bold mr-2">AI 动态调度:</span>{{ weatherInfo.ai_proposal }}
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div class="lg:col-span-3 glass-card p-6 rounded-2xl relative overflow-hidden">
          <h3 class="text-sm font-bold text-gray-300 mb-6 flex items-center gap-2 relative z-10">
            <span class="w-1.5 h-4 bg-eco-primary rounded-full animate-pulse shadow-[0_0_8px_#34d399]"></span> AI 自动研判与调度建议
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative z-10">
            <div v-for="(item, key) in {
              nitrogen: { label: '氮肥利用率决策', color: 'emerald' },
              pest: { label: '病虫害干预预警', color: 'yellow' },
              soil: { label: '土壤墒情动态调控', color: 'blue' }
            }" :key="key" class="space-y-2 border-l border-white/10 pl-4">
              <p class="text-xs text-gray-500 flex justify-between">
                <span>{{ item.label }}</span>
                <span :class="`text-${item.color}-400`">{{ apiData[key + '_efficiency']?.status_tag || apiData[key + '_risk']?.status_tag || apiData[key + '_moisture']?.status_tag }}</span>
              </p>
              <p class="text-sm text-gray-200 leading-loose mt-2 tracking-wide min-h-[60px]">
                {{ apiData[key + '_efficiency']?.ai_analysis || apiData[key + '_risk']?.ai_analysis || apiData[key + '_moisture']?.ai_analysis || 'AI 模型数据同步中...' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div @click="openDrillDown('nitrogen')" class="glass-card p-6 rounded-2xl cursor-pointer group hover:-translate-y-1 hover:shadow-[0_15px_40px_rgba(16,185,129,0.2)] transition-all duration-300 relative overflow-hidden">
          <h4 class="text-gray-400 text-xs mb-2">氮肥利用率 (NUE)</h4>
          <div class="text-4xl font-mono mb-2 text-white">
             <span v-if="isLoading" class="animate-pulse">--</span>
             <span v-else>{{ apiData.nitrogen_efficiency?.current_value }}</span><span class="text-base text-gray-600">%</span>
          </div>
          <div class="h-[60px] w-full mt-2 opacity-40 group-hover:opacity-100 transition-opacity">
            <div ref="sparklineNitrogen" class="w-full h-full"></div>
          </div>
        </div>

        <div @click="openDrillDown('pest')" class="glass-card p-6 rounded-2xl cursor-pointer group hover:-translate-y-1 hover:shadow-[0_15px_40px_rgba(234,179,8,0.2)] transition-all duration-300 relative overflow-hidden">
          <h4 class="text-gray-400 text-xs mb-2">病虫害等级预警</h4>
          <div class="text-3xl font-bold mb-2" :class="apiData.pest_risk?.current_value === 'MEDIUM' ? 'text-yellow-500' : 'text-emerald-500'">
            <span v-if="isLoading" class="animate-pulse">LOADING</span>
            <span v-else>{{ apiData.pest_risk?.current_value }}</span>
          </div>
          <div class="h-[60px] w-full mt-2 opacity-40 group-hover:opacity-100 transition-opacity">
            <div ref="sparklinePest" class="w-full h-full"></div>
          </div>
        </div>

        <div @click="openDrillDown('moisture')" class="glass-card p-6 rounded-2xl cursor-pointer group hover:-translate-y-1 hover:shadow-[0_15px_40px_rgba(96,165,250,0.2)] transition-all duration-300 relative overflow-hidden">
          <h4 class="text-gray-400 text-xs mb-2">土壤墒情监测</h4>
          <div class="text-4xl font-mono text-blue-400 mb-2">
            <span v-if="isLoading" class="animate-pulse">--</span>
            <span v-else>{{ apiData.soil_moisture?.current_value }}</span><span class="text-base text-blue-400/50">%</span>
          </div>
          <div class="h-[60px] w-full mt-2 opacity-40 group-hover:opacity-100 transition-opacity">
            <div ref="sparklineMoisture" class="w-full h-full"></div>
          </div>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="closeModal"></div>
        <div class="modal-box glass-card rounded-2xl w-full max-w-4xl p-6 md:p-8 relative z-10 shadow-[0_0_80px_rgba(16,185,129,0.15)]">
          <button @click="closeModal" class="absolute top-5 right-5 text-gray-500 hover:text-eco-primary transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
          <div v-if="isDrilling" class="h-[400px] flex flex-col items-center justify-center text-eco-primary">
            <svg class="animate-spin h-10 w-10 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            <span class="tracking-widest font-mono text-sm">云端时序溯源中...</span>
          </div>
          <div v-else>
            <div class="border-b border-white/10 pb-4 mb-6">
              <h3 class="text-xl md:text-2xl font-bold text-white flex items-center gap-3">
                <span class="w-1.5 h-6 bg-eco-primary rounded shadow-[0_0_8px_#34d399]"></span>{{ drillData?.metric_name }}
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
            <div class="flex flex-wrap gap-4">
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';
import EcoLogo from '../../components/EcoLogo.vue';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const isLoading = ref(true);
const apiData = ref({});
const errorMessage = ref('');

// 引用微缩图容器
const sparklineNitrogen = ref(null);
const sparklinePest = ref(null);
const sparklineMoisture = ref(null);
let sparklineInstances = [];

const weatherInfo = ref({
  temp: '--', condition: '卫星数据同步中', humidity: '--', warning: null,
  ai_proposal: 'AI 气象感知模型全域扫描中...'
});

const fetchWeather = async () => {
  try {
    const res = await axios.get('https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&current=temperature_2m,relative_humidity_2m,weather_code');
    if (res.status === 200) {
      const cur = res.data.current;
      weatherInfo.value.temp = cur.temperature_2m + '°C';
      weatherInfo.value.humidity = cur.relative_humidity_2m + '%';
      const code = cur.weather_code;
      let text = '晴朗'; let warn = false;
      if (code <= 3) text = '多云转晴';
      else if (code <= 49) text = '雾霾/低能见度';
      else if (code <= 69) { text = '降雨'; warn = true; }
      else if (code <= 79) { text = '降雪'; warn = true; }
      else if (code >= 80) { text = '雷暴'; warn = true; }
      weatherInfo.value.condition = text;
      if (warn) {
        weatherInfo.value.warning = { level: '黄色预警', title: `侦测到${text}过程` };
        weatherInfo.value.ai_proposal = `感知到${text}。建议：暂停户外作业，切换排灌模式，机库物理锁定。`;
      } else {
        weatherInfo.value.warning = null;
        weatherInfo.value.ai_proposal = '全域气象平稳，链路正常，各项全自动生产设备按标准策略运行。';
      }
    }
  } catch (e) {
    weatherInfo.value.ai_proposal = '无法连接外部卫星链路，请检查网络。';
  }
};

const isModalOpen = ref(false);
const isDrilling = ref(false);
const drillData = ref(null);
const chartRef = ref(null);
let myChart = null;

const initSparkline = (el, data, color) => {
  if (!el) return;
  const ins = echarts.init(el);
  ins.setOption({
    grid: { left: 0, right: 0, top: 10, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, min: 'dataMin' },
    series: [{
      data: data, type: 'line', smooth: true, symbol: 'none',
      lineStyle: { width: 2, color: color },
      areaStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0, color:`${color}33`},{offset:1, color:'transparent'}]) }
    }]
  });
  sparklineInstances.push(ins);
};

const handleResize = () => {
  myChart?.resize();
  sparklineInstances.forEach(ins => ins.resize());
};

onMounted(async () => {
  window.addEventListener('resize', handleResize);
  fetchWeather();
  try {
    const res = await axios.get(`${API_BASE}/api/dashboard/overview`);
    apiData.value = res.data;
    await nextTick();
    // 初始化微缩图
    initSparkline(sparklineNitrogen.value, [70, 72, 75, 71, 78, 82, 82.5], '#10b981');
    initSparkline(sparklinePest.value, [1, 2, 1, 3, 2, 2, 1.5], '#eab308');
    initSparkline(sparklineMoisture.value, [40, 41, 39, 43, 42, 42.8, 42.8], '#60a5fa');
  } catch (e) {
    errorMessage.value = '指挥中心数据同步异常';
  } finally {
    setTimeout(() => isLoading.value = false, 1500);
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  myChart?.dispose();
  sparklineInstances.forEach(ins => ins.dispose());
});

const openDrillDown = async (id) => {
  if (isDrilling.value) return;
  isModalOpen.value = true;
  isDrilling.value = true;
  try {
    const res = await axios.get(`${API_BASE}/api/dashboard/drill-down/${id}`);
    drillData.value = res.data;
    isDrilling.value = false;
    await nextTick();
    renderChart(drillData.value.timeline_data, {pest:'#eab308', moisture:'#60a5fa', nitrogen:'#10b981'}[id] || '#10b981');
  } catch (e) { isDrilling.value = false; }
};

const closeModal = () => {
  isModalOpen.value = false;
  myChart?.dispose();
  myChart = null;
};

const renderChart = (data, color) => {
  if (!chartRef.value) return;
  myChart = echarts.init(chartRef.value);
  myChart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(0,0,0,0.9)', borderColor: color, textStyle: { color: '#fff' } },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: data.map(i=>i.time), axisLine: { lineStyle: { color: '#333' } }, axisLabel: { color: '#9ca3af' } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }, axisLabel: { color: '#9ca3af' } },
    series: [{
      data: data.map(i=>i.value), type: 'line', smooth: true, itemStyle: { color: color },
      lineStyle: { color: color, width: 3 },
      areaStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0, color:`${color}66`},{offset:1, color:`${color}00`}]) }
    }]
  });
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease, backdrop-filter 0.4s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.fade-enter-active .modal-box { transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.4s ease; }
.fade-leave-active .modal-box { transition: transform 0.3s ease-in, opacity 0.3s ease; }
.fade-enter-from .modal-box { transform: scale(0.85) translateY(40px); opacity: 0; }
.fade-leave-to .modal-box { transform: scale(0.95) translateY(15px); opacity: 0; }

.tech-grid {
  background-image: linear-gradient(rgba(16, 185, 129, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(16, 185, 129, 0.08) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(circle at 50% 20%, black 40%, transparent 90%);
  -webkit-mask-image: radial-gradient(circle at 50% 20%, black 40%, transparent 90%);
}

.glass-card {
  background: linear-gradient(135deg, rgba(20, 25, 22, 0.6) 0%, rgba(5, 10, 5, 0.8) 100%);
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  border-left: 1px solid rgba(255, 255, 255, 0.05);
  border-right: 1px solid rgba(0, 0, 0, 0.4);
  border-bottom: 1px solid rgba(0, 0, 0, 0.6);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
</style>