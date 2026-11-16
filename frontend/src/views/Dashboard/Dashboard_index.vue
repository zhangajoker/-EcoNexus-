<template>
  <div class="relative w-full h-full text-white overflow-hidden font-sans select-none">

    <!-- 材质打底 -->
    <svg class="pointer-events-none fixed inset-0 z-50 h-full w-full opacity-[0.03] mix-blend-overlay">
      <filter id="noiseFilter"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/></filter>
      <rect width="100%" height="100%" filter="url(#noiseFilter)"/>
    </svg>

    <!-- 中心 3D 量子神经元大脑与粒子场 -->
    <canvas ref="threeCanvas" @click="startJarvisVoice" class="absolute inset-0 z-0 opacity-90 cursor-pointer"></canvas>

    <div class="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-cyan-900/20 to-transparent pointer-events-none z-10"></div>

    <main class="absolute inset-0 z-10 flex justify-between p-4 lg:p-6 pointer-events-none min-w-[1024px]">

      <!-- 左侧面板 -->
      <aside class="w-[28vw] min-w-[320px] max-w-[420px] flex flex-col gap-4 lg:gap-6 pointer-events-auto animate-fade-in-left">
        <div class="eco-card group relative">
          <div class="eco-card-texture bg-[url('https://images.unsplash.com/photo-1592982537447-6f296d9e50be?q=80&w=800&auto=format&fit=crop')]"></div>
          <h2 class="eco-card-title"><span class="eco-title-indicator bg-cyan-400"></span> 实时传感网络 (点击溯源)</h2>

          <div class="grid grid-cols-2 gap-4 mt-6">
            <div class="eco-data-block relative overflow-hidden group cursor-crosshair">
              <div class="absolute inset-0 bg-gradient-to-br from-cyan-900/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <span class="text-[11px] text-gray-400 font-mono flex justify-between tracking-widest relative z-10 items-center">
                <span class="flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" :class="isLocating ? 'animate-spin text-yellow-400' : 'text-cyan-400'" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                  {{ locationName }}
                </span>
                <span class="text-cyan-400 text-[10px]" :class="isLocating ? 'opacity-50' : 'animate-pulse'">● LIVE</span>
              </span>
              <div class="flex items-baseline gap-1 mt-3 relative z-10">
                <span class="text-5xl font-black text-cyan-300 drop-shadow-[0_0_15px_#67e8f9] transition-all">{{ weatherData.temp }}</span>
                <span class="text-base text-gray-500 font-bold">°C</span>
              </div>
            </div>

            <div class="eco-data-block relative overflow-hidden group cursor-crosshair">
              <div class="absolute inset-0 bg-gradient-to-br from-blue-900/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <span class="text-[11px] text-gray-400 font-mono flex justify-between tracking-widest relative z-10 items-center">
                <span class="flex items-center gap-1">
                   <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" :class="isLocating ? 'animate-spin text-yellow-400' : 'text-blue-400'" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" /></svg>
                  区域湿度
                </span>
                <span class="text-blue-400 text-[10px]" :class="isLocating ? 'opacity-50' : 'animate-pulse'">● LIVE</span>
              </span>
              <div class="flex items-baseline gap-1 mt-3 relative z-10">
                <span class="text-5xl font-black text-blue-300 drop-shadow-[0_0_15px_#93c5fd] transition-all">{{ weatherData.humidity }}</span>
                <span class="text-base text-gray-500 font-bold">%</span>
              </div>
            </div>

            <div @click="openDrillDown('moisture')" class="eco-data-block cursor-pointer hover:border-emerald-500/60 hover:bg-emerald-900/30 transition-all shadow-lg group/btn">
              <span class="text-sm text-gray-400 font-mono flex justify-between group-hover/btn:text-emerald-400 transition-colors tracking-widest font-bold">土壤水势 ⇲</span>
              <div class="flex items-baseline gap-1 mt-3">
                <span class="text-5xl font-black text-emerald-300 drop-shadow-[0_0_15px_#34d399]">{{ dashboardData.moisture }}</span>
                <span class="text-base text-gray-500 font-bold">%</span>
              </div>
            </div>
            <div @click="openDrillDown('nitrogen')" class="eco-data-block cursor-pointer hover:border-teal-500/60 hover:bg-teal-900/30 transition-all shadow-lg group/btn">
              <span class="text-sm text-gray-400 font-mono flex justify-between group-hover/btn:text-teal-400 transition-colors tracking-widest font-bold">氮肥利用率 ⇲</span>
              <div class="flex items-baseline gap-1 mt-3">
                <span class="text-5xl font-black text-teal-300 drop-shadow-[0_0_15px_#5eead4]">{{ dashboardData.nitrogen }}</span>
                <span class="text-base text-gray-500 font-bold">%</span>
              </div>
            </div>
          </div>
        </div>

        <div class="eco-card group relative flex-1">
           <div class="eco-card-texture bg-[url('https://images.unsplash.com/photo-1592982537447-6f296d9e50be?q=80&w=800&auto=format&fit=crop')]"></div>
           <h2 class="eco-card-title"><span class="eco-title-indicator bg-emerald-400"></span> 动态趋势推演 (后端下发)</h2>
          <div ref="trendChartRef" class="w-full h-full min-h-[180px] lg:min-h-[220px] mt-2"></div>
        </div>
      </aside>

      <!-- 中心雷达扫描标靶 (根据交互状态改变颜色) -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none w-[45vw] h-[45vw] max-w-[650px] max-h-[650px] opacity-30 flex items-center justify-center transition-colors duration-500"
           :class="jarvisState === 'listening' ? 'text-amber-500' : 'text-cyan-500'">
        <div class="w-full h-full rounded-full border border-current opacity-30 animate-[spin_20s_linear_infinite]"></div>
        <div class="absolute w-[85%] h-[85%] rounded-full border border-dashed border-current opacity-40 animate-[spin_15s_linear_infinite_reverse]"></div>
      </div>

      <!-- 中心文字唤醒提示区 -->
      <div class="absolute top-[42%] left-1/2 -translate-x-1/2 -translate-y-1/2 z-20 flex flex-col items-center pointer-events-none">
        <div @click="startJarvisVoice" class="pointer-events-auto cursor-pointer group flex flex-col items-center mt-32">

          <div @click.stop="toggleAIChat" class="mb-4 px-5 py-2 rounded-full bg-cyan-950/80 border border-cyan-400/60 backdrop-blur text-cyan-300 font-mono text-xs shadow-[0_0_25px_rgba(8,145,178,0.5)] hover:scale-105 transition-all flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
            开启手动终端
          </div>

          <div class="px-8 py-4 rounded-2xl backdrop-blur-xl font-mono text-center shadow-2xl transition-all duration-300 border-2"
               :class="{
                 'bg-cyan-950/40 border-cyan-500/20 text-cyan-400': jarvisState === 'idle',
                 'bg-amber-950/80 border-amber-400 text-amber-300 scale-110 shadow-[0_0_50px_rgba(245,158,11,0.5)]': jarvisState === 'listening',
                 'bg-emerald-950/80 border-emerald-400 text-emerald-300 scale-105 shadow-[0_0_50px_rgba(16,185,129,0.5)]': jarvisState === 'thinking'
               }">

            <div v-if="jarvisState === 'idle'" class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg>
              <span class="text-sm font-bold tracking-widest">点击任意区域 或按空格 唤醒声控</span>
            </div>

            <div v-else-if="jarvisState === 'listening'" class="flex flex-col items-center gap-2">
              <div class="flex gap-1 mb-1">
                <span class="w-1.5 h-6 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite]"></span>
                <span class="w-1.5 h-8 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite_0.2s]"></span>
                <span class="w-1.5 h-10 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite_0.4s]"></span>
                <span class="w-1.5 h-8 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite_0.6s]"></span>
                <span class="w-1.5 h-6 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite_0.8s]"></span>
              </div>
              <span class="text-sm font-bold tracking-widest text-amber-200 uppercase">正在聆听指令...</span>
              <span class="text-xs text-amber-500/80 mt-1 max-w-[300px] truncate">"{{ currentTranscript }}"</span>
            </div>

            <div v-else-if="jarvisState === 'thinking'" class="flex flex-col items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              <span class="text-sm font-bold tracking-widest text-emerald-200 uppercase">语义解析与路由规划中...</span>
            </div>

          </div>
        </div>
      </div>

      <transition name="modal-fade">
        <div v-if="isAIActive"
             ref="modalRef"
             :style="{ left: modalPos.x + 'px', top: modalPos.y + 'px', transform: 'none' }"
             class="absolute z-[300] w-[800px] h-[600px] bg-[#030712]/95 backdrop-blur-2xl border-2 border-cyan-500/60 rounded-2xl shadow-[0_0_100px_rgba(8,145,178,0.7)] pointer-events-auto flex flex-col font-mono overflow-hidden">

          <div @mousedown="startDrag" class="cursor-move flex justify-between items-center border-b border-cyan-500/30 p-5 bg-cyan-900/30 hover:bg-cyan-900/50 transition-colors">
            <div class="flex items-center gap-4 pointer-events-none">
              <span class="w-4 h-4 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_15px_#22d3ee]"></span>
              <h3 class="text-2xl font-bold text-cyan-200 tracking-widest">天衍生境交互终端 (手动模式)</h3>
            </div>
            <button @click="isAIActive = false" class="text-gray-400 hover:text-cyan-300 text-4xl font-bold px-2 cursor-pointer leading-none">×</button>
          </div>

          <div ref="chatScrollRef" class="flex-1 overflow-y-auto space-y-5 p-6 custom-scrollbar text-base">
            <div class="p-4 rounded-xl bg-cyan-950/40 border border-cyan-500/30 text-cyan-100">
              <span class="text-cyan-400 font-bold block mb-2 text-lg">Nexus-Agent:</span>
              您好！您可以向我提问系统状态，或者直接对我说：“帮我切换到 ESG 页面”。
            </div>
            <div v-for="(msg, idx) in chatMessages" :key="idx" class="p-4 rounded-xl border shadow-lg" :class="msg.role === 'user' ? 'bg-white/5 border-white/10 text-right text-gray-100 ml-16' : 'bg-cyan-950/50 border-cyan-500/40 text-cyan-50 mr-16'">
              <span class="font-bold block mb-2 text-lg tracking-wider" :class="msg.role === 'user' ? 'text-gray-400' : 'text-cyan-400'">{{ msg.role === 'user' ? '操作员' : 'Nexus-Agent' }}</span>
              <p class="font-sans text-lg leading-relaxed whitespace-pre-wrap">{{ msg.content }}</p>
            </div>
          </div>

          <div class="p-5 border-t border-cyan-500/30 bg-black/60 space-y-4">
            <div class="flex gap-4">
              <input v-model="userInput" @keyup.enter="sendManualChat" type="text" placeholder="输入指令..." class="flex-1 bg-black/80 border border-cyan-400/50 rounded-xl px-5 py-4 text-lg text-white focus:outline-none focus:border-cyan-300 font-sans shadow-inner" />
              <button @click="sendManualChat" class="px-10 py-4 bg-cyan-500/20 border-2 border-cyan-400 text-cyan-300 hover:bg-cyan-400 hover:text-black font-black tracking-widest transition-all text-xl rounded-xl shadow-[0_0_20px_rgba(34,211,238,0.4)]">发送</button>
            </div>
          </div>
        </div>
      </transition>

      <!-- 右侧面板 -->
      <aside class="w-[28vw] min-w-[320px] max-w-[420px] flex flex-col gap-4 lg:gap-6 pointer-events-auto animate-fade-in-right">
        <div class="eco-card group relative h-full">
          <div class="eco-card-texture bg-[url('https://images.unsplash.com/photo-1592982537447-6f296d9e50be?q=80&w=800&auto=format&fit=crop')]"></div>
          <div class="flex justify-between items-center mb-4">
             <h2 class="eco-card-title !mb-0"><span class="eco-title-indicator bg-yellow-400 animate-pulse"></span> AI 自动研判中心</h2>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono border border-emerald-500/40 bg-emerald-500/10 text-emerald-400">双引擎协同</span>
          </div>

          <div class="space-y-8 mt-10">
            <div @click="openDrillDown('pest')" class="cursor-pointer p-6 rounded-xl bg-black/60 border border-white/10 hover:border-yellow-500/60 hover:bg-yellow-900/30 transition-all shadow-[0_4px_20px_rgba(0,0,0,0.5)] group/ai">
              <div class="text-base text-gray-400 font-mono mb-4 flex justify-between items-center tracking-widest">
                <span class="group-hover/ai:text-yellow-400 transition-colors font-bold">[Pest Alert] 边缘靶向拦截 ⇲</span>
                <span class="text-yellow-400 font-bold border border-yellow-500/50 px-3 py-1.5 rounded bg-yellow-500/20 drop-shadow-[0_0_5px_rgba(234,179,8,0.6)]">
                  {{ dashboardData.pestStatus }}
                </span>
              </div>
              <p class="text-lg text-gray-200 leading-loose font-sans font-medium">{{ dashboardData.pestAnalysis }}</p>
            </div>

            <div class="p-6 rounded-xl bg-black/60 border border-white/10 hover:border-cyan-500/50 transition-colors shadow-[0_4px_20px_rgba(0,0,0,0.5)]">
              <div class="text-base text-gray-400 font-mono mb-4 flex justify-between tracking-widest">
                <span class="font-bold">[NUE-Ratio] 氮肥转化决策</span>
                <span class="text-cyan-400 font-bold drop-shadow-[0_0_5px_rgba(34,211,238,0.6)]">{{ dashboardData.nitrogenStatus }}</span>
              </div>
              <p class="text-lg text-gray-200 leading-loose font-sans font-medium">{{ dashboardData.nitrogenAnalysis }}</p>
            </div>

            <div class="mt-auto border-t-2 border-white/10 pt-8 flex justify-between items-center">
              <div class="text-lg text-gray-400 font-mono tracking-widest uppercase font-bold">全域生产效能评分</div>
              <div class="text-7xl font-mono font-black text-emerald-400 drop-shadow-[0_0_25px_#34d399]">{{ dashboardData.score }}</div>
            </div>
          </div>
        </div>
      </aside>
    </main>

    <!-- 溯源下钻弹窗 -->
    <transition name="modal-fade">
      <div v-if="isModalOpen" class="fixed inset-0 z-[200] flex items-center justify-center p-4 pointer-events-auto">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="closeModal"></div>
        <div class="eco-card w-full max-w-3xl relative z-10 !bg-[#050b14] !border-cyan-500/50 shadow-[0_0_50px_rgba(8,145,178,0.3)]">
          <button @click="closeModal" class="absolute top-4 right-4 text-gray-500 hover:text-cyan-400 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
          <div class="flex items-center gap-3 mb-6 border-b border-white/10 pb-4">
            <span class="w-1.5 h-6 bg-cyan-400 rounded shadow-[0_0_8px_#22d3ee]"></span>
            <h3 class="text-lg font-bold text-white tracking-widest">{{ drillData.metric_name }}</h3>
          </div>
          <div class="bg-cyan-900/10 border border-cyan-500/20 p-4 rounded-lg mb-6 text-sm text-cyan-100/80 leading-relaxed">
            <span class="font-bold text-cyan-400">AI 溯源诊断：</span>{{ drillData.summary_analysis }}
          </div>
          <div ref="modalChartRef" class="w-full h-[280px] bg-black/40 rounded-lg border border-white/5 mb-4"></div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import * as THREE from 'three';
