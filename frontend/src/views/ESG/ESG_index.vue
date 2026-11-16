<template>
  <!-- 核心修复1：外层允许整个网页自然垂直滚动 -->
  <div id="esg-dashboard-container" class="p-8 min-h-screen relative text-white bg-[#0a0c0a] overflow-x-hidden overflow-y-auto custom-scrollbar select-none">

    <div class="absolute inset-0 z-0">
      <img src="https://images.pexels.com/photos/259280/pexels-photo-259280.jpeg?auto=compress&cs=tinysrgb&w=1600"
           class="w-full h-full object-cover opacity-10 grayscale mix-blend-luminosity" alt="Southwest China Terrain" />
      <div class="absolute inset-0 bg-gradient-to-b from-[#0a0c0a]/80 via-[#0a0c0a]/95 to-[#0a0c0a] z-10"></div>
    </div>

    <div class="relative z-10 min-h-full flex flex-col view-animate">

      <!-- 头部 -->
      <div class="mb-8 flex justify-between items-end border-b border-white/10 pb-6">
        <div>
          <h2 class="text-4xl font-bold border-l-[6px] border-eco-primary pl-5 tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.5)]">ESG 绿色碳汇与生态合规资产看板</h2>
          <p class="text-xl font-bold text-gray-400 mt-3 font-mono uppercase tracking-widest">Model-driven Ecological Assets & Carbon Footprint Accounting</p>
        </div>
        <div class="flex gap-4">
          <button @click="exportToPDF" class="bg-white/5 border border-white/10 px-5 py-2.5 rounded text-sm font-bold font-mono text-gray-300 hover:text-white hover:border-eco-primary/50 transition-all flex items-center gap-2 group shadow-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 group-hover:text-eco-primary transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            导出年度合规审计报告 (PDF)
          </button>
        </div>
      </div>

      <!-- 第一部分：四大 KPI 数字卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-emerald-500/40 transition-colors border-l-[4px] border-l-emerald-500 shadow-[inset_1px_0_10px_rgba(16,185,129,0.1)]">
          <div class="absolute -top-[1px] -right-[1px] w-3 h-3 border-t-2 border-r-2 border-emerald-500/50"></div>
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-emerald-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-sm font-bold text-gray-300 font-mono tracking-widest uppercase">累计碳减排当量</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" /></svg>
          </div>
          <div class="flex items-baseline gap-2">
            <div class="text-6xl font-bold font-mono transition-all duration-500 origin-left inline-block tracking-tighter"
                 :class="isUpdating ? 'text-white drop-shadow-[0_0_25px_rgba(16,185,129,1)] scale-[1.05]' : 'text-transparent bg-clip-text bg-gradient-to-br from-emerald-300 to-cyan-500 drop-shadow-[0_2px_10px_rgba(52,211,153,0.3)]'">
              {{ formatNumber(esgData.assets.co2_reduction, 3) }}
            </div>
            <span class="text-base font-bold text-gray-400">tCO₂e</span>
          </div>
          <div class="mt-5 flex justify-between items-center border-t border-white/10 pt-4">
             <div class="text-sm text-emerald-400 font-bold font-mono bg-emerald-500/10 px-2.5 py-1 rounded flex items-center gap-1 border border-emerald-500/20">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>
               +2.4% MoM
             </div>
             <div class="text-xs font-bold text-gray-400">智能调度实时累加</div>
          </div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-teal-500/40 transition-colors border-l-[4px] border-l-teal-500 shadow-[inset_1px_0_10px_rgba(20,184,166,0.1)]">
          <div class="absolute -top-[1px] -right-[1px] w-3 h-3 border-t-2 border-r-2 border-teal-500/50"></div>
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-teal-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-sm font-bold text-gray-300 font-mono tracking-widest uppercase">面源污染拦截量</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
          </div>
          <div class="flex items-baseline gap-2">
            <div class="text-6xl font-bold font-mono transition-all duration-500 origin-left inline-block tracking-tighter"
                 :class="isUpdating ? 'text-white drop-shadow-[0_0_25px_rgba(20,184,166,1)] scale-[1.05]' : 'text-transparent bg-clip-text bg-gradient-to-br from-teal-300 to-emerald-500 drop-shadow-[0_2px_10px_rgba(20,184,166,0.3)]'">
              {{ formatNumber(esgData.assets.pollution_interception, 1) }}
            </div>
            <span class="text-base font-bold text-gray-400">kg (N/P)</span>
          </div>
          <div class="mt-5 flex justify-between items-center border-t border-white/10 pt-4">
             <div class="text-sm text-teal-400 font-bold font-mono bg-teal-500/10 px-2.5 py-1 rounded flex items-center gap-1 border border-teal-500/20">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>
               +1.8% MoM
             </div>
             <div class="text-xs font-bold text-gray-400">视觉靶向拦截解构</div>
          </div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-blue-500/40 transition-colors border-l-[4px] border-l-blue-500 shadow-[inset_1px_0_10px_rgba(59,130,246,0.1)]">
          <div class="absolute -top-[1px] -right-[1px] w-3 h-3 border-t-2 border-r-2 border-blue-500/50"></div>
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-blue-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-sm font-bold text-gray-300 font-mono tracking-widest uppercase">国家绿色金融评级</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" /></svg>
          </div>
          <div class="flex items-baseline gap-2">
            <div class="text-6xl font-bold font-mono tracking-widest text-transparent bg-clip-text bg-gradient-to-br from-blue-300 to-indigo-400 drop-shadow-[0_2px_15px_rgba(59,130,246,0.4)]">
              {{ esgData.assets.financial_rating }}
            </div>
            <span class="text-base font-bold text-gray-400">级</span>
          </div>
          <div class="mt-5 flex justify-between items-center border-t border-white/10 pt-4">
             <div class="text-sm font-bold text-gray-300 font-mono bg-white/10 px-2.5 py-1 rounded">
               - 维持不变
             </div>
             <div class="text-xs font-bold text-gray-400">智能决策合规率达标</div>
          </div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-amber-500/40 transition-colors border-l-[4px] border-l-amber-500 shadow-[inset_1px_0_10px_rgba(245,158,11,0.1)]">
          <div class="absolute -top-[1px] -right-[1px] w-3 h-3 border-t-2 border-r-2 border-amber-500/50"></div>
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-amber-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-sm font-bold text-gray-300 font-mono tracking-widest uppercase">预估碳汇交易核算</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <div class="flex items-baseline gap-2">
            <div class="text-6xl font-bold font-mono transition-all duration-500 origin-left inline-block tracking-tighter"
                 :class="isUpdating ? 'text-white drop-shadow-[0_0_25px_rgba(245,158,11,1)] scale-[1.05]' : 'text-transparent bg-clip-text bg-gradient-to-br from-amber-200 to-orange-500 drop-shadow-[0_2px_10px_rgba(245,158,11,0.3)]'">
              {{ formatNumber(esgData.assets.carbon_revenue, 0) }}
            </div>
            <span class="text-base font-bold text-gray-400">CNY</span>
          </div>
          <div class="mt-5 flex justify-between items-center border-t border-white/10 pt-4">
             <div class="text-sm text-amber-400 font-bold font-mono bg-amber-500/10 px-2.5 py-1 rounded flex items-center gap-1 border border-amber-500/20">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>
               +4.2% YoY
             </div>
             <div class="text-xs font-bold text-gray-400">全国碳权市场实时挂钩</div>
          </div>
        </div>
      </div>

      <!-- 第二部分：图表与日志 (核心修复2：横向4列布局，条形图移至最左边) -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8 flex-1">

        <!-- 左侧第1列：污染削减条形图 -->
        <div class="lg:col-span-1 bg-black/40 border border-white/5 rounded-none p-6 relative group flex flex-col min-h-[420px]">
          <div class="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-teal-500/0 via-teal-500/30 to-teal-500/0"></div>
          <h3 class="text-lg font-bold text-white font-mono tracking-widest mb-4 flex items-center gap-3">
            <span class="w-2 h-2 bg-teal-500 shadow-[0_0_10px_#14b8a6]"></span>
            面源污染削减解构 (kg)
          </h3>
          <!-- 移除了内部 scrollbar，让画布充满容器 -->
          <div ref="reductionChartRef" class="w-full flex-1 min-h-[300px]"></div>
        </div>

        <!-- 中间2列：能耗折线图 -->
        <div class="lg:col-span-2 bg-black/40 border border-white/5 rounded-none p-6 relative group flex flex-col min-h-[420px]">
          <div class="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-emerald-500/0 via-emerald-500/30 to-emerald-500/0"></div>
          <h3 class="text-lg font-bold text-white font-mono tracking-widest mb-4 flex items-center gap-3">
            <span class="w-2 h-2 bg-emerald-500 shadow-[0_0_10px_#10b981]"></span>
            模型驱动下的能耗与碳排放双轨对比 (tCO₂e)
          </h3>
          <!-- 移除了内部 scrollbar -->
          <div ref="trendChartRef" class="w-full flex-1 min-h-[300px]"></div>
        </div>

        <!-- 右侧第1列：合规日志区 -->
        <div class="lg:col-span-1 bg-black/40 border border-white/5 rounded-none p-6 flex flex-col relative border-t-[4px] border-t-blue-500/50 min-h-[420px]">
          <h3 class="text-lg font-bold text-white font-mono tracking-widest mb-6 border-b border-white/10 pb-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
               <span class="w-2 h-2 bg-blue-500 shadow-[0_0_10px_#3b82f6]"></span>
               调度合规日志
            </div>
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_10px_#10b981]"></span>
          </h3>

          <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-6 font-mono max-h-[220px]">
            <transition-group name="log-list">
              <div v-for="log in esgData.logs" :key="log.id" class="relative pl-5 border-l-2 transition-all duration-300"
                   :class="log.category === '靶向干预' ? 'border-amber-500/40' : (log.category === '闭环控制' ? 'border-blue-500/40' : 'border-emerald-500/40')">
                <span class="absolute -left-2 top-1.5 w-3.5 h-3.5 bg-black border-[2px] rounded-full shadow-[0_0_8px_currentColor]"
                      :class="log.category === '靶向干预' ? 'border-amber-400 text-amber-400' : (log.category === '闭环控制' ? 'border-blue-400 text-blue-400' : 'border-emerald-400 text-emerald-400')"></span>
                <div class="text-xs font-bold text-gray-400 mb-1.5 flex justify-between">
                   <span>{{ log.timestamp }}</span>
                   <span :class="log.category === '靶向干预' ? 'text-amber-400' : 'text-emerald-400'">[{{ log.category }}]</span>
                </div>
                <div class="text-base text-white mb-2 font-bold truncate" :title="log.title">{{ log.title }}</div>
                <div class="text-sm font-medium text-gray-300 leading-relaxed">{{ log.description }}</div>
              </div>
            </transition-group>
          </div>

          <div class="mt-6 pt-4 border-t border-white/10">
            <div class="bg-emerald-900/20 border border-emerald-500/40 p-4 relative shadow-[inset_0_0_20px_rgba(16,185,129,0.1)]">
              <div class="absolute top-0 left-0 w-1.5 h-full bg-emerald-500"></div>
              <div class="text-sm text-emerald-400 font-bold mb-2 flex items-center gap-2">
                 <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                 天衍中枢判定：达标
              </div>
              <p class="text-xs font-bold text-gray-300 leading-relaxed font-sans pl-7">
                视觉靶向拦截符合《可持续发展指令》，已通过跨链账本认证。
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { API_BASE } from '../../config';
import html2pdf from 'html2pdf.js';

