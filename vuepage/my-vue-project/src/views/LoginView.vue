<template>
  <div class="login-container">
    <h1 class="login-title">登录</h1>
    <el-form class="login-form" :model="form" label-width="80px">
      <el-form-item label="邮箱" prop="email">
        <el-input type="email" v-model="form.email" placeholder="请输入邮箱" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="form.password" placeholder="请输入密码" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="login">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      form: {
        email: '',
        password: ''
      }
    };
  },
  methods: {
    login() {
      console.log('Email:', this.form.email, 'Password:', this.form.password);
      // 在这里添加登录逻辑
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 1000px;
  margin: 200px auto;
  padding: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.login-form {
  width: 100%;
}
</style>
