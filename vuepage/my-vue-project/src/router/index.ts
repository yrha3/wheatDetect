import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import AboutView from '../views/AboutView.vue';
import ChatDialogView from '../views/ChatDialogView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/chatAI',
    name: 'chatAI',
    component: ChatDialogView
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