const trendChartRef = ref(null);
const reductionChartRef = ref(null);
let trendChart = null;
let reductionChart = null;

const isUpdating = ref(false);

const esgData = ref({
  assets: { co2_reduction: 0, pollution_interception: 0, financial_rating: "AAA", carbon_revenue: 0 },
  logs: [],
  charts: {
    trend: { categories: [], baseline: [], actual: [] },
    reduction: []
  }
});

const formatNumber = (num, decimals = 2) => {
  if (num === undefined || num === null) return "";
  return num.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
};

const fetchEsgDashboardData = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/esg/dashboard`);
    if (!response.ok) return;
    const data = await response.json();

    if (esgData.value.assets.pollution_interception > 0 &&
        data.assets.pollution_interception > esgData.value.assets.pollution_interception) {
        isUpdating.value = true;
        setTimeout(() => { isUpdating.value = false; }, 1000);
    }

    esgData.value = data;
    nextTick(() => { updateCharts(); });
  } catch (error) {
    console.error("读取动态资产失败", error);
  }
};

const exportToPDF = async () => {
  const element = document.getElementById('esg-dashboard-container');
  if (!element) return;
  const opt = {
    margin: 0.1, filename: `天衍_ESG生态合规审计报告_2026.pdf`, image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true, backgroundColor: '#0a0c0a' }, jsPDF: { unit: 'in', format: 'a4', orientation: 'landscape' }
  };
  await html2pdf().set(opt).from(element).save();
};

const initCharts = () => {
  if (trendChartRef.value && !trendChart) trendChart = echarts.init(trendChartRef.value);
  if (reductionChartRef.value && !reductionChart) reductionChart = echarts.init(reductionChartRef.value);
};

const updateCharts = () => {
  if (!trendChart || !reductionChart) return;
  const chartData = esgData.value.charts;
  if (!chartData) return;

  trendChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(10, 12, 10, 0.95)',
      borderColor: 'rgba(52,211,153,0.3)',
      textStyle: { color: '#fff', fontSize: 14, fontFamily: 'monospace', fontWeight: 'bold' }
    },
    legend: { data: ['粗放经验基准排放', 'AI模型调度实际排放'], textStyle: { color: '#ccc', fontSize: 13, fontFamily: 'monospace', fontWeight: 'bold' }, top: 0, right: 0, icon: 'circle', itemWidth: 12 },
    grid: { left: '2%', right: '4%', bottom: '2%', top: '15%', containLabel: true },
    xAxis: { type: 'category', data: chartData.trend.categories, axisLine: { lineStyle: { color: '#333' } }, axisLabel: { color: '#999', fontFamily: 'monospace', fontSize: 13, fontWeight: 'bold' }, boundaryGap: false },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)', type: 'dashed' } }, axisLabel: { color: '#999', fontFamily: 'monospace', fontSize: 13, fontWeight: 'bold' } },
    series: [
      {
        name: '粗放经验基准排放', type: 'line', data: chartData.trend.baseline, symbol: 'none',
        lineStyle: { color: '#4b5563', width: 2, type: 'dashed' }
      },
      {
        name: 'AI模型调度实际排放', type: 'line', data: chartData.trend.actual, symbol: 'circle', symbolSize: 8,
        itemStyle: { color: '#10b981', borderColor: '#fff', borderWidth: 2, shadowColor: '#10b981', shadowBlur: 10 },
        lineStyle: { color: '#10b981', width: 3, shadowColor: 'rgba(16,185,129,0.5)', shadowBlur: 10 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(16, 185, 129, 0.4)' },
            { offset: 1, color: 'rgba(16, 185, 129, 0)' }
          ])
        }
      }
    ]
  });

  const gradientColors = [
    new echarts.graphic.LinearGradient(0, 0, 1, 0, [{ offset: 0, color: 'rgba(14,165,233,0.2)' }, { offset: 1, color: '#0ea5e9' }]),
    new echarts.graphic.LinearGradient(0, 0, 1, 0, [{ offset: 0, color: 'rgba(16,185,129,0.2)' }, { offset: 1, color: '#10b981' }]),
    new echarts.graphic.LinearGradient(0, 0, 1, 0, [{ offset: 0, color: 'rgba(245,158,11,0.2)' }, { offset: 1, color: '#f59e0b' }]),
    new echarts.graphic.LinearGradient(0, 0, 1, 0, [{ offset: 0, color: 'rgba(239,68,68,0.2)' }, { offset: 1, color: '#ef4444' }])
  ];

  const formattedBarData = chartData.reduction.map((item, idx) => ({
    value: item.value,
    itemStyle: { color: gradientColors[idx % gradientColors.length] }
  }));

  reductionChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(10, 12, 10, 0.95)',
      borderColor: 'rgba(255,255,255,0.1)',
      textStyle: { color: '#fff', fontSize: 14, fontFamily: 'monospace', fontWeight: 'bold' }
    },
    // 核心修复3：去掉了 left: 160px，改用 2%，利用 containLabel 自动适应宽度，柱子向左靠齐！
    grid: { left: '2%', right: '15%', bottom: '2%', top: '5%', containLabel: true },
    xAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)', type: 'dashed' } }, axisLabel: { color: '#999', fontFamily: 'monospace', fontSize: 13, fontWeight: 'bold' }, show: false },
    yAxis: {
      type: 'category',
      data: chartData.reduction.map(item => item.name),
      axisLine: { show: false },
      axisTick: { show: false },
      // 缩小左侧分类标签字体，确保在窄列里不溢出
      axisLabel: { color: '#cbd5e1', fontFamily: 'monospace', fontSize: 12, fontWeight: 'bold' }
    },
    series: [{
      name: '削减量', type: 'bar', barWidth: '40%',
      data: formattedBarData,
      itemStyle: { borderRadius: [0, 4, 4, 0] },
      label: { show: true, position: 'right', color: '#fff', fontFamily: 'monospace', fontSize: 14, fontWeight: 'bold' }
    }]
  });
};

onMounted(async () => {
  initCharts();
  await fetchEsgDashboardData();
  setInterval(fetchEsgDashboardData, 3000);
  window.addEventListener('resize', handleResize);
});

const handleResize = () => {
  if (trendChart) trendChart.resize();
  if (reductionChart) reductionChart.resize();
};

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (trendChart) trendChart.dispose();
  if (reductionChart) reductionChart.dispose();
});
</script>

<style scoped>
.view-animate { animation: fadeIn 0.5s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* 页面主滚动条样式 */
.custom-scrollbar::-webkit-scrollbar { width: 8px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.4); }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(52, 211, 153, 0.5); border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(52, 211, 153, 0.9); }

.log-list-enter-active,
.log-list-leave-active {
  transition: all 0.5s ease;
}
.log-list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.log-list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>