import * as echarts from 'echarts';
import { API_BASE } from '../../config';


const router = useRouter();

// ==========================================
// 【终极重构】：J.A.R.V.I.S 语音交互引擎
// ==========================================
const jarvisState = ref('idle'); // 'idle' | 'listening' | 'thinking'
const currentTranscript = ref('');

const speakOutLoud = (text) => {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'zh-CN';
  utterance.rate = 1.1;
  utterance.pitch = 1.0;

  utterance.onend = () => {
    jarvisState.value = 'idle';
  };

  window.speechSynthesis.speak(utterance);
};

const startJarvisVoice = () => {
  if (jarvisState.value !== 'idle') return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("您的浏览器不支持原生 Web Speech API。推荐使用 Chrome。");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'zh-CN';
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = () => {
    jarvisState.value = 'listening';
    currentTranscript.value = '';

    if (brainGroup) {
      brainGroup.scale.set(1.5, 1.5, 1.5);
      baseRotationSpeed = 0.02;
    }
  };

  recognition.onresult = (event) => {
    let interim = '';
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        currentTranscript.value += event.results[i][0].transcript;
      } else {
        interim += event.results[i][0].transcript;
      }
    }
    if (interim) currentTranscript.value = interim;
  };

  recognition.onend = async () => {
    if (!currentTranscript.value) {
      jarvisState.value = 'idle';
      resetBrainScale();
      return;
    }

    jarvisState.value = 'thinking';
    if (brainGroup) {
      brainGroup.scale.set(1.2, 1.2, 1.2);
      baseRotationSpeed = 0.005;
    }

    await processVoiceCommand(currentTranscript.value);
  };

  recognition.start();
};

