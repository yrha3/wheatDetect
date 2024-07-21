<template>
 <div class="common-layout">
    <el-container>
      <el-header>
        <h1>欢迎来到检测平台</h1>
      </el-header>
      <el-container>
        <el-aside width="200px" class="sidebar">
          <Sidebar />
        </el-aside>
        <el-container>
          <el-main>
            <el-carousel :interval="4000" type="card" height="300px">
              <el-carousel-item v-for="item in carouselData" :key="item">
                <img :src="item.url" alt="not found" class="carousel-image" />
              </el-carousel-item>
            </el-carousel>
            <UploadComponent />
            <!-- <DetectionResults :results="detectionResults" /> -->
            <WheatInfoSlider/>
          </el-main>
          <el-footer>
            <Footer/>
          </el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.home-view {
  display: flex;
  height: 100vh; /* Fill the full height */
}
.sidebar-column {
  height: 100%; /* Ensure the sidebar fills the height */
}
</style>

<script>
import UploadComponent from '../components/UploadComponent.vue';
import DetectionResults from '../components/DetectionResults.vue';
import Sidebar from '../components/Sidebar.vue';
import Footer from '../components/Footer.vue';
import WheatInfoSlider from '../components/WheatInfoSlider.vue';


import carousel01 from '@/assets/images/carousel01.jpeg';
import carousel02 from '@/assets/images/carousel02.png';
import carousel03 from '@/assets/images/carousel03.jpeg';
import carousel04 from '@/assets/images/carousel04.jpeg';
import carousel05 from '@/assets/images/carousel05.png';

export default {
  components: {
    UploadComponent,
    DetectionResults,
    WheatInfoSlider,
    Sidebar,
    Footer,
  },
  data() {
    return {
      carouselData: [
        { url: carousel01 },
        { url: carousel02 },
        { url: carousel03 },
        { url: carousel04 },
        { url: carousel05 },
      ],
      detectionResults: [
        { image: 'url_to_image_1', status: '合格', details: '检测通过' },
        { image: 'url_to_image_2', status: '不合格', details: '检测未通过' },
        // 添加更多检测结果
      ],
    };
  },
};
</script>
