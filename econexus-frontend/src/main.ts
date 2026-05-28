import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { router } from './router' // 引入你的路由实例

const app = createApp(App)
app.use(router) // 必须有这一行，把路由注入到 app 中
app.mount('#app')