const handleKeyDown = (e) => {
  if (e.code === 'Space' && jarvisState.value === 'idle' && !isAIActive.value) {
    e.preventDefault();
    startJarvisVoice();
  }
};

const processVoiceCommand = async (text) => {
  try {
    const res = await axios.post(`${API_BASE}/api/ai/command`, { prompt: text });

    if (res.data.status === 'success') {
      const { action, target, reply } = res.data.data;

      speakOutLoud(reply);

      if (action === 'navigate' && target !== 'none') {
        setTimeout(() => {
          router.push(target);
          resetBrainScale();
        }, 1500);
      } else {
         setTimeout(resetBrainScale, 1000);
      }

    } else {
      speakOutLoud("抱歉长官，指令格式解析失败。");
      resetBrainScale();
    }
  } catch (error) {
    console.error(error);
    jarvisState.value = 'idle';
    speakOutLoud("网络连接中断，天衍中枢离线。");
    resetBrainScale();
  }
};


// --- 手动文本 AI 终端代码保持 ---
const isAIActive = ref(false);
const userInput = ref('');
const chatMessages = ref([]);
const chatScrollRef = ref(null);

const modalPos = ref({ x: 960 - 400, y: 540 - 300 });
let isDragging = false;
const startDrag = () => { isDragging = true; document.addEventListener('mousemove', onDrag); document.addEventListener('mouseup', stopDrag); };
const onDrag = (e) => { if (!isDragging) return; const scaleX = window.innerWidth / 1920; const scaleY = window.innerHeight / 1080; modalPos.value.x += e.movementX / scaleX; modalPos.value.y += e.movementY / scaleY; };
const stopDrag = () => { isDragging = false; document.removeEventListener('mousemove', onDrag); document.removeEventListener('mouseup', stopDrag); };

