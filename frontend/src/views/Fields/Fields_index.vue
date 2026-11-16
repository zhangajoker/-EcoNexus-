<template>
  <div class="p-8 min-h-screen relative text-white bg-[#0a0c0a] overflow-hidden select-none">

    <!-- 骨架屏也强制固定布局 -->
    <div v-if="isLoading" class="grid grid-cols-3 gap-6 animate-pulse relative z-10 h-full">
      <div class="col-span-2 h-[650px] bg-white/5 rounded-2xl border border-white/10 flex items-center justify-center">
        <span class="text-gray-500 font-mono tracking-widest text-sm">正在同步全域节点数据...</span>
      </div>
      <div class="space-y-4">
        <div v-for="i in 4" :key="i" class="h-28 bg-white/5 rounded-xl border border-white/10"></div>
      </div>
    </div>

    <template v-else>
      <div v-if="viewMode === 'map'" class="relative z-10 h-full flex flex-col view-animate">

        <!-- 头部标题区：字号放大，加入发光特效 -->
        <div class="mb-6 flex justify-between items-end">
          <div>
            <h2 class="text-4xl font-bold border-l-[6px] border-eco-primary pl-5 tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.5)]">农田生态孪生节点监测 (GIS 态势感知)</h2>
            <p class="text-lg font-bold text-gray-400 mt-3 font-mono tracking-widest">空间灾害热力图与物联网节点拓扑</p>
          </div>
          <div class="flex gap-4 font-mono text-sm">
            <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></span> 正常节点</div>
            <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-yellow-500 shadow-[0_0_8px_#eab308]"></span> 预警节点</div>
            <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-red-500 animate-pulse shadow-[0_0_8px_#ef4444]"></span> 高危节点</div>
          </div>
        </div>

        <!-- 强制 grid-cols-3，永远不会乱版 -->
        <div class="grid grid-cols-3 gap-6 flex-1">
          <!-- 左侧地图：强制 col-span-2 -->
          <div class="col-span-2 bg-black/40 border border-white/10 rounded-2xl p-4 relative overflow-hidden shadow-2xl h-[750px] flex flex-col">
            <div class="absolute top-4 left-4 z-20 bg-black/60 border border-white/10 p-3 rounded backdrop-blur">
              <div class="text-xs text-gray-400 font-mono mb-2">实时态势遥测</div>
              <div class="text-sm text-white flex items-center gap-2">
                <span class="w-2 h-2 bg-eco-primary rounded-full animate-pulse"></span>
                全局态势雷达网格持续扫描中...
              </div>
            </div>
            <div ref="mapRef" class="w-full h-full flex-1 z-10 cursor-crosshair"></div>
          </div>

          <!-- 右侧列表区：全面放大字号与边距 -->
          <div class="space-y-6 h-[750px] overflow-y-auto pr-4 custom-scrollbar">
            <div v-for="field in store.fields" :key="field.id"
                 @click="triggerShuttle(field)"
                 class="pointer-events-auto bg-black/40 p-6 rounded-2xl border-l-8 cursor-pointer border border-white/10 hover:border-eco-primary/50 transition-all duration-300 group relative overflow-hidden"
                 :class="field.status.includes('健康') ? 'border-l-emerald-500' : 'border-l-red-500 bg-red-950/20'">

              <div class="flex justify-between items-center mb-6">
                <span class="font-black text-2xl tracking-widest text-white group-hover:text-eco-primary transition-colors">
                  {{ field.name }}
                </span>
                <span class="text-sm px-4 py-1.5 bg-black/80 rounded border shadow-inner font-mono tracking-widest"
                      :class="field.status.includes('健康') ? 'text-emerald-400 border-emerald-500/40' : 'text-red-400 border-red-500/50 animate-pulse drop-shadow-[0_0_8px_#ef4444]'">
                  {{ field.status }}
                </span>
              </div>

              <div class="grid grid-cols-2 gap-4 text-base text-gray-400 bg-black/50 p-4 rounded-xl border border-white/5 font-mono">
                <div class="flex justify-between"><span>湿度:</span> <span class="text-white font-bold">{{ field.moisture || 0 }}%</span></div>
                <div class="flex justify-between"><span>虫情:</span> <span class="text-white font-bold">{{ field.pestIndex || '正常' }}</span></div>
                <div class="flex justify-between"><span>叶绿素:</span> <span class="text-white font-bold">{{ field.spad || 0 }}</span></div>
                <div class="flex justify-between"><span>温度:</span> <span class="text-white font-bold">{{ field.temp || 0 }}°C</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 穿梭动画：高速同步握手序列 -->
      <div v-if="viewMode === 'shuttle'" class="fixed inset-0 z-[9999] bg-[#050705] flex flex-col items-center justify-center overflow-hidden">
        <!-- 背景星空穿梭保留 -->
        <canvas ref="warpCanvas" class="absolute inset-0 w-full h-full z-0"></canvas>
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,#050705_100%)] z-10 pointer-events-none"></div>

        <!-- 全新的 HUD 前景面板 -->
        <div class="relative z-20 w-full max-w-2xl px-8 flex flex-col items-center">

          <!-- 标题：明确显示正在加载的田块 -->
          <div class="text-eco-primary text-3xl font-bold tracking-widest uppercase mb-6 flex flex-col items-center gap-2">
            <span>正在加载全息生境舱</span>
            <span class="text-white text-4xl mt-1 tracking-widest">>> {{ selectedField?.name || '未知区域' }} <<</span>
          </div>

          <!-- 进度条容器 -->
          <div class="w-full bg-black/60 border border-emerald-500/30 rounded-lg backdrop-blur-md overflow-hidden flex flex-col">
            <div class="px-6 py-3 border-b border-emerald-500/30 flex justify-between items-center text-sm">
              <span class="text-emerald-300 tracking-widest">边缘网关解析中</span>
              <span class="text-emerald-500 font-mono font-bold animate-pulse">UPLINK ACTIVE...</span>
            </div>

            <!-- 真正的动态进度条 -->
            <div class="w-full h-2 bg-black/80">
              <div class="h-full bg-emerald-500 shadow-[0_0_15px_#10b981] transition-all duration-75 ease-linear relative" :style="{ width: warpProgress + '%' }">
                <div class="absolute right-0 top-0 w-10 h-full bg-white/50 blur-[2px]"></div>
              </div>
            </div>

            <!-- 终端日志滚动区 -->
            <div class="h-32 bg-black/80 p-4 font-mono text-xs overflow-hidden relative">
              <div class="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:100%_4px]"></div>
              <div class="flex flex-col-reverse h-full space-y-1.5 space-y-reverse">
                <div v-for="(log, idx) in warpLogs" :key="idx" class="flex gap-3 items-center animate-log-in">
                  <span class="text-emerald-500/60">[{{ log.time }}]</span>
                  <span :class="log.color">{{ log.text }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 进度大字 -->
          <div class="mt-6 text-emerald-400 font-mono text-5xl font-black tracking-widest drop-shadow-[0_0_15px_#34d399]">
            {{ Math.floor(warpProgress) }}%
          </div>
        </div>
      </div>

      <!-- 快门动画 -->
      <div v-if="showShutter" class="fixed inset-0 z-[10000] pointer-events-none overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1/2 bg-[#070907] border-b border-eco-primary/40 flex items-end justify-between px-16 pb-3 shutter-top-anim">
          <span class="text-sm font-mono text-eco-primary/60 tracking-widest animate-pulse">系统：全息转场已激活</span>
          <span class="text-sm font-mono text-eco-primary/40">矩阵快门_A // 开启</span>
        </div>
        <div class="absolute bottom-0 left-0 w-full h-1/2 bg-[#070907] border-t border-eco-primary/40 flex items-start justify-between px-16 pt-3 shutter-bottom-anim">
          <span class="text-sm font-mono text-eco-primary/60 tracking-widest">正在解密多模态数据流...</span>
          <span class="text-sm font-mono text-eco-primary/40">加密链路_B // 稳定</span>
        </div>
        <div class="absolute top-1/2 left-0 w-full h-[2px] bg-white shadow-[0_0_15px_#34d399,0_0_5px_#fff] -translate-y-1/2 shutter-line-anim"></div>
      </div>

      <!-- 详情舱 -->
      <div v-if="viewMode === 'detail'" class="relative z-10 h-full flex flex-col view-animate">
        <div class="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
          <div class="flex items-center gap-4">
            <button @click="viewMode = 'map'" class="group bg-white/5 border border-white/10 px-4 py-2 rounded-xl text-sm font-mono text-gray-400 hover:text-eco-primary hover:border-eco-primary/40 transition-all flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transform group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
              [ 返回 GIS 主控台 ]
            </button>
            <div class="h-6 w-px bg-white/10"></div>
            <h3 class="text-2xl font-bold tracking-wider flex items-center gap-3">
              <span class="w-2 h-6 bg-eco-primary rounded-full"></span>
              {{ selectedField?.name }} 全息生境舱
            </h3>
          </div>
          <span class="text-sm font-mono text-gray-500 tracking-widest">实时加密链路</span>
        </div>

        <div class="grid grid-cols-3 gap-6 flex-1">
          <!-- 详情页图片部分强制 col-span-2 -->
          <div class="col-span-2 bg-black/40 border border-white/5 rounded-2xl relative overflow-hidden shadow-2xl h-[680px] flex flex-col justify-center items-center group">
            <template v-if="currentVisionVideo">
              <video :src="currentVisionVideo" autoplay loop muted playsinline
                     class="absolute inset-0 w-full h-full object-cover opacity-20 blur-2xl grayscale pointer-events-none transition-all duration-700"></video>
            </template>
            <template v-else>
              <img :src="currentVisionImg || fallbackImg"
                   class="absolute inset-0 w-full h-full object-cover opacity-20 blur-2xl grayscale pointer-events-none transition-all duration-700" />
            </template>

            <template v-if="currentVisionVideo">
              <video :src="currentVisionVideo" autoplay loop controls muted playsinline
                     class="relative w-[96%] h-[96%] object-contain object-center transition-all duration-700 z-10"
                     :class="isScanning ? 'opacity-30 grayscale blur-sm' : 'opacity-100 drop-shadow-[0_0_30px_rgba(0,0,0,0.5)]'"></video>
            </template>
            <template v-else>
              <img :src="currentVisionImg || fallbackImg"
                   alt="Terrace Imagery"
                   class="relative w-[96%] h-[96%] object-contain object-center transition-all duration-700 z-10"
                   :class="isScanning ? 'opacity-30 grayscale blur-sm' : 'opacity-100 drop-shadow-[0_0_30px_rgba(0,0,0,0.5)]'" />
            </template>

            <div class="absolute inset-0 shadow-[inset_0_0_60px_rgba(0,0,0,0.8)] pointer-events-none z-10"></div>
            <div class="absolute bottom-0 left-0 w-full h-24 bg-gradient-to-t from-[#0a0c0a] to-transparent pointer-events-none z-10"></div>

            <div v-if="isScanning" class="absolute inset-0 z-20 pointer-events-none">
              <div class="w-full h-1 bg-eco-primary shadow-[0_0_20px_#34d399] animate-radar-scan absolute top-0"></div>
              <div class="absolute inset-0 bg-[linear-gradient(rgba(52,211,153,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(52,211,153,0.05)_1px,transparent_1px)] bg-[size:40px_40px]"></div>
            </div>

            <div class="absolute bottom-6 right-6 z-30">
              <input type="file" ref="fileInput" @change="uploadToYOLOv8" accept="image/*,video/*" class="hidden" />
              <button @click="$refs.fileInput.click()"
                      :disabled="isScanning"
                      class="bg-black/80 border border-eco-primary hover:bg-eco-primary/20 text-eco-primary font-mono text-sm px-8 py-4 rounded-none backdrop-blur transition-all flex items-center gap-3 group-hover:opacity-100 opacity-60 shadow-[0_0_15px_rgba(0,0,0,0.5)]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                {{ isScanning ? scanningText : '接入多模态数据流 (支持视频)' }}
              </button>
            </div>
          </div>

          <!-- 右侧详情舱数据面板 -->
          <div class="col-span-1 space-y-6 h-[680px] overflow-y-auto pr-1 custom-scrollbar font-mono">
            <div class="bg-black/50 p-6 rounded-2xl border border-white/10 flex flex-col gap-5 relative overflow-hidden">
              <h4 class="text-sm text-gray-400 tracking-widest uppercase flex justify-between items-center relative z-10">
                <span>● 装备遥测与边缘算力</span>
                <span class="text-emerald-400 animate-pulse text-[11px]">已连接</span>
              </h4>

              <div class="grid grid-cols-2 gap-4 relative z-10">
                <div class="bg-white/5 border border-eco-primary/20 p-4 rounded-xl text-xs space-y-3 relative overflow-hidden group hover:border-eco-primary/50 transition-colors">
                  <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-eco-primary/50 to-transparent opacity-0 group-hover:opacity-100"></div>
                  <div class="flex justify-between items-center border-b border-eco-primary/20 pb-2 mb-2">
                    <span class="font-bold text-white tracking-wider">边缘节点</span>
                    <span class="text-eco-primary font-bold">Jetson Orin</span>
                  </div>
                  <div class="flex justify-between text-gray-400">
                    <span>摄像机</span><span class="text-gray-300">{{ selectedField?.id || 'F-001' }}_RGB</span>
                  </div>
                  <div class="flex justify-between text-gray-400">
                    <span>部署模型</span><span class="text-gray-300">TianYan-v1.2</span>
                  </div>
                  <div class="flex justify-between text-gray-400">
                    <span>推理延迟</span><span class="text-white font-bold">{{ edgeLatency }} ms</span>
                  </div>
                  <div class="flex justify-between text-gray-400">
                    <span>处理帧率</span><span class="text-white font-bold">{{ edgeFPS }} 帧/s</span>
                  </div>
                  <div v-if="diseaseDiagnosis !== null" class="mt-3 pt-3 border-t border-eco-primary/20 flex justify-between items-center text-sm">
                    <span class="text-gray-500 font-bold tracking-widest">智能诊断</span>
                    <span class="font-bold tracking-wide shadow-[0_0_8px_currentColor] px-2 py-1 rounded"
                          :class="diseaseDiagnosis.includes('Healthy') || diseaseDiagnosis.includes('健康') ? 'text-emerald-400 bg-emerald-500/10' : 'text-red-400 bg-red-500/10 animate-pulse'">
                      {{ diseaseDiagnosis }}
                    </span>
                  </div>
                </div>

                <div class="bg-white/5 border border-blue-400/20 p-4 rounded-xl text-xs space-y-3 relative overflow-hidden group hover:border-blue-400/50 transition-colors">
                  <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-blue-400/50 to-transparent opacity-0 group-hover:opacity-100"></div>
                  <div class="flex justify-between items-center border-b border-blue-400/20 pb-2 mb-2">
                    <span class="font-bold text-white tracking-wider">植保无人机</span>
                    <div class="flex items-center gap-1 text-blue-400 font-bold">链路稳定 <span class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span></div>
                  </div>
                  <div class="flex justify-between text-gray-400">
                    <span>飞行高度</span><span class="text-white font-bold">{{ uavAltitude }} m</span>
                  </div>
                  <div class="flex justify-between text-gray-400">
                    <span>实时风速</span><span class="text-gray-300">2.1 m/s (西南风)</span>
                  </div>
                  <div class="flex justify-between text-gray-400">
                    <span>北纬 (LAT)</span><span class="text-gray-300">39.904° N</span>
                  </div>
                  <div class="flex justify-between text-gray-400">
                    <span>东经 (LON)</span><span class="text-gray-300">116.407° E</span>
                  </div>
                </div>
              </div>

              <div v-if="visionDetectCount !== null"
                   class="w-full text-center py-2.5 rounded-lg border text-sm font-bold tracking-widest transition-all relative z-10"
                   :class="visionDetectCount > 0 ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400 shadow-[0_0_15px_rgba(234,179,8,0.2)]' : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'">
                视觉追踪目标锁定 : {{ visionDetectCount }}
              </div>
            </div>

            <div class="bg-black/50 p-6 rounded-2xl border border-white/10">
              <h4 class="text-sm text-gray-400 mb-6 tracking-widest uppercase flex justify-between items-center">
                <span>● 生境要素遥测 (IoT)</span>
                <span class="text-emerald-400 animate-pulse text-[11px]">已同步</span>
              </h4>

              <div class="grid grid-cols-2 gap-4 text-sm mb-4">
                <div class="bg-white/5 p-4 rounded-xl border border-white/5 relative overflow-hidden group h-32 flex flex-col justify-between hover:border-white/20 transition-colors">
                  <div class="relative z-10 flex justify-between items-start">
                    <div class="text-gray-500 mb-1">容积含水率</div>
                    <div class="text-[10px] text-emerald-500/50 font-mono border border-emerald-500/20 px-2 rounded animate-pulse">实况</div>
                  </div>
                  <div class="relative z-10 text-white font-bold text-3xl">{{ selectedField?.moisture || 0 }}%</div>
                  <div ref="moistureSparkRef" class="absolute bottom-0 left-0 w-full h-[65%] opacity-50 group-hover:opacity-100 transition-opacity"></div>
                </div>

                <div class="bg-white/5 p-4 rounded-xl border border-white/5 relative overflow-hidden group h-32 flex flex-col justify-between hover:border-white/20 transition-colors">
                  <div class="relative z-10 flex justify-between items-start">
                    <div class="text-gray-500 mb-1">地表绝对温度</div>
                    <div class="text-[10px] text-blue-400/50 font-mono border border-blue-400/20 px-2 rounded animate-pulse">实况</div>
                  </div>
                  <div class="relative z-10 text-white font-bold text-3xl">{{ selectedField?.temp || 0 }}°C</div>
                  <div ref="tempSparkRef" class="absolute bottom-0 left-0 w-full h-[65%] opacity-50 group-hover:opacity-100 transition-opacity"></div>
                </div>
              </div>

              <div class="space-y-3 text-sm relative z-10">
                <div class="flex justify-between items-center bg-white/5 p-3 rounded-xl border border-white/5">
                  <span class="text-gray-400">全氮 (N)</span><span class="text-white font-bold text-lg">{{ selectedField?.n || 0 }} <span class="text-[11px] text-gray-600">mg/kg</span></span>
                </div>
                <div class="flex justify-between items-center bg-white/5 p-3 rounded-xl border border-white/5">
                  <span class="text-gray-400">有效磷 (P)</span><span class="text-white font-bold text-lg">{{ selectedField?.p || 0 }} <span class="text-[11px] text-gray-600">mg/kg</span></span>
                </div>
              </div>
            </div>

            <div class="bg-eco-primary/5 p-6 rounded-2xl border transition-all duration-500"
                 :class="visionDetectCount > 0 ? 'border-yellow-500/50 bg-yellow-900/10' : (visionDetectCount === 0 ? 'border-emerald-500/50 bg-emerald-900/10' : 'border-eco-primary/20')">
              <h4 class="text-sm font-bold mb-4 flex items-center gap-2" :class="visionDetectCount > 0 ? 'text-yellow-400' : 'text-eco-primary'">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                云端大模型综合调度决策
              </h4>

              <p v-if="visionDetectCount === null" class="text-sm text-gray-400 leading-relaxed font-sans">
                当前区域传感数据已就绪。等待触发边缘视觉雷达，以便大模型结合多模态特征下达智能生产调度指令。
              </p>

              <div v-else class="space-y-4">
                <div class="text-sm leading-relaxed font-sans border-l-4 pl-4"
                     :class="visionDetectCount > 0 ? 'text-yellow-300 border-yellow-500' : 'text-emerald-300 border-emerald-500'">
                  <span class="font-bold block mb-3 font-mono text-white opacity-80 text-xs">
                    > 大模型推理引擎 // 运行中
                  </span>
                  <span class="text-base font-bold tracking-wide">{{ aiAdvice }}</span>
                </div>

                <div v-if="visionDetectCount > 0" class="flex flex-wrap gap-3 mt-3">
                   <span class="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs px-3 py-1 rounded shadow-[0_0_8px_rgba(16,185,129,0.2)]">农药减量预测 ↓ 65%</span>
                   <span class="bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs px-3 py-1 rounded shadow-[0_0_8px_rgba(59,130,246,0.2)]">碳汇潜力 +0.05 tCO₂e</span>
                </div>

                <div class="text-[11px] text-gray-500 font-mono mt-3 flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full animate-ping"
                        :class="visionDetectCount > 0 ? 'bg-yellow-500' : 'bg-emerald-500'"></span>
                  上述大模型干预指令已同步写入 ESG 碳汇智能合约底层账本。
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted, watch } from 'vue';
import { useEcoStore } from '../../store/ecoStore.js';
import * as echarts from 'echarts';

// ======================= 本地图片导入 =======================
import localFieldImg from './field.jpg';
import { API_BASE } from '../../config';

// ======================= 基础状态变量 =======================
const store = useEcoStore();
const isLoading = ref(true);
const viewMode = ref('map');
const selectedField = ref(null);
const showShutter = ref(false);

const mapRef = ref(null);
let myChart = null;

const warpCanvas = ref(null);
let warpFrameId = null;
let warpParticles = [];

// ======================= 机器视觉协同状态 =======================
const fallbackImg = localFieldImg;

const currentVisionImg = ref(null);
const currentVisionVideo = ref(null);
const isScanning = ref(false);
const scanningText = ref("神经网格与大模型通信中...");
const visionDetectCount = ref(null);
const diseaseDiagnosis = ref(null);
const aiAdvice = ref(null);
const fileInput = ref(null);

// ======================= 遥测数据伪心跳动画 =======================
const edgeFPS = ref(45);
const edgeLatency = ref(14);
const uavAltitude = ref(2.40);
let telemetryTimer = null;

const moistureSparkRef = ref(null);
const tempSparkRef = ref(null);
let moistureChart = null;
let tempChart = null;
let mData = [];
let tData = [];

// ==================== 联动监听 (实时刷新) ====================
watch(() => store.fields, (newFields) => {
  if (selectedField.value && newFields.length > 0) {
    const updatedField = newFields.find(f => f.id === selectedField.value.id);
    if (updatedField) {
      selectedField.value = { ...updatedField };
    }
  }
}, { deep: true });

// 初始化传感器折线图
const initIoTSparklines = () => {
  if (moistureChart) moistureChart.dispose();
  if (tempChart) tempChart.dispose();

  if (moistureSparkRef.value && selectedField.value) {
    moistureChart = echarts.init(moistureSparkRef.value);
    const baseM = selectedField.value.moisture || 40;
    mData = Array.from({length: 20}, () => baseM + (Math.random() * 2 - 1));
    moistureChart.setOption({
      grid: { left: 0, right: 0, top: 0, bottom: 0 },
      xAxis: { type: 'category', show: false },
      yAxis: { type: 'value', show: false, min: baseM - 5, max: baseM + 5 },
      series: [{
        data: mData, type: 'line', smooth: true, symbol: 'none',
        lineStyle: { width: 1.5, color: '#10b981' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(16, 185, 129, 0.4)' },
            { offset: 1, color: 'rgba(16, 185, 129, 0)' }
          ])
        }
      }]
    });
  }

  if (tempSparkRef.value && selectedField.value) {
    tempChart = echarts.init(tempSparkRef.value);
    const baseT = selectedField.value.temp || 25;
    tData = Array.from({length: 20}, () => baseT + (Math.random() * 1 - 0.5));
    tempChart.setOption({
      grid: { left: 0, right: 0, top: 0, bottom: 0 },
      xAxis: { type: 'category', show: false },
      yAxis: { type: 'value', show: false, min: baseT - 2, max: baseT + 2 },
      series: [{
        data: tData, type: 'line', smooth: true, symbol: 'none',
        lineStyle: { width: 1.5, color: '#60a5fa' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(96, 165, 250, 0.4)' },
            { offset: 1, color: 'rgba(96, 165, 250, 0)' }
          ])
        }
      }]
    });
  }
};

