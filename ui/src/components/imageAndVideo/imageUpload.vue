<template>
  <div class="upload-section">
    <div class="background-container1">
      <p class="text-center max-w-[620px] mx-auto text-subhead">
        上传图片检测
      </p>
    </div>
    <div class="content-wrapper">
      <div class="upload-wrapper">
        <el-upload
          class="upload-demo"
          :action="`${baseUrl}/api/image/upload`"
          :on-preview="handlePreview"
          :on-success="handleUploadSuccess"
          :on-remove="handleRemove"
          :file-list="fileList"
          list-type="picture"
          :limit="5"
        >
          <el-button type="primary">点击上传<i class="el-icon-upload el-icon--right" /></el-button>
          <div slot="tip" class="el-upload__tip">
            <el-link type="warning">请上传jpg/png文件</el-link>
          </div>
        </el-upload>
      </div>
      <div v-if="results.length > 0" class="table-wrapper">
        <!-- 显示检测结果 -->
        <el-table :data="paginatedResults" style="width: 100%">
          <el-table-column
            prop="imageUrl"
            label="标注图像"
            width="300"
          >
            <template slot-scope="scope">
              <el-image :src="scope.row.imageUrl" style="width: 100px; height: 100px; object-fit: cover" />
            </template>
          </el-table-column>
          <el-table-column
            prop="wheatCount"
            label="麦穗头数量"
            width="300"
          />
          <el-table-column
            label="下载"
            width="300"
          >
            <template slot-scope="scope">
              <el-button size="small" @click="viewImage(scope.row.imageUrl)">查看图片</el-button>
              <el-button size="small" @click="downloadImage(scope.row.downloadImageUrl)">下载图片</el-button>
              <el-button size="small" @click="downloadData(scope.row.dataUrl)">下载数据</el-button>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页组件 -->
        <el-pagination
          :page-size="pageSize"
          :current-page="currentPage"
          :total="results.length"
          layout="total, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
    <el-dialog :visible.sync="dialogVisible" @close="dialogVisible = false">
      <img :src="currentImageUrl" alt="Image Preview" class="image-dialog">
    </el-dialog>
    <section class="news-section">
      <div class="container">
        <h2 class="sr-only">News</h2>
        <div class="news-grid">
          <div v-for="(item, index) in newsItems" :key="index" class="news-item">
            <div class="news-content">
              <h4>{{ item.title }}</h4>
              <p>{{ item.description }}</p>
              <div class="cta">
                <a :href="item.link" target="_blank">点击 {{ item.title.split(' ')[0] }} 了解更多 </a>
              </div>
            </div>
            <div class="news-image">
              <img :src="item.imageUrl" :alt="item.title">
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fileList: [],
      results: [],
      currentImageUrl: '',
      dialogVisible: false,
      currentPage: 1,
      pageSize: 5,
      newsItems: [
        {
          title: 'WheatOmics——小麦组学大数据可视化和在线分析平台',
          description: '实现了对48套麦族物种基因组、500余份小麦转录组、2000多种小麦变异组、三套小麦突变体库外显子组、多套小麦表观修饰组等组学大数据的可视化， 并开发了各种功能基因学研究息息相关的在线分析工具。',
          imageUrl: 'http://wheatomics.sdau.edu.cn/css/logo.jpg',
          link: 'http://wheatomics.sdau.edu.cn/'
        },
        {
          title: 'WGGC——农学院小麦研究中心',
          description: '围绕着小麦遗传资源的发掘与创新、小麦抗逆性遗传改良、小麦多倍体和杂种优势形成的分子机制、小麦产量与品质功能基因组和小麦分子育种等重要研究方向开展工作。',
          imageUrl: 'http://wheat.cau.edu.cn/assets/img/gallery/about3.png',
          link: 'http://wheat.cau.edu.cn/zh/index.html'
        },
        {
          title: 'IWGSC——小麦的高质量基因组序列',
          description: 'IWGSC 在 68 个国家/地区拥有 2,400 名成员，是一个国际合作联盟，由一群小麦种植者、植物科学家以及公共和私人育种者于 2005 年成立。',
          imageUrl: 'https://tse3-mm.cn.bing.net/th/id/OIP-C.YX6_W4RHD_Ngsb9NuqXxbgAAAA?w=136&h=132&c=7&r=0&o=5&dpr=1.6&pid=1.7',
          link: 'https://wheat-urgi.versailles.inra.fr/Projects/IWGSC'
        }
      ],
      baseUrl: process.env.VUE_APP_API_URL // 从环境变量中获取 baseUrl
    }
  },
  computed: {
    paginatedResults() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.results.slice(start, end)
    }
  },
  methods: {
    handleUploadSuccess(response) {
      console.log('Upload successful:', response)
      const baseUrl = process.env.VUE_APP_API_URL // 从环境变量中获取 baseUrl
      this.results.push({
        imageUrl: `${baseUrl}/api/image${response.image_url}`, // 正确引用 baseUrl
        downloadImageUrl: `${baseUrl}/api/image/download${response.image_url}`, // 正确引用 baseUrl
        dataUrl: `${baseUrl}/api/image/data${response.data_url}`, // 正确引用 baseUrl
        wheatCount: response.wheat_count
      })
    },
    handleRemove(file, fileList) {
      this.fileList = fileList
      this.imageUrl = ''
    },
    handlePreview(file) {
      // Directly set imageUrl based on file.preview URL if available
      console.log('File preview:', file) // Debug log
      this.imageUrl = file.url
      this.dialogVisible = true
    },
    viewImage(imageUrl) {
      console.log('ImageUrl:', imageUrl)
      this.currentImageUrl = imageUrl
      this.dialogVisible = true
    },
    downloadImage(downloadImageUrl) {
      const fileName = downloadImageUrl.split('/').pop()
      const link = document.createElement('a')
      link.href = downloadImageUrl
      link.download = fileName // 设置下载文件名
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    downloadData(dataUrl) {
      const link = document.createElement('a')
      link.href = dataUrl
      link.download = dataUrl.split('/').pop()
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    getFileName() {
      return this.imageUrl.split('/').pop()
    },
    handleSizeChange(val) {
      this.pageSize = val
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }
}
</script>

<style scoped>
.background-container1 {
  position: relative;
  width: 100%;
  height: 20vh;
  overflow: hidden;
}

.background-container1::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('https://images.ctfassets.net/kftzwdyauwt9/3H5j3oawTq7P42sqqfaVFp/6fba4c7e9c4b9e465d7cfb576f609249/oai_o1_preview_bg.png?w=3840&q=90&fm=webp');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.7;
  z-index: -1;
}
.content-wrapper {
  display: flex;
  justify-content: space-between;
}

.upload-wrapper {
  flex-basis: 30%;
  padding-right: 20px;
}

.table-wrapper {
  flex-basis: 70%;
}
.upload-demo {
  margin: 20px;
}
.image-preview {
  margin-top: 20px;
  text-align: center;
}

.image-display {
  width: 100%;
  max-width: 400px;
  margin-bottom: 10px;
}

.button-group {
  display: flex;
  justify-content: space-around;
}

.image-dialog {
  width: 100%;
  max-width: 500px;
}
/* 基本样式 */
.text-center {
  text-align: center;
}

/* .max-w-[620px] {
  max-width: 620px;
} */

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.text-subhead {
  font-size: 2.25rem; /* 可以根据需要调整字体大小 */
  line-height: 1.5;   /* 行高可以调整 */
  color: gray;        /* 字体颜色 */
  font-weight:bold;
}

/* 响应式样式 */
@media (max-width: 640px) {
  .text-balance {
    /* 在小屏幕下调整文字样式 */
    font-size: 1.125rem; /* 或其他适合小屏幕的字体大小 */
  }
}
.news-section {
  background-color: #f0f0f0;
  padding: 20px 0;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.news-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.news-item {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  width: 30%;
  margin-bottom: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: box-shadow 0.3s ease;
}

.news-item:hover {
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.news-content {
  margin-bottom: 20px;
}

.news-content h4 {
  font-size: 18px;
  margin-bottom: 10px;
  height: 84px;
}

.news-content p {
  font-size: 14px;
  margin-bottom: 20px;
  height: 96px;
}

.cta a {
  color: #0077cc;
  text-decoration: none;
}

.cta a:hover {
  text-decoration: underline;
}

.news-image img {
  width: 100%;
  height: auto;
  border-radius: 4px;
}
</style>
