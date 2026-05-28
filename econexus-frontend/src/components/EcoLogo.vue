<template>
  <div class="flex items-center gap-3 group relative cursor-pointer" @mouseenter="startProcessing" @mouseleave="stopProcessing">
    <div class="w-12 h-12 relative flex items-center justify-center">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="absolute inset-0 h-full w-full"
        viewBox="0 0 512 512"
        fill="none"
      >
        <path
          d="M256 16L40.9 140.2v231.6L256 496l215.1-124.2V140.2L256 16z"
          class="eco-frame-flow"
          stroke="#34d399"
          stroke-width="12"
          stroke-miterlimit="10"
        />

        <path
          d="M256 160c0 0-48 48-48 96s48 96 48 96 48-48 48-96-48-96-48-96zm0 160c-26.5 0-48-21.5-48-48s21.5-48 48-48 48 21.5 48 48-21.5 48-48 48z"
          class="eco-leaf-pulse"
          stroke="#34d399"
          stroke-width="12"
          stroke-linecap="round"
        />

        <path
          d="M168 256c0-66.3 53.7-120 120-120 44.2 0 81.3 23.9 100.8 59.2M168 256c0 66.3 53.7 120 120 120 22.1 0 42.1-6 59.1-16.3"
          class="eco-circuit-flow"
          stroke="#a7f3d0"
          stroke-width="10"
          stroke-linecap="round"
        />

        <g class="eco-circuit-nodes">
          <circle cx="288" cy="208" r="16" fill="#34d399"/>
          <circle cx="288" cy="304" r="16" fill="#34d399"/>
          <circle cx="368" cy="256" r="16" fill="#34d399"/>
        </g>
      </svg>

      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="absolute inset-0 h-full w-full rotate-45 scale-110"
        viewBox="0 0 512 512"
        fill="none"
      >
        <circle
          cx="288"
          cy="256"
          r="100"
          class="eco-data-orbit"
          stroke="#34d399"
          stroke-width="2"
          stroke-dasharray="100 1500"
        />
        <circle cx="288" cy="156" r="4" fill="#a7f3d0" class="eco-data-node" />
        <circle cx="388" cy="256" r="4" fill="#a7f3d0" class="eco-data-node" style="animation-delay: -0.2s;"/>
        <circle cx="288" cy="356" r="4" fill="#a7f3d0" class="eco-data-node" style="animation-delay: -0.4s;"/>
      </svg>
    </div>

    <div class="flex flex-col">
      <span class="text-2xl font-bold tracking-wider text-white group-hover:text-eco-primary transition-colors">EcoNexus</span>
      <span class="text-xs text-eco-text uppercase tracking-widest font-mono">天衍·生境 IoT</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isProcessing = ref(false);

const startProcessing = () => {
  isProcessing.value = true;
};

const stopProcessing = () => {
  isProcessing.value = false;
};
</script>

<style scoped>
/* 定义动画帧 */

/* 1. 外部框架能量描边流动 */
@keyframes ecoFrameFlow {
  0% { stroke-dasharray: 0 1500; stroke-dashoffset: 0; }
  30% { stroke-dasharray: 400 1500; }
  60% { stroke-dasharray: 800 1500; }
  100% { stroke-dasharray: 1200 1500; stroke-dashoffset: -1200; }
}

/* 2. 内部电路能量描边流动 */
@keyframes ecoCircuitFlow {
  0% { stroke-dasharray: 0 600; stroke-dashoffset: 0; opacity: 0.3; }
  50% { stroke-dasharray: 300 600; opacity: 1; }
  100% { stroke-dasharray: 600 600; stroke-dashoffset: -600; opacity: 0.3; }
}

/* 3. 叶子脉动呼吸 */
@keyframes ecoLeafPulse {
  0%, 100% { transform: scale(1); filter: blur(0px); }
  50% { transform: scale(1.05); filter: blur(1.5px); }
}

/* 4. 数据光环轨道描边流动 */
@keyframes ecoDataOrbitFlow {
  0% { stroke-dashoffset: 1500; }
  100% { stroke-dashoffset: 0; }
}

/* 5. 数据节点亮点脉动 */
@keyframes ecoDataNodePulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.3); opacity: 1; }
}

/* 应用动画 */

.eco-frame-flow {
  animation: ecoFrameFlow 3s infinite linear;
  /* 应用静态Glow效果，鼠标 hover 时增强 */
  filter: drop-shadow(0 0 5px rgba(52, 211, 153, 0.5));
}

.eco-circuit-flow {
  animation: ecoCircuitFlow 2s infinite ease-in-out;
  animation-delay: -0.5s;
}

.eco-leaf-pulse {
  animation: ecoLeafPulse 2s infinite ease-in-out;
  transform-origin: center center;
}

.eco-circuit-nodes {
  animation: ecoDataNodePulse 1s infinite alternate;
  animation-delay: -0.8s;
  transform-origin: center center;
}

.eco-data-orbit {
  animation: ecoDataOrbitFlow 0.8s infinite linear;
}

.eco-data-node {
  animation: ecoDataNodePulse 0.5s infinite alternate;
  transform-origin: center center;
}

/* 鼠标悬停交互效果：增强Glow，加速光环，模拟“运行中”状态 */
.group:hover .eco-frame-flow {
  filter: drop-shadow(0 0 10px rgba(52, 211, 153, 1));
}

.group:hover .eco-leaf-pulse {
  animation: ecoLeafPulse 0.5s infinite ease-in-out; /* 加速脉动 */
}

.group:hover .eco-data-orbit {
  animation: ecoDataOrbitFlow 0.2s infinite linear; /* 疯狂加速数据流动 */
}
</style>