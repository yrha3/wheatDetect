<template>
  <el-row :gutter="20">
    <!-- 左侧：两个图片和信息 -->
    <el-col :span="12">
      <div class="media-row">
        <el-card shadow="hover" class="transparent-card" style="width: 300px; margin-right: 50px">
          <img src="../assets/images/carousel02.png" alt="Image 1" class="image"/>
          <div class="card-content">
            <p>This is the description for image</p>
          </div>
        </el-card>

        <el-card shadow="hover" class="transparent-card" style="width: 300px">
          <img src="../assets/images/carousel02.png" alt="Image 2" class="image"/>
          <div class="card-content">
            <p>This is the description for image</p>
          </div>
        </el-card>
      </div>
    </el-col>

    <!-- 右侧：两个视频 -->
    <el-col :span="12">
      <div class="media-row">
        <div class="video-container" style="margin-right: 50px">
          <div class="video-wrapper">
            <video
              playsinline
              autoplay
              loop
              muted
              ref="video1"
              class="video-element"
            >
              <source src="https://cdn.openai.com/chatgpt/browsing.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <div class="video-overlay">
              <button
                type="button"
                class="pause-button"
                aria-label="Pause video"
                @click="togglePlay($refs.video1)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="10" viewBox="0 0 10 12" fill="none">
                  <rect width="3" height="11" y=".5" fill="currentColor" rx="1.5"></rect>
                  <rect width="3" height="11" x="7" y=".5" fill="currentColor" rx="1.5"></rect>
                </svg>
              </button>
            </div>
            <div class="video-blur"></div>
          </div>
        </div>

        <div class="video-container">
          <div class="video-wrapper">
            <video
              playsinline
              autoplay
              loop
              muted
              ref="video2"
              class="video-element"
            >
              <source src="https://cdn.openai.com/chatgpt/browsing.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <div class="video-overlay">
              <button
                type="button"
                class="pause-button"
                aria-label="Pause video"
                @click="togglePlay($refs.video2)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="10" viewBox="0 0 10 12" fill="none">
                  <rect width="3" height="11" y=".5" fill="currentColor" rx="1.5"></rect>
                  <rect width="3" height="11" x="7" y=".5" fill="currentColor" rx="1.5"></rect>
                </svg>
              </button>
            </div>
            <div class="video-blur"></div>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'MediaLayout',
  methods: {
    togglePlay(video) {
      if (video.paused) {
        video.play();
      } else {
        video.pause();
      }
    }
  }
}
</script>

<style scoped>
.media-row {
  display: flex;
}

.transparent-card {
  background-color: rgba(255, 255, 255, 0.8); /* 设定透明度 */
  border: 1px solid rgba(0, 0, 0, 0.1); /* 设定边框颜色 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 阴影 */
}

.image {
  width: 240px;
  height: 200px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.card-content {
  padding: 10px;
  color: #333; /* 文本颜色 */
}

.video-container {
  width: 300px;
  position: relative;
}

.video-wrapper {
  position: relative;
  width: 100%;
  padding-top: 100%;
  overflow: hidden;
  border-radius: 0.5rem;
}

.video-element {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 4px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  color: white;
  z-index: 1;
}

.pause-button {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  border-radius: 50%;
  cursor: pointer;
}

.video-blur {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  filter: blur(20px);
  opacity: 0;
  transition: opacity 0.3s;
}

.video-wrapper:hover .video-blur,
.video-wrapper:focus .video-blur {
  opacity: 1;
}
</style>