const startTelemetryAnim = () => {
  telemetryTimer = setInterval(() => {
    edgeFPS.value = 42 + Math.floor(Math.random() * 5);
    edgeLatency.value = 12 + Math.floor(Math.random() * 4);
    uavAltitude.value = (2.4 + (Math.random() * 0.1 - 0.05)).toFixed(2);

    if (moistureChart && selectedField.value) {
      mData.push((selectedField.value.moisture || 40) + (Math.random() * 2 - 1));
      if (mData.length > 20) mData.shift();
      moistureChart.setOption({ series: [{ data: mData }] });
    }
    if (tempChart && selectedField.value) {
      tData.push((selectedField.value.temp || 25) + (Math.random() * 1 - 0.5));
      if (tData.length > 20) tData.shift();
      tempChart.setOption({ series: [{ data: tData }] });
    }
  }, 1000);
};

const stopTelemetryAnim = () => {
  if (telemetryTimer) clearInterval(telemetryTimer);
};

watch(viewMode, (newVal) => {
  if (newVal === 'map') {
    nextTick(() => {
      if (moistureChart) { moistureChart.dispose(); moistureChart = null; }
      if (tempChart) { tempChart.dispose(); tempChart = null; }
      if (myChart != null && myChart.dispose) myChart.dispose();
      initMap();
    });
  }
});

