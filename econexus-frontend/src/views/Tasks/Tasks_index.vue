<template>
  <div class="relative min-h-screen bg-[#0a0c0a] text-white p-8">
    <div class="flex justify-between items-end mb-8 border-b border-white/10 pb-6">
      <div>
        <h2 class="text-2xl font-bold tracking-wider">病虫害风险评估与 AI 防治建议</h2>
        <p class="text-xs text-eco-primary font-mono mt-2 uppercase tracking-widest">YOLOv8 + SAHI Real-time Inference & Decision Support</p>
      </div>

      <div class="flex items-center gap-6">
        <div class="flex gap-2 bg-white/5 p-1 rounded-xl border border-white/10">
          <button @click="currentTab = 'pending'" :class="currentTab === 'pending' ? 'bg-eco-primary text-black font-bold' : 'text-gray-400 hover:text-white'" class="px-4 py-2 rounded-lg text-xs font-mono transition-all">
            待处理实时告警 ({{ pendingTasks.length }})
          </button>
          <button @click="currentTab = 'history'" :class="currentTab === 'history' ? 'bg-white/10 text-white font-bold' : 'text-gray-400 hover:text-white'" class="px-4 py-2 rounded-lg text-xs font-mono transition-all">
            历史决策日志 ({{ historyTasks.length }})
          </button>
        </div>
        <div class="h-8 w-px bg-white/10"></div>
        <div class="flex gap-4">
          <div class="bg-black/40 border border-white/5 px-4 py-2 rounded-xl text-sm font-mono">
            全域未结告警: <span class="text-red-400 font-bold">{{ pendingTasks.length }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div v-for="risk in riskOverview" :key="risk.zone" class="bg-black/40 border border-white/5 p-4 rounded-xl flex justify-between items-center shadow-lg">
        <div>
          <span class="text-xs text-gray-500 block mb-1">{{ risk.zone }} 孪生空间</span>
          <span class="text-sm font-bold text-gray-200">{{ risk.crop }}</span>
        </div>
        <span class="text-xs font-mono px-2 py-0.5 rounded border" :class="risk.zone.includes('B') && pendingTasks.length > 0 ? 'bg-red-500/10 text-red-400 border-red-500/20 animate-pulse' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'">
          {{ risk.zone.includes('B') && pendingTasks.length > 0 ? '生态受扰 / 待干预' : '环境安全 / 监视中' }}
        </span>
      </div>
    </div>

    <div v-if="currentTab === 'pending' ? pendingTasks.length === 0 : historyTasks.length === 0" class="h-64 flex flex-col items-center justify-center border border-dashed border-white/10 rounded-2xl bg-black/20 text-gray-500 font-mono text-sm tracking-widest">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mb-3 text-gray-600 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
      当前数据列表中无任何日志记录
    </div>

    <div class="space-y-6" v-else>
      <div v-for="advice in (currentTab === 'pending' ? displayedPendingTasks : historyTasks)" :key="advice.id"
           @click="openEvidenceModal(advice)"
           class="bg-black/40 border border-white/5 rounded-2xl p-6 transition-all hover:border-eco-primary/30 cursor-pointer shadow-xl relative overflow-hidden group">

        <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-2 text-eco-primary bg-eco-primary/10 px-3 py-1.5 rounded-lg border border-eco-primary/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
          <span class="text-xs font-bold tracking-wider">点击查阅 YOLO 渲染图文凭证</span>
        </div>

        <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 border-b border-white/5 pb-4 mb-4">
          <div class="flex items-center gap-3">
            <span class="w-2 h-2 rounded-full" :class="advice.level === 'HIGH' ? 'bg-red-500 shadow-[0_0_8px_#ef4444]' : 'bg-yellow-500 shadow-[0_0_8px_#eab308]'"></span>
            <h3 class="text-lg font-bold tracking-wide text-white">{{ advice.title }}</h3>
            <span class="text-xs text-gray-400 font-mono bg-white/5 px-2 py-0.5 rounded border border-white/5">位置: {{ advice.location }}</span>
          </div>
          <div class="flex items-center gap-4 text-xs font-mono text-gray-500 md:mr-44">
            <span>特征置信度: <span class="text-gray-300">{{ advice.confidence }}</span></span>
            <span>触发时序: <span class="text-gray-300">{{ advice.time }}</span></span>
            <span v-if="advice.status !== 'PENDING'" class="px-2 py-0.5 border text-[10px] rounded" :class="advice.status === 'APPROVED' ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/5' : 'text-gray-500 border-white/10 bg-white/5'">
              {{ advice.status === 'APPROVED' ? '决策采纳已归档' : '决策忽略已归档' }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div class="lg:col-span-2 space-y-2">
            <div class="text-[10px] text-gray-500 uppercase tracking-widest font-mono">AI 模型多模态研判结论</div>
            <p class="text-sm text-gray-300 leading-relaxed font-sans bg-black/20 p-4 rounded-xl border border-white/5 min-h-[80px]">
              {{ advice.analysis }}
            </p>
          </div>

          <div class="bg-black/30 p-4 rounded-xl border border-white/5 flex flex-col justify-between">
            <div>
              <div class="text-[10px] text-gray-500 uppercase tracking-widest font-mono mb-2">推荐生态调控方案</div>
              <p class="text-xs text-eco-primary leading-relaxed font-sans">
                {{ advice.strategy }}
              </p>
            </div>
            <div class="text-[10px] text-gray-400 border-t border-white/5 pt-2 mt-3 font-mono flex justify-between">
              <span>预计化学农药减量:</span>
              <span class="text-white font-bold">{{ advice.pesticide_reduction || advice.pesticideReduction }}</span>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3" v-if="advice.status === 'PENDING'">
          <button @click.stop="submitAction(advice.id, 'IGNORED')" class="px-4 py-2 rounded text-xs text-gray-500 hover:text-white border border-transparent hover:border-white/10 transition-colors z-10 font-mono">
            忽略警报
          </button>
          <button @click.stop="submitAction(advice.id, 'APPROVED')" class="bg-eco-primary/10 border border-eco-primary/40 text-eco-primary px-5 py-2 rounded text-xs font-bold hover:bg-eco-primary hover:text-eco-dark transition-all shadow-[0_0_10px_rgba(52,211,153,0.05)] hover:shadow-[0_0_15px_rgba(52,211,153,0.3)] z-10 font-mono">
            批准 AI 调控方案
          </button>
        </div>
      </div>

      <div v-if="currentTab === 'pending' && pendingTasks.length > 2" class="text-center mt-6 mb-4">
        <span class="bg-white/5 border border-white/10 text-gray-400 text-[11px] px-6 py-2.5 rounded-full font-mono shadow-inner inline-flex items-center gap-3">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-yellow-500"></span>
          </span>
          系统队列中还有 <span class="text-white font-bold">{{ pendingTasks.length - 2 }}</span> 个次级告警等待您的处置...
        </span>
      </div>

    </div>

    <transition name="fade">
      <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/90 backdrop-blur-md" @click="closeModal"></div>

        <div class="bg-[#0a0c0a] border border-white/10 rounded-2xl w-full max-w-4xl p-6 relative z-10 shadow-[0_0_50px_rgba(0,0,0,0.8)]">
          <button @click="closeModal" class="absolute top-4 right-4 text-gray-500 hover:text-eco-primary transition-colors z-20">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>

          <div class="flex items-center gap-3 mb-4">
            <span class="w-1.5 h-5 bg-eco-primary rounded"></span>
            <h3 class="text-lg font-bold text-white tracking-widest font-mono">YOLOv8 现场推理溯源舱</h3>
            <span class="text-xs text-gray-500 ml-2">网格定位: {{ selectedAdvice?.location }}</span>
          </div>

          <div class="relative w-full h-[450px] bg-black rounded-lg border border-white/10 overflow-hidden select-none flex items-center justify-center">
            <template v-if="selectedAdvice?.evidence_image?.endsWith('.mp4') || selectedAdvice?.evidence_image?.endsWith('.webm')">
              <video :src="selectedAdvice?.evidence_image" controls autoplay loop muted class="w-full h-full object-contain"></video>
            </template>
            <template v-else>
              <img :src="selectedAdvice?.evidence_image || selectedAdvice?.evidenceImage" alt="Field Matrix Capture" class="w-full h-full object-contain" />
            </template>

            <div class="absolute inset-0 bg-gradient-to-b from-transparent via-eco-primary/5 to-transparent h-full w-full opacity-30 pointer-events-none animate-scan"></div>

            <div class="absolute bottom-3 left-3 text-[10px] font-mono text-eco-primary/70 bg-black/60 px-2 py-1 border border-white/5 rounded">
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

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const currentTab = ref('pending'); // pending(待处理面板) / history(历史决策日志面板)
const pendingTasks = ref([]);
const historyTasks = ref([]);

const riskOverview = ref([
  { zone: 'A区-核心稻田', crop: '水稻（分蘖期）' },
  { zone: 'B区-试验田区', crop: '水稻（拔节期）' },
  { zone: 'C区-果林套种', crop: '柑橘（幼果期）' }
]);

// 弹窗状态管理
const isModalOpen = ref(false);
const selectedAdvice = ref(null);

// ==========================================
// 【核心修改】：优先队列计算属性 (Priority Queue)
// ==========================================
const displayedPendingTasks = computed(() => {
  // 1. 复制一份数组避免直接修改原响应式数据
  const sortedTasks = [...pendingTasks.value];

  // 2. 排序规则：
  //    先按告警等级排（HIGH 优先于 MEDIUM）
  //    等级相同时，按时间倒序排（最新生成的告警排在前面）
  sortedTasks.sort((a, b) => {
    if (a.level === 'HIGH' && b.level !== 'HIGH') return -1; // a 靠前
    if (a.level !== 'HIGH' && b.level === 'HIGH') return 1;  // b 靠前
    return b.id - a.id; // 等级一样时，新任务(id大)靠前
  });

  // 3. 限制只返回前 2 条
  return sortedTasks.slice(0, 2);
});
// ==========================================

// 从后端同步全量动态告警数据
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

// 提交审批或忽略指令动作
const submitAction = async (id, actionType) => {
  try {
    const res = await axios.post(`${API_BASE}/api/tasks/${id}/action`, { action: actionType });
    if (res.data.status === 'success') {
      // 动作执行完后，重新加载列表，自动把项目划分进历史档案中
      // 下面的任务会自动顶上来！
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
  // 每隔5秒高频自动同步一次后端
  setInterval(loadTasksFromServer, 5000);
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@keyframes scan { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
.animate-scan { animation: scan 5s linear infinite; }
</style>