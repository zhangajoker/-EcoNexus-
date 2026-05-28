<template>
  <div class="h-full flex flex-col md:flex-row gap-6 p-2 text-white">

    <div class="flex-1 space-y-6 bg-black/20 p-4 rounded-xl border border-white/5">
      <h4 class="text-sm font-bold text-eco-primary mb-4 flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" /></svg>
        环境参数调节阀
      </h4>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-xs text-eco-text mb-1">未来24h气象</label>
          <div class="relative">
            <select v-model="weather" class="w-full bg-black/40 border border-eco-border rounded p-2 text-sm text-white appearance-none focus:outline-none focus:border-eco-primary transition-colors cursor-pointer">
              <option value="晴朗" class="bg-eco-dark text-white">持续晴朗 (高蒸发)</option>
              <option value="多云" class="bg-eco-dark text-white">多云间晴</option>
              <option value="降雨" class="bg-eco-dark text-white">降雨过程</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-eco-primary">
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
            </div>
          </div>
        </div>

        <div>
          <label class="block text-xs text-eco-text mb-1">当前作物生长期</label>
          <div class="relative">
            <select v-model="growthStage" class="w-full bg-black/40 border border-eco-border rounded p-2 text-sm text-white appearance-none focus:outline-none focus:border-eco-primary transition-colors cursor-pointer">
              <option value="分蘖期" class="bg-eco-dark text-white">分蘖期 (需氮量大)</option>
              <option value="拔节期" class="bg-eco-dark text-white">拔节期 (水肥敏感)</option>
              <option value="抽穗期" class="bg-eco-dark text-white">抽穗期 (需水量大)</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-eco-primary">
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
            </div>
          </div>
        </div>
      </div>

      <div>
        <div class="flex justify-between text-xs text-eco-text mb-1">
          <label>实时根系土壤湿度</label>
          <span class="text-white font-mono">{{ moisture }}%</span>
        </div>
        <input type="range" v-model="moisture" min="10" max="80" class="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500 hover:accent-blue-400 transition-all">
        <div class="flex justify-between text-[10px] text-gray-500 mt-1">
          <span>干旱 (10%)</span>
          <span>饱和 (80%)</span>
        </div>
      </div>

      <div>
        <div class="flex justify-between text-xs text-eco-text mb-1">
          <label>当前土壤全氮 (N) 评估</label>
          <span class="text-white font-mono">{{ nitrogen }} mg/kg</span>
        </div>
        <input type="range" v-model="nitrogen" min="50" max="250" class="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-green-500 hover:accent-green-400 transition-all">
        <div class="flex justify-between text-[10px] text-gray-500 mt-1">
          <span>贫瘠 (50)</span>
          <span>富营养 (250)</span>
        </div>
      </div>
    </div>

    <div class="flex-1 flex flex-col gap-4">

      <div class="bg-blue-900/10 border border-blue-500/30 p-4 rounded-xl relative overflow-hidden group">
        <div class="absolute right-0 top-0 w-16 h-16 bg-blue-500/10 rounded-bl-full -z-10 group-hover:scale-125 transition-transform duration-500"></div>
        <h4 class="text-xs text-blue-400 mb-1 font-bold flex items-center gap-1.5">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
          AI 靶向灌溉指令
        </h4>
        <div class="text-xl font-bold tracking-wide mt-2" :class="aiIrrigation.color">
          {{ aiIrrigation.command }}
        </div>
        <p class="text-[11px] text-gray-400 mt-1">{{ aiIrrigation.reason }}</p>
      </div>

      <div class="bg-green-900/10 border border-green-500/30 p-4 rounded-xl relative overflow-hidden group">
        <div class="absolute right-0 top-0 w-16 h-16 bg-green-500/10 rounded-bl-full -z-10 group-hover:scale-125 transition-transform duration-500"></div>
        <h4 class="text-xs text-eco-primary mb-1 font-bold flex items-center gap-1.5">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
          AI 精准追肥建议
        </h4>
        <div class="text-xl font-bold tracking-wide mt-2" :class="aiFertilizer.color">
          {{ aiFertilizer.command }}
        </div>
        <p class="text-[11px] text-gray-400 mt-1">{{ aiFertilizer.reason }}</p>
      </div>

      <div class="mt-auto bg-black/40 border border-white/10 p-3 rounded-lg">
        <h4 class="text-[10px] text-gray-400 uppercase tracking-widest mb-2 border-b border-white/5 pb-1">预估单次调控效益</h4>
        <div class="flex justify-between text-xs font-mono">
          <span class="text-blue-300">节水: {{ ecoBenefits.waterSaved }} 吨/亩</span>
          <span class="text-green-300">减排: {{ ecoBenefits.fertilizerSaved }} kg/亩</span>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const weather = ref('晴朗');
const growthStage = ref('拔节期');
const moisture = ref(42);
const nitrogen = ref(142);

const aiIrrigation = computed(() => {
  if (weather.value === '降雨') {
    return { command: '0 mm - 暂停灌溉', reason: '预判有效降水将补充墒情，开启排水防涝预案', color: 'text-gray-300' };
  }
  if (moisture.value > 65) {
    return { command: '0 mm - 无需灌溉', reason: '根系层土壤含水率已达饱和度', color: 'text-gray-300' };
  }
  if (weather.value === '晴朗' && moisture.value < 40) {
    let amount = growthStage.value === '抽穗期' ? '25' : '15';
    return { command: `${amount} mm - 启动滴灌`, reason: '强蒸腾作用且墒情亏缺，触发临界补水阈值', color: 'text-blue-400' };
  }
  return { command: '5 mm - 维持性微灌', reason: '弥补日均蒸散发(ETc)损耗，保持适宜墒情', color: 'text-blue-300' };
});

const aiFertilizer = computed(() => {
  if (nitrogen.value > 180) {
    return { command: '0 kg - 停止追肥', reason: '土壤全氮过剩，继续施肥易导致贪青及水体富营养化', color: 'text-gray-300' };
  }
  if (nitrogen.value < 100) {
    let amount = growthStage.value === '分蘖期' ? '12' : '8';
    return { command: `${amount} kg/亩 - 启动追肥`, reason: '养分亏缺严重，当前生长期急需合成蛋白质', color: 'text-eco-alert' };
  }
  return { command: '监测中 - 暂不施肥', reason: '当前养分储备足以支撑现阶段作物生长', color: 'text-eco-primary' };
});

const ecoBenefits = computed(() => {
  let water = 0;
  if (aiIrrigation.value.command.includes('0 mm')) water = 45;
  else if (aiIrrigation.value.command.includes('滴灌')) water = 20;

  let fert = 0;
  if (aiFertilizer.value.command.includes('0 kg')) fert = 15;
  else if (aiFertilizer.value.command.includes('监测中')) fert = 8;

  return { waterSaved: water, fertilizerSaved: fert };
});
</script>