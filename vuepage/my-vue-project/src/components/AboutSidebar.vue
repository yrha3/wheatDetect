<template>  
    <div class="container">  
      <div class="drawer">  
        <button  
          class="drawer-button"  
          v-for="item in contents"  
          :key="item.id"  
          @click="scrollToContent(item.id)"    
        >  
          <p>{{ item.title }}</p>
          <div>{{item.id}}</div>
        </button>  
      </div>  
      <div class="content scrollable">  
        <div  
          v-for="item in contents"  
          :key="item.id"  
          :id="'content-' + item.id"  
          class="content-item"  
        > 
        <h2>{{ item.title }}</h2>
        <p>{{ item.description }}</p> 
        <img :src="item.image" alt="图片" class="content-image" />      
        </div>  
      </div>  
    </div>  
  </template>  
  
  <style scoped>  
  .container {  
    display: flex;  
    height: 100vh;  
  }  
  
  .drawer {  
    flex: 1;    
    display: flex;  
    flex-direction: column;  
  }  
  
  .drawer-button {
    display: flex;
    height: 19%;
    width: 75%;  
    padding: 0px;
    border: none;
    margin-top: 5%;  
    border-radius: 0px 15px 15px 0px;  
    background: none;  
    cursor: pointer;  
    text-align: left;
    transform: translateX(-75%);  
    transition: background-color 0.3s;
    transition: transform 1s;
    background-image: url("../assets/images/lvye.jpg");
    background-size: cover;
  }
  .drawer-button p{
    color:rgb(89,166,152) ;
    font-style: oblique;
    position: absolute;
    top:-60px;
    left: 20px;
    font-size: 70px;
    text-indent: -9999px;
  }
  .drawer-button div{
    margin-left: auto;
    text-align: right;
    font-weight:bold;
    font-size: 150px;
    font-style: italic;
    color: rgb(202,228,178);
  }  
  
  .drawer-button:focus{  
    transform:translateX(0%);
    text-indent: 0%;

  }  
  .drawer-button:focus p{
    text-indent: 0px;

  }
  
  .content {  
    flex: 1;  
    padding: 20px;  
    overflow-y: auto;  
  }  
  
  .content-item {  
    margin-bottom: 30px;
    height: 100%;
  }  
  
  .content-image {  
    max-width: 100%;  
    height: auto;  
  }  
  
  .scrollable {  
    overflow-y: auto;  
  }  
  </style>  
  
  <script>  
  export default {  
    name: 'App',  
    data() {  
      return {  
        contents: [  
          { id: 1, title: '立项目的', description: '这里是内容 1 的详细描述。', image: require('@/assets/images/carousel01.jpeg') },  
          { id: 2, title: '项目介绍', description: '这里是内容 2 的详细描述。', image: require('@/assets/images/carousel02.png') },  
          { id: 3, title: '人员组成', description: '这里是内容 3 的详细描述。', image: require('@/assets/images/carousel03.jpeg') },  
          { id: 4, title: '特别鸣谢', description: '这里是内容 4 的详细描述。', image: require('@/assets/images/carousel04.jpeg') },  
        ],  
      };  
    },  
    methods: {  
      scrollToContent(id) {  
        const element = document.getElementById(`content-${id}`);  
        if (element) {  
          const scrollContainer = this.$el.querySelector('.scrollable');  
          const { top } = element.getBoundingClientRect();  
          const containerTop = scrollContainer.getBoundingClientRect().top;  
          const offsetTop = top - containerTop + scrollContainer.scrollTop;  
  
          scrollContainer.scrollTo({  
            top: offsetTop,  
            behavior: 'smooth',  
          });  
        }  
      },  
    },  
  }  
  </script>