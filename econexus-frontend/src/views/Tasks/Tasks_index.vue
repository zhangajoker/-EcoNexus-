<template>
  <div class="relative min-h-screen bg-[#0a0c0a] text-white p-8">
    <div class="flex justify-between items-end mb-8 border-b border-white/10 pb-6">
      <div>
        <h2 class="text-2xl font-bold tracking-wider">病虫害风险评估与 AI 防治建议</h2>
        <p class="text-xs text-eco-primary font-mono mt-2 uppercase tracking-widest">YOLOv8 + SAHI Real-time Inference & Decision Support</p>
      </div>
      <div class="flex gap-4">
        <div class="bg-black/40 border border-white/5 px-4 py-2 rounded-xl text-sm font-mono">
          全域高风险区域: <span class="text-red-400 font-bold">1</span>
        </div>
        <div class="bg-black/40 border border-white/5 px-4 py-2 rounded-xl text-sm font-mono">
          识别置信度均值: <span class="text-eco-primary font-bold">94.5%</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div v-for="risk in riskOverview" :key="risk.zone" class="bg-black/40 border border-white/5 p-4 rounded-xl flex justify-between items-center shadow-lg">
        <div>
          <span class="text-xs text-gray-500 block mb-1">{{ risk.zone }} 孪生图像分析</span>
          <span class="text-sm font-bold text-gray-200">{{ risk.crop }}</span>
        </div>
        <span class="text-xs font-mono px-2 py-0.5 rounded border" :class="risk.style">
          {{ risk.status }}
        </span>
      </div>
    </div>

    <div class="space-y-6">
      <div v-for="advice in aiAdvices" :key="advice.id"
           @click="openEvidenceModal(advice)"
           class="bg-black/40 border border-white/5 rounded-2xl p-6 transition-all hover:border-eco-primary/30 cursor-pointer shadow-xl relative overflow-hidden group">

        <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-2 text-eco-primary bg-eco-primary/10 px-3 py-1.5 rounded-lg border border-eco-primary/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
          <span class="text-xs font-bold tracking-wider">点击查看 YOLO 原始推理图像</span>
        </div>

        <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 border-b border-white/5 pb-4 mb-4">
          <div class="flex items-center gap-3">
            <span class="w-2 h-2 rounded-full" :class="advice.level === 'HIGH' ? 'bg-red-500 shadow-[0_0_8px_#ef4444]' : 'bg-yellow-500 shadow-[0_0_8px_#eab308]'"></span>
            <h3 class="text-lg font-bold tracking-wide text-white">{{ advice.title }}</h3>
            <span class="text-xs text-gray-400 font-mono bg-white/5 px-2 py-0.5 rounded border border-white/5">监测点: {{ advice.location }}</span>
          </div>
          <div class="flex items-center gap-4 text-xs font-mono text-gray-500 mr-40">
            <span>特征置信度 (Conf): <span class="text-gray-300">{{ advice.confidence }}</span></span>
            <span>触发时间: <span class="text-gray-300">{{ advice.time }}</span></span>
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
              <span class="text-white font-bold">{{ advice.pesticideReduction }}</span>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3">
          <button @click.stop="rejectAdvice(advice.id)" class="px-4 py-2 rounded text-xs text-gray-500 hover:text-white border border-transparent hover:border-white/10 transition-colors z-10">
            忽略警报
          </button>
          <button @click.stop="approveAdvice(advice.id, advice.actionName)" class="bg-eco-primary/10 border border-eco-primary/40 text-eco-primary px-5 py-2 rounded text-xs font-bold hover:bg-eco-primary hover:text-eco-dark transition-all shadow-[0_0_10px_rgba(52,211,153,0.05)] hover:shadow-[0_0_15px_rgba(52,211,153,0.3)] z-10">
            批准 AI 调控方案
          </button>
        </div>
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
            <h3 class="text-lg font-bold text-white tracking-widest font-mono">YOLOv8 现场推理溯源</h3>
            <span class="text-xs text-gray-500 ml-2">Location: {{ selectedAdvice?.location }}</span>
          </div>

          <div class="relative w-full h-[400px] bg-black rounded-lg border border-white/10 overflow-hidden select-none">
            <img :src="selectedAdvice?.evidenceImage" alt="Field Capture" class="w-full h-full object-cover opacity-80" />

            <div class="absolute inset-0 bg-gradient-to-b from-transparent via-eco-primary/10 to-transparent h-full w-full opacity-50 animate-scan"></div>

            <div v-for="(box, idx) in selectedAdvice?.boundingBoxes" :key="idx"
                 class="absolute border-2 transition-all duration-500 flex items-start"
                 :class="selectedAdvice.level === 'HIGH' ? 'border-red-500 bg-red-500/10' : 'border-yellow-400 bg-yellow-400/10'"
                 :style="{ left: box.x, top: box.y, width: box.w, height: box.h }">
              <div class="absolute -top-6 left-[-2px] px-2 py-0.5 text-[10px] font-mono font-bold text-black"
                   :class="selectedAdvice.level === 'HIGH' ? 'bg-red-500' : 'bg-yellow-400'">
                {{ box.label }} {{ box.conf }}
              </div>

              <div class="absolute -left-1 -top-1 w-2 h-2 border-t-2 border-l-2" :class="selectedAdvice.level === 'HIGH' ? 'border-red-500' : 'border-yellow-400'"></div>
              <div class="absolute -right-1 -bottom-1 w-2 h-2 border-b-2 border-r-2" :class="selectedAdvice.level === 'HIGH' ? 'border-red-500' : 'border-yellow-400'"></div>
            </div>

            <div class="absolute bottom-2 left-2 text-[10px] font-mono text-eco-primary/70">
              FRAME: 004829 | INFERENCE: 14ms | RESOLUTION: 1920x1080
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const riskOverview = ref([
  { zone: 'A区-核心稻田', crop: '水稻（分蘖期）', status: '正常 / 动态监视', style: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' },
  { zone: 'B区-试验田', crop: '水稻（拔节期）', status: '高危 / 建议干预', style: 'bg-red-500/10 text-red-400 border-red-500/20 animate-pulse' },
  { zone: 'C区-果林套种', crop: '柑橘（幼果期）', status: '正常 / 无异常', style: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' }
]);

// 数据中加入了 evidenceImage 和 boundingBoxes 用于渲染弹窗图像
const aiAdvices = ref([
  {
    id: 1,
    level: 'HIGH',
    title: '稻飞虱群落边缘入侵研判',
    location: 'B区-试验田东侧前沿',
    confidence: '97.2%',
    time: '10:42:01',
    analysis: '边缘诱虫采集点通过 SAHI 切片推理算法在前沿叶片检测到高密度小个体稻飞虱聚集（局部特征密度达 142/㎡）。多模态气象模型显示，当前局部风向与湿度极利于该群落向中心腹地蔓延。',
    strategy: '启动边缘阻断方案，控制大疆 T40 无人机对东侧交界带实施精准靶向阻断喷洒，阻止扩散，无需全田普施化学药剂。',
    pesticideReduction: '85%',
    actionName: '无人机边缘阻断喷洒作业',
    evidenceImage: 'https://images.unsplash.com/photo-1596704104273-0941df2a16d5?q=80&w=1200&auto=format&fit=crop',
    boundingBoxes: [
      { x: '45%', y: '30%', w: '18%', h: '25%', label: 'Planthopper', conf: '0.97' },
      { x: '65%', y: '50%', w: '12%', h: '18%', label: 'Planthopper', conf: '0.94' }
    ]
  },
  {
    id: 2,
    level: 'MEDIUM',
    title: '零星蚜虫点状发生趋向提示',
    location: 'A区-核心稻田南部',
    confidence: '94.1%',
    time: '09:12:45',
    analysis: '机器视觉算法在作物中下部叶片提取到点状蚜虫群落特征值，目前尚未达到经济受害阈值（EIL）。但结合未来 48 小时温度微幅回升趋势，存在斑块化扩散的风险。',
    strategy: '当前阶段不建议实施化学药剂干预。建议通过水肥控制阀下调局部湿度，并利用物理诱虫灯调光进行生态压制。',
    pesticideReduction: '100%',
    actionName: '调整局部小气候进行物理生态防治',
    evidenceImage: 'https://images.unsplash.com/photo-1614902120092-211c470aefb4?q=80&w=1200&auto=format&fit=crop',
    boundingBoxes: [
      { x: '35%', y: '40%', w: '15%', h: '15%', label: 'Aphid', conf: '0.94' }
    ]
  }
]);

// 弹窗状态管理
const isModalOpen = ref(false);
const selectedAdvice = ref(null);

const openEvidenceModal = (advice) => {
  selectedAdvice.value = advice;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  setTimeout(() => {
    selectedAdvice.value = null;
  }, 300);
};

const approveAdvice = (id, action) => {
  alert(`生产调度指令已成功下发至现场执行单元\n------------------------\n建议 ID: ${id}\n执行方案: ${action}\n状态: 自动控制链路已通过 LoRa 网关激活，进入精准调控闭环。`);
};

const rejectAdvice = (id) => {
  alert(`已记录忽略反馈。模型将自动优化该区域的特征提取权重，减少过度预警。`);
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 模拟雷达扫描线的动画 */
@keyframes scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}
.animate-scan {
  animation: scan 4s linear infinite;
}
</style>