const toggleAIChat = () => { isAIActive.value = !isAIActive.value; };
const sendManualChat = async () => {
  if (!userInput.value.trim()) return;
  const question = userInput.value;
  chatMessages.value.push({ role: 'user', content: question });
  userInput.value = '';
  await nextTick();
  if (chatScrollRef.value) chatScrollRef.value.scrollTop = chatScrollRef.value.scrollHeight;

  try {
    const res = await axios.post(`${API_BASE}/api/ai/chat`, { prompt: question });
    chatMessages.value.push({ role: 'assistant', content: res.data.reply });
    speakOutLoud(res.data.reply);
  } catch (e) {
    chatMessages.value.push({ role: 'assistant', content: "网络断开。" });
  }
  await nextTick();
  if (chatScrollRef.value) chatScrollRef.value.scrollTop = chatScrollRef.value.scrollHeight;
};

// ==========================================
// 数据获取与杂项配置
// ==========================================
const weatherData = ref({ temp: '26.5', humidity: '60' });
const locationName = ref('获取定位中');
const isLocating = ref(true);

const fetchWeatherByCoords = async (lat, lon) => {
  try {
    const res = await axios.get(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m&timezone=auto`);
    weatherData.value = { temp: res.data.current.temperature_2m.toFixed(1), humidity: res.data.current.relative_humidity_2m.toString() };
  } catch (error) {}
};

const initDynamicLocationWeather = () => {
  isLocating.value = true;
  locationName.value = '卫星定位扫描中...';
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude; const lon = position.coords.longitude;
        locationName.value = `Local Node [${lat.toFixed(2)}°, ${lon.toFixed(2)}°]`;
        isLocating.value = false;
        await fetchWeatherByCoords(lat, lon);
      },
      (error) => { locationName.value = '默认区域 (Fallback)'; isLocating.value = false; fetchWeatherByCoords(22.3193, 114.1694); },
      { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
    );
  } else {
    locationName.value = '定位离线'; isLocating.value = false; fetchWeatherByCoords(22.3193, 114.1694);
  }
};

const dashboardData = ref({
  score: 95, moisture: '42.8', nitrogen: '82.5', pestStatus: '加载中', pestAnalysis: '连接边缘中枢...', nitrogenStatus: '加载中', nitrogenAnalysis: '初始化...'
});

const trendChartRef = ref(null);
let trendChart = null;

const fetchDashboardData = async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/dashboard/overview`);
    const data = res.data;
    dashboardData.value = {
      score: data.efficiency_score, moisture: data.soil_moisture.current_value, nitrogen: data.nitrogen_efficiency.current_value,
      pestStatus: data.pest_risk.status_tag, pestAnalysis: data.pest_risk.ai_analysis, nitrogenStatus: data.nitrogen_efficiency.status_tag, nitrogenAnalysis: data.nitrogen_efficiency.ai_analysis
    };

    const mBase = parseFloat(data.soil_moisture.current_value) || 42.8; const mData = Array.from({length: 6}, (_, i) => mBase + Math.sin(i) * 2);
    const nBase = parseFloat(data.nitrogen_efficiency.current_value) || 82.5; const nData = Array.from({length: 6}, (_, i) => nBase - Math.cos(i) * 3);

    if (trendChartRef.value) {
      if (!trendChart) trendChart = echarts.init(trendChartRef.value);
      trendChart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(3,7,18,0.9)', borderColor: '#0891b2', textStyle: { color: '#fff' } },
        grid: { left: '3%', right: '5%', bottom: '5%', top: '15%', containLabel: true },
        xAxis: { type: 'category', boundaryGap: false, data: ['-5h', '-4h', '-3h', '-2h', '-1h', 'Now'], axisLabel: { color: '#6b7280' } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)', type: 'dashed' } } },
        series: [
          { name: '土壤水势', type: 'line', smooth: true, symbol: 'none', data: mData, lineStyle: { width: 3, color: '#34d399', shadowBlur: 10, shadowColor: '#34d399' } },
          { name: 'NUE转化率', type: 'line', smooth: true, symbol: 'none', data: nData, lineStyle: { width: 3, color: '#22d3ee', shadowBlur: 10, shadowColor: '#22d3ee' } }
        ]
      });
    }
  } catch (e) {}
};