const resetDetailState = () => {
  currentVisionImg.value = null;
  currentVisionVideo.value = null;
  visionDetectCount.value = null;
  diseaseDiagnosis.value = null;
  aiAdvice.value = null;
  isScanning.value = false;
  scanningText.value = "神经网格与大模型通信中...";
};

// ======================= 跃迁动画专享状态 =======================
const warpProgress = ref(0);
const warpLogs = ref([]);

// 🟢 触发穿梭动画与数据加载
const triggerShuttle = (field) => {
  selectedField.value = field || store.fields[0];
  const currentId = selectedField.value?.id || '未知网格';

  warpProgress.value = 0;
  warpLogs.value = [];
  resetDetailState();

  viewMode.value = 'shuttle';
  showShutter.value = false;

  nextTick(() => {
    initWarpDrive();

    const logMessages = [
      { text: `Ping 边缘网关网格 ${currentId}... [OK]`, color: 'text-gray-300' },
      { text: "正在获取多光谱传感器校验码...", color: 'text-gray-300' },
      { text: "加载 YOLOv8 TensorRT 推理引擎...", color: 'text-blue-400 font-bold' },
      { text: "同步最新 ESG 碳汇账本哈希...", color: 'text-yellow-400' },
      { text: "初始化气象与土壤遥测双向链路...", color: 'text-emerald-400' },
      { text: "UPLINK ESTABLISHED. 进入全息矩阵.", color: 'text-white font-bold' }
    ];

    let logIdx = 0;

    const totalDuration = 1500;
    const intervalTime = 50;
    let elapsedTime = 0;

    const progInterval = setInterval(() => {
      elapsedTime += intervalTime;

      let calculatedProg = (elapsedTime / totalDuration) * 100;
      warpProgress.value = Math.min(calculatedProg + (Math.random() * 5), 100);

      if (elapsedTime % 250 === 0 && logIdx < logMessages.length) {
        const timeStr = new Date().toISOString().split('T')[1].slice(0, 12);
        warpLogs.value = [
          { time: timeStr, text: logMessages[logIdx].text, color: logMessages[logIdx].color },
          ...warpLogs.value
        ];
        logIdx++;
      }

      if (elapsedTime >= totalDuration) {
        clearInterval(progInterval);
        warpProgress.value = 100;

        if (warpFrameId) cancelAnimationFrame(warpFrameId);

        showShutter.value = true;
        viewMode.value = 'detail';

        nextTick(() => {
          initIoTSparklines();
        });

        setTimeout(() => {
          showShutter.value = false;
        }, 800);
      }
    }, intervalTime);
  });
};

