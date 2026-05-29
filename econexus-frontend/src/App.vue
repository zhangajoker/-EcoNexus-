<template>
  <div class="flex h-screen bg-eco-dark text-white overflow-hidden">
    <nav class="w-20 border-r border-eco-border bg-black/20 flex flex-col items-center py-8 gap-8 z-50">

      <router-link to="/" title="主控看板" class="p-3 rounded-xl text-gray-500 hover:text-eco-primary hover:bg-eco-primary/10 transition-all" active-class="text-eco-primary bg-eco-primary/10 border border-eco-primary/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter">
          <rect x="3" y="3" width="7" height="7" />
          <rect x="14" y="3" width="7" height="11" />
          <rect x="14" y="17" width="7" height="4" />
          <rect x="3" y="13" width="7" height="8" />
        </svg>
      </router-link>

      <router-link to="/fields" title="农田孪生感知" class="p-3 rounded-xl text-gray-500 hover:text-eco-primary hover:bg-eco-primary/10 transition-all" active-class="text-eco-primary bg-eco-primary/10 border border-eco-primary/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter">
          <polygon points="12 2 22 8 22 16 12 22 2 16 2 8" />
          <polyline points="2 8 12 14 22 8" />
          <line x1="12" y1="14" x2="12" y2="22" />
        </svg>
      </router-link>

      <router-link to="/tasks" title="AI 防治调度" class="p-3 rounded-xl text-gray-500 hover:text-eco-primary hover:bg-eco-primary/10 transition-all" active-class="text-eco-primary bg-eco-primary/10 border border-eco-primary/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter">
          <path d="M3 9V5h4M21 9V5h-4M3 15v4h4M21 15v4h-4" />
          <rect x="8" y="8" width="8" height="8" />
          <line x1="12" y1="2" x2="12" y2="6" />
          <line x1="12" y1="18" x2="12" y2="22" />
          <line x1="2" y1="12" x2="6" y2="12" />
          <line x1="18" y1="12" x2="22" y2="12" />
        </svg>
      </router-link>

      <router-link to="/esg" title="ESG 碳汇资产" class="p-3 rounded-xl text-gray-500 hover:text-eco-primary hover:bg-eco-primary/10 transition-all" active-class="text-eco-primary bg-eco-primary/10 border border-eco-primary/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
        </svg>
      </router-link>

      <router-link to="/settings" title="系统核心设置" class="p-3 rounded-xl text-gray-500 hover:text-eco-primary hover:bg-eco-primary/10 transition-all" active-class="text-eco-primary bg-eco-primary/10 border border-eco-primary/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter">
          <line x1="4" y1="6" x2="20" y2="6" />
          <line x1="4" y1="12" x2="20" y2="12" />
          <line x1="4" y1="18" x2="20" y2="18" />
          <rect x="8" y="4" width="4" height="4" />
          <rect x="14" y="10" width="4" height="4" />
          <rect x="6" y="16" width="4" height="4" />
        </svg>
      </router-link>

    </nav>

    <main class="flex-1 overflow-y-auto relative">
      <router-view />
    </main>
  </div>
</template>