const isModalOpen = ref(false);
const drillData = ref({ metric_name: '', summary_analysis: '', timeline_data: [], device_status: [] });
const modalChartRef = ref(null);
let modalChart = null;

const openDrillDown = async (id) => {
  isModalOpen.value = true;
  try {
    const res = await axios.get(`${API_BASE}/api/dashboard/drill-down/${id}`);
    drillData.value = res.data;
    await nextTick();
    if (!modalChartRef.value) return;
    if (modalChart) modalChart.dispose();
    modalChart = echarts.init(modalChartRef.value);
    const color = id === 'pest' ? '#eab308' : (id === 'moisture' ? '#34d399' : '#22d3ee');
    modalChart.setOption({
      tooltip: { trigger: 'axis', backgroundColor: 'rgba(0,0,0,0.9)' },
      grid: { left: '3%', right: '4%', bottom: '5%', top: '10%', containLabel: true },
      xAxis: { type: 'category', boundaryGap: false, data: res.data.timeline_data.map((i)=>i.time), axisLabel: { color: '#9ca3af' } },
      yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }, min: 'dataMin' },
      series: [{
        data: res.data.timeline_data.map((i)=>i.value), type: 'line', smooth: true, symbol: 'none',
        lineStyle: { color, width: 3, shadowBlur: 10, shadowColor: color },
        areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: `${color}66` }, { offset: 1, color: 'transparent' }]) }
      }]
    });
  } catch (e) {}
};

