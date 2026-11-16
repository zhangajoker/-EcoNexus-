import { shallowRef, onMounted, onUnmounted } from 'vue';
import type { Ref } from 'vue'; // 【关键修复】：加上 type 关键字，告诉 Vite 这仅仅是个类型
import * as echarts from 'echarts';

export function useEcharts(elRef: Ref<HTMLElement | null>) {
  const chartInstance = shallowRef<echarts.ECharts | null>(null);

  const setOption = (option: echarts.EChartsCoreOption) => {
    if (!chartInstance.value && elRef.value) {
      chartInstance.value = echarts.init(elRef.value);
    }
    chartInstance.value?.setOption(option);
  };

  const resize = () => chartInstance.value?.resize();

  onMounted(() => window.addEventListener('resize', resize));

  onUnmounted(() => {
    window.removeEventListener('resize', resize);
    chartInstance.value?.dispose();
    chartInstance.value = null;
  });

  return { chartInstance, setOption, resize };
}