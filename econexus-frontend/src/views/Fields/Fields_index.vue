<template>
  <div class="p-8 min-h-screen relative text-white bg-[#0a0c0a] overflow-hidden select-none">

    <div v-if="viewMode === 'map'" class="relative z-10 h-full flex flex-col view-animate">
      <div class="mb-6 flex justify-between items-end">
        <div>
          <h2 class="text-2xl font-bold border-l-4 border-eco-primary pl-4 tracking-wider">农田生态孪生节点监测 (GIS 态势感知)</h2>
          <p class="text-xs text-eco-text mt-2 font-mono">Spatial Disaster Heatmap & IoT Node Topology</p>
        </div>
        <div class="flex gap-4 font-mono text-xs">
          <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></span> 正常节点</div>
          <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-yellow-500 shadow-[0_0_8px_#eab308]"></span> 预警节点</div>
          <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-red-500 animate-pulse shadow-[0_0_8px_#ef4444]"></span> 高危节点</div>
        </div>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-3 gap-6 flex-1">
        <div class="xl:col-span-2 bg-black/40 border border-white/10 rounded-2xl p-4 relative overflow-hidden shadow-2xl h-[650px] flex flex-col">
          <div class="absolute top-4 left-4 z-20 bg-black/60 border border-white/10 p-2 rounded backdrop-blur">
            <div class="text-[10px] text-gray-400 font-mono mb-1">REAL-TIME TELEMETRY</div>
            <div class="text-xs text-white flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-eco-primary rounded-full animate-pulse"></span>
              全局态势雷达网格持续扫描中...
            </div>
          </div>
          <div ref="mapRef" class="w-full h-full flex-1 z-10 cursor-crosshair"></div>
        </div>

        <div class="space-y-4 h-[650px] overflow-y-auto pr-2 custom-scrollbar">
          <div v-for="field in fields" :key="field.id"
               @click="triggerShuttle(field)"
               class="bg-black/40 p-4 rounded-xl border-l-4 cursor-pointer border border-white/5 hover:border-eco-primary/30 transition-all duration-300 group relative overflow-hidden"
               :class="field.status === '健康' ? 'border-l-emerald-500' : (field.status === '预警' ? 'border-l-yellow-500' : 'border-l-red-500 bg-red-950/5')">
            <div class="flex justify-between items-center mb-3">
              <span class="font-bold text-lg tracking-wide text-white group-hover:text-eco-primary transition-colors">{{ field.name }}</span>
              <span class="text-xs px-2 py-1 bg-black/60 rounded border shadow-inner font-mono"
                    :class="field.status === '健康' ? 'text-emerald-400 border-emerald-500/20' : (field.status === '预警' ? 'text-yellow-400 border-yellow-500/20' : 'text-red-400 border-red-500/30 animate-pulse')">
                {{ field.status }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-xs text-eco-text bg-black/30 p-2 rounded border border-white/5 font-mono">
              <div>湿度: <span class="text-white">{{ field.moisture }}%</span></div>
              <div>虫情: <span class="text-white">{{ field.pestIndex }}</span></div>
              <div>叶绿素: <span class="text-white">{{ field.spad }}</span></div>
              <div>温度: <span class="text-white">{{ field.temp }}°C</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="viewMode === 'shuttle'" class="fixed inset-0 z-[9999] bg-[#050705] flex flex-col items-center justify-center overflow-hidden">
      <canvas ref="warpCanvas" class="absolute inset-0 w-full h-full z-0"></canvas>
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,#050705_100%)] z-10 pointer-events-none"></div>

      <div class="relative z-20 text-center font-mono space-y-4 warp-hud-animate">
        <div class="text-eco-primary text-4xl font-bold tracking-[0.8em] uppercase warp-text-glitch">
          SPATIAL JUMPING...
        </div>
        <div class="text-emerald-300/80 bg-black/40 px-6 py-2 rounded-full border border-emerald-500/30 text-sm tracking-widest backdrop-blur-sm mx-auto inline-block">
          目标锁定: <span class="text-white font-bold">{{ selectedField?.name }}</span> | 正在解析多模态全息矩阵
        </div>
      </div>
    </div>

    <div v-if="showShutter" class="fixed inset-0 z-[10000] pointer-events-none overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-1/2 bg-[#070907] border-b border-eco-primary/40 flex items-end justify-between px-16 pb-3 shutter-top-anim">
        <span class="text-[10px] font-mono text-eco-primary/60 tracking-widest animate-pulse">SYSTEM: HOLOGRAPHIC TRANSITION ACTIVE</span>
        <span class="text-[10px] font-mono text-eco-primary/40">MATRIX_SHUTTER_A // ON</span>
      </div>
      <div class="absolute bottom-0 left-0 w-full h-1/2 bg-[#070907] border-t border-eco-primary/40 flex items-start justify-between px-16 pt-3 shutter-bottom-anim">
        <span class="text-[10px] font-mono text-eco-primary/60 tracking-widest">DECRYPTING QUANTUM DATA STREAMS...</span>
        <span class="text-[10px] font-mono text-eco-primary/40">SECURE_LINK_B // STABLE</span>
      </div>
      <div class="absolute top-1/2 left-0 w-full h-[2px] bg-white shadow-[0_0_15px_#34d399,0_0_5px_#fff] -translate-y-1/2 shutter-line-anim"></div>
    </div>

    <div v-if="viewMode === 'detail'" class="relative z-10 h-full flex flex-col view-animate">
      <div class="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
        <div class="flex items-center gap-4">
          <button @click="viewMode = 'map'" class="group bg-white/5 border border-white/10 px-4 py-2 rounded-xl text-xs font-mono text-gray-400 hover:text-eco-primary hover:border-eco-primary/40 transition-all flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
            [ RETURN TO GIS MAIN CAPTAIN ]
          </button>
          <div class="h-4 w-px bg-white/10"></div>
          <h3 class="text-xl font-bold tracking-wider flex items-center gap-2">
            <span class="w-1.5 h-5 bg-eco-primary rounded-full"></span>
            {{ selectedField?.name }} 全息生境舱
          </h3>
        </div>
        <span class="text-xs font-mono text-gray-500">SECURE LINK AT REAL-TIME</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">

        <div class="lg:col-span-2 bg-black/40 border border-white/5 rounded-2xl relative overflow-hidden shadow-2xl h-[620px] group">

          <img :src="currentVisionImg || fallbackImg"
               alt="Terrace Imagery"
               class="w-full h-full object-cover object-center transition-all duration-700"
               :class="isScanning ? 'opacity-30 grayscale blur-sm' : 'opacity-80 mix-blend-luminosity'" />

          <div class="absolute inset-0 bg-gradient-to-t from-[#0a0c0a] via-transparent to-transparent z-10 pointer-events-none"></div>
          <div class="absolute inset-0 border-[20px] border-black/20 pointer-events-none z-10"></div>

          <div class="absolute top-10 left-10 text-[10px] font-mono text-eco-primary/80 bg-black/60 border border-eco-primary/30 p-2 rounded backdrop-blur z-20">
            <div>CAM_INDEX: {{ selectedField?.id }}_RGB</div>
            <div>STATUS: {{ isScanning ? 'ANALYZING...' : 'ONLINE' }}</div>
            <div v-if="visionDetectCount !== null" class="mt-1 pt-1 border-t border-eco-primary/30" :class="visionDetectCount > 0 ? 'text-yellow-400' : 'text-emerald-400'">
              YOLOv8_OBJECTS: {{ visionDetectCount }}
            </div>
          </div>

          <div v-if="isScanning" class="absolute inset-0 z-20 pointer-events-none">
            <div class="w-full h-1 bg-eco-primary shadow-[0_0_20px_#34d399] animate-radar-scan absolute top-0"></div>
            <div class="absolute inset-0 bg-[linear-gradient(rgba(52,211,153,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(52,211,153,0.05)_1px,transparent_1px)] bg-[size:40px_40px]"></div>
          </div>

          <div class="absolute bottom-8 right-8 z-30">
            <input type="file" ref="fileInput" @change="uploadToYOLOv8" accept="image/*" class="hidden" />
            <button @click="$refs.fileInput.click()"
                    :disabled="isScanning"
                    class="bg-black/80 border border-eco-primary hover:bg-eco-primary/20 text-eco-primary font-mono text-xs px-6 py-3 rounded-none backdrop-blur transition-all flex items-center gap-2 group-hover:opacity-100 opacity-40">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              {{ isScanning ? '神经网格计算中...' : '启动 AI 靶向诊断' }}
            </button>
          </div>

        </div>

        <div class="lg:col-span-1 space-y-4 h-[620px] overflow-y-auto pr-1 custom-scrollbar font-mono">
          <div class="bg-black/50 p-5 rounded-2xl border border-white/10">
            <h4 class="text-xs text-gray-400 mb-4 tracking-widest uppercase flex justify-between items-center">
              <span>● 生境要素遥测 (IoT)</span>
              <span class="text-emerald-400 animate-pulse text-[10px]">SYNCED</span>
            </h4>
            <div class="grid grid-cols-2 gap-3 text-xs mb-3">
              <div class="bg-white/5 p-3 rounded border border-white/5">
                <div class="text-gray-500 mb-1">容积含水率</div>
                <div class="text-white font-bold text-base">{{ selectedField?.moisture }}%</div>
              </div>
              <div class="bg-white/5 p-3 rounded border border-white/5">
                <div class="text-gray-500 mb-1">地表绝对温度</div>
                <div class="text-white font-bold text-base">{{ selectedField?.temp }}°C</div>
              </div>
            </div>
            <div class="space-y-2 text-xs">
              <div class="flex justify-between items-center bg-white/5 p-2 rounded border border-white/5">
                <span class="text-gray-400">全氮 (N)</span><span class="text-white font-bold">{{ selectedField?.n }} <span class="text-[10px] text-gray-600">mg/kg</span></span>
              </div>
              <div class="flex justify-between items-center bg-white/5 p-2 rounded border border-white/5">
                <span class="text-gray-400">有效磷 (P)</span><span class="text-white font-bold">{{ selectedField?.p }} <span class="text-[10px] text-gray-600">mg/kg</span></span>
              </div>
            </div>
          </div>

          <div class="bg-eco-primary/5 p-5 rounded-2xl border transition-all duration-500"
               :class="visionDetectCount > 0 ? 'border-yellow-500/50 bg-yellow-900/10' : (visionDetectCount === 0 ? 'border-emerald-500/50 bg-emerald-900/10' : 'border-eco-primary/20')">
            <h4 class="text-xs font-bold mb-3 flex items-center gap-2" :class="visionDetectCount > 0 ? 'text-yellow-400' : 'text-eco-primary'">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
              天衍中枢调度策略
            </h4>

            <p v-if="visionDetectCount === null" class="text-xs text-gray-400 leading-relaxed font-sans">
              当前区域传感数据均值正常。等待边缘视觉雷达进一步切片确认，以防发生“漏斗型”隐蔽病虫害聚集。
            </p>

            <div v-else-if="visionDetectCount === 0" class="space-y-3">
              <div class="text-xs text-emerald-300 leading-relaxed font-sans border-l-2 border-emerald-500 pl-3">
                <span class="font-bold block mb-1 font-mono">STATUS: SECURE & CLEAR</span>
                YOLOv8 边缘推理完毕。当前生境切片未发现已知病虫害或异常目标聚集。
              </div>
              <div class="text-[10px] text-gray-500 font-mono mt-2 flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                系统继续维持现有水肥自适应滴灌排程。
              </div>
            </div>

            <div v-else class="space-y-3">
              <div class="text-xs text-yellow-300 leading-relaxed font-sans border-l-2 border-yellow-500 pl-3">
                <span class="font-bold block mb-1 font-mono">WARNING: ABNORMAL ENTITIES DETECTED</span>
                YOLOv8 边缘推理完毕。在当前切片中发现 <strong class="text-white">{{ visionDetectCount }}</strong> 处异常聚集特征。
              </div>
              <div class="text-[10px] text-gray-500 font-mono mt-2 flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-yellow-500 animate-ping"></span>
                已自动将坐标数据下发至 P3 植保无人机群，准备实施靶向物理压制。
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';

const viewMode = ref('map');
const selectedField = ref(null);
const showShutter = ref(false);

const fields = ref([]);
const mapRef = ref(null);
let myChart = null;

const warpCanvas = ref(null);
let warpFrameId = null;
let warpParticles = [];

// ======================= 机器视觉协同状态 =======================
const fallbackImg = "https://images.pexels.com/photos/259280/pexels-photo-259280.jpeg?auto=compress&cs=tinysrgb&w=1600";
const currentVisionImg = ref(null);
const isScanning = ref(false);
const visionDetectCount = ref(null);
const fileInput = ref(null);

watch(viewMode, (newVal) => {
  if (newVal === 'map') {
    nextTick(() => {
      if (myChart != null && myChart.dispose) myChart.dispose();
      initMap();
    });
  }
});

const resetDetailState = () => {
  currentVisionImg.value = null;
  visionDetectCount.value = null;
  isScanning.value = false;
};

const triggerShuttle = (field) => {
  selectedField.value = field;
  viewMode.value = 'shuttle';
  showShutter.value = false;
  resetDetailState();

  nextTick(() => { initWarpDrive(); });

  setTimeout(() => {
    showShutter.value = true;
    viewMode.value = 'detail';
    if (warpFrameId) cancelAnimationFrame(warpFrameId);
  }, 2200);

  setTimeout(() => {
    showShutter.value = false;
  }, 3000);
};

// ==================== YOLOv8 边缘推理核心调用 ====================
const uploadToYOLOv8 = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  isScanning.value = true;
  visionDetectCount.value = null;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://127.0.0.1:8000/api/vision/analyze', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error('视觉推理引擎异常');

    const result = await response.json();

    // 延迟 1.5 秒以展示逼真的雷达扫描动效
    setTimeout(() => {
      currentVisionImg.value = result.image_data;
      visionDetectCount.value = result.detected_count;
      isScanning.value = false;
    }, 1500);

  } catch (error) {
    console.error('YOLOv8 通信失败:', error);
    alert('中枢连接丢失，请检查 FastAPI 服务状态。');
    isScanning.value = false;
  }
};


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
  if (!mapRef.value || fields.value.length === 0) return;
  myChart = echarts.init(mapRef.value);
  const scatterData = fields.value.map(f => {
    let color = '#10b981';
    let symbolSize = 16;
    if (f.status === '高危') { color = '#ef4444'; symbolSize = 24; }
    if (f.status === '预警') { color = '#eab308'; symbolSize = 20; }
    return { name: f.name, value: [f.x, f.y], itemStyle: { color: color }, symbolSize: symbolSize, rawData: f };
  });

  const heatData = fields.value.filter(f => f.status === '高危').map(f => ({
    name: f.name, value: [f.x, f.y], itemStyle: { color: 'rgba(239, 68, 68, 0.15)' }, symbolSize: 150
  }));

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: 'rgba(10, 12, 10, 0.95)',
      borderColor: 'rgba(255,255,255,0.08)',
      textStyle: { color: '#fff', fontSize: 11, fontFamily: 'monospace' },
      formatter: (p) => p.seriesName === '热力' ? '' : `<div>${p.name} [点击进入全息生境]</div>`
    },
    graphic: {
      elements: [{
        type: 'image',
        style: { image: 'https://images.pexels.com/photos/2832039/pexels-photo-2832039.jpeg?auto=compress&cs=tinysrgb&w=1200', width: 1000, height: 600, opacity: 0.25 },
        left: 'center', top: 'center'
      }]
    },
    xAxis: { show: false, min: 0, max: 1000 },
    yAxis: { show: false, min: 0, max: 600, inverse: true },
    series: [
      { name: '热力', type: 'scatter', data: heatData, silent: true, itemStyle: { shadowBlur: 40, shadowColor: '#ef4444' } },
      { name: '节点', type: 'effectScatter', coordinateSystem: 'cartesian2d', data: scatterData, showEffectOn: 'render', rippleEffect: { brushType: 'stroke', scale: 4 }, label: { show: true, formatter: '{b}', position: 'right', color: '#ccc', fontSize: 10 } }
    ]
  };

  myChart.setOption(option);
  myChart.on('click', (p) => { if (p.seriesName === '节点') triggerShuttle(p.data.rawData); });
};