const closeModal = () => { isModalOpen.value = false; if (modalChart) { modalChart.dispose(); modalChart = null; } };

// ==========================================
// Three.js 联动引擎
// ==========================================
const threeCanvas = ref(null);
let renderer, scene, camera;
let brainGroup;
let particles;
let animationFrameId;

let baseRotationSpeed = 0.003;

const resetBrainScale = () => {
  if (brainGroup) {
    brainGroup.scale.set(1, 1, 1);
    baseRotationSpeed = 0.003;
  }
};

const initThreeJS = () => {
  if (!threeCanvas.value) return;

  const SCREEN_W = 1920; const SCREEN_H = 1080;
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(50, SCREEN_W / SCREEN_H, 0.1, 1000);
  camera.position.z = 45; camera.position.y = -3;

  renderer = new THREE.WebGLRenderer({ canvas: threeCanvas.value, alpha: true, antialias: true });
  renderer.setSize(SCREEN_W, SCREEN_H); renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  brainGroup = new THREE.Group();

  const coreGeo = new THREE.IcosahedronGeometry(6, 2);
  const coreMat = new THREE.MeshBasicMaterial({ color: 0x0891b2, wireframe: true, transparent: true, opacity: 0.15 });
  brainGroup.add(new THREE.Mesh(coreGeo, coreMat));

  const shellGeo = new THREE.IcosahedronGeometry(9, 1);
  const shellMat = new THREE.MeshBasicMaterial({ color: 0x34d399, wireframe: true, transparent: true, opacity: 0.25 });
  brainGroup.add(new THREE.Mesh(shellGeo, shellMat));

  const ringMat = new THREE.MeshBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.3, side: THREE.DoubleSide });
  const ring1 = new THREE.Mesh(new THREE.TorusGeometry(14, 0.05, 16, 100), ringMat);
  const ring2 = new THREE.Mesh(new THREE.TorusGeometry(17, 0.05, 16, 100), ringMat);
  const ring3 = new THREE.Mesh(new THREE.TorusGeometry(20, 0.05, 16, 100), ringMat);

  ring1.rotation.x = Math.PI / 2; ring2.rotation.y = Math.PI / 3; ring3.rotation.x = Math.PI / 4;
  brainGroup.add(ring1, ring2, ring3);
  scene.add(brainGroup);

  const particlesGeometry = new THREE.BufferGeometry();
  const posArray = new Float32Array(1500 * 3);
  for(let i = 0; i < 4500; i++) posArray[i] = (Math.random() - 0.5) * 120;
  particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
  particles = new THREE.Points(particlesGeometry, new THREE.PointsMaterial({ size: 0.2, color: 0x6ee7b7, transparent: true, opacity: 0.5, blending: THREE.AdditiveBlending }));
  scene.add(particles);

  let mouseX = 0, mouseY = 0;
  document.addEventListener('mousemove', (e) => { mouseX = (e.clientX - window.innerWidth / 2) * 0.03; mouseY = (e.clientY - window.innerHeight / 2) * 0.03; });

  const animate = () => {
    animationFrameId = requestAnimationFrame(animate);

    brainGroup.rotation.y += baseRotationSpeed;
    brainGroup.rotation.x += (baseRotationSpeed / 3);
    ring1.rotation.z += (baseRotationSpeed * 1.5);
    ring2.rotation.z -= (baseRotationSpeed * 1.2);
    ring3.rotation.z += (baseRotationSpeed * 0.8);

    const positions = particles.geometry.attributes.position.array;
    for(let i = 1; i < 4500; i += 3) {
      positions[i] += (baseRotationSpeed * 10);
      if (positions[i] > 60) positions[i] = -60;
    }
    particles.geometry.attributes.position.needsUpdate = true;

    camera.position.x += (mouseX - camera.position.x) * 0.05;
    camera.position.y += (-mouseY - camera.position.y) * 0.05;
    camera.lookAt(scene.position);
    renderer.render(scene, camera);
  };
  animate();
};

