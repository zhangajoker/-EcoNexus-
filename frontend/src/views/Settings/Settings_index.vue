<template>
  <div class="relative min-h-screen text-white select-none bg-[#0a0c0a] pb-32"> <!-- 增加了底部 padding 防遮挡 -->

    <div class="absolute inset-0 z-0 pointer-events-none">
      <img src="https://images.unsplash.com/photo-1542224566-6e85f2e6772f?q=80&w=2000&auto=format&fit=crop"
           class="w-full h-full object-cover opacity-10 grayscale mix-blend-luminosity" alt="Server Room" />
      <div class="absolute inset-0 bg-gradient-to-b from-[#0a0c0a]/80 via-[#0a0c0a]/95 to-[#0a0c0a] z-10"></div>
    </div>

    <div class="relative z-10 p-8 flex flex-col view-animate h-full">

      <div class="mb-8 flex justify-between items-end border-b border-white/10 pb-6 shrink-0">
        <div>
          <h2 class="text-4xl font-bold border-l-[6px] border-eco-primary pl-5 tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.5)]">边缘节点运维控制台</h2>
          <p class="text-xl font-bold text-gray-400 mt-3 font-mono uppercase tracking-widest">Edge Computing & IoT Gateway Management</p>
        </div>
        <button class="bg-white/5 border border-white/10 px-5 py-2.5 rounded text-sm font-bold font-mono text-gray-300 hover:text-white hover:border-cyan-500/50 transition-all flex items-center gap-2 group shadow-lg">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 group-hover:text-cyan-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          全域系统自检
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 shrink-0">
        <!-- 卡片1：核心温度 -->
        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-emerald-500/40 transition-colors border-l-[4px] border-l-emerald-500 shadow-[inset_1px_0_10px_rgba(16,185,129,0.1)]">
          <div class="absolute -top-[1px] -right-[1px] w-3 h-3 border-t-2 border-r-2 border-emerald-500/50"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-sm font-bold text-gray-300 font-mono tracking-widest uppercase">NVIDIA Jetson 核心温度</span>
            <span class="text-emerald-400 font-bold font-mono text-xs bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">NORMAL</span>
          </div>
          <div class="flex items-baseline gap-2 mt-2">
            <div class="text-6xl font-bold font-mono tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-emerald-300 to-cyan-500 drop-shadow-[0_2px_10px_rgba(52,211,153,0.3)]">42.5</div>
            <span class="text-xl font-bold text-gray-400">°C</span>
          </div>
          <div class="w-full bg-black/80 h-2 mt-5 rounded-full overflow-hidden border border-white/5">
            <div class="bg-gradient-to-r from-emerald-500 to-cyan-400 h-full w-[42%] shadow-[0_0_10px_#34d399] relative">
              <div class="absolute right-0 top-0 w-4 h-full bg-white/50 blur-[2px]"></div>
            </div>
          </div>
        </div>

        <!-- 卡片2：MQTT 吞吐量 -->
        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-blue-500/40 transition-colors border-l-[4px] border-l-blue-500 shadow-[inset_1px_0_10px_rgba(59,130,246,0.1)]">
          <div class="absolute -top-[1px] -right-[1px] w-3 h-3 border-t-2 border-r-2 border-blue-500/50"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-sm font-bold text-gray-300 font-mono tracking-widest uppercase">MQTT Broker 代理状态</span>
            <span class="text-blue-400 font-bold font-mono text-xs bg-blue-500/10 px-2 py-1 rounded border border-blue-500/20 flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></span> ACTIVE
            </span>
          </div>
          <div class="flex items-baseline gap-2 mt-2">
            <div class="text-6xl font-bold font-mono tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-cyan-300 to-blue-500 drop-shadow-[0_2px_10px_rgba(59,130,246,0.3)]">1,248</div>
            <span class="text-xl font-bold text-gray-400">msg/s</span>
          </div>
          <div class="mt-4 pt-4 border-t border-white/5 text-xs text-cyan-500/70 font-mono flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            Topic: /econexus/sensors/#
          </div>
        </div>

        <!-- 卡片3：SSD 存储 -->
        <div class="bg-black/40 border border-white/5 p-6 rounded-none relative group hover:border-amber-500/40 transition-colors border-l-[4px] border-l-amber-500 shadow-[inset_1px_0_10px_rgba(245,158,11,0.1)]">
          <div class="absolute -top-[1px] -right-[1px] w-3 h-3 border-t-2 border-r-2 border-amber-500/50"></div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-sm font-bold text-gray-300 font-mono tracking-widest uppercase">边缘存储 (SSD)</span>
            <span class="text-amber-400 font-bold font-mono text-xs bg-amber-500/10 px-2 py-1 rounded border border-amber-500/20">CLEANING</span>
          </div>
          <div class="flex items-baseline gap-2 mt-2">
            <div class="text-6xl font-bold font-mono tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-yellow-200 to-orange-500 drop-shadow-[0_2px_10px_rgba(245,158,11,0.3)]">18.2</div>
            <span class="text-xl font-bold text-gray-400">%</span>
          </div>
          <div class="w-full bg-black/80 h-2 mt-5 rounded-full overflow-hidden border border-white/5">
            <div class="bg-gradient-to-r from-yellow-500 to-orange-400 h-full w-[18%] shadow-[0_0_10px_#f59e0b] relative">
              <div class="absolute right-0 top-0 w-4 h-full bg-white/50 blur-[2px]"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 下半部分：设备拓扑与日志流 (核心修复：移除死板高度，让内容自由撑开！) -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">

        <!-- 左侧：设备拓扑 -->
        <div class="lg:col-span-1 bg-black/40 border border-white/5 rounded-none p-6 relative flex flex-col h-full">
          <div class="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-emerald-500/0 via-emerald-500/30 to-emerald-500/0"></div>
          <h3 class="text-lg font-bold text-white uppercase tracking-widest mb-6 border-b border-white/10 pb-4 flex items-center gap-3">
            <span class="w-2 h-2 bg-emerald-500 shadow-[0_0_10px_#10b981]"></span>
            现场设备拓扑 (IoT Topology)
          </h3>
          <div class="flex-1 space-y-4">
            <div v-for="device in devices" :key="device.name"
                 class="bg-black/60 p-5 rounded-lg border transition-colors flex items-center justify-between shadow-md"
                 :class="device.online ? 'border-white/5 hover:border-emerald-500/30' : 'border-red-900/50 bg-red-950/10'">
              <div>
                <div class="text-base font-bold text-gray-200 tracking-wide">{{ device.name }}</div>
                <div class="text-sm text-cyan-500/70 font-mono mt-1 flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                  {{ device.ip }}
                </div>
              </div>
              <div class="flex flex-col items-end gap-2">
                <span class="text-xs px-3 py-1 rounded font-mono font-bold flex items-center gap-2 border"
                      :class="device.online ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-red-500/10 text-red-400 border-red-500/20'">
                  <span class="w-2 h-2 rounded-full"
                        :class="device.online ? 'bg-emerald-400 animate-pulse shadow-[0_0_8px_#34d399]' : 'bg-red-500'"></span>
                  {{ device.online ? 'ONLINE' : 'OFFLINE' }}
                </span>
                <button v-if="!device.online" @click="rebootDevice(device.name)" class="text-xs font-bold text-gray-400 hover:text-white underline decoration-dashed underline-offset-2">尝试唤醒</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：真实赛博终端日志 -->
        <div class="lg:col-span-2 bg-[#05090f]/90 border border-white/5 rounded-none p-6 relative flex flex-col h-full border-t-[4px] border-t-cyan-500/50 shadow-[inset_0_0_50px_rgba(8,145,178,0.05)]">
          <div class="flex justify-between items-center mb-6 border-b border-white/10 pb-4 shrink-0">
            <h3 class="text-lg font-bold text-gray-200 uppercase tracking-widest flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-cyan-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
              TAILING SYSTEM.LOG
            </h3>
            <div class="flex items-center gap-2 text-xs text-cyan-400 font-mono font-bold bg-cyan-900/30 px-3 py-1 rounded">
              <span class="w-2 h-2 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_8px_#22d3ee]"></span>
              LIVE_STREAM
            </div>
          </div>

          <div class="flex-1 font-mono text-base leading-loose space-y-3">
            <div v-for="(log, idx) in logs" :key="idx" class="hover:bg-white/5 px-3 py-2 rounded transition-colors group">
              <span class="text-gray-500 mr-4 font-bold group-hover:text-gray-300 transition-colors">[{{ log.time }}]</span>
              <span class="mr-3 font-bold tracking-wide"
                    :class="log.module === 'AI_VISION' ? 'text-purple-400' : (log.module === 'HARDWARE' ? 'text-orange-400' : 'text-blue-400')">
                [{{ log.module }}]
              </span>
              <span class="font-bold"
                    :class="{'text-red-400 drop-shadow-[0_0_5px_rgba(248,113,113,0.5)]': log.level === 'ERROR',
                             'text-yellow-400': log.level === 'WARN',
                             'text-emerald-300': log.level === 'INFO'}">
                {{ log.msg }}
              </span>
            </div>
            <div class="text-cyan-500/50 mt-6 flex items-center gap-3 font-bold px-3">
              <span class="w-2 h-4 bg-cyan-500 animate-pulse"></span>
              Waiting for incoming connections...
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const devices = ref([
  { name: 'LoRa 主网关 (Base)', ip: '192.168.1.10', online: true },
  { name: 'YOLOv8 视觉边缘节点', ip: '192.168.1.15', online: true },
  { name: '墒情阵列 (A区)', ip: '10.0.0.42', online: true },
  { name: '水质检测仪 (总阀)', ip: '10.0.0.45', online: true },
  { name: '大疆 T40 停机坪', ip: '192.168.1.50', online: false },
  // 增加几个模拟设备把页面撑满，证明现在它是全局滚动的了！
  { name: '微波气象雷达 (基站)', ip: '192.168.1.66', online: true },
  { name: '太阳能供电中枢', ip: '10.0.0.99', online: true },
  { name: '自动灌溉伺服电磁阀', ip: '192.168.1.108', online: true }
]);

