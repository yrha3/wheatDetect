<template>
  <div class="dashboard-container">
    <!-- <div class="dashboard-text">name: {{ name }}</div> -->
    <el-menu
      class="el-menu-demo"
      mode="horizontal"
      background-color="#ffffff"
      text-color="#303133"
      active-text-color="#409EFF"
    >
      <el-menu-item index="1" @click="navigateTo('image-upload')">Image Upload</el-menu-item>
      <el-menu-item index="2" @click="navigateTo('video-upload')">Video Upload</el-menu-item>
      <el-menu-item index="3" @click="navigateTo('chat')">Chat AI</el-menu-item>
      <el-menu-item index="3" @click="navigateTo('wheat-disease')">Wheat Disease</el-menu-item>
    </el-menu>
    <!-- 子页面显示 -->
    <router-view />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',

  computed: {
    ...mapGetters([
      'name'
    ])
  },
  methods: {
    // 导航到不同的页面
    navigateTo(page) {
      this.$router.push({ name: page })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
.el-menu-demo {
  line-height: 60px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  font-size: 16px;
  padding: 0 20px;
}

.el-menu-item {
  font-weight: 500;
  padding-left: 20px;
  padding-right: 20px;
}

.el-menu-item:hover {
  background-color: #f5f5f5;
}

.el-menu-item.is-active {
  color: #409EFF;
  border-bottom: 2px solid #409EFF;
}
</style>