// ==================== 轮询与上传逻辑 ====================
const uploadToYOLOv8 = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  isScanning.value = true;
  scanningText.value = "正在上传多模态数据...";

  // 👉 【核心修复】：在此处一并清空所有的旧状态
  visionDetectCount.value = null;
  aiAdvice.value = null;
  diseaseDiagnosis.value = null;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('field_id', selectedField.value?.id || 'F-001');

  try {
    const response = await fetch(`${API_BASE}/api/vision/analyze`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error('网络网关拒绝访问');

    const initResult = await response.json();
    const taskId = initResult.task_id;

    scanningText.value = "云端算力群持续解析中... (后台排队处理)";
    pollVisionResult(taskId);

  } catch (error) {
    console.error('上传失败:', error);
    alert('中枢连接丢失，请检查 FastAPI 服务状态。');
    isScanning.value = false;
  }
};

const pollVisionResult = async (taskId) => {
    try {
        const res = await fetch(`${API_BASE}/api/vision/result/${taskId}`);
        const data = await res.json();

        if (data.status === 'processing') {
            setTimeout(() => pollVisionResult(taskId), 1500);
        } else if (data.status === 'success') {
            if (data.type === 'video') {
                currentVisionVideo.value = data.video_url;
                currentVisionImg.value = null;
            } else {
                currentVisionImg.value = data.image_data;
                currentVisionVideo.value = null;
            }
            visionDetectCount.value = data.detected_count;
            diseaseDiagnosis.value = data.disease_diagnosis;
            aiAdvice.value = data.ai_advice;
            isScanning.value = false;
        } else {
            throw new Error(data.message || '模型推理失败');
        }
    } catch (error) {
        console.error('轮询失败:', error);
        alert('云端大模型算力节点离线。');
        isScanning.value = false;
    }
};

