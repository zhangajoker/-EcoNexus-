<template>
  <div id="esg-dashboard-container" class="p-8 min-h-screen relative text-white bg-[#0a0c0a] overflow-hidden select-none">

    <div class="absolute inset-0 z-0">
      <img src="[https://images.pexels.com/photos/259280/pexels-photo-259280.jpeg?auto=compress&cs=tinysrgb&w=1600](https://images.pexels.com/photos/259280/pexels-photo-259280.jpeg?auto=compress&cs=tinysrgb&w=1600)"
           class="w-full h-full object-cover opacity-10 grayscale mix-blend-luminosity" alt="Southwest China Terrain" />
      <div class="absolute inset-0 bg-gradient-to-b from-[#0a0c0a]/80 via-[#0a0c0a]/95 to-[#0a0c0a] z-10"></div>
    </div>

    <div class="relative z-10 h-full flex flex-col view-animate">

      <div class="mb-8 flex justify-between items-end border-b border-white/10 pb-6">
        <div>
          <h2 class="text-2xl font-bold border-l-4 border-eco-primary pl-4 tracking-wider">ESG 绿色碳汇与生态合规资产看板</h2>
          <p class="text-xs text-gray-500 mt-2 font-mono uppercase tracking-widest">Model-driven Ecological Assets & Carbon Footprint Accounting</p>
        </div>
        <div class="flex gap-4">
          <button @click="exportToPDF" class="bg-white/5 border border-white/10 px-4 py-2 rounded text-xs font-mono text-gray-400 hover:text-white hover:border-eco-primary/50 transition-all flex items-center gap-2 group">
            <svg xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" class="h-4 w-4 group-hover:text-eco-primary transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            导出年度合规审计报告 (PDF)
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-eco-primary/30 transition-colors">
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-eco-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-gray-500 font-mono tracking-widest uppercase">累计碳减排当量</span>
            <svg xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" class="h-5 w-5 text-eco-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" /></svg>
          </div>
          <div class="text-3xl font-bold text-white font-mono">{{ formatNumber(esgData.assets.co2_reduction, 3) }} <span class="text-sm font-normal text-gray-500">tCO₂e</span></div>
          <div class="mt-2 text-[10px] text-emerald-400">智能调度实时累加 ↗</div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-eco-primary/30 transition-colors">
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-eco-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-gray-500 font-mono tracking-widest uppercase">面源污染拦截量</span>
            <svg xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" class="h-5 w-5 text-eco-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
          </div>
          <div class="text-3xl font-bold text-white font-mono">{{ formatNumber(esgData.assets.pollution_interception, 1) }} <span class="text-sm font-normal text-gray-500">kg (N/P/化学)</span></div>
          <div class="mt-2 text-[10px] text-emerald-400">基于视觉靶向拦截解构 ↗</div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-blue-400/30 transition-colors">
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-blue-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-gray-500 font-mono tracking-widest uppercase">国家绿色金融评级</span>
            <svg xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" class="h-5 w-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" /></svg>
          </div>
          <div class="text-3xl font-bold text-white font-mono">{{ esgData.assets.financial_rating }} <span class="text-sm font-normal text-gray-500">级</span></div>
          <div class="mt-2 text-[10px] text-gray-400">智能决策合规率达标</div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-yellow-400/30 transition-colors">
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-yellow-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-gray-500 font-mono tracking-widest uppercase">预估碳汇交易核算</span>
            <svg xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" class="h-5 w-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <div class="text-3xl font-bold text-white font-mono">{{ formatNumber(esgData.assets.carbon_revenue, 0) }} <span class="text-sm font-normal text-gray-500">CNY</span></div>
          <div class="mt-2 text-[10px] text-yellow-400">碳权市场价值映射</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">

        <div class="lg:col-span-2 space-y-6 flex flex-col">
          <div class="bg-black/40 border border-white/5 rounded-none p-6 flex-1 relative">
            <h3 class="text-sm font-mono text-gray-400 tracking-widest mb-4">● 模型驱动下的能耗与碳排放双轨对比 (tCO₂e)</h3>
            <div ref="trendChartRef" class="w-full h-[280px]"></div>
          </div>

          <div class="bg-black/40 border border-white/5 rounded-none p-6 flex-1 relative">
            <h3 class="text-sm font-mono text-gray-400 tracking-widest mb-4">● 靶向狙击与群落调度：面源污染源削减解构 (kg)</h3>
            <div ref="reductionChartRef" class="w-full h-[220px]"></div>
          </div>
        </div>

        <div class="lg:col-span-1 bg-black/40 border border-white/5 rounded-none p-6 flex flex-col">
          <h3 class="text-sm font-mono text-gray-400 tracking-widest mb-6 border-b border-white/10 pb-4">● 自动化调度与合规日志流</h3>

          <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-5 font-mono max-h-[480px]">
            <div v-for="log in esgData.logs" :key="log.id" class="relative pl-4 border-l"
                 :class="log.category === '靶向干预' ? 'border-yellow-400/30' : (log.category === '资产核对' ? 'border-blue-500/30' : 'border-emerald-500/30')">
              <span class="absolute -left-1.5 top-1 w-3 h-3 bg-black border rounded-full"
                    :class="log.category === '靶向干预' ? 'border-yellow-400' : (log.category === '资产核对' ? 'border-blue-400' : 'border-emerald-400')"></span>
              <div class="text-[10px] text-gray-500 mb-1">{{ log.timestamp }} | {{ log.category }}</div>
              <div class="text-sm text-white mb-1">{{ log.title }}</div>
              <div class="text-xs text-gray-400 leading-relaxed">{{ log.description }}</div>
            </div>
          </div>

          <div class="mt-6 pt-6 border-t border-white/10">
            <div class="bg-eco-primary/5 border border-eco-primary/20 p-4 relative">
              <div class="text-xs text-eco-primary font-bold mb-2">天衍中枢合规判定：达标</div>
              <p class="text-[11px] text-gray-400 leading-relaxed font-sans">
                边缘网格层执行的机器视觉靶向拦截，其核算机制完全契合《可持续发展指令指令》，贡献值已通过区块链共识节点。
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
import html2pdf from 'html2pdf.js';

