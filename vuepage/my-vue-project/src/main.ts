import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

const app = createApp(App);

app.config.globalProperties.$baseUrl = 'http://39.107.142.23:5000';
app.use(router);
app.use(ElementPlus);
app.mount('#app');
