<template>
  <div class="p-8 min-h-screen relative text-white bg-[#0a0c0a] overflow-hidden select-none">

    <div class="absolute inset-0 z-0">
      <img src="https://images.pexels.com/photos/259280/pexels-photo-259280.jpeg?auto=compress&cs=tinysrgb&w=1600"
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
          <button class="bg-white/5 border border-white/10 px-4 py-2 rounded text-xs font-mono text-gray-400 hover:text-white hover:border-white/30 transition-colors flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            导出年度合规审计报告 (PDF)
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-eco-primary/30 transition-colors">
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-eco-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-gray-500 font-mono tracking-widest uppercase">累计碳减排当量</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-eco-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" /></svg>
          </div>
          <div class="text-3xl font-bold text-white font-mono">1,482.5 <span class="text-sm font-normal text-gray-500">tCO₂e</span></div>
          <div class="mt-2 text-[10px] text-emerald-400">较基准线下降 24.5% ↗</div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-eco-primary/30 transition-colors">
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-eco-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-gray-500 font-mono tracking-widest uppercase">面源污染拦截量</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-eco-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
          </div>
          <div class="text-3xl font-bold text-white font-mono">3,105 <span class="text-sm font-normal text-gray-500">kg (N/P)</span></div>
          <div class="mt-2 text-[10px] text-emerald-400">基于模型精量调度 ↗</div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-blue-400/30 transition-colors">
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-blue-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-gray-500 font-mono tracking-widest uppercase">国家绿色金融评级</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" /></svg>
          </div>
          <div class="text-3xl font-bold text-white font-mono">AAA <span class="text-sm font-normal text-gray-500">级</span></div>
          <div class="mt-2 text-[10px] text-gray-400">合规审计基准达标</div>
        </div>

        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-yellow-400/30 transition-colors">
          <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-yellow-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-gray-500 font-mono tracking-widest uppercase">预估碳汇交易核算</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <div class="text-3xl font-bold text-white font-mono">118,600 <span class="text-sm font-normal text-gray-500">CNY</span></div>
          <div class="mt-2 text-[10px] text-yellow-400">全国碳排放权交易均价映射</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">

        <div class="lg:col-span-2 space-y-6 flex flex-col">
          <div class="bg-black/40 border border-white/5 rounded-none p-6 flex-1 relative">
            <h3 class="text-sm font-mono text-gray-400 tracking-widest mb-4">● 模型驱动下的能耗与碳排放双轨对比 (tCO₂e)</h3>
            <div ref="trendChartRef" class="w-full h-[280px]"></div>
          </div>

          <div class="bg-black/40 border border-white/5 rounded-none p-6 flex-1 relative">
            <h3 class="text-sm font-mono text-gray-400 tracking-widest mb-4">● 靶向狙击与孪生调度：面源污染源削减解构 (kg)</h3>
            <div ref="reductionChartRef" class="w-full h-[220px]"></div>
          </div>
        </div>

        <div class="lg:col-span-1 bg-black/40 border border-white/5 rounded-none p-6 flex flex-col">
          <h3 class="text-sm font-mono text-gray-400 tracking-widest mb-6 border-b border-white/10 pb-4">● 自动调度与合规日志流</h3>

          <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-5 font-mono">

            <div class="relative pl-4 border-l border-eco-primary/30">
              <span class="absolute -left-1.5 top-1 w-3 h-3 bg-black border border-eco-primary rounded-full"></span>
              <div class="text-[10px] text-gray-500 mb-1">2026-05-28 14:30:22 | 靶向干预</div>
              <div class="text-sm text-white mb-1">YOLOv8 模型触发边缘阻断</div>
              <div class="text-xs text-gray-400">取代全田漫洒，模型自动调度植保无人机对 B 区实施点状喷洒。核算节省化学农药 <span class="text-eco-primary">12.4 kg</span>。</div>
            </div>

            <div class="relative pl-4 border-l border-white/10">
              <span class="absolute -left-1.5 top-1 w-3 h-3 bg-black border border-white/30 rounded-full"></span>
              <div class="text-[10px] text-gray-500 mb-1">2026-05-27 09:15:00 | 孪生排程</div>
              <div class="text-sm text-white mb-1">蒸散发模型优化水肥阵列</div>
              <div class="text-xs text-gray-400">基于 Penman-Monteith 方程重算土壤蒸发通量，模型自适应缩减 C 区灌溉时长 45 分钟，截断氮磷流失 <span class="text-blue-400">5.8 kg</span>。</div>
            </div>

            <div class="relative pl-4 border-l border-yellow-400/30">
              <span class="absolute -left-1.5 top-1 w-3 h-3 bg-black border border-yellow-400 rounded-full"></span>
              <div class="text-[10px] text-gray-500 mb-1">2026-05-25 18:00:00 | 资产核对</div>
              <div class="text-sm text-white mb-1">碳汇区块链节点同步完成</div>
              <div class="text-xs text-gray-400">本周期内累计生态贡献数据已打包加密，并通过标准 API 推送至区域碳交易核算中心账本。</div>
            </div>

            <div class="relative pl-4 border-l border-white/10">
              <span class="absolute -left-1.5 top-1 w-3 h-3 bg-black border border-white/30 rounded-full"></span>
              <div class="text-[10px] text-gray-500 mb-1">2026-05-22 11:20:15 | 靶向干预</div>
              <div class="text-sm text-white mb-1">诱虫灯特征提取与物理压制</div>
              <div class="text-xs text-gray-400">SAHI 切片推理确诊高危虫害，模型调度物理灯光灭杀取代化学药剂，核算减少碳排放 <span class="text-eco-primary">0.05 tCO₂e</span>。</div>
            </div>

          </div>

          <div class="mt-6 pt-6 border-t border-white/10">
            <div class="bg-eco-primary/5 border border-eco-primary/20 p-4 relative">
              <div class="text-xs text-eco-primary font-bold mb-2">模型合规判定结果：达标</div>
              <p class="text-[11px] text-gray-400 leading-relaxed">
                当前运行周期内，天衍中枢基于模型自动调度的水肥与病虫害干预策略，完全符合《ESG企业可持续发展报告指令》绿色农业实施标准。
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

