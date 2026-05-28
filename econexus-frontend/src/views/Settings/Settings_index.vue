<template>
  <div class="relative min-h-screen text-white overflow-hidden" style="background-image: url('https://images.unsplash.com/photo-1542224566-6e85f2e6772f?q=80&w=2000&auto=format&fit=crop'); background-size: cover; background-position: center;">

    <div class="absolute inset-0 bg-gradient-to-br from-eco-dark/95 via-black/80 to-eco-dark/95 backdrop-blur-sm z-0"></div>

    <div class="relative z-10 p-8">
      <div class="flex justify-between items-end mb-8 border-b border-white/5 pb-4">
        <div>
          <h2 class="text-2xl font-bold text-white border-l-4 border-eco-primary pl-4 tracking-wider">边缘节点运维控制台</h2>
          <p class="text-xs text-eco-text mt-2 font-mono">Edge Computing & IoT Gateway Management</p>
        </div>
        <button class="bg-eco-primary/10 border border-eco-primary/50 text-eco-primary px-4 py-2 rounded text-sm hover:bg-eco-primary hover:text-black transition-colors flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          全域系统自检
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="eco-card group">
          <div class="text-eco-text text-xs uppercase tracking-widest mb-2 flex justify-between">
            <span>NVIDIA Jetson 核心温度</span>
            <span class="text-green-400">NORMAL</span>
          </div>
          <div class="text-3xl font-mono text-white">42.5<span class="text-lg text-gray-500 ml-1">°C</span></div>
          <div class="w-full bg-black/50 h-1 mt-3 rounded-full overflow-hidden">
            <div class="bg-eco-primary h-full w-[42%]"></div>
          </div>
        </div>

        <div class="eco-card group">
          <div class="text-eco-text text-xs uppercase tracking-widest mb-2 flex justify-between">
            <span>MQTT Broker 代理状态</span>
            <span class="text-eco-primary animate-pulse">● ACTIVE</span>
          </div>
          <div class="text-3xl font-mono text-white">1,248<span class="text-lg text-gray-500 ml-1">msg/s</span></div>
          <div class="mt-2 text-[10px] text-gray-400 font-mono">Topic: /econexus/sensors/#</div>
        </div>

        <div class="eco-card group">
          <div class="text-eco-text text-xs uppercase tracking-widest mb-2 flex justify-between">
            <span>边缘存储 (SSD)</span>
            <span class="text-yellow-500">CLEANING</span>
          </div>
          <div class="text-3xl font-mono text-white">18.2<span class="text-lg text-gray-500 ml-1">%</span></div>
           <div class="w-full bg-black/50 h-1 mt-3 rounded-full overflow-hidden">
            <div class="bg-yellow-500 h-full w-[18%]"></div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="eco-card lg:col-span-1 h-[400px] flex flex-col">
          <h3 class="text-sm font-bold mb-4 text-white uppercase tracking-widest border-b border-white/10 pb-2">现场设备拓扑 (IoT Topology)</h3>
          <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-3">
            <div v-for="device in devices" :key="device.name"
                 class="bg-black/30 p-3 rounded border transition-colors flex items-center justify-between"
                 :class="device.online ? 'border-white/5 hover:border-eco-primary/30' : 'border-red-900/50'">
              <div>
                <div class="text-sm text-gray-200">{{ device.name }}</div>
                <div class="text-[10px] text-gray-500 font-mono mt-1">{{ device.ip }}</div>
              </div>
              <div class="flex flex-col items-end gap-1">
                <span class="text-[10px] px-2 py-0.5 rounded font-mono flex items-center gap-1" :class="device.online ? 'bg-eco-primary/10 text-eco-primary' : 'bg-red-500/10 text-red-400'">
                  <span class="w-1.5 h-1.5 rounded-full" :class="device.online ? 'bg-eco-primary' : 'bg-red-500'"></span>
                  {{ device.online ? 'ONLINE' : 'OFFLINE' }}
                </span>
                <button v-if="!device.online" @click="rebootDevice(device.name)" class="text-[10px] text-gray-400 hover:text-white underline">尝试唤醒</button>
              </div>
            </div>
          </div>
        </div>

        <div class="eco-card lg:col-span-2 h-[400px] flex flex-col bg-black/80">
          <div class="flex justify-between items-center mb-2 border-b border-white/10 pb-2">
            <h3 class="text-sm font-bold text-gray-300 uppercase tracking-widest flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
              Tailing system.log
            </h3>
            <span class="text-[10px] text-eco-primary font-mono animate-pulse">_ Live</span>
          </div>
          <div class="flex-1 overflow-y-auto font-mono text-[11px] leading-relaxed custom-scrollbar">
            <div v-for="(log, idx) in logs" :key="idx" class="hover:bg-white/5 px-1 rounded transition-colors">
              <span class="text-gray-600 mr-3">[{{ log.time }}]</span>
              <span class="mr-2" :class="log.module === 'AI_VISION' ? 'text-purple-400' : 'text-blue-400'">[{{ log.module }}]</span>
              <span :class="{'text-red-400': log.level === 'ERROR', 'text-yellow-400': log.level === 'WARN', 'text-eco-text': log.level === 'INFO'}">
                {{ log.msg }}
              </span>
            </div>
            <div class="text-gray-500 mt-2 flex items-center gap-2">
              <span class="w-1.5 h-3 bg-gray-500 animate-pulse"></span>
              Waiting for new logs...
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
  { name: '大疆 T40 停机坪', ip: '192.168.1.50', online: false }
]);

const logs = ref([
  { time: '14:22:10', module: 'SYSTEM', level: 'INFO', msg: 'Core framework initialized successfully. TensorRT engine loaded.' },
  { time: '14:22:15', module: 'MQTT', level: 'INFO', msg: 'Subscribed to topic: sensor/water_quality/#' },
  { time: '14:28:01', module: 'AI_VISION', level: 'WARN', msg: 'Pest threshold exceeded in node A. SAHI inference completed in 42ms.' },
  { time: '14:35:22', module: 'HARDWARE', level: 'ERROR', msg: 'Drone hangar heartbeat timeout. Retrying connection (1/3)...' },
  { time: '14:36:05', module: 'SYSTEM', level: 'INFO', msg: 'Irrigation schedule optimized via PM model. Saved 14.5% water.' }
]);

const rebootDevice = (name) => {
  alert(`已向 [${name}] 发送 Wake-on-LAN 唤醒指令，请观察日志输出。`);
};
</script>

<style scoped>
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