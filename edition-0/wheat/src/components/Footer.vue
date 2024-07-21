<template>
    <el-footer class="footer">
      <div class="footer-content">
        <div class="footer-links">
          <el-button type="text" @click="goToHome">首页</el-button>
          <el-button type="text" @click="goToAbout">关于我们</el-button>
          <el-button type="text" @click="goToContact">联系我们</el-button>
        </div>
        <div class="footer-info">
          <p>© 2024 Wheat Detection Platform. All Rights Reserved.</p>
        </div>
      </div>
    </el-footer>
  </template>
  
  <script>
  export default {
    name: 'Footer',
    methods: {
      goToHome() {
        this.$router.push({ name: 'home' });
      },
      goToAbout() {
        this.$router.push({ name: 'about' });
      },
      goToContact() {
        this.$router.push({ name: 'contact' });
      },
    },
  };
  </script>
  
  <style scoped>
  .footer {
    background-color: #545c64;
    color: #fff;
    padding: 20px 0;
  }
  .footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  .footer-links {
    display: flex;
  }
  .footer-info {
    text-align: right;
  }
  </style>
  