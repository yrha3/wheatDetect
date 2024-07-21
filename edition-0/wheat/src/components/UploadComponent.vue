<template>
  <div>
    <el-row :gutter="20" justify="center" align="middle" class="container">
      <el-col :span="10">
        <el-card class="custom-card hover">
          <template #header>
            <div class="card-header">
              <span>图片上传</span>
            </div>
          </template>
          <el-upload
            v-model:file-list="imageFileList"
            class="upload-demo"
            action="/upload/image"
            :http-request="uploadImageFile"
            :on-preview="handleImagePreview"
            :on-remove="handleImageRemove"
            list-type="picture"
          >
            <el-button type="primary">点击上传图片</el-button>
            <template #tip>
              <div class="el-upload__tip">
                上传大小不超过500kb的jpg/png文件
              </div>
            </template>
          </el-upload>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card class="custom-card hover">
          <template #header>
            <div class="card-header">
              <span>视频上传</span>
            </div>
          </template>
          <el-upload
            v-model:file-list="videoFileList"
            class="upload-demo"
            action="/upload/video"
            :http-request="uploadVideoFile"
            :on-preview="handleVideoPreview"
            :on-remove="handleVideoRemove"
            list-type="picture"
          >
            <el-button type="primary">点击上传视频</el-button>
            <template #tip>
              <div class="el-upload__tip">
                上传大小不超过500mb的mp4文件
              </div>
            </template>
          </el-upload>
        </el-card>
      </el-col>
    </el-row>
    <!-- <detection-results :results="results" v-if="results.length > 0" /> -->
    <detection-results :results="imageResults" v-if="imageResults.length > 0" />
    <video-detection-results :results="videoResults" v-if="videoResults.length > 0" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import axios from 'axios';
import DetectionResults from './DetectionResults.vue';
import VideoDetectionResults from './VideoDetectionResults.vue';

import type { UploadProps, UploadUserFile } from 'element-plus';

const fileList = ref<UploadUserFile[]>([]);
const imageFileList = ref<UploadUserFile[]>([]);
const videoFileList = ref<UploadUserFile[]>([]);
const imageResults = ref<Array<{ image: string; wheat_count: number; data_url: string }>>([]);
const videoResults = ref<Array<{ video: string; frame_count: number; data_url: string }>>([]);

const handleImagePreview: UploadProps['onPreview'] = (file) => {
  console.log('图片预览:', file);
};

const handleImageRemove: UploadProps['onRemove'] = (file, fileList) => {
  console.log('移除图片:', file, fileList);
};

const handleVideoPreview: UploadProps['onPreview'] = (file) => {
  console.log('视频预览:', file);
};

const handleVideoRemove: UploadProps['onRemove'] = (file, fileList) => {
  console.log('移除视频:', file, fileList);
};

const uploadImageFile = async (options: any) => {
  const { file } = options;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://127.0.0.1:5000/upload/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    imageResults.value.push({
      image: `http://127.0.0.1:5000/results/${file.name}`,
      wheat_count: response.data.wheat_count,
      data_url: response.data.data_url,
    });
  } catch (error) {
    console.error('Error uploading image file:', error);
  }
};

const uploadVideoFile = async (options: any) => {
  const { file } = options;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://127.0.0.1:5000/upload/video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    const video_url = response.data.video_url;
    const data_url = response.data.data_url;

    videoResults.value.push({
      video: `http://127.0.0.1:5000${video_url}`,
      frame_count: response.data.frame_count, // 假设后端返回 frame_count，如果没有需要修改
      data_url: `http://127.0.0.1:5000${data_url}`,
    });

    console.log('视频上传成功', response.data);
  } catch (error) {
    console.error('Error uploading video file:', error);
  }
};


</script>

<style scoped>
.custom-card {
  margin-top: 20px;
  max-width: 480px;
  margin-bottom: 20px;
  transition: transform 0.3s ease;
  background-color: #ffffff;
}

.custom-card:hover {
  transform: scale(1.05);
  background-color: #98ea98;
}
</style>
