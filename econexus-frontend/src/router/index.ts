import { createRouter, createWebHistory } from 'vue-router';
import DashboardIndex from '../views/Dashboard/Dashboard_index.vue';
import TasksIndex from '../views/Tasks/Tasks_index.vue';
import FieldsIndex from '../views/Fields/Fields_index.vue'; // 新增地图模块
import SettingsIndex from '../views/Settings/Settings_index.vue'; // 新增运维日志模块
import ESG_index from "../views/ESG/ESG_index.vue";

const routes = [
  { path: '/', component: DashboardIndex },
  { path: '/tasks', component: TasksIndex },
  { path: '/fields', component: FieldsIndex },
  { path: '/settings', component: SettingsIndex },
  {path: '/ESG', component: ESG_index}
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});