


<template>
  <router-view></router-view>
</template>

<script setup>

</script>

<style>
/* 全局自定义鼠标样式 - 应用于所有元素 */
html, body, 
input, textarea, [contenteditable="true"], .el-input,
a, button, .el-button, [role="button"], .clickable,
* {
  cursor: url('src/assets/pointer/default.cur'), default !important;
}

/* 添加全局样式重置 */
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  box-sizing: border-box;
}

* {
  box-sizing: inherit;
}

/* 全局背景设置
body {
  background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.95)), 
              url('src/assets/背景.png') center/cover no-repeat fixed;
  min-height: 100vh;
} */

/* 移除全局背景设置相关代码 */
#app {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  position: relative;
}

/* 移除渐变色覆盖 */
#app::before {
  display: none;  /* 或直接删除整个 #app::before 块 */
}

.el-container, .el-header, .el-main {
  padding: 0;
  margin: 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  body {
    background-size: 200% auto;
  }
}
</style>