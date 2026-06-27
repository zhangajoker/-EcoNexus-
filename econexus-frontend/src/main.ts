import { createApp } from 'vue'
import { createPinia } from 'pinia' // 1. 必须导入 Pinia
import App from './App.vue'
import { router } from './router'       // 导入你的路由
import './style.css'                // 导入你的 Tailwind 全局样式

const app = createApp(App)
const pinia = createPinia()

// 2. 核心顺序：必须先挂载 pinia，再挂载 router，最后 mount！
app.use(pinia)
app.use(router)

app.mount('#app')