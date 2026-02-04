<template>
  <div class="loading-container" v-if="visible">
    <div class="loading-wrapper">
      <img src="@/assets/loading.gif" alt="加载中" class="loading-gif">
      <p class="loading-text">{{ text }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  visible: {
    type: Boolean,
    default: true
  },
  text: {
    type: String,
    default: '加载中...'
  }
});
</script>

<style scoped>
.loading-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.3);
  z-index: 9999;
  backdrop-filter: blur(3px);
}

.loading-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: transparent;
  padding: 20px;
  border-radius: 12px;
  animation: fadeIn 0.3s ease-in-out;
}

.loading-gif {
  width: 35%;
  height: auto;
  margin-bottom: 10px;
}

.loading-text {
  font-size: 16px;
  color: #2196f3;
  margin: 0;
  font-weight: 500;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>