// ==================== 动画与地图渲染 ====================
const initWarpDrive = () => {
  const canvas = warpCanvas.value;
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let w = canvas.width = window.innerWidth;
  let h = canvas.height = window.innerHeight;
  let centerX = w / 2;
  let centerY = h / 2;

  const particleCount = 2000;
  let baseSpeed = 2;
  warpParticles = [];

  for (let i = 0; i < particleCount; i++) {
    warpParticles.push({
      x: Math.random() * w - centerX,
      y: Math.random() * h - centerY,
      z: Math.random() * w,
      o: Math.random(),
      isWhite: Math.random() > 0.9
    });
  }

  const renderWarp = () => {
    ctx.fillStyle = 'rgba(5, 7, 5, 0.2)';
    ctx.fillRect(0, 0, w, h);

    baseSpeed += 0.2;
    const currentSpeed = Math.min(baseSpeed, 45);

    for (let i = 0; i < particleCount; i++) {
      let p = warpParticles[i];

      let pastZ = p.z;
      let pastX = (p.x / pastZ) * w + centerX;
      let pastY = (p.y / pastZ) * w + centerY;

      p.z -= currentSpeed;

      if (p.z <= 0) {
        p.x = Math.random() * w - centerX;
        p.y = Math.random() * h - centerY;
        p.z = w;
        p.o = Math.random();
        p.isWhite = Math.random() > 0.9;
        continue;
      }

      let newX = (p.x / p.z) * w + centerX;
      let newY = (p.y / p.z) * w + centerY;

      ctx.beginPath();
      ctx.moveTo(pastX, pastY);
      ctx.lineTo(newX, newY);

      let depthAlpha = (1 - p.z / w) * p.o;
      ctx.lineWidth = depthAlpha * 3;

      if (p.isWhite) {
        ctx.strokeStyle = `rgba(255, 255, 255, ${depthAlpha * 1.5})`;
      } else {
        ctx.strokeStyle = `rgba(52, 211, 153, ${depthAlpha})`;
      }
      ctx.stroke();
    }
    warpFrameId = requestAnimationFrame(renderWarp);
  };
  renderWarp();

  window.addEventListener('resize', resizeCanvas);
  function resizeCanvas() {
    if(!canvas) return;
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
    centerX = w / 2;
    centerY = h / 2;
  }
};

