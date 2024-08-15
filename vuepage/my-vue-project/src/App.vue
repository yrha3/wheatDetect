<template>
  <div>
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
/* 全局样式 */
body {
  background: linear-gradient(to bottom, #9be96d 0%, #8ec5fc 100%),
              linear-gradient(to right, #f7c6c7 0%, #f7f8d9 100%),
              linear-gradient(to bottom, #f0f9ff 0%, #d0e6f1 100%);
  background-blend-mode: multiply;
  background-size: 200% 200%;
  animation: gradientAnimation 15s ease infinite;
  height: 100vh;
  margin: 0;
  font-family: Arial, sans-serif;
}

@keyframes gradientAnimation {
  0% {
    background-position: 0% 0%;
  }
  50% {
    background-position: 100% 100%;
  }
  100% {
    background-position: 0% 0%;
  }
}

/* 使主内容区保持在背景上方 */
#app {
  position: relative;
  z-index: 1;
}
</style>
