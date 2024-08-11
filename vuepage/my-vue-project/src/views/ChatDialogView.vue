<!-- src/views/ChatDialogView.vue -->
<template>
    <div>
      <ChatDialog />
    </div>
  </template>
  
  <script>
  import ChatDialog from '@/components/ChatDialog.vue';
  
  export default {
    name: 'ChatDialogView',
    components: {
      ChatDialog,
    },
  };
  </script>
  