const initMap = () => {
  if (!mapRef.value || store.fields.length === 0) return;
  myChart = echarts.init(mapRef.value);

  const scatterData = store.fields.map(f => {
    const isHealthy = f.status.includes('健康');
    return {
      name: f.name,
      value: [f.x, f.y],
      rawData: f,
      itemStyle: { color: isHealthy ? '#10b981' : '#ef4444' }
    };
  });

  const heatData = store.fields.filter(f => !f.status.includes('健康')).map(f => ({
    name: f.name, value: [f.x, f.y], itemStyle: { color: 'rgba(239, 68, 68, 0.15)' }, symbolSize: 150
  }));

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: 'rgba(10, 12, 10, 0.95)',
      borderColor: 'rgba(255,255,255,0.2)',
      textStyle: { color: '#fff', fontSize: 18, fontFamily: 'monospace' },
      formatter: (p) => p.seriesName === '热力' ? '' : `<div class="p-3"><strong class="text-2xl">${p.name}</strong><br/><span class="text-eco-primary mt-2 inline-block">[点击进入全息生境]</span></div>`
    },
    graphic: {
      elements: [{
        type: 'image',
        style: { image: localFieldImg, width: 1000, height: 600, opacity: 0.25 },
        left: 'center', top: 'center'
      }]
    },
    xAxis: { show: false, min: 0, max: 1000 },
    yAxis: { show: false, min: 0, max: 600, inverse: true },
    series: [
      { name: '热力', type: 'scatter', data: heatData, silent: true, itemStyle: { shadowBlur: 100, shadowColor: '#ef4444' } },
      { name: '节点', type: 'effectScatter', coordinateSystem: 'cartesian2d',
        data: scatterData.map(d => ({...d, symbolSize: d.itemStyle.color === '#10b981' ? 24 : 36})),
        showEffectOn: 'render', rippleEffect: { brushType: 'stroke', scale: 6 },
        label: { show: true, formatter: '{b}', position: 'right', color: '#fff', fontSize: 18, fontWeight: 'bold', textBorderColor: '#000', textBorderWidth: 3 }
      }
    ]
  };

  myChart.setOption(option);
  myChart.on('click', (p) => {
    if (p.seriesName === '节点' && p.data.rawData) {
      triggerShuttle(p.data.rawData);
    }
  });
};