const logs = ref([
  { time: '14:22:10', module: 'SYSTEM', level: 'INFO', msg: 'Core framework initialized successfully. TensorRT engine loaded.' },
  { time: '14:22:15', module: 'MQTT', level: 'INFO', msg: 'Subscribed to topic: sensor/water_quality/#' },
  { time: '14:28:01', module: 'AI_VISION', level: 'WARN', msg: 'Pest threshold exceeded in node A. SAHI inference completed in 42ms.' },
  { time: '14:35:22', module: 'HARDWARE', level: 'ERROR', msg: 'Drone hangar heartbeat timeout. Retrying connection (1/3)...' },
  { time: '14:36:05', module: 'SYSTEM', level: 'INFO', msg: 'Irrigation schedule optimized via PM model. Saved 14.5% water.' },
  // 增加几条日志
  { time: '14:38:12', module: 'SYSTEM', level: 'INFO', msg: 'Syncing ESG blockchain ledger data to core server...' },
  { time: '14:40:01', module: 'AI_VISION', level: 'INFO', msg: 'Routine field patrol scan complete. No anomalies detected.' },
  { time: '14:42:55', module: 'MQTT', level: 'WARN', msg: 'High latency detected on node C. Packet loss 2.5%.' },
  { time: '14:45:10', module: 'HARDWARE', level: 'ERROR', msg: 'Soil sensor C-02 disconnected unexpectedly.' }
]);

const rebootDevice = (name) => {
  alert(`已向 [${name}] 发送 Wake-on-LAN 唤醒指令，请观察日志输出。`);
};
</script>

<style scoped>
.view-animate { animation: fadeIn 0.5s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>