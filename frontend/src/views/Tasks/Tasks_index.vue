<template>
  <div class="relative min-h-screen bg-[#0a0c0a] text-white select-none pb-32"> <!-- 增加了底部 padding 防遮挡 -->

    <div class="flex justify-between items-end mb-10 border-b border-white/10 pb-8 px-8 pt-8 shrink-0">
      <div>
        <h2 class="text-4xl font-bold tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.5)]">病虫害风险评估与 AI 防治建议</h2>
        <p class="text-xl font-bold text-eco-primary font-mono mt-3 uppercase tracking-widest">YOLOv8 + SAHI Real-time Inference & Decision Support</p>
      </div>
      <div class="flex items-center gap-8">
        <div class="flex gap-2 bg-white/5 p-1.5 rounded-xl border border-white/10">
          <!-- 标签页文字放大 -->
          <button @click="currentTab = 'pending'" :class="currentTab === 'pending' ? 'bg-eco-primary text-black font-bold' : 'text-gray-400 hover:text-white'" class="px-6 py-3 rounded-lg text-base font-mono transition-all">
            待处理实时告警 ({{ pendingTasks.length }})
          </button>
          <button @click="currentTab = 'history'" :class="currentTab === 'history' ? 'bg-white/10 text-white font-bold' : 'text-gray-400 hover:text-white'" class="px-6 py-3 rounded-lg text-base font-mono transition-all">
            历史决策日志 ({{ historyTasks.length }})
          </button>
        </div>
        <div class="h-10 w-px bg-white/10"></div>
        <div class="flex gap-4">
          <div class="bg-black/40 border border-white/5 px-6 py-3 rounded-xl text-base font-mono flex items-center gap-3">
            全域未结告警: <span class="text-red-400 font-bold text-2xl drop-shadow-[0_0_8px_#ef4444]">{{ pendingTasks.length }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 风险总览卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 px-8 mb-10 shrink-0">
      <div v-for="risk in riskOverview" :key="risk.zone" class="bg-black/40 border border-white/5 p-6 rounded-xl flex justify-between items-center shadow-lg hover:border-white/20 transition-all group">
        <div>
          <!-- 文字放大 -->
          <span class="text-sm text-gray-400 block mb-2 font-mono uppercase tracking-wider group-hover:text-gray-300">{{ risk.zone }} 孪生空间</span>
          <span class="text-xl font-bold text-gray-100">{{ risk.crop }}</span>
        </div>
        <!-- 标签文字放大 -->
        <span class="text-sm font-mono px-3 py-1.5 rounded border font-bold"
              :class="risk.zone.includes('B') && pendingTasks.length > 0 ? 'bg-red-500/10 text-red-400 border-red-500/30 animate-pulse shadow-[0_0_15px_rgba(239,68,68,0.2)]' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'">
          {{ risk.zone.includes('B') && pendingTasks.length > 0 ? '生态受扰 / 待干预' : '环境安全 / 监视中' }}
        </span>
      </div>
    </div>

    <div v-if="currentTab === 'pending' ? pendingTasks.length === 0 : historyTasks.length === 0" class="mx-8 h-80 flex flex-col items-center justify-center border-2 border-dashed border-white/10 rounded-2xl bg-black/20 text-gray-500 font-mono text-lg tracking-widest">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4 text-gray-600 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
      当前数据列表中无任何日志记录
    </div>

    <!-- 任务卡片列表区 -->
    <div class="space-y-8 px-8 flex-1" v-else>
      <div v-for="advice in (currentTab === 'pending' ? displayedPendingTasks : historyTasks)" :key="advice.id"
           @click="openEvidenceModal(advice)"
           class="bg-black/40 border border-white/5 rounded-2xl p-8 transition-all hover:border-eco-primary/40 hover:bg-[#081210]/50 cursor-pointer shadow-[0_10px_30px_rgba(0,0,0,0.5)] relative overflow-hidden group">

        <!-- 悬浮查看证据按钮放大 -->
        <div class="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-2 text-eco-primary bg-eco-primary/10 px-4 py-2 rounded-lg border border-eco-primary/30 shadow-[0_0_15px_rgba(52,211,153,0.2)]">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
          <span class="text-sm font-bold tracking-wider">点击查阅 YOLO 渲染图文凭证</span>
        </div>

        <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 border-b border-white/10 pb-6 mb-6">
          <div class="flex items-center gap-4">
            <span class="w-3 h-3 rounded-full" :class="advice.level === 'HIGH' ? 'bg-red-500 shadow-[0_0_12px_#ef4444] animate-pulse' : 'bg-yellow-500 shadow-[0_0_12px_#eab308]'"></span>
            <!-- 标题极度放大 -->
            <h3 class="text-2xl font-bold tracking-wide text-white">{{ advice.title }}</h3>
            <span class="text-sm text-gray-300 font-mono bg-white/10 px-3 py-1 rounded border border-white/10">位置: {{ advice.location }}</span>
          </div>
          <div class="flex items-center gap-6 text-sm font-mono text-gray-400 md:mr-56">
            <span>特征置信度: <span class="text-gray-100 font-bold text-base">{{ advice.confidence }}</span></span>
            <span>触发时序: <span class="text-gray-100 font-bold text-base">{{ advice.time }}</span></span>
            <span v-if="advice.status !== 'PENDING'" class="px-3 py-1 border text-xs font-bold rounded" :class="advice.status === 'APPROVED' ? 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10' : 'text-gray-400 border-white/20 bg-white/10'">
              {{ advice.status === 'APPROVED' ? '决策采纳已归档' : '决策忽略已归档' }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">

          <div class="lg:col-span-2 space-y-3">
            <div class="text-sm text-gray-400 uppercase tracking-widest font-mono font-bold flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-gray-400 rounded-full"></span> AI 模型多模态研判结论
            </div>
            <!-- 大模型回复文字加倍放大，提升行距 -->
            <p class="text-lg text-gray-200 leading-relaxed font-sans bg-black/40 p-6 rounded-xl border border-white/10 min-h-[100px] shadow-inner">
              {{ advice.analysis }}
            </p>
          </div>

          <div class="bg-gradient-to-br from-black/60 to-[#0a1512]/60 p-6 rounded-xl border border-emerald-500/20 flex flex-col justify-between shadow-[inset_0_0_20px_rgba(16,185,129,0.05)]">
            <div>
              <div class="text-sm text-emerald-500/80 uppercase tracking-widest font-mono mb-4 font-bold flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                推荐生态调控方案
              </div>
              <!-- 建议文字放大 -->
              <p class="text-base text-emerald-300 leading-relaxed font-sans font-bold">
                {{ advice.strategy }}
              </p>
            </div>
            <div class="text-sm text-gray-400 border-t border-emerald-500/20 pt-4 mt-6 font-mono flex justify-between items-center">
              <span>预计化学农药减量:</span>
              <span class="text-white font-black text-xl drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]">{{ advice.pesticide_reduction || advice.pesticideReduction }}</span>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-4" v-if="advice.status === 'PENDING'">
          <button @click.stop="submitAction(advice.id, 'IGNORED')" class="px-6 py-3 rounded-lg text-sm font-bold text-gray-400 hover:text-white border border-white/10 hover:bg-white/5 transition-colors z-10 font-mono">
            忽略警报 (Discard)
          </button>
          <!-- 按钮巨大化 -->
          <button @click.stop="submitAction(advice.id, 'APPROVED')" class="bg-emerald-950 border border-emerald-500/50 text-emerald-400 px-8 py-3 rounded-lg text-sm font-black tracking-widest hover:bg-emerald-500 hover:text-black transition-all shadow-[0_0_20px_rgba(16,185,129,0.1)] hover:shadow-[0_0_30px_rgba(16,185,129,0.5)] z-10 font-mono">
            批准执行 AI 调控方案 >>
          </button>
        </div>
      </div>

      <div v-if="currentTab === 'pending' && pendingTasks.length > 2" class="text-center mt-10 mb-8">
        <span class="bg-white/5 border border-white/10 text-gray-300 text-sm px-8 py-3.5 rounded-full font-mono shadow-inner inline-flex items-center gap-3">
          <span class="relative flex h-3 w-3">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-yellow-500"></span>
          </span>
          系统队列中还有 <span class="text-yellow-400 font-black text-lg mx-1">{{ pendingTasks.length - 2 }}</span> 个次级告警等待您的处置...
        </span>
      </div>

    </div>

    <!-- 凭证弹窗保持原样但增加了尺寸适应 -->
    <transition name="fade">
      <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/90 backdrop-blur-md" @click="closeModal"></div>

        <div class="bg-[#0a0c0a] border border-cyan-500/30 rounded-2xl w-full max-w-5xl p-8 relative z-10 shadow-[0_0_80px_rgba(8,145,178,0.4)]">
          <button @click="closeModal" class="absolute top-6 right-6 text-gray-500 hover:text-cyan-400 transition-colors z-20">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>

          <div class="flex items-center gap-4 mb-6">
            <span class="w-2 h-6 bg-cyan-400 rounded shadow-[0_0_10px_#22d3ee]"></span>
            <h3 class="text-xl font-bold text-white tracking-widest font-mono">YOLOv8 现场推理溯源舱</h3>
            <span class="text-sm font-bold text-cyan-500/70 ml-4 font-mono">网格定位: {{ selectedAdvice?.location }}</span>
          </div>

          <div class="relative w-full h-[550px] bg-black rounded-xl border border-white/10 overflow-hidden select-none flex items-center justify-center">
            <template v-if="selectedAdvice?.evidence_image?.endsWith('.mp4') || selectedAdvice?.evidence_image?.endsWith('.webm')">
              <video :src="selectedAdvice?.evidence_image" controls autoplay loop muted class="w-full h-full object-contain"></video>
            </template>
            <template v-else>
              <img :src="selectedAdvice?.evidence_image || selectedAdvice?.evidenceImage" alt="Field Matrix Capture" class="w-full h-full object-contain" />
            </template>

            <div class="absolute inset-0 bg-gradient-to-b from-transparent via-cyan-500/10 to-transparent h-full w-full opacity-40 pointer-events-none animate-scan"></div>

            <div class="absolute bottom-4 left-4 text-xs font-mono text-cyan-400/80 bg-black/80 px-3 py-1.5 border border-cyan-500/30 rounded">
              EDGE GATEWAY LINK READY | FRAME INDEXED | REAL-TIME RENDERED VIA TENSORRT
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { API_BASE } from '../../config';



const currentTab = ref('pending');
const pendingTasks = ref([]);
const historyTasks = ref([]);

const riskOverview = ref([
  { zone: 'A区-核心稻田', crop: '水稻（分蘖期）' },
  { zone: 'B区-试验田区', crop: '水稻（拔节期）' },
  { zone: 'C区-果林套种', crop: '柑橘（幼果期）' }
]);

const isModalOpen = ref(false);
const selectedAdvice = ref(null);

const displayedPendingTasks = computed(() => {
  const sortedTasks = [...pendingTasks.value];
  sortedTasks.sort((a, b) => {
    if (a.level === 'HIGH' && b.level !== 'HIGH') return -1;
    if (a.level !== 'HIGH' && b.level === 'HIGH') return 1;
    return b.id - a.id;
  });
  return sortedTasks.slice(0, 2);
});

const loadTasksFromServer = async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/tasks`);
    if (Array.isArray(res.data)) {
      pendingTasks.value = res.data.filter(t => t.status === 'PENDING');
      historyTasks.value = res.data.filter(t => t.status !== 'PENDING');
    }
  } catch (error) {
    console.error('中枢任务同步故障:', error);
  }
};

const submitAction = async (id, actionType) => {
  try {
    const res = await axios.post(`${API_BASE}/api/tasks/${id}/action`, { action: actionType });
    if (res.data.status === 'success') {
      await loadTasksFromServer();
    } else {
      alert(`异常信息: ${res.data.message}`);
    }
  } catch (error) {
    console.error('边缘网关下达控制流失败:', error);
    alert('同步网络指令超时，请检查后端网关是否就绪');
  }
};

const openEvidenceModal = (advice) => {
  selectedAdvice.value = advice;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  setTimeout(() => { selectedAdvice.value = null; }, 300);
};

onMounted(() => {
  loadTasksFromServer();
  setInterval(loadTasksFromServer, 5000);
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@keyframes scan { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
.animate-scan { animation: scan 3s linear infinite; }
</style>