// ==================== 生命周期 ====================
onMounted(async () => {
  await store.fetchFields();
  isLoading.value = false;

  if (store.fields && store.fields.length > 0) {
    selectedField.value = store.fields[0];
  }

  startTelemetryAnim();

  nextTick(() => {
    initMap();
    initIoTSparklines();
  });
});

onUnmounted(() => {
  stopTelemetryAnim();
  if (myChart) myChart.dispose();
  if (moistureChart) moistureChart.dispose();
  if (tempChart) tempChart.dispose();
  if (warpFrameId) cancelAnimationFrame(warpFrameId);
});
</script>

<style scoped>
.view-animate { animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(52, 211, 153, 0.3); border-radius: 6px; }

.animate-radar-scan { animation: radarScan 2.5s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate; }
@keyframes radarScan { 0% { transform: translateY(0); opacity: 0.8; } 100% { transform: translateY(620px); opacity: 0.2; } }

.warp-hud-animate { animation: hudScale 2.2s cubic-bezier(0.1, 0.8, 0.2, 1) forwards; }
@keyframes hudScale {
  0% { transform: scale(0.8); opacity: 0; }
  10% { transform: scale(1.02); opacity: 1; }
  90% { transform: scale(1.08); opacity: 1; filter: blur(0px); }
  100% { transform: scale(1.8); opacity: 0; filter: blur(4px); }
}

