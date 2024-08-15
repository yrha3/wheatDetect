<template>
    <div class="sidebar-content">
      <h2>小麦科普知识</h2>
      <el-divider></el-divider>
      <ul>
        <li><strong>小麦的种类：</strong>小麦主要分为硬小麦和软小麦，常用于制作面粉和面包。</li>
        <li><strong>小麦的生长条件：</strong>小麦适合在温暖、湿润的环境中生长，主要分布在北半球的温带地区。</li>
        <li><strong>营养价值：</strong>小麦富含碳水化合物、蛋白质和多种维生素，是人类的重要粮食来源。</li>
        <li><strong>小麦的用途：</strong>除用于食品外，小麦的秸秆还可用于造纸和制作生物燃料。</li>
      </ul>
  
      <h2>网页功能解释</h2>
      <el-divider></el-divider>
      <ul>
        <li><strong>图像上传：</strong>用户可以上传小麦相关的图片进行检测。</li>
        <li><strong>检测结果：</strong>系统会对上传的图片进行分析，并返回检测结果。</li>
        <li><strong>科普知识：</strong>提供小麦相关的知识，以增加用户的了解。</li>
        <li><strong>轮播图：</strong>展示小麦的多样性和相关活动。</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Sidebar',
  };
  </script>
  
  <style scoped>
  .sidebar-content {
    padding: 15px;
    background-color: #f9f9f9;
  }
  .sidebar-content h2 {
    margin-bottom: 10px;
  }
  .sidebar-content ul {
    list-style-type: none;
    padding: 0;
  }
  .sidebar-content li {
    margin-bottom: 10px;
  }
  </style>
  