import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Dashboard', component: () => import('../views/Dashboard/Dashboard_index.vue') },
    { path: '/fields', name: 'Fields', component: () => import('../views/Fields/Fields_index.vue') },
    { path: '/tasks', name: 'Tasks', component: () => import('../views/Tasks/Tasks_index.vue') },
    { path: '/esg', name: 'ESG', component: () => import('../views/ESG/ESG_index.vue') },
    { path: '/settings', name: 'Settings', component: () => import('../views/Settings/Settings_index.vue') }
  ]
})

export { router }
export default router