<template>
    <div class="chat-wrapper">
      <div class="chat-container">
        <div class="chat-messages">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="message.type"
            class="message"
          >
            {{ message.text }}
          </div>
        </div>
        <div class="chat-input">
          <input v-model="inputText" placeholder="Enter message..." />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { getCurrentInstance } from 'vue';

  const { proxy } = getCurrentInstance();
  const baseUrl = proxy.$baseUrl;


  
  interface Message {
    type: string;
    text: string;
  }
  
  // 定义响应式数据
  const inputText = ref('');
  const messages = ref<Message[]>([]);
  
  // 发送消息的函数
  const sendMessage = async () => {
    if (inputText.value.trim() === "") return;
  
    // 添加用户消息到聊天记录
    messages.value.push({ type: "user", text: inputText.value });
  
    try {
      // 发送请求到后台
      const response = await axios.post(`${baseUrl}/api/chat`, {
        message: inputText.value,
      });
  
      // 添加后台响应到聊天记录
      messages.value.push({ type: "ai", text: response.data.reply });
    } catch (error) {
      console.error("Error sending message:", error);
    }
  
    // 清空输入字段
    inputText.value = "";
  };
  </script>
  
  <style scoped>
  .chat-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* Full viewport height */
    padding: 20px;
    box-sizing: border-box;
  }
  
  .chat-container {
    width: 80%;
    max-width: 600px;
    height: 500px;
    display: flex;
    flex-direction: column;
    border: 1px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
    background-color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .chat-messages {
    flex: 1;
    padding: 16px;
    overflow-y: auto;
    background-color: #f9f9f9;
    border-bottom: 1px solid #ccc;
  }
  
  .message {
    margin-bottom: 8px;
    padding: 8px;
    border-radius: 4px;
  }
  
  .user {
    text-align: right;
    color: #1976d2;
    background-color: #e3f2fd;
  }
  
  .ai {
    text-align: left;
    color: #d32f2f;
    background-color: #fce4ec;
  }
  
  .chat-input {
    display: flex;
    padding: 16px;
    border-top: 1px solid #ccc;
    background-color: #fff;
  }
  
  .chat-input input {
    flex: 1;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-right: 8px;
  }
  
  .chat-input button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background-color: #1976d2;
    color: #fff;
    cursor: pointer;
  }
  
  .chat-input button:hover {
    background-color: #1565c0;
  }
  </style>
  