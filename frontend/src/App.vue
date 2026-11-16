<template>
  <!-- 最外层容器：铺满浏览器窗口，溢出隐藏，背景设置为深色调 -->
  <div class="w-screen h-screen overflow-hidden bg-[#030712] relative flex flex-col font-sans text-white">
    
    <!-- 核心大屏容器：尺寸永远固定 1920x1080，由内部 JS 控制缩放比例 -->
    <div 
      ref="screenRef" 
      class="absolute top-1/2 left-1/2 origin-center transition-transform duration-300 flex flex-col"
      style="width: 1920px; height: 1080px;"
    >
      
      <!-- 全局悬浮科幻导航 (美化放大版) -->
      <header class="relative shrink-0 h-24 z-[100] flex items-center justify-between px-10 bg-[#0a1120]/95 backdrop-blur-md border-b border-cyan-900/50 shadow-[0_4px_30px_rgba(8,145,178,0.2)]">
        <div class="flex items-center gap-4">
          <div class="scale-75 origin-left -mr-2"><EcoLogo /></div>
          <div class="flex flex-col">
            <span class="text-3xl font-black tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.5)]">
              天衍·生境
            </span>
            <span class="text-xs text-cyan-500/60 font-mono tracking-widest mt-1">EcoNexus OS v3.0</span>
          </div>
        </div>

        <nav class="flex gap-6">
          <router-link to="/" class="nav-btn">主控看板</router-link>
          <router-link to="/fields" class="nav-btn">农田孪生</router-link>
          <router-link to="/tasks" class="nav-btn">AI防治调度</router-link>
          <router-link to="/esg" class="nav-btn">ESG碳汇资产</router-link>
          <router-link to="/settings" class="nav-btn">边缘节点运维</router-link>
        </nav>

        <div class="font-mono text-cyan-400 text-xl tracking-widest flex items-center gap-3 drop-shadow-[0_0_5px_rgba(34,211,238,0.5)]">
          <span class="relative flex h-3 w-3">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
          </span>
          {{ currentTime }}
        </div>
      </header>

      <!-- 动态路由视图 -->
      <main class="flex-1 relative w-full h-full overflow-hidden">
        <router-view v-slot="{ Component }">
          <transition name="cyber-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <!-- ==================================================== -->
      <!-- 【新增】全局悬浮 J.A.R.V.I.S 语音交互终端 (UI 部分) -->
      <!-- ==================================================== -->
      <div class="fixed bottom-12 right-12 z-[9999] flex flex-col items-end gap-6 pointer-events-none">

        <transition name="slide-up">
          <div v-if="jarvisState !== 'idle'" class="pointer-events-auto bg-[#050b14]/90 backdrop-blur-xl border-2 p-6 rounded-2xl shadow-2xl w-[380px] transition-all duration-300"
               :class="jarvisState === 'listening' ? 'border-amber-500/50 shadow-[0_0_40px_rgba(245,158,11,0.3)]' : 'border-emerald-500/50 shadow-[0_0_40px_rgba(16,185,129,0.3)]'">

            <div v-if="jarvisState === 'listening'" class="flex flex-col gap-3">
              <div class="flex items-center gap-3 mb-2">
                <div class="flex gap-1">
                  <span class="w-1 h-4 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite]"></span>
                  <span class="w-1 h-6 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite_0.2s]"></span>
                  <span class="w-1 h-8 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite_0.4s]"></span>
                  <span class="w-1 h-6 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite_0.6s]"></span>
                  <span class="w-1 h-4 bg-amber-400 rounded-full animate-[bounce_0.8s_infinite_0.8s]"></span>
                </div>
                <span class="text-amber-400 font-bold tracking-widest font-mono text-sm">正在接收指令...</span>
              </div>
              <div class="text-white/80 font-sans text-lg min-h-[60px] italic">
                "{{ currentTranscript || '请说话...' }}"
              </div>
            </div>

            <div v-else-if="jarvisState === 'thinking'" class="flex flex-col gap-3">
              <div class="flex items-center gap-3 mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                <span class="text-emerald-400 font-bold tracking-widest font-mono text-sm">LLM 意图解析中...</span>
              </div>
              <div class="text-white/60 font-mono text-xs">
                正在通过大模型中枢执行语义路由匹配与生产资料调取。
              </div>
            </div>
          </div>
        </transition>

        <button @click="startJarvisVoice"
                class="pointer-events-auto relative group flex items-center justify-center w-20 h-20 rounded-full border-2 transition-all duration-500 shadow-2xl"
                :class="jarvisState === 'idle' ? 'bg-cyan-950 border-cyan-400 shadow-[0_0_20px_rgba(34,211,238,0.3)] hover:scale-110 hover:shadow-[0_0_40px_rgba(34,211,238,0.6)]' : 'bg-black border-amber-400 scale-110 shadow-[0_0_30px_rgba(245,158,11,0.5)]'">

          <div v-if="jarvisState === 'idle'" class="absolute w-full h-full rounded-full border border-cyan-400/50 animate-ping opacity-50"></div>

          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 relative z-10 transition-colors duration-300" :class="jarvisState === 'idle' ? 'text-cyan-400' : 'text-amber-400'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>

          <span class="absolute right-24 whitespace-nowrap bg-black/80 border border-cyan-900 px-4 py-2 rounded text-xs font-mono text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity">
            按 Alt+V 或点击唤醒
          </span>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import EcoLogo from '@/components/EcoLogo.vue';
import { API_BASE } from './config';


const router = useRouter();

// ====================================================
// 基础逻辑：时钟与大屏自适应
// ====================================================
const currentTime = ref('');
let timer: ReturnType<typeof setInterval>;

const updateTime = () => {
  const now = new Date();
  const date = now.toLocaleDateString('zh-CN').replace(/\//g, '.');
  const time = now.toLocaleTimeString('zh-CN', { hour12: false });
  currentTime.value = `${date} | ${time}`;
};

const screenRef = ref<HTMLElement | null>(null);
const DESIGN_WIDTH = 1920;
const DESIGN_HEIGHT = 1080;

const handleResize = () => {
  if (!screenRef.value) return;
  const scaleX = window.innerWidth / DESIGN_WIDTH;
  const scaleY = window.innerHeight / DESIGN_HEIGHT;
  const scale = Math.min(scaleX, scaleY);
  screenRef.value.style.transform = `translate(-50%, -50%) scale(${scale})`;
};

// ====================================================
// 全局 J.A.R.V.I.S 语音交互中枢引擎 (TypeScript 兼容版)
// ====================================================
type JarvisState = 'idle' | 'listening' | 'thinking';
const jarvisState = ref<JarvisState>('idle');
const currentTranscript = ref('');

// TTS: 语音播报
const speakOutLoud = (text: string) => {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'zh-CN';
  utterance.rate = 1.1;
  utterance.pitch = 1.0;

  utterance.onend = () => { jarvisState.value = 'idle'; };
  window.speechSynthesis.speak(utterance);
};

// STT: 语音识别
const startJarvisVoice = () => {
  if (jarvisState.value !== 'idle') return;

  // 处理 TypeScript 的 window 属性类型检查
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
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
  };

  recognition.onresult = (event: any) => {
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
      return;
    }
    jarvisState.value = 'thinking';
    await processVoiceCommand(currentTranscript.value);
  };

  recognition.start();
};

// LLM 意图解析与执行
const processVoiceCommand = async (text: string) => {
  try {
    const res = await axios.post(`${API_BASE}/api/ai/command`, { prompt: text });

    if (res.data.status === 'success') {
      const { action, target, reply } = res.data.data;
      speakOutLoud(reply);

      if (action === 'navigate' && target !== 'none') {
        setTimeout(() => {
          router.push(target);
        }, 1500);
      } else {
         setTimeout(() => { jarvisState.value = 'idle'; }, 1000);
      }
    } else {
      speakOutLoud("抱歉长官，指令格式解析失败。");
      jarvisState.value = 'idle';
    }
  } catch (error) {
    console.error(error);
    speakOutLoud("网络连接中断，天衍中枢离线。");
    jarvisState.value = 'idle';
  }
};

// 全局快捷键唤醒 (Alt + V)
const handleGlobalKeyDown = (e: KeyboardEvent) => {
  const target = e.target as HTMLElement;
  if (target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA')) return;

  if (e.altKey && e.code === 'KeyV' && jarvisState.value === 'idle') {
    e.preventDefault();
    startJarvisVoice();
  }
};

onMounted(() => {
  updateTime();
  timer = setInterval(updateTime, 1000);
  handleResize();
  window.addEventListener('resize', handleResize);
  window.addEventListener('keydown', handleGlobalKeyDown);
});

onUnmounted(() => {
  clearInterval(timer);
  window.removeEventListener('resize', handleResize);
  window.removeEventListener('keydown', handleGlobalKeyDown);
});
</script>

<style>
body { margin: 0; padding: 0; overflow: hidden; background-color: #030712; }

.nav-btn {
  @apply relative px-6 py-3 text-lg font-bold tracking-widest text-gray-400 transition-all duration-300 rounded overflow-hidden;
}
.nav-btn:hover {
  @apply text-cyan-300 bg-cyan-900/20 drop-shadow-[0_0_8px_rgba(34,211,238,0.5)];
}
.nav-btn.router-link-active {
  @apply text-emerald-400 font-bold bg-emerald-900/20 drop-shadow-[0_0_10px_rgba(52,211,153,0.8)] shadow-[inset_0_0_15px_rgba(52,211,153,0.2)];
  border-bottom: 3px solid #34d399;
}

.cyber-fade-enter-active, .cyber-fade-leave-active { transition: opacity 0.2s ease, filter 0.2s ease; }
.cyber-fade-enter-from, .cyber-fade-leave-to { opacity: 0; filter: blur(5px); }

.slide-up-enter-active, .slide-up-leave-active { transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translateY(20px) scale(0.95); }
</style>