const trendChartRef = ref(null);
const reductionChartRef = ref(null);
let trendChart = null;
let reductionChart = null;

const initTrendChart = () => {
  if (!trendChartRef.value) return;
  trendChart = echarts.init(trendChartRef.value);

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(10, 12, 10, 0.9)',
      borderColor: 'rgba(255,255,255,0.1)',
      textStyle: { color: '#fff', fontSize: 12, fontFamily: 'monospace' }
    },
    legend: {
      data: ['粗放经验基准排放', '模型调度实际排放'],
      textStyle: { color: '#888', fontSize: 11, fontFamily: 'monospace' },
      top: 0,
      right: 0,
      icon: 'rect',
      itemWidth: 12,
      itemHeight: 2
    },
    grid: { left: '3%', right: '4%', bottom: '5%', top: '15%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      axisLine: { lineStyle: { color: '#333' } },
      axisLabel: { color: '#666', fontFamily: 'monospace' }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#222', type: 'dashed' } },
      axisLabel: { color: '#666', fontFamily: 'monospace' }
    },
    series: [
      {
        name: '粗放经验基准排放',
        type: 'line',
        data: [120, 132, 145, 160, 180, 210],
        symbol: 'none',
        lineStyle: { color: '#555', width: 2, type: 'dashed' }
      },
      {
        name: '模型调度实际排放',
        type: 'line',
        data: [115, 120, 110, 105, 95, 80],
        symbol: 'circle',
        symbolSize: 6,
        itemStyle: { color: '#10b981' },
        lineStyle: { color: '#10b981', width: 2 }
      }
    ]
  };
  trendChart.setOption(option);
};

const initReductionChart = () => {
  if (!reductionChartRef.value) return;
  reductionChart = echarts.init(reductionChartRef.value);

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(10, 12, 10, 0.9)',
      borderColor: 'rgba(255,255,255,0.1)',
      textStyle: { color: '#fff', fontSize: 12, fontFamily: 'monospace' }
    },
    grid: { left: '3%', right: '4%', bottom: '5%', top: '10%', containLabel: true },
    xAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#222', type: 'dashed' } },
      axisLabel: { color: '#666', fontFamily: 'monospace' }
    },
    yAxis: {
      type: 'category',
      data: ['水资源无效渗漏', '化学除草剂', '无机氮磷肥', '广谱杀虫剂'],
      axisLine: { lineStyle: { color: '#333' } },
      axisLabel: { color: '#888', fontFamily: 'monospace' }
    },
    series: [
      {
        name: '模型干预削减量',
        type: 'bar',
        barWidth: '30%',
        data: [
          { value: 12450, itemStyle: { color: '#3b82f6' } }, // 水资源 (蓝色)
          { value: 420, itemStyle: { color: '#10b981' } },   // 除草剂
          { value: 2105, itemStyle: { color: '#eab308' } },  // 肥料 (黄色)
          { value: 890, itemStyle: { color: '#10b981' } }    // 杀虫剂
        ],
        itemStyle: { borderRadius: [0, 2, 2, 0] }
      }
    ]
  };
  reductionChart.setOption(option);
};

onMounted(() => {
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
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.custom-scrollbar::-webkit-scrollbar { width: 2px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(52, 211, 153, 0.5); }
</style>