onMounted(() => {
  initThreeJS();
  fetchDashboardData();
  setInterval(fetchDashboardData, 5000);
  initDynamicLocationWeather();

  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  if (animationFrameId) cancelAnimationFrame(animationFrameId);
  renderer?.dispose();
  if (trendChart) trendChart.dispose();
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<style>
.eco-card { @apply relative p-4 lg:p-6 rounded-2xl bg-[#0a1120]/80 backdrop-blur-xl border border-cyan-900/40 shadow-[0_8px_32px_rgba(0,0,0,0.5)] overflow-hidden; }
.eco-card-texture { @apply absolute inset-0 opacity-[0.08] mix-blend-screen pointer-events-none transition-opacity duration-500 group-hover:opacity-[0.15]; filter: sepia(1) hue-rotate(130deg) saturate(300%); }
.eco-card-title { @apply relative z-10 text-sm font-bold text-gray-200 flex items-center gap-2 tracking-widest mb-4; }
.eco-title-indicator { @apply w-1.5 h-4 rounded-full shadow-[0_0_8px_currentColor]; }
.eco-data-block { @apply relative z-10 p-3 rounded-lg bg-white/[0.02] border border-white/10 backdrop-blur-sm; }

@keyframes fadeInLeft { from { transform: translateX(-50px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.animate-fade-in-left { animation: fadeInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; opacity: 0; }
@keyframes fadeInRight { from { transform: translateX(50px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.animate-fade-in-right { animation: fadeInRight 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.3s; opacity: 0; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.95) translateY(20px); }
</style>