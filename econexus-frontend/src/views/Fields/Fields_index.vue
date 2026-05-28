<template>
  <div class="p-8 min-h-screen relative text-white" style="background-image: url('https://images.unsplash.com/photo-1542224566-6e85f2e6772f?q=80&w=2000&auto=format&fit=crop'); background-size: cover; background-position: center;">

    <div class="absolute inset-0 bg-gradient-to-br from-eco-dark/95 via-black/80 to-eco-dark/95 backdrop-blur-sm z-0"></div>

    <div class="relative z-10">
      <h2 class="text-2xl font-bold mb-6 border-l-4 border-eco-primary pl-4 tracking-wider">农田生态孪生节点监测</h2>

      <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div class="xl:col-span-2 eco-card h-[600px] flex items-center justify-center relative overflow-hidden group">
          <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-20"></div>
          <div class="z-10 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-eco-primary mx-auto mb-3 opacity-50 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" /></svg>
            <span class="text-eco-primary font-mono tracking-widest text-sm bg-black/50 px-4 py-2 rounded-full border border-eco-primary/30 shadow-[0_0_10px_rgba(52,211,153,0.2)]">[ GIS 空间测绘引擎挂载中 ]</span>
          </div>
        </div>

        <div class="space-y-4 h-[600px] overflow-y-auto pr-2 custom-scrollbar">
          <div v-for="field in fields" :key="field.id"
               @click="openDetail(field)"
               class="eco-card border-l-4 cursor-pointer hover:border-l-eco-primary hover:-translate-x-1 duration-300"
               :class="field.status === '健康' ? 'border-l-eco-primary' : 'border-l-red-500'">
            <div class="flex justify-between items-center mb-3">
              <span class="font-bold text-lg tracking-wide text-white group-hover:text-eco-primary transition-colors">{{ field.name }}</span>
              <span class="text-xs px-2 py-1 bg-black/40 rounded border border-white/5 shadow-inner" :class="field.status === '健康' ? 'text-eco-primary' : 'text-red-400'">{{ field.status }}</span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-xs text-eco-text bg-black/20 p-2 rounded border border-white/5 font-mono">
              <div>湿度: <span class="text-white">{{ field.moisture }}%</span></div>
              <div>虫情: <span class="text-white">{{ field.pestIndex }}</span></div>
              <div>叶绿素: <span class="text-white">{{ field.spad }}</span></div>
              <div>温度: <span class="text-white">{{ field.temp }}°C</span></div>
            </div>
            <div class="mt-3 text-right">
              <span class="text-eco-primary font-mono text-xs opacity-60 hover:opacity-100 transition-opacity flex items-center justify-end gap-1">
                点击展开全息剖析 <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="closeModal"></div>

        <div class="bg-eco-dark/95 border border-eco-primary/30 rounded-2xl w-full max-w-2xl p-8 relative z-10 shadow-[0_0_50px_rgba(0,0,0,0.8)]">
          <button @click="closeModal" class="absolute top-5 right-5 text-gray-500 hover:text-eco-primary transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>

          <div class="border-b border-white/10 pb-4 mb-6">
            <h3 class="text-2xl font-bold text-white flex items-center gap-3">
              <span class="w-1.5 h-6 bg-eco-primary rounded shadow-[0_0_8px_#34d399]"></span>
              {{ selectedField?.name }}
              <span class="text-sm font-normal text-eco-text bg-eco-primary/10 px-2 py-0.5 rounded border border-eco-primary/20">深度剖析报告</span>
            </h3>
            <p class="text-xs text-gray-500 font-mono mt-2 flex gap-4">
              <span>节点 ID: {{ selectedField?.id }}</span>
              <span>最新同步: {{ new Date().toLocaleTimeString() }}</span>
            </p>
          </div>

          <div class="grid grid-cols-2 gap-6 font-mono text-sm">
            <div class="space-y-4">
              <h4 class="text-eco-text text-xs border-b border-white/5 pb-1 uppercase tracking-widest">土壤核心养分 (NPK)</h4>
              <div class="bg-black/40 p-3 rounded-lg border border-white/5 flex justify-between items-center group hover:border-eco-primary/30 transition-colors">
                <span class="text-gray-400 group-hover:text-white transition-colors">土壤全氮 (N)</span>
                <span class="text-white font-bold text-lg">{{ selectedField?.n }} <span class="text-xs font-normal text-gray-500">mg/kg</span></span>
              </div>
              <div class="bg-black/40 p-3 rounded-lg border border-white/5 flex justify-between items-center group hover:border-eco-primary/30 transition-colors">
                <span class="text-gray-400 group-hover:text-white transition-colors">有效磷 (P)</span>
                <span class="text-white font-bold text-lg">{{ selectedField?.p }} <span class="text-xs font-normal text-gray-500">mg/kg</span></span>
              </div>
              <div class="bg-black/40 p-3 rounded-lg border border-white/5 flex justify-between items-center group hover:border-eco-primary/30 transition-colors">
                <span class="text-gray-400 group-hover:text-white transition-colors">速效钾 (K)</span>
                <span class="text-white font-bold text-lg">{{ selectedField?.k }} <span class="text-xs font-normal text-gray-500">mg/kg</span></span>
              </div>
            </div>

            <div class="space-y-4">
              <h4 class="text-eco-text text-xs border-b border-white/5 pb-1 uppercase tracking-widest">端侧设备链路</h4>
              <div class="bg-black/40 p-4 rounded-lg border border-white/5 h-[190px] overflow-y-auto space-y-3 custom-scrollbar">
                <div class="flex justify-between items-center bg-white/5 p-2 rounded border border-white/5 hover:bg-white/10 transition-colors">
                  <div class="flex flex-col">
                    <span class="text-gray-300 text-xs">5G 虫情微型监测灯</span>
                    <span class="text-[10px] text-gray-500">MAC: 0A:1B:2C...</span>
                  </div>
                  <span class="text-eco-primary text-xs flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-eco-primary animate-pulse"></span> 活跃</span>
                </div>
                <div class="flex justify-between items-center bg-white/5 p-2 rounded border border-white/5 hover:bg-white/10 transition-colors">
                  <div class="flex flex-col">
                    <span class="text-gray-300 text-xs">根系层墒情传感器</span>
                    <span class="text-[10px] text-gray-500">MAC: 0A:1B:2D...</span>
                  </div>
                  <span class="text-eco-primary text-xs flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-eco-primary animate-pulse"></span> 活跃</span>
                </div>
                 <div class="flex justify-between items-center bg-white/5 p-2 rounded border border-white/5 hover:bg-white/10 transition-colors">
                  <div class="flex flex-col">
                    <span class="text-gray-300 text-xs">LoRa 滴灌控制阀</span>
                    <span class="text-[10px] text-gray-500">MAC: 0A:1B:2E...</span>
                  </div>
                  <span class="text-gray-500 text-xs flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-gray-500"></span> 休眠</span>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-8 flex justify-end gap-3">
            <button class="px-4 py-2 rounded text-sm text-gray-400 hover:text-white transition-colors border border-transparent hover:border-gray-600">
              导出分析报告
            </button>
            <button @click="closeModal" class="bg-eco-primary/10 border border-eco-primary/50 text-eco-primary px-6 py-2 rounded text-sm font-bold hover:bg-eco-primary hover:text-eco-dark transition-all shadow-[0_0_10px_rgba(52,211,153,0.1)] hover:shadow-[0_0_15px_rgba(52,211,153,0.4)]">
              关闭视窗
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 扩展后的多维度模拟数据
const fields = ref([
  { id: 'F-001', name: 'A区-核心稻田', status: '健康', moisture: 45, pestIndex: '低', spad: 42.1, temp: 26.5, n: 142, p: 35, k: 120 },
  { id: 'F-002', name: 'B区-试验田', status: '预警', moisture: 32, pestIndex: '高', spad: 38.5, temp: 28.2, n: 98, p: 20, k: 85 },
  { id: 'F-003', name: 'C区-果林套种', status: '健康', moisture: 55, pestIndex: '无', spad: 45.0, temp: 25.1, n: 160, p: 40, k: 135 },
  { id: 'F-004', name: 'D区-育秧温室', status: '健康', moisture: 60, pestIndex: '低', spad: 40.2, temp: 29.0, n: 155, p: 45, k: 140 }
]);

// 弹窗控制逻辑
const isModalOpen = ref(false);
const selectedField = ref(null);

const openDetail = (field) => {
  selectedField.value = field;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  setTimeout(() => {
    selectedField.value = null;
  }, 300); // 配合 CSS 过渡动画延迟清空数据
};
</script>

<style scoped>
/* 弹窗渐隐渐现动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 工业级暗色滚动条 */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(52, 211, 153, 0.3);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(52, 211, 153, 0.6);
}
</style>