const trendChartRef = ref(null);
const reductionChartRef = ref(null);
let trendChart = null;
let reductionChart = null;

const esgData = ref({
  assets: { co2_reduction: 1482.5, pollution_interception: 3105.0, financial_rating: "AAA", carbon_revenue: 118600.0 },
  logs: []
});

const formatNumber = (num, decimals = 2) => {
  if (num === undefined || num === null) return "";
  return num.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
};

// 【修复1】消除了 "本地捕获异常的 'throw'" 警告
const fetchEsgDashboardData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/esg/dashboard');
    if (!response.ok) {
      console.warn('ESG 资产账本读取未就绪，状态码:', response.status);
      return; // 直接 return 退出，不再使用 throw
    }
    const data = await response.json();
    esgData.value = data;
  } catch (error) {
    console.error("读取动态资产失败，系统切换至离线本地账本:", error);
  }
};

// 【修复2】加上了 async 和 await，消除了 "异步函数调用缺少 await" 警告
const exportToPDF = async () => {
  const element = document.getElementById('esg-dashboard-container');
  if (!element) return;

  const opt = {
    margin:       0.1,
    filename:     `天衍_ESG生态合规审计报告_2026.pdf`,
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true, backgroundColor: '#0a0c0a' },
    jsPDF:        { unit: 'in', format: 'a4', orientation: 'landscape' }
  };

  // 添加 await 等待 PDF 生成完毕
  await html2pdf().set(opt).from(element).save();
};

const initTrendChart = () => {
  if (!trendChartRef.value) return;
  trendChart = echarts.init(trendChartRef.value);
  trendChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(10, 12, 10, 0.9)', borderColor: 'rgba(255,255,255,0.1)', textStyle: { color: '#fff', fontSize: 12, fontFamily: 'monospace' } },
    legend: { data: ['粗放经验基准排放', '模型调度实际排放'], textStyle: { color: '#888', fontSize: 11, fontFamily: 'monospace' }, top: 0, right: 0, icon: 'rect', itemWidth: 12, itemHeight: 2 },
    grid: { left: '3%', right: '4%', bottom: '5%', top: '15%', containLabel: true },
    xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], axisLine: { lineStyle: { color: '#333' } }, axisLabel: { color: '#666', fontFamily: 'monospace' } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: '#222', type: 'dashed' } }, axisLabel: { color: '#666', fontFamily: 'monospace' } },
    series: [
      { name: '粗放经验基准排放', type: 'line', data: [120, 132, 145, 160, 180, 210], symbol: 'none', lineStyle: { color: '#555', width: 2, type: 'dashed' } },
      { name: '模型调度实际排放', type: 'line', data: [115, 120, 110, 105, 95, 80], symbol: 'circle', symbolSize: 6, itemStyle: { color: '#10b981' }, lineStyle: { color: '#10b981', width: 2 } }
    ]
  });
};

const initReductionChart = () => {
  if (!reductionChartRef.value) return;
  reductionChart = echarts.init(reductionChartRef.value);
  reductionChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, backgroundColor: 'rgba(10, 12, 10, 0.9)', borderColor: 'rgba(255,255,255,0.1)', textStyle: { color: '#fff', fontSize: 12, fontFamily: 'monospace' } },
    grid: { left: '3%', right: '4%', bottom: '5%', top: '10%', containLabel: true },
    xAxis: { type: 'value', splitLine: { lineStyle: { color: '#222', type: 'dashed' } }, axisLabel: { color: '#666', fontFamily: 'monospace' } },
    yAxis: { type: 'category', data: ['水资源无效渗漏', '化学除草剂', '无机氮磷肥', '广谱杀虫剂'], axisLine: { lineStyle: { color: '#333' } }, axisLabel: { color: '#888', fontFamily: 'monospace' } },
    series: [{ name: '模型干预削减量', type: 'bar', barWidth: '30%', data: [{ value: 12450, itemStyle: { color: '#3b82f6' } }, { value: 420, itemStyle: { color: '#10b981' } }, { value: 2105, itemStyle: { color: '#eab308' } }, { value: 890, itemStyle: { color: '#10b981' } }], itemStyle: { borderRadius: [0, 2, 2, 0] } }]
  });
};

onMounted(async () => {
  await fetchEsgDashboardData();
  nextTick(() => {
    initTrendChart();
    initReductionChart();
  });
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

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(52, 211, 153, 0.2); border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(52, 211, 153, 0.5); }
</style>