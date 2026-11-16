import { defineStore } from 'pinia';
import { API_BASE } from '../config';

export const useEcoStore = defineStore('eco', {
  state: () => ({
    fields: [],
    esgData: null,
    lastFetched: 0
  }),
  actions: {
    async fetchFields() {
      // 如果 30 秒内拉过数据，就不再重复拉取，直接用缓存
      if (Date.now() - this.lastFetched < 30000) return;
      try {
        const res = await fetch(`${API_BASE}/api/fields`);
        this.fields = await res.json();
        this.lastFetched = Date.now();
      } catch (e) {
        console.error("同步失败", e);
      }
    }
  }
});