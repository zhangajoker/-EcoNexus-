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
      <div v-for="advice in aiAdvices" :key="advice.id" class="bg-black/40 border border-white/5 rounded-2xl p-6 transition-all hover:border-eco-primary/20 shadow-xl">

        <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 border-b border-white/5 pb-4 mb-4">
          <div class="flex items-center gap-3">
            <span class="w-2 h-2 rounded-full" :class="advice.level === 'HIGH' ? 'bg-red-500 shadow-[0_0_8px_#ef4444]' : 'bg-yellow-500 shadow-[0_0_8px_#eab308]'"></span>
            <h3 class="text-lg font-bold tracking-wide text-white">{{ advice.title }}</h3>
            <span class="text-xs text-gray-400 font-mono bg-white/5 px-2 py-0.5 rounded border border-white/5">监测点: {{ advice.location }}</span>
          </div>
          <div class="flex items-center gap-4 text-xs font-mono text-gray-500">
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
          <button @click="rejectAdvice(advice.id)" class="px-4 py-2 rounded text-xs text-gray-500 hover:text-white border border-transparent hover:border-white/10 transition-colors">
            忽略警报
          </button>
          <button @click="approveAdvice(advice.id, advice.actionName)" class="bg-eco-primary/10 border border-eco-primary/40 text-eco-primary px-5 py-2 rounded text-xs font-bold hover:bg-eco-primary hover:text-eco-dark transition-all shadow-[0_0_10px_rgba(52,211,153,0.05)] hover:shadow-[0_0_15px_rgba(52,211,153,0.3)]">
            批准 AI 调控方案
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const riskOverview = ref([
  { zone: 'A区-核心稻田', crop: '水稻（分蘖期）', status: '正常 / 动态监视', style: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' },
  { zone: 'B区-试验田', crop: '水稻（拔节期）', status: '高危 / 建议干预', style: 'bg-red-500/10 text-red-400 border-red-500/20 animate-pulse' },
  { zone: 'C区-果林套种', crop: '柑橘（幼果期）', status: '正常 / 无异常', style: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' }
]);

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
    actionName: '无人机边缘阻断喷洒作业'
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
    actionName: '调整局部小气候进行物理生态防治'
  }
]);

const approveAdvice = (id, action) => {
  alert(`生产调度指令已成功下发至现场执行单元\n------------------------\n建议 ID: ${id}\n执行方案: ${action}\n状态: 自动控制链路已通过 LoRa 网关激活，进入精准调控闭环。`);
};

const rejectAdvice = (id) => {
  alert(`已记录忽略反馈。模型将自动优化该区域的特征提取权重，减少过度预警。`);
};
</script>

<style scoped>
/* 自定义滚动条及页面微动效 */
button {
  will-change: transform, shadow;
}
</style>