const fetchFieldsData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/fields');
    if (!response.ok) throw new Error('Network response was not ok');
    fields.value = await response.json();
    nextTick(() => { initMap(); });
  } catch (error) { console.error('获取数据失败:', error); }
};

onMounted(() => {
  fetchFieldsData();
  window.addEventListener('resize', () => { if (myChart) myChart.resize(); });
});

onUnmounted(() => {
  window.removeEventListener('resize', () => { if (myChart) myChart.resize(); });
  if (myChart) myChart.dispose();
  if (warpFrameId) cancelAnimationFrame(warpFrameId);
});
</script>

<style scoped>
.view-animate { animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(52, 211, 153, 0.2); border-radius: 4px; }

/* 机器视觉雷达光栅特效 */
.animate-radar-scan {
  animation: radarScan 2.5s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}
@keyframes radarScan {
  0% { transform: translateY(0); opacity: 0.8; }
  100% { transform: translateY(620px); opacity: 0.2; }
}

.warp-hud-animate { animation: hudScale 2.2s cubic-bezier(0.1, 0.8, 0.2, 1) forwards; }
@keyframes hudScale {
  0% { transform: scale(0.8); opacity: 0; }
  10% { transform: scale(1.02); opacity: 1; }
  90% { transform: scale(1.08); opacity: 1; filter: blur(0px); }
  100% { transform: scale(1.8); opacity: 0; filter: blur(4px); }
}

.warp-text-glitch {
  position: relative;
  text-shadow: 0 0 15px rgba(52, 211, 153, 0.8);
  animation: glitch-skew 2.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) both infinite;
}
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
</style>