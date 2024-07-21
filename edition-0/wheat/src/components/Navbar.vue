<template>
  <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :ellipsis="false"
    @select="handleSelect">
    <el-menu-item index="0">
      <img style="width: 100px" src="../assets/images/小麦.png" alt="Element logo" />
    </el-menu-item>
    <div class="flex-grow" />
    <el-menu-item index="1" @click="navigateTo('home')">首页</el-menu-item>
    <el-menu-item index="2" @click="navigateTo('login')">登录</el-menu-item>
    <el-menu-item index="3" @click="navigateTo('about')">关于我们</el-menu-item>
    <el-sub-menu index="4">
      <template #title>更多选项</template>
      <el-menu-item index="4-1">选项一</el-menu-item>
      <el-menu-item index="4-2">选项二</el-menu-item>
      <el-menu-item index="4-3">选项三</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const activeIndex = ref('1');
const router = useRouter();

const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};

const navigateTo = (route: string) => {
  router.push({ name: route });
};
</script>

<style>
.flex-grow {
  flex-grow: 1;
}
</style>
