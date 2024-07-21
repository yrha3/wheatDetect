<template>
  <div class="video-detection-results">
    <h2>视频检测结果</h2>
    <!-- 表格显示检测数据 -->
    <el-table :data="results" style="width: 100%">
      <el-table-column prop="video" label="视频" width="150">
        <template #default="scope">
          <video :src="scope.row.video" controls class="result-video" />
        </template>
      </el-table-column>
      <el-table-column prop="frame_count" label="帧数">
        <template #default="scope">
          <div>{{ scope.row.frame_count || 'N/A' }}</div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300">
        <template #default="scope">
          <el-button @click="openDialog(scope.row.video)" type="primary" size="small" class="action-btn">查看视频</el-button>
          <el-button @click="handleDownloadData(scope.row.data_url)" type="success" size="small" class="action-btn">下载数据</el-button>
          <el-button @click="handleDownloadVideo(scope.row.video)" type="success" size="small" class="action-btn">下载视频</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 弹出对话框 -->
    <el-dialog v-model="dialogVisible" title="查看视频" width="80%" :before-close="handleClose">
      <video :src="dialogVideo" controls class="dialog-video" />
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleDownloadVideo(dialogVideo)">下载视频</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const props = defineProps<{
  results: Array<{ video: string; frame_count: number, data_url: string }>
}>()

const dialogVisible = ref(false)
const dialogVideo = ref('')

// 打开查看视频对话框
const openDialog = (video: string) => {
  if (video) {
    console.log(`Opening video dialog for video: ${video}`);
    dialogVideo.value = video
    dialogVisible.value = true
  }
}

// 处理对话框关闭
const handleClose = (done: () => void) => {
  done()
}

// 处理下载数据
const handleDownloadData = (data_url: string) => {
  console.log("尝试下载数据");
  console.log("data_url:", data_url);
  if (data_url) {
    // 使用绝对路径来避免潜在的路径问题
    const absoluteUrl = new URL(data_url, window.location.origin).toString();
    console.log("下载数据 URL:", absoluteUrl);

    // 创建一个临时的 <a> 元素，并触发下载
    const link = document.createElement('a');
    link.href = absoluteUrl;
    link.download = data_url.split('/').pop() || 'data.json'; // 设置下载的文件名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}


const handleDownloadVideo = (video: string) => {
  if (video) {
    // 提取文件夹名和文件名
    const parts = video.split('/');
    const videoFilename = parts.pop() || 'video.mp4';
    const videoFolder = parts.pop() || '';

    // 拼接正确的下载 URL
    const downloadUrl = `/results/download/video/${videoFolder}/${videoFilename}`;
    console.log('Download URL:', downloadUrl);

    // 创建一个临时的 <a> 元素，并触发下载
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = videoFilename; // 设置下载的文件名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}



</script>

<style scoped>
.video-detection-results {
  padding: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 5px;
  background-color: #ffffff;
  margin-top: 20px;
}

.result-video {
  width: 100px;
  height: auto;
  object-fit: cover;
  cursor: pointer;
}

.action-btn {
  margin-right: 10px;
}

.dialog-video {
  width: 100%;
  height: auto;
  object-fit: contain;
}
</style>
