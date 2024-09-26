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
          :action="`${baseUrl}/api/image/classify`"
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
        <el-table :data="results" style="width: 100%">
          <el-table-column
            label="检测类别"
            width="300"
          >
            <template slot-scope="scope">
              {{ scope.row.class_name }}  <!-- 显示分类名称 -->
            </template>
          </el-table-column>
          <el-table-column
            label="置信度"
            width="300"
          >
            <template slot-scope="scope">
              {{ scope.row.confidence }}%  <!-- 显示置信度 -->
            </template>
          </el-table-column>
          <el-table-column
            prop="imageUrl"
            label="图像"
            width="300"
          >
            <template slot-scope="scope">
              <img v-if="scope.row.imageUrl" :src="scope.row.imageUrl" alt="Result Image" class="result-image">  <!-- 显示图像 -->
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
      <div v-else>
        <p class="text-center">尚未检测到任何结果，请上传图片进行分类检测。</p>
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
      results: [], // 存储分类结果
      dialogVisible: false,
      currentImageUrl: '', // 用于预览的图片URL
      pageSize: 5, // 每页显示的数量
      currentPage: 1, // 当前页码
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
      baseUrl: process.env.VUE_APP_API_URL
    }
  },
  methods: {
    handleUploadSuccess(response) {
      if (response.classification_results) {
        const classificationResult = response.classification_results
        const baseUrl = process.env.VUE_APP_API_URL
        // 将结果保存到results中
        this.results.push({
          class: classificationResult.class,
          class_name: classificationResult.class_name,
          confidence: (classificationResult.confidence * 100).toFixed(2), // 置信度转为百分比形式
          imageUrl: `${baseUrl}/${classificationResult.imageUrl}`// 接收图像URL
        })

        console.log(this.results) // 确认结果是否正确
      } else {
        console.error('No classification results in response')
      }
    },
    handleRemove(file, fileList) {
      this.fileList = fileList
      this.imageUrl = ''
      // this.results = [] // 清空结果
    },
    handlePreview(file) {
      console.log('File preview:', file) // Debug log
      this.currentImageUrl = file.url // 预览图像的URL
      this.dialogVisible = true
    },
    handleSizeChange(val) {
      this.pageSize = val // 更新每页显示的数量
    },
    handleCurrentChange(val) {
      this.currentPage = val // 更新当前页码
    },
    beforeUpload(file) {
      if (this.fileList.length >= 5) {
        this.$message.warning('最多同时上传5张图片')
        return false
      }
      return true
    }
  }
}
</script>
<style scoped>
.result-image {
  width: 100px;
  height: auto;
}

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
