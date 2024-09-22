<template>

  <div class="background-image">
    <div id="chat-container">
      <div id="chat-box">
        <div v-for="(message, index) in messages" :key="index" class="message">
          <div :class="message.role">{{ message.content }}</div>
        </div>
      </div>
      <div id="input-box">
        <input
          v-model="userMessage"
          placeholder="Type your message..."
          @keyup.enter="sendMessage"
        >
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      userMessage: '',
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' }
      ]
    }
  },
  methods: {
    async sendMessage() {
      if (this.userMessage.trim() === '') {
        console.log('User message is empty.')
        return
      }

      // Add user message to the chat
      this.messages.push({
        role: 'user',
        content: this.userMessage
      })

      try {
        console.log('Sending message to server:', this.userMessage)

        const response = await axios.post('http://127.0.0.1:5000/api/chat', {
          message: this.userMessage
        })
        console.log('Respoonse from server:', response.data)
        // Add assistant's response to the chat
        this.messages.push({
          role: 'assistant',
          content: response.data.reply
        })
      } catch (error) {
        console.error('Error sending message:', error)
        this.messages.push({
          role: 'error',
          content: 'There was an error. Please try again.'
        })
      }

      // Clear input field after sending the message
      this.userMessage = ''
    }
  }
}
</script>

  <style scoped>
  #chat-container {
    width: 60%;
    margin:0 auto;
    padding: 20px;
    background-color: #f1f1f1;
    border-radius: 8px;
    opacity:0.8
  }

  #chat-box {
    position:relative;
    height: 60vh;
    overflow-y: scroll;
    padding: 10px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .message {
    margin-bottom: 10px;
  }

  .user {
    text-align: right;
    color: blue;
  }

  .assistant {
    text-align: left;
    color: green;
  }

  #error {
    color: red;
  }

  #input-box {
    margin-top: 20px;
    display: flex;
  }

  input {
    flex: 1;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
  }

  button {
    padding: 10px 15px;
    margin-left: 10px;
    border-radius: 5px;
    border: none;
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }
  .background-image {
  width: 100vw;
  height: 100vh;
  background-image: url('https://images.ctfassets.net/kftzwdyauwt9/3XDJfuQZLCKWAIOleFIFZn/14b93d23652347ee7706eca921e3a716/enterprise.png?w=3840&q=90&fm=webp');
  background-size: cover;
  background-position:center center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  /* display: flex; */
  align-items:center;
  justify-content: center;
  color: white; /* 根据背景图片调整文本颜色 */
}
  </style>