.warp-text-glitch { position: relative; text-shadow: 0 0 15px rgba(52, 211, 153, 0.8); animation: glitch-skew 2.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) both infinite; }
@keyframes glitch-skew {
  0% { transform: skew(0deg); } 2% { transform: skew(-4deg); } 4% { transform: skew(4deg); }
  6% { transform: skew(0deg); } 100% { transform: skew(0deg); }
}

.shutter-top-anim { animation: shutterUpOpen 0.8s cubic-bezier(0.85, 0, 0.15, 1) forwards; }
.shutter-bottom-anim { animation: shutterDownOpen 0.8s cubic-bezier(0.85, 0, 0.15, 1) forwards; }
.shutter-line-anim { animation: lineLaserSplit 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards; }

@keyframes shutterUpOpen { 0%, 15% { transform: translateY(0); } 100% { transform: translateY(-100%); } }
@keyframes shutterDownOpen { 0%, 15% { transform: translateY(0); } 100% { transform: translateY(100%); } }
@keyframes lineLaserSplit {
  0% { transform: translateY(-50%) scaleX(0); opacity: 0; }
  15% { transform: translateY(-50%) scaleX(1); opacity: 1; }
  40% { transform: translateY(-50%) scaleX(1); opacity: 1; height: 4px; }
  100% { transform: translateY(-50%) scaleX(0); opacity: 0; }
}
@keyframes logIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-log-in { animation: logIn 0.2s ease